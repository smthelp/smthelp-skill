---
name: kanban-multi-agent-workflow
description: "Class-level umbrella for Hermes Kanban multi-agent coordination: orchestrator decomposition patterns and worker execution lifecycle. Load this skill when setting up a Kanban board, routing work across specialist profiles, or executing as a Kanban worker."
metadata:
  source: hermes
  origin: "autonomous-ai-agents/kanban-multi-agent-workflow"
---
# Kanban Multi-Agent Workflow — Class Umbrella

This skill is the class-level umbrella for **Hermes Kanban** — a SQLite-backed persistent task board with multi-agent dispatch, dependency chains, and cross-profile coordination. It covers both the **orchestrator role** (decomposition, routing, fan-out) and the **worker role** (execution, handoff, block/complete).

## Two Roles, One System

| Role | Skill | Job |
|------|-------|-----|
| **Orchestrator** | `kanban-orchestrator` (§1) | Decompose goals, create tasks, link dependencies, fan out to specialists |
| **Worker** | `kanban-worker` (§2) | Execute assigned tasks, send heartbeats, block when stuck, complete with metadata |

## §1 — Kanban Orchestrator (Decomposition & Routing)

The orchestrator's job is **route, don't execute**. It discovers available profiles, sketches a task graph, creates cards, links dependencies, and reports back to the user.

### Discovery Before Decomposition

Always discover available profiles first — the dispatcher silently fails to spawn unknown assignees:

```bash
hermes profile list
```

### When to Use the Board

Create Kanban tasks when:
- Multiple specialists are needed (research + analysis + writing)
- Work should survive a crash or restart
- User might want to interject (human-in-the-loop)
- Multiple subtasks can run in parallel
- Review/iteration is expected
- The audit trail matters

Otherwise: use `delegate_task` for one-shot reasoning tasks.

### Anti-Temptation Rules

- **Do not execute the work yourself** — your restricted toolset usually excludes terminal/file/code
- **For any concrete task, create a Kanban task and assign it**
- **Split multi-lane requests before creating cards** — extract independent lanes first
- **Run independent lanes in parallel** — link only true data dependencies
- **Never create dependent work as independent ready cards** — use `parents=[...]`

### Decomposition Playbook

```
Step 1: Understand the goal (ask clarifying questions if ambiguous)
Step 2: Sketch the task graph (lanes → profiles → dependencies)
Step 3: Create tasks and link (capture returned ids for parent links)
Step 4: Complete your own task (summarize what you created)
Step 5: Report back to the user
```

### Key Patterns

**Fan-out + fan-in:** N research cards (no parents), one synthesis card with all as parents.

**Pipeline with gates:** `planner → implementer → reviewer`, each gated by `parents=[previous_task]`.

**Goal-mode cards:** For long open-ended tasks, pass `goal_mode=True` to wrap the worker in a judge loop.

See `kanban-orchestrator` skill for the full playbook (anti-temptation rules, dependency linking, stuck-worker recovery, goal-mode, metadata shapes).

## §2 — Kanban Worker (Execution & Handoff)

The worker's job is **execute and hand off**. It orients to the workspace, does the work, sends heartbeats, and completes with structured metadata.

### Workspace Kinds

| Kind | Behavior |
|------|----------|
| `scratch` | Fresh tmp dir, yours alone, GC'd when task archived |
| `dir:<path>` | Shared persistent directory — treat as long-lived state |
| `worktree` | Git worktree — run `git worktree add` if `.git` missing |

### Tenant Isolation

If `$HERMES_KANBAN_TENANT` is set, prefix memory entries with the tenant to prevent cross-tenant leakage.

### Good Handoff Shapes

```python
# Coding task
kanban_complete(
    summary="shipped rate limiter — token bucket, 14 tests pass",
    metadata={"changed_files": ["rate_limiter.py"], "tests_run": 14, "tests_passed": 14},
)

# Research task
kanban_complete(
    summary="3 libraries reviewed; vLLM wins on throughput",
    metadata={"sources_read": 12, "recommendation": "vLLM"},
)
```

### Claiming Cards You Created

If your run produced new tasks, pass their ids in `created_cards` on `kanban_complete`. Only list ids you captured from successful `kanban_create` returns — never invent ids.

### Block Reasons That Get Answered Fast

Bad: `"stuck"`. Good: one sentence naming the specific decision needed.
```python
kanban_block(reason="Rate limit key choice: IP (NAT-unsafe) or user_id (requires auth)?")
```

### Do NOT

- Call `delegate_task` as a substitute for `kanban_create`
- Call `clarify` — use `kanban_block` + comment instead
- Modify files outside `$HERMES_KANBAN_WORKSPACE`
- Create follow-up tasks assigned to yourself
- Complete a task you didn't finish

See `kanban-worker` skill for the full reference (workspace handling, retry diagnostics, claim validation, CLI fallback).

## Common Pitfalls

| Issue | Prevention |
|-------|------------|
| Unknown profile names silently fail | Always run `hermes profile list` before assigning |
| Over-linking due to wording | "Also check X" is often parallel, not dependent |
| Forgetting dependency links | `research → implement → review` needs explicit parents |
| Worker crashing/hallucinating | Use Reclaim → Reassign → Change profile model recovery path |
| Background sessions accumulating | Clean up with `tmux kill-session` or `process(action="kill")` |

## Related Skills

- `autonomous-coding-agents` — delegate coding to Claude Code, Codex, OpenCode
- `hermes-agent` — Hermes CLI setup and configuration
- `plan` — Hermes slash-command planner
