---
name: autonomous-ai-agents
description: "Delegate coding to external AI coding agents: Claude Code, Codex, OpenCode. Use when you want an external coding agent to implement, refactor, review, or test code."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agents, claude-code, codex, opencode, autonomous, delegation, coding]
    related_skills: []
---

# Autonomous Coding Agents

Use external AI coding agents (Claude Code, Codex, OpenCode) to implement, refactor, review, or test code. Each has different strengths — pick based on the provider ecosystem and task requirements.

## When to Use

Use a coding agent when:
- User asks to "use Claude Code", "use Codex", or "use OpenCode"
- You need an external agent to implement, refactor, or review code
- Bounded coding task benefits from isolated execution
- Multi-agent parallelization for independent tasks

**This skill vs individual skills:** This umbrella covers the shared orchestration patterns. Each agent also has its own deep-dive skill for agent-specific flags and workflows.

## Quick Reference

| Agent | Provider | Best For | Install |
|-------|----------|----------|---------|
| Claude Code | Anthropic | General coding, complex reasoning, PR review | `npm install -g @anthropic-ai/claude-code` |
| Codex | OpenAI | General coding, fast iterations | `npm install -g @openai/codex` |
| OpenCode | Open source / multi-provider | Provider-agnostic, open-source ecosystems | `npm i -g opencode-ai@latest` |

## Common Orchestration Patterns

### Pattern 1: Print Mode (One-Shot, Preferred)

Non-interactive, bounded task, exits when done. Use this for most automation.

```python
terminal(command="claude -p 'Add error handling to src/api/' --max-turns 10", workdir="/path/to/project", timeout=120)
```

```python
terminal(command="codex exec 'Add error handling to src/api/'", workdir="/path/to/project", pty=True)
```

```python
terminal(command="opencode run 'Add error handling to src/api/'", workdir="/path/to/project")
```

### Pattern 2: Interactive PTY (Multi-Turn)

Conversational, iterative work. Requires PTY. For Claude Code, wrap in tmux.

```python
# Claude Code via tmux
terminal(command="tmux new-session -d -s claude -x 140 -y 40")
terminal(command="tmux send-keys -t claude 'cd /path && claude' Enter")
terminal(command="sleep 5 && tmux send-keys -t claude 'Refactor auth module' Enter")
terminal(command="sleep 30 && tmux capture-pane -t claude -p -S -60")
```

### Pattern 3: Background + Monitor

For long tasks, start in background and poll.

```python
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="/path", background=True, pty=True)

# Poll
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>", limit=200)
```

## Authentication

Each agent needs its own auth setup. Quick checks:

```bash
# Claude Code
claude auth status
claude --version

# Codex
codex --version

# OpenCode
opencode --version
opencode auth list
```

## Agent-Specific Skills

For detailed reference on each agent, use the individual skills:
- `claude-code` — Claude Code v2.x full reference, print mode, interactive mode, tmux orchestration, slash commands, MCP integration, PR review patterns
- `codex` — Codex CLI, worktrees, parallel PR reviews, `--full-auto` / `--yolo` modes
- `opencode` — OpenCode CLI, TUI keybindings, session management, multi-provider auth

## Shared Best Practices

1. **Always use `workdir`** — keep the agent focused on the right project
2. **Set `--max-turns` in print mode** — prevents runaway loops and runaway costs
3. **Use `pty=true` for interactive sessions** — required for TUI-based agents
4. **Monitor background sessions** — check progress with `process(action="poll")`
5. **Clean up tmux sessions** — `tmux kill-session -t <name>` when done
6. **Report results to user** — summarize what changed, tests passed, remaining risks

## Delegation vs Direct Implementation

| | Coding Agent | Direct (you) |
|-|-------------|--------------|
| Isolation | Fresh context, no session pollution | Your accumulated context |
| Speed | Good for bounded tasks | Faster for small fixes |
| Complexity | Handles multi-step well | Better for simple one-liners |
| Tool access | Full terminal + file tools | Same tools |
| Best for | Large features, reviews, parallel work | Quick fixes, research |

## Quick Start by Provider

**Claude Code (Anthropic):**
```bash
npm install -g @anthropic-ai/claude-code
claude  # interactive, or:
claude -p "task" --max-turns 10
```

**Codex (OpenAI):**
```bash
npm install -g @openai/codex
codex exec "task"
```

**OpenCode (multi-provider):**
```bash
npm i -g opencode-ai@latest
opencode run "task"
opencode auth list
```

## References

- `references/claude-code-reference.md` — Claude Code full CLI reference (flags, modes, settings)
- `references/codex-reference.md` — Codex CLI reference
- `references/opencode-reference.md` — OpenCode CLI reference
- `templates/` — Prompt templates for common tasks
