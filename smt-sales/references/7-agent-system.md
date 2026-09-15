# 7-Agent Sales Orchestration System
**Profile Directory:** `/Users/mac/.hermes/profiles/`
**Skill Reference:** `smt-sales`

## Architecture

7 independent Hermes profiles installed at `/Users/mac/.hermes/profiles/`:

| Profile | Role | Entry Command |
|---------|------|--------------|
| `orchestrator` | CEO Jason — routes & decides | `orchestrator chat` |
| `leadhunter` | Finds & qualifies EMS prospects | `leadhunter chat` |
| `inboxsorter` | Classifies inbound inquiries A/B/C | `inboxsorter chat` |
| `solutionarchitect` | Designs solution + ROI | `solutionarchitect chat` |
| `negotiator` | Follow-up & objection handling | `negotiator chat` |
| `postsales` | Delivery, installation, retention | `postsales chat` |
| `contentrepurposer` | Case study → multi-channel content | `contentrepurposer chat` |

## Directory Structure

```
/Users/mac/.hermes/profiles/
  orchestrator/     AGENT.md + hermes.json
  leadhunter/       SOUL.md + hermes.json
  inboxsorter/      SOUL.md + hermes.json
  solutionarchitect/SOUL.md + hermes.json
  negotiator/       SOUL.md + hermes.json
  postsales/        SOUL.md + hermes.json
  contentrepurposer/SOUL.md + hermes.json

/Users/mac/.hermes/agents/_shared/
  distribution.yaml  (profile bundle manifest)
  log-task-local.sh  (shared logging script)

/Users/mac/Documents/SouthernMachinerySales/
  leads/            raw prospect data
  projects/          active deals (demo_customer/ template)
  proposals/        generated proposals
  casestudies/       success stories
  content/LinkedIn/  repurposed social posts
  content/YouTube/  video scripts
  roi/              ROI analyses
  followups/        negotiation follow-up logs
  competitors/       competitive intel
```

## Workflow Flow

```
LeadHunter ──(qualified lead)──> InboxSorter ──(Grade A)──> SolutionArchitect
                                                                   │
                                              <──(proposal)───────┘
                                                                   │
                                                       Negotiator ──(order)
                                                           │
                                                      PostSales ──(installed)
                                                           │
                                                 ContentRepurposer ──(content)
                                                           │
                                               ┌───────────┘
                                               └──> InboxSorter (new inbound leads loop)
```

## Key Learnings from Installation

### What worked
- `hermes profile install <local-dir>` with `distribution.yaml` at root — installs ALL profiles from a single bundle
- `hermes profile alias <name>` creates shell wrappers at `/Users/mac/.local/bin/<name>` (no sudo needed)
- hermes.json per profile sets per-profile model + toolsets override
- SOUL.md for specialist agents; AGENT.md for orchestrator role

### Common install errors
- **Missing `distribution.yaml`**: `hermes profile install` fails silently or with unclear error — always include it
- **Script heredoc truncation**: Original installer script had embedded copy that truncated the log-task-local.sh heredoc — Python script execution was more reliable than nested heredocs in bash
- **`hermes profile alias` positional args**: Must be `hermes profile alias <profile_name>` not the reverse; `--name` flag is for custom alias name override

### `hermes.json` per profile template
```json
{
  "model": {
    "default": "MiniMax-M2.7-highspeed",
    "provider": "custom"
  },
  "toolsets": ["web", "terminal", "file", "skills", "delegation"],
  "agent": {
    "max_turns": 90,
    "gateway_timeout": 1800
  }
}
```

## Multi-Agent Collaboration Patterns

### Pattern 1: Direct delegate_task (fast, single-session)
```
default/orchestrator session
  └── delegate_task to leadhunter  (stateless, one-shot)
  └── delegate_task to solutionarchitect (stateless, one-shot)
  └── collect results, present to Jason
```
Use when: tasks are independent, no persistent state needed.

### Pattern 2: Kanban board (persistent, cross-session)
```
default session ──> kanban_create(task, assignee=leadhunter)
                  ──> kanban_create(task, assignee=solutionarchitect)
                  ──> dispatcher spawns workers for ready tasks
                  ──> workers complete, results collected
```
Use when: tasks span multiple sessions, need audit trail, or involve human review gates.

### Pattern 3: Shell wrapper pipeline
```
inboxsorter chat ──(output file)──> solutionarchitect chat
solutionarchitect chat ──(output file)──> negotiator chat
```
Use when: passing structured documents between agents (proposal.md, roi_analysis.md).

## Quick Reference

```bash
# List all profiles
hermes profile list

# Start any agent
orchestrator chat
leadhunter chat
inboxsorter chat
solutionarchitect chat
negotiator chat
postsales chat
contentrepurposer chat

# Hermes native form
hermes -p orchestrator chat
hermes -p leadhunter chat

# Shared logging
/Users/mac/.hermes/agents/_shared/log-task-local.sh orchestrator "task" "done" "MiniMax-M2.7-highspeed"
```

## Test Cases Summary

### Test 1: Full Lead-to-CaseStudy Flow
```
InboxSorter → SolutionArchitect → Negotiator → PostSales → ContentRepurposer
```
Simulates: Vietnam EMS customer inquiry → solution → order → installation → case study.

### Test 2: LeadHunter Alone
```
leadhunter chat
```
Input: Search criteria for Mexico EMS factories. Output: Qualified prospect list + personalized outreach messages.

### Test 3: Orchestrator Routing Validation
```
orchestrator chat
```
Input: 3 mixed tasks. Output: Correct agent routing decisions with reasoning.
