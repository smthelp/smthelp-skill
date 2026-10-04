---
name: superpowers
description: "Superpowers agentic software development methodology and skills framework from obra/superpowers (253k stars on GitHub). Installs 14 composable skills under ~/.hermes/skills/superpowers/. Use when building features, debugging, planning, or running multi-step development tasks. Trigger: any creative work request, plan request, or debugging session."
version: 1.0.0
author: Hermes Agent / Jason Wu
tags: [agentic, software-development, TDD, debugging, planning, subagent, skills-framework]
---

# Superpowers Skills Framework

Superpowers is a complete software development methodology for coding agents. It was installed globally into `~/.hermes/skills/superpowers/` from https://github.com/obra/superpowers.

## Architecture

- **Umbrella**: `superpowers` (this skill) — the entry point
- **Sub-skills**: 14 skills in `~/.hermes/skills/superpowers/`
- **Collision note**: 4 sub-skills share bare names with existing built-in Hermes skills (subagent-driven-development, systematic-debugging, test-driven-development, writing-plans). Use full path `superpowers/<name>` for lookup to avoid ambiguity.

## The 14 Sub-Skills

| Skill | Trigger | Key Output |
|---|---|---|
| `brainstorming` | Any creative/implementation request | Approved design doc in `docs/superpowers/specs/` |
| `writing-plans` | After design approved | Bite-sized task plan in `docs/superpowers/plans/` |
| `subagent-driven-development` | Plan ready for execution | Parallel subagent task execution with 2-stage review |
| `test-driven-development` | During implementation | RED-GREEN-REFACTOR enforcement |
| `systematic-debugging` | Bug investigation | 4-phase root cause analysis |
| `verification-before-completion` | After a fix | Confirmed fix, not just symptom relief |
| `dispatching-parallel-agents` | Concurrent task batching | Parallel subagent workflows |
| `executing-plans` | Batch execution | Plan execution with human checkpoints |
| `requesting-code-review` | Between tasks | Severity-tagged review findings |
| `receiving-code-review` | Review feedback received | Actionable response to critique |
| `using-git-worktrees` | Parallel branch work | Isolated worktree per branch |
| `finishing-a-development-branch` | Tasks complete | Merge/PR/keep/discard decision |
| `writing-skills` | Creating new skills | Well-formed SKILL.md with testing |
| `using-superpowers` | Framework onboarding | Skills system introduction |

## Core Workflow Sequence

```
brainstorming → writing-plans → subagent-driven-development
                ↓
        test-driven-development (per task)
                ↓
        requesting-code-review (between tasks)
                ↓
        finishing-a-development-branch
```

## Loading Sub-Skills

Load any sub-skill explicitly by full path to avoid the built-in name collision:

```
/skill superpowers/brainstorming
/skill superpowers/writing-plans
/skill superpowers/subagent-driven-development
```

Or at Hermes startup:
```
hermes -s superpowers/brainstorming,superpowers/writing-plans
```

## Key Principles

- **Design before code**: brainstorming gates ALL implementation
- **TDD always**: write failing test first, never code before test
- **Plans as gate**: writing-plans must complete before any code is written
- **Subagent autonomy**: subagent-driven-development allows agents to work autonomously for hours
- **Evidence over claims**: verify before declaring success

## Visual Companion (Optional)

The brainstorming skill includes an optional visual companion feature that shows diagrams in-browser. It loads the Prime Radiant logo from their CDN by default. To disable: set `SUPERPOWERS_DISABLE_TELEMETRY=1` in environment.

## Reference

- Repo: https://github.com/obra/superpowers
- License: MIT
- Community: Discord (discord.gg/35wsABTejz)
