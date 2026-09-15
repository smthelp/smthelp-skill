---
name: software-development
description: "Complete software development workflow: planning, implementation, testing, debugging, code review, and prototyping. Use when building, fixing, or reviewing code."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, planning, implementation, testing, debugging, code-review, tdd, delegation]
    related_skills: []
---

# Software Development — Complete Workflow

Complete guide for software development: planning, implementation, testing, debugging, code review, prototyping, and skill authoring. Covers the full development lifecycle from idea to shipped code.

---

## 1. Planning & Implementation (Plan Mode)

### Plan Mode

Use when the user wants a plan instead of execution. Write the plan to `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md` with concrete, actionable tasks. Each task = 2-5 minutes of focused work.

```python
write_file(".hermes/plans/2024-01-15_143000-auth-feature.md", plan_content)
```

### Writing Implementation Plans

Use `plan` skill or write directly. Every task needs:
- Exact file paths (not "the config file" but `src/config/settings.py:45-67`)
- Complete code examples (copy-pasteable)
- Exact commands with expected output
- Verification steps

**Plan document structure:**
```markdown
# [Feature] Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** [One sentence]

---

### Task 1: Create User model with email field
**Step 1:** Write failing test
**Step 2:** `pytest tests/test_user.py::test_email -v` → FAIL
**Step 3:** Write minimal code
**Step 4:** Verify pass
**Step 5:** Commit
```

**Key principles:**
- DRY — extract reusable logic
- YAGNI — implement only what's needed now
- TDD — tests before code
- Bite-sized tasks — 2-5 minutes each
- Frequent commits — one per task

See `references/two-stage-review.md` for the full implementation → review workflow.

---

## 2. Implementation via Subagents

> Absorbed from `subagent-driven-development` skill.

Execute implementation plans by dispatching fresh subagents per task with two-stage review.

### The Loop

For each task in the plan:

**Step 1: Dispatch Implementer**
```python
delegate_task(
    goal="Implement Task 1: Create User model",
    context="""TASK: Create src/models/user.py with User class.
    Fields: email (str), password_hash (str).
    Use bcrypt for hashing. Include __repr__.
    FOLLOW TDD:
    1. Write failing test
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (no regressions)
    6. Commit""",
    toolsets=['terminal', 'file']
)
```

**Step 2: Spec Compliance Reviewer** (fresh subagent)
```python
delegate_task(
    goal="Check if implementation matches the spec",
    context="""ORIGINAL SPEC:
    - Create src/models/user.py with User class
    - Fields: email, password_hash
    - Use bcrypt
    OUTPUT: PASS or list of gaps""",
    toolsets=['file']
)
```

**Step 3: Code Quality Reviewer** (fresh subagent)
```python
delegate_task(
    goal="Review code quality",
    context="""FILES: src/models/user.py, tests/models/test_user.py
    CHECK: style, error handling, naming, tests, security
    OUTPUT: APPROVED or REQUEST_CHANGES""",
    toolsets=['file']
)
```

**Key rules:**
- Fresh subagent per task — no context pollution
- Two-stage review every time — spec FIRST, quality SECOND
- Never skip reviews
- Provide full task text in context, don't make subagents read plan files

---

## 3. Test-Driven Development

> Absorbed from `test-driven-development` skill.

**Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.

### Red-Green-Refactor

**RED:** Write failing test
```python
def test_retries_failed_operations_3_times():
    attempts = 0
    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception('fail')
        return 'success'
    result = retry_operation(operation)
    assert result == 'success' and attempts == 3
```

**GREEN:** Minimal code to pass — nothing more
```python
def retry_operation(operation):
    for i in range(3):
        try:
            return operation()
        except:
            pass
    return operation()
```

**REFACTOR:** Clean up only AFTER green. No new behavior.

### Why Order Matters

Tests written after code pass immediately — proving nothing. Test-first forces you to watch the test fail, proving it tests the right thing.

| Excuse | Reality |
|--------|---------|
| "I'll test after" | Tests passing immediately prove nothing |
| "Deleting X hours is wasteful" | Sunk cost — unverified code is technical debt |
| "TDD slows me down" | Debugging after is slower than TDD upfront |

---

## 4. Systematic Debugging

> Absorbed from `systematic-debugging` skill.

**Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

### The Four Phases

**Phase 1: Root Cause Investigation**
- Read error messages completely
- Reproduce consistently
- Check recent changes (`git log --oneline -10`)
- Trace data flow upstream to find the actual source

**Phase 2: Pattern Analysis**
- Find similar working code
- Compare against the broken version
- Identify every difference

**Phase 3: Hypothesis & Testing**
- Form one specific hypothesis: "X is the root cause because Y"
- Make the smallest possible change to test
- Don't add more fixes on top

**Phase 4: Implementation**
- Create failing test reproducing the bug FIRST
- Fix the root cause
- Verify: `pytest tests/test_module.py -v`

**If 3+ fixes failed:** Stop and question the architecture — each fix revealing a new problem in a different place indicates a design issue, not a code issue.

### Common Rationalizations

| "Just try X" | Systematic approach finds root cause faster |
|-------------|----------------------------------------------|
| "Skip the test" | No verification the fix works |
| "One more fix attempt" | 3 failures = wrong architecture |

---

## 5. Pre-Commit Code Review

> Absorbed from `requesting-code-review` skill.

Automated verification pipeline before `git commit` or `git push`.

### Step 1: Get the Diff
```bash
git diff --cached   # staged changes
git diff            # unstaged changes
```

### Step 2: Static Security Scan
```bash
# Hardcoded secrets
git diff --cached | grep "^+" | grep -iE "(api_key|secret|password|token)\s*=\s*['\"][^'\"]{6,}['\"]"

# Shell injection
git diff --cached | grep "^+" | grep -E "os\.system\(|subprocess.*shell=True"

# SQL injection
git diff --cached | grep "^+" | grep -E "execute\(f\"|\.format\(.*SELECT"
```

### Step 3: Baseline Tests + Linting
```bash
# Run tests — compare failure count against baseline
python -m pytest --tb=no -q 2>&1 | tail -5

# Run linter
which ruff && ruff check . 2>&1 | tail -10
```

### Step 4: Independent Reviewer Subagent
```python
delegate_task(
    goal="""Review the git diff and return ONLY valid JSON:
    {"passed": true/false, "security_concerns": [], "logic_errors": [], "suggestions": []}""",
    context="Static scan results + git diff...",
    toolsets=["terminal"]
)
```

### Step 5: Auto-Fix (if needed)
Maximum 2 fix-and-reverify cycles. Spawn a separate fix agent — not the implementer.

### Step 6: Commit
```bash
git add -A && git commit -m "[verified] <description>"
```

---

## 6. Spike (Throwaway Prototyping)

> Absorbed from `spike` skill.

Use when the user wants to validate an idea before committing to a real build — validating feasibility, comparing approaches, or surfacing unknowns.

### Core Loop
```
decompose → research → build → verdict
```

### Decompose
Break into 2-5 independent feasibility questions. Present as a table:

| # | Spike | Risk |
|---|-------|------|
| 001 | websocket-streaming | High |
| 002a | pdf-parse-pdfjs | Medium |
| 002b | pdf-parse-camelot | Medium |

### Build
One directory per spike, standalone:
```
spikes/
├── 001-websocket-streaming/
│   ├── README.md
│   └── main.py
```

### Verdict
Each `README.md` closes with:
```markdown
## Verdict: VALIDATED | PARTIAL | INVALIDATED

### What worked
- ...

### What didn't
- ...

### Recommendation
- ...
```

**VALIDATED** = core question answered yes.
**PARTIAL** = works under constraints X, Y, Z.
**INVALIDATED** = doesn't work. This is a successful spike.

---

## 7. Debugging Workflows

### Node.js Debugging (node-inspect)

> Absorbed from `node-inspect-debugger` skill.

```bash
# Launch paused on first line
node inspect path/to/script.js

# Attach to running process
kill -SIGUSR1 <pid>
node inspect -p <pid>
```

Inside `debug>` prompt:
| Command | Action |
|---------|--------|
| `c` / `cont` | continue |
| `n` / `next` | step over |
| `s` / `step` | step into |
| `sb('file.js', 42)` | set breakpoint |
| `bt` | backtrace |
| `repl` | drop into REPL with local scope |

### Python Debugging (debugpy)

> Absorbed from `python-debugpy` skill.

**Quick breakpoint:**
```python
breakpoint()  # drops into pdb
```

**Remote debug (long-lived processes):**
```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))
debugpy.wait_for_client()
```

**Post-mortem:**
```python
import pdb, sys
try:
    run_the_thing()
except Exception:
    pdb.post_mortem(sys.exc_info()[2])
```

Inside `(Pdb)` prompt:
| Command | Action |
|---------|--------|
| `n` | next line |
| `s` | step into |
| `w` | where (stack trace) |
| `p expr` | print expression |
| `interact` | full Python REPL in current scope |

**pytest debugging:**
```bash
pytest tests/test_file.py --pdb -p no:xdist  # xdist breaks pdb
```

### Hermes TUI Debugging

> Absorbed from `debugging-hermes-tui-commands` skill.

Three layers: Python backend (`hermes_cli/commands.py`) → TUI gateway (`tui_gateway/server.py`) → Ink frontend (`ui-tui/src/app/slash/`).

**Debug Python side:** Use `python-debugpy` skill — `remote-pdb` into `_SlashWorker.exec`.

**Debug Ink side:** Use `node-inspect-debugger` skill — `sb('dist/app.js', 220)`.

**Key insight:** Python `COMMAND_REGISTRY` is the source of truth for autocomplete, gateway dispatch, and help text. Mismatches between Python and TypeScript definitions cause most command issues.

---

## 8. Hermes Skill Authoring

> Absorbed from `hermes-agent-skill-authoring` skill.

### Frontmatter Requirements

```yaml
---
name: my-skill-name        # lowercase, hyphens, ≤64 chars
description: "Use when <trigger>. <one-line behavior>."  # ≤1024 chars
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [short, descriptive, tags]
    related_skills: [other-skill]
---
```

### Size Limits
- Description: ≤ 1024 chars
- Full SKILL.md: ≤ 100,000 chars (aim for 8-15k)

### Peer-Matched Structure
```
# <Title>
## Overview
## When to Use
## <Topic sections>
## Common Pitfalls
## Verification Checklist
```

### Directory Placement
```
skills/<category>/<skill-name>/SKILL.md
```

Categories: `autonomous-ai-agents`, `creative`, `data-science`, `devops`, `github`, `mlops/*`, `productivity`, `software-development`, etc.

### Workflow
1. Survey peers in the target category
2. Draft with `write_file`
3. Validate: frontmatter at byte 0, `name` + `description` present
4. Git add + commit

---

## References

- `references/two-stage-review.md` — Spec compliance + quality review process
- `references/gates-taxonomy.md` — Gate types for validation checkpoints
- `references/context-budget-discipline.md` — Context window management
- `templates/` — Starter templates for plans, tests, bug reports
- `scripts/` — Utility scripts
