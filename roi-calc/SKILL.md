---
name: roi-calc
description: Calculate and explain ROI for Southern Machinery automation projects. Use when Codex needs to compare manual labor vs SMT/THT automation, estimate payback period, monthly labor savings, 3-year savings, assumptions, and customer-facing ROI summaries for machines such as S3010A, S4000, S7020, S-600SV, S-530SV, or S-V8.
---

# ROI Calc

## Purpose

Build transparent ROI calculations that help customers evaluate automation investment without overstating certainty.

## Required Inputs

- Current worker count and monthly salary per worker.
- Work days per month and hours per day.
- Current monthly output and component count per PCB if throughput comparison is needed.
- Target machine, expected operator count, and equipment price if provided by the user.
- Currency and analysis period.

## Calculation Rules

- Monthly labor cost = `worker_count × monthly_salary`.
- Post-automation labor cost = `remaining_operator_count × monthly_salary`.
- Monthly labor saving = `current_labor_cost - post_automation_labor_cost`.
- Payback months = `equipment_price / monthly_labor_saving` when equipment price is provided.
- 3-year gross labor saving = `monthly_labor_saving × 36`.
- Net 3-year saving = `3-year gross labor saving - equipment_price` when equipment price is provided.
- State all assumptions; do not invent price, wage, or utilization data.

## Output Format

```markdown
## Assumptions
- 

## ROI Summary
| Metric | Value |
|---|---:|
| Current monthly labor cost | |
| Post-automation labor cost | |
| Monthly labor saving | |
| Payback period | |
| 3-year gross saving | |
| 3-year net saving | |

## Manual vs Automation
| Item | Manual | Automation |
|---|---:|---:|

## Customer-Ready Summary
[English paragraph under 100 words with CTA.]
```

## Shared Southern Machinery Rules

- Default customer-facing output to English unless the user requests another language.
- Keep emails under 300 words, WhatsApp messages under 100 words, and LinkedIn posts at 150-300 words with 3 relevant hashtags.
- Use consultative selling: identify pain points, use verified data, position Southern Machinery as an automation partner, and end with a clear CTA.
- Do not invent prices, lead times, unavailable specifications, customer names, or unverified competitor claims.
- Treat product specs as catalog-based; if a requested spec is outside known data, say it needs further confirmation via `jasonwu@smthelp.com`.
- Include assumptions for ROI or capacity calculations so the customer can verify them.
- Add the Southern Machinery email signature when drafting a full email.

## Core Product Facts

- `S3010A`: radial component auto insertion, `12,000 CPH`, replaces `8-10` workers.
- `S4000`: axial component auto insertion, `13,000 CPH`, replaces `10` workers.
- `S7020`: odd-form component auto insertion, `6,500 CPH`, replaces `7` workers.
- `S-600SV`: standard LED mounter, `40,000 CPH`, replaces `20` workers.
- `S-530SV`: long-board LED mounter, `45,000 CPH`, supports PCB length up to `1.5 m`, ROI usually `<= 6 months` when assumptions support it.
- `S-V8`: lens + LED mounter, `40,000 CPH LED / 18,000 CPH lens`.
- Peripheral equipment includes `SP-1200`, `S-6600`, `S-H680`, `S-1688`, `S-SPM01`, `S-WS350B`, `S-B400`, `SME5600`, `SDS-900`, board handling, nozzles, and feeders.

## Signature

```text
Best regards,
[Your Name]
Sales Engineer | Southern Machinery Co., Ltd.
📧 jasonwu@smthelp.com
🌐 www.smthelp.com
📱 WhatsApp: +8613602562576
🏭 Shenzhen, China | Smart PCB Assembly Automation Since 2011
```
