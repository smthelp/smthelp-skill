---
name: autonomous-coding-agents
description: "Class-level umbrella for delegating coding tasks to external autonomous coding agents (Claude Code, Codex, OpenCode). Covers orchestration patterns, PTY handling, session management, PR workflows, and parallel execution. Load this skill when asked to delegate coding to an external CLI agent, run an autonomous coding session, or coordinate multiple coding workers."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermmes:
    tags: [Coding-Agent, Claude, Codex, OpenAI, OpenCode, Autonomous, PR-Review, Refactoring, PTY, Automation]
    related_skills: [claude-code, codex, opencode]
---

# Autonomous Coding Agents — Class Umbrella

This skill is the class-level umbrella for **all three major autonomous coding agent CLIs**: Claude Code (Anthropic), Codex (OpenAI), and OpenCode (open-source). Each agent's specific reference content lives in its named subsection below.

## When to Load This Umbrella vs. a Specific Skill

| Situation | Load |
|---|---|
| User asks to "use Claude Code" / "delegate to claude-code" | `autonomous-coding-agents` (this umbrella) — loads the claude-code subsection |
| User asks to "use Codex" / "delegate to codex" | `autonomous-coding-agents` (this umbrella) — loads the codex subsection |
| User asks to "use OpenCode" | `autonomous-coding-agents` (this umbrella) — loads the opencode subsection |
| Kanban worker wants to run Codex as an isolated lane | `kanban-codex-lane` (specialized — see §4) |
| Generic "delegate this coding task" | `autonomous-coding-agents` (this umbrella) |

## Quick Decision Tree

```
Is the task a one-shot code edit/refactor/review?
├── YES → Use print/non-interactive mode (fastest, no PTY needed)
└── NO (multi-turn, iterative) → Use interactive background mode with PTY

Does the user want Claude Code specifically?
├── YES → §1 Claude Code
└── NO → Does the user prefer OpenAI Codex?
    ├── YES → §2 Codex
    └── NO → §3 OpenCode (provider-agnostic, open-source)
```

---

## §1 — Claude Code (Anthropic)

Claude Code is Anthropic's official autonomous coding agent CLI. Rich orchestration support including print mode, interactive PTY via tmux, structured JSON output, session continuation, worktrees, custom subagents, and MCP integration.

### Key Characteristics
- **CLI**: `claude` (npm: `@anthropic-ai/claude-code`)
- **Auth**: OAuth (Pro/Max), API key (`ANTHROPIC_API_KEY`), or SSO (Enterprise)
- **Modes**: Print (`-p`) for one-shot; Interactive via tmux for multi-turn
- **Requires PTY**: Interactive mode requires tmux orchestration
- **Best for**: Complex multi-file refactors, deep reasoning tasks, Claude-specific features (Plan mode, `/review`, `/security-review`)

### One-Shot (Print Mode — PREFERRED)
```bash
# Simplest integration — no PTY, structured output
terminal(command="claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)
```

### Interactive via tmux
```bash
# Start session
terminal(command="tmux new-session -d -s claude-work -x 140 -y 40")
terminal(command="tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter")
sleep 5 && tmux send-keys -t claude-work Enter  # trust dialog

# Send task
terminal(command="tmux send-keys -t claude-work 'Refactor the auth module to use JWT' Enter")

# Monitor
terminal(command="tmux capture-pane -t claude-work -p -S -50")

# Exit
terminal(command="tmux send-keys -t claude-work '/exit' Enter")
```

### Dialog Handling (CRITICAL for Interactive Mode)
Claude Code presents two dialogs on first launch:
1. **Workspace Trust** — default "Yes, I trust this folder" → just press Enter
2. **Permissions Bypass** — defaults to "No, exit" → must press Down then Enter

### Structured JSON Output
```bash
terminal(command="claude -p 'Analyze auth.py for security issues' --output-format json --max-turns 5", workdir="/project", timeout=120)
```
Returns: `session_id`, `num_turns`, `total_cost_usd`, `subtype` (`success`/`error_max_turns`).

### Key Flags
| Flag | Purpose |
|------|---------|
| `-p` | Print mode (non-interactive, exits when done) |
| `--max-turns N` | Cap agentic loops (print mode only) |
| `--dangerously-skip-permissions` | Auto-approve all tool use |
| `--allowedTools` | Whitelist specific tools |
| `--output-format json` | Structured output |
| `--json-schema` | Force structured JSON matching a schema |
| `-c, --continue` | Resume most recent session in same dir |
| `-r, --resume <id>` | Resume specific session |
| `--bare` | Skip hooks/plugins/MCP for fastest startup (needs API key) |
| `-w, --worktree <name>` | Isolated git worktree + optional tmux |

### Session Continuation
```bash
# Start task, save session ID
terminal(command="claude -p 'Start refactoring' --output-format json --max-turns 10 > /tmp/session.json", workdir="/project", timeout=180)
SESSION_ID=$(cat /tmp/session.json | python3 -c 'import json,sys; print(json.load(sys.stdin)["session_id"])')

# Resume
terminal(command="claude -p 'Continue and add connection pooling' --resume $SESSION_ID --max-turns 5", workdir="/project", timeout=120)
```

### MCP Integration
```bash
# Add GitHub MCP
terminal(command="claude mcp add -s user github -- npx @modelcontextprotocol/server-github", timeout=30)
```

### Cost Tips
- Use `--max-turns` to prevent runaway loops
- `--bare` skips plugin discovery for faster startup in CI
- Use `--effort low` for simple tasks, `high`/`max` for complex reasoning
- Monitor with `/context` — quality degrades above 70% context window

### Full Reference
For the complete Claude Code reference (settings, hooks, slash commands, keyboard shortcuts, PR review patterns, parallel instances, CLAUDE.md hierarchy, environment variables, pitfalls), see the absorbed standalone at `references/claude-code.md` (archived original) or refer to §1 above.

---

## §2 — Codex (OpenAI)

Codex is OpenAI's autonomous coding agent CLI. One-shot execution via `codex exec`, background mode for long tasks, and worktree-based parallel issue fixing.

### Key Characteristics
- **CLI**: `codex` (npm: `@openai/codex`)
- **Auth**: `OPENAI_API_KEY` or Codex OAuth (`~/.codex/auth.json`)
- **Modes**: `codex exec "prompt"` (one-shot), background with `--full-auto`
- **Requires PTY**: YES — always use `pty=true`
- **Requires git repo**: Codex refuses to run outside a git directory
- **Best for**: Issue fixing, PR reviews, batch worktrees

### One-Shot
```bash
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

### Background (Long Tasks)
```bash
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=True)
# Monitor
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")
# Send input if needed
process(action="submit", session_id="<id>", data="yes")
```

### Key Flags
| Flag | Purpose |
|------|---------|
| `exec "prompt"` | One-shot execution |
| `--full-auto` | Auto-approve file changes in sandbox |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |
| `--sandbox danger-full-access` | No bubblewrap sandbox |

### Gateway Caveat
When running from a Hermes gateway/service context (e.g., Telegram-driven sessions), `workspace-write` sandboxing may fail with `setting up uid map: Permission denied`. Use:
```bash
codex exec --sandbox danger-full-access "<task>"
```

### Parallel Worktrees
```bash
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each (parallel)
terminal(command="codex --yolo exec 'Fix issue #78' 2>&1", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99' 2>&1", workdir="/tmp/issue-99", background=true, pty=true)
```

### PR Review
```bash
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

### Full Reference
For the complete Codex reference, see `references/codex.md` (archived original) or §2 above.

---

## §3 — OpenCode (Open-Source / Provider-Agnostic)

OpenCode is an open-source, provider-agnostic autonomous coding agent with a TUI and CLI. Supports any OpenRouter-compatible model.

### Key Characteristics
- **CLI**: `opencode` (npm: `opencode-ai@latest` or `brew install anomalyco/tap/opencode`)
- **Auth**: `opencode auth login` or set `OPENROUTER_API_KEY` etc.
- **Modes**: `opencode run` (one-shot, no PTY), interactive background (PTY)
- **Requires PTY**: Only for interactive TUI sessions; `opencode run` does NOT need PTY
- **Best for**: Provider-agnostic work, multi-model comparison, open-source preference

### One-Shot
```bash
terminal(command="opencode run 'Add retry logic to API calls and update tests'", workdir="~/project")
```

### Attach Context Files
```bash
terminal(command="opencode run 'Review this config for security issues' -f config.yaml -f .env.example", workdir="~/project")
```

### Interactive Background
```bash
terminal(command="opencode", workdir="~/project", background=true, pty=true)
# Send a prompt
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow and add tests")
# Monitor
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")
# Exit — use Ctrl+C, NOT /exit
process(action="write", session_id="<id>", data="\x03")
```

### Key Flags
| Flag | Purpose |
|------|---------|
| `run 'prompt'` | One-shot execution (no PTY needed) |
| `-c, --continue` | Continue last session |
| `-s, --session <id>` | Continue specific session |
| `--model provider/model` | Force specific model |
| `--format json` | Machine-readable output |
| `-f, --file <path>` | Attach file(s) to message |
| `--thinking` | Show model thinking blocks |

### PR Review
```bash
terminal(command="opencode pr 42", workdir="~/project", pty=true)
# Or in temp clone:
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run 'Review this PR vs main...'", pty=true)
```

### Full Reference
For the complete OpenCode reference, see `references/opencode.md` (archived original) or §3 above.

---

## §4 — Kanban Codex Lane (Specialized Protocol)

> **Note**: `kanban-codex-lane` is a specialized skill, not a general-purpose delegation skill. It defines a specific Hermes+Codex dual-lane convention where Hermes owns task lifecycle and Codex runs as an isolated implementation input lane. Load `kanban-codex-lane` directly for the full protocol reference.

### When to Use the Codex Lane
- Kanban task is coding/refactor/test/mechanical migration with clear acceptance criteria
- Bounded diff evaluable by Hermes in one run
- Repo can be copied/checked out in isolated git worktree
- Hermes can run tests after Codex exits

### When NOT to Use
- Task requires human judgment not in Kanban body
- Worker lacks repo access, Codex auth, or time to reconcile
- Task touches secrets, credentials, live trading, production order-entry
- Small direct edit is faster

### Lane Ownership Rules
1. **Hermes owns Kanban lifecycle** — Codex must never call `kanban_complete`, `kanban_block`, etc.
2. **Hermes owns final acceptance** — treat Codex output as untrusted until reviewed
3. **Hermes owns test execution** — repeat verification from Hermes after Codex exits
4. **Hermes owns safety** — reject lane if safety boundaries are changed
5. **Hermes owns cleanup** — kill stuck Codex processes, remove temporary worktrees

### Quick Start
```bash
# Create isolated worktree
TASK_ID="t_$(date +%s)"
BRANCH="codex/${TASK_ID}/$(date +%Y%m%d%H%M%S)"
WORKTREE="/tmp/${TASK_ID}-codex-lane"
git -C "$REPO" worktree add -b "$BRANCH" "$WORKTREE" main

# Run Codex bounded task
terminal(command="codex exec --full-auto '$(cat /tmp/codex_prompt.md)'", workdir="$WORKTREE", background=true, pty=true, notify_on_complete=True)

# Hermes reconciliation checklist (before accepting lane):
# [ ] git status shows only expected files
# [ ] Diff reviewed by Hermes
# [ ] No secrets or out-of-scope changes
# [ ] Hermes ran canonical tests
# [ ] kanban_complete.metadata.codex_lane populated
```

Load `kanban-codex-lane` skill directly for the full protocol (worktree pattern, prompt construction, monitoring, timeout, kill, reconciliation checklist, metadata schema).

---

## Common Pitfalls (All Three Agents)

| Agent | Pitfall |
|-------|---------|
| Claude Code | Interactive mode REQUIRES tmux — using `pty=true` alone is unreliable |
| Claude Code | `--dangerously-skip-permissions` dialog defaults to WRONG choice (No) — must send Down+Enter |
| Claude Code | `--max-budget-usd` minimum is ~$0.05 (cache creation cost) |
| Claude Code | Context degrades above 70% window — use `/compact` proactively |
| Codex | ALWAYS use `pty=true` — hangs without it |
| Codex | MUST run inside a git repo — use `mktemp -d && git init` for scratch |
| Codex | Sandbox failures in gateway context → use `--sandbox danger-full-access` |
| OpenCode | `/exit` is NOT valid — opens agent selector. Use Ctrl+C (`\x03`) |
| OpenCode | PATH mismatch can select wrong binary — check `which -a opencode` |
| All | Background sessions accumulate — clean up with `tmux kill-session` or `process(action="kill")` |
| All | Parallel worktrees prevent collisions — never share one workdir across parallel agents |

## Environment Limitations (Known Constraints)

### Terminal Access in Subagents

**Critical**: `delegate_task` subagents spawned via the HTTP API channel do NOT have shell/terminal access, even when `toolsets: ["terminal"]` is specified. Multiple subagent instances across this codebase consistently report: "I do not have access to shell commands like `git clone`" — their available tools are limited to `read_file`, `write_file`, `search_files`, and `patch` only.

**Workaround for git clone / build tasks**: When a task requires `git clone`, building from source, or running shell commands:
1. Do NOT delegate to a subagent — perform the work in the parent session directly
2. If the parent session also lacks `execute_code` shell access (blocked by cron approval gates), provide the user with manual terminal commands to run
3. For GitHub README content specifically: use `browser_navigate` to the GitHub page + `browser_console` with `document.body.innerText` to extract rendered markdown content (GitHub's raw content endpoints require auth for high-rate-limit access)

**Note**: This limitation applies to the HTTP API stateless channel. The tmux/CLI channel may have different access characteristics — test before assuming no terminal access exists.

## Verification Smoke Test

```bash
# Claude Code
terminal(command="claude -p 'Respond with exactly: CLAUDE_OK'")

# Codex
terminal(command="codex exec 'Respond with exactly: CODEX_OK'", workdir="$HOME/project", pty=true)

# OpenCode
terminal(command="opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'")
```

## Related Skills

- `kanban-orchestrator` — Hermes Kanban board orchestration
- `kanban-worker` — individual Kanban worker task execution
- `kanban-codex-lane` — Codex-as-lane protocol for Kanban workers
- `hermes-agent` — Hermes CLI setup and configuration
