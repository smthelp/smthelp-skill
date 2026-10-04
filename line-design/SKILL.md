---
name: line-design
description: Design SMT/THT PCB assembly line concepts for Southern Machinery prospects. Use when Codex needs to recommend full production line configurations, process flow, machine sequence, board handling, peripheral equipment, assumptions, capacity notes, or layout-ready equipment lists.
---

# Line Design

## Purpose

Create practical line configuration concepts for PCB assembly automation projects using Southern Machinery equipment.

## Workflow

1. Identify process scope: SMT, THT, mixed SMT+THT, LED line, wave soldering, inspection, cleaning, or board handling.
2. Define required inputs: PCB size, product type, component mix, target UPH/CPH, shifts, current bottleneck, available floor space, and inspection needs.
3. Propose a process sequence with machine names only where appropriate.
4. Separate confirmed recommendations from assumptions requiring engineering confirmation.
5. Provide a next-step data checklist for layout and quotation.

## Typical Modules

- SMT line: loader → printer `SP-1200` → mounter (`S-600SV`, `S-530SV`, or `S-V8`) → reflow `S-6600` → AOI `S-H680` → unloader.
- THT line: insertion (`S3010A`, `S4000`, or `S7020`) → wave soldering `S-WS350B` → cleaning `SME5600` → inspection/handling.
- Board handling: loaders, unloaders, buffer, inverter, turning conveyor, translation conveyor, NG/OK unloader, intelligent rack.

## Output Format

```markdown
## Proposed Line Concept
| Step | Equipment | Purpose | Notes |
|---|---|---|---|

## Capacity And Assumptions
- 

## Optional Add-ons
- 

## Information Needed For Final Layout
1.
2.
3.
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
