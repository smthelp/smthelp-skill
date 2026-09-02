---
name: session-2026-05-01-ems-global
description: "Critical session learnings from 2026-05-01 EMS global sales system initialization — CRM data, sensitivity bugs, cron setup, all skill documents created"
metadata:
  source: hermes
  origin: "sales-engineering/session-2026-05-01-ems-global"
---
# Session 2026-05-01 — EMS Global Sales System Initialization

## CRM SEEDED PROSPECTS
- PL-001: Poland Automotive EMS | Stage: QUALIFIED | Deal: $420,000 | Urgency: IATF 16949 audit in 7 weeks (CRITICAL)
- VN-001: Vietnam Consumer EMS | Stage: LEAD | Deal: $380,000
- MX-001: Mexico Industrial EMS | Stage: LEAD | Deal: $320,000
- Pipeline total: $1,120,000 | Weighted: $537,000

## ROI CALCULATOR — CRITICAL SENSITIVITY BUG
`/tmp/smt_roi_calculator.py`
- Default operator cost $3,600/yr → artificially HIGH payback in low-wage markets (76mo Vietnam, 79mo Mexico)
- Poland scenario: 8 ops × 3 shifts × $5,200/yr = $249,600/yr labor savings → 18.7mo payback (strongest close)
- ALWAYS confirm actual fully-loaded operator cost before running calculator
- If prospect quotes <$2,400/yr, challenge: "fully loaded means wages+benefits+management+supervision"

## SKILL DOCUMENTS CREATED (all in ~/.hermes/skills/sales-engineering/)
1. `objection-handling-global` — Feel-Felt-Found scripts for China quality objections
2. `pitchdeck-ems-global-smt-line` — Feynman-level 5-machine breakdown, 15 discovery Qs (16KB)
3. `cold-email-templates-ems-global` — 3 ROI emails, 14 discovery Qs, 9-slide PPT outline (8.7KB)
4. `improved-pitch-ems-global-smt-line` — 5 close scripts from testing loop gaps (11KB)
5. `autonomous-ems-sales-execution` — Self-running weekly sales cycle + cron (3.5KB)

## CRON JOB
- Job ID: 137cfa914274
- Name: "EMS Non-China Global — Weekly Sales Cycle"
- Schedule: Every Monday 9:00 AM +08:00 (next: 2026-05-04)
- Generates updated CRM report + prompts for real client updates

## SYSTEM FILES
- /tmp/smt_crm_pipeline.json — CRM pipeline (3 prospects)
- /tmp/smt_weekly_activity_log.md — Weekly activity tracker
- /tmp/smt_self_evolution_log.md — Self-evolution cycle log
- /tmp/prospect_research_brief_template.md — Prospect research brief
- /tmp/30day_sales_roadmap.json — 30-day roadmap (37KB)
- ~/SOUL.md — Master identity document (247 lines, 11.7KB)

## KEY CLOSE SCRIPTS (from improved-pitch-ems-global-smt-line)
- Close 1: Used equipment / liquidator objection → "3 hidden costs" script
- Close 2: Yamaha ±0.025mm vs our ±0.030mm → "placement ≠ joint accuracy" script
- Close 3: 48h service geography → named route (Monterrey→Queretaro), remote-first mechanism
- Close 4: 30-second changeover reality → "magazine rack staged within 1 meter" installation standard
- Close 5: Compliance documentation → named documents (CoC, hole-fill report, temp profile log)

## SELF-EVOLUTION CYCLE FINDINGS
- Strengthened: RoHS close ("auditable not just a PDF"), 48h service structure, payback as primary metric
- New gaps: PROACTIVELY address liquidator objection BEFORE buyer raises it
- Buyer behavior: Objection order is predictable — liquidator first, then specs, then service, then changeover
