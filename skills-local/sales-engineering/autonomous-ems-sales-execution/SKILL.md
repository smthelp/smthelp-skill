---
name: autonomous-ems-sales-execution
description: Closed-loop autonomous sales system for Southern Machinery EMS non-China global outreach. Run each cycle to generate CRM reports, execute outreach, and evolve pitch. Phase 1 of the autonomous sales engine.
triggers:
  - "autonomous sales run"
  - "closed loop execution"
  - "EMS outreach cycle"
  - "sales system run"
---

# Skill: Autonomous EMS Sales Execution System

## Context
This skill runs the complete closed-loop sales system for Southern Machinery targeting
EMS电子产品制造代工厂 (non-China global). Execute this skill to run each sales cycle.
It reads all existing skills, generates the cycle report, updates the CRM, and identifies
new skill documents to create or update.

## Reference
- SOUL.md (master identity + strategy)
- pitchdeck-ems-global-smt-line (machine breakdowns)
- improved-pitch-ems-global-smt-line (close scripts)
- cold-email-templates-ems-global (email templates)
- objection-handling-global (objection scripts)
- smt_roi_calculator.py (ROI tool)

## Each Cycle Does the Following:

### PHASE 1: READ CRM PIPELINE
File: /tmp/smt_crm_pipeline.json
Read current stage for each prospect.
Flag: any stuck >14 days, any new qualified leads.

### PHASE 2: REVIEW LAST INTERACTION LOG
File: /tmp/smt_weekly_activity_log.md
Count: emails sent, responses, calls, pipeline movement.
Calculate: conversion rates per stage.

### PHASE 3: EXECUTE OUTREACH (n8n or manual)
- Read cold-email-templates-ems-global for current email angle
- Use region-specific template (Labor for Vietnam, CapEx for Poland, RoHS for Mexico)
- Bcc jasonwu@smthelp.com for tracking
- Track opens/clicks via n8n workflow at n8n.autoinsertion.com

### PHASE 4: RUN ROI CALCULATOR
For each qualified prospect on call:
  python3 /tmp/smt_roi_calculator.py --cli [country] [lines] [ops] [shifts] [op_cost] [vol] [defect] [rework] [scrap] [scrap_r] [line_cost] [changeovers] [old_co] [new_co]

Key: Always confirm operator cost. If <$2,400/yr, flag and verify.

### PHASE 5: GENERATE CYCLE REPORT
Output: CRM progress report (this format):

## CYCLE [N] CRM PROGRESS REPORT
Date: [DATE]
Pipeline: [LEADS] leads → [QUALIFIED] qualified → [MEETINGS] meetings → [PROPOSALS] → [CLOSED]

| Prospect | Region | Stage | Urgency | Next Action | Deal Value | Probability |
|---------|--------|-------|---------|------------|-----------|------------|
| [Name] | [Region] | [Stage] | [Level] | [Action] | $[Amount] | [X]% |

Movement this cycle:
- [Stage change 1]
- [Stage change 2]

New skills created: [list]
Skills updated: [list]

Next action plan:
1. [Action]
2. [Action]
3. [Action]

### PHASE 6: SELF-EVOLUTION
After each cycle, ask:
1. What objection was not in the library?
2. What pitch moment landed best?
3. What metric is not moving?

Create new skill document if:
- New objection encountered → skills/Objection_Handling_[Region].md
- New pitch moment documented → skills/Pitch_[Region]_[Vertical].md
- New vertical encountered → skills/Vertical_[VerticalName].md
- Competitive intelligence found → skills/Competitive_[Competitor]_[Region].md

## FILES PRODUCED BY THIS SKILL
- /tmp/smt_crm_pipeline.json — CRM pipeline data
- /tmp/smt_weekly_activity_log.md — Activity tracker
- /tmp/prospect_research_brief_template.md — Research brief
- /tmp/smt_roi_calculator.py — ROI calculator

## CYCLE LOG
| Cycle | Date | Leads | Qualified | Meetings | Proposals | Closed |
|-------|------|-------|---------|---------|---------|--------|
| 1 | 2026-05-01 | 3 | 1 | 0 | 0 | 0 |
