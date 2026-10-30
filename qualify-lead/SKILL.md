---
name: qualify-lead
description: Qualify Southern Machinery SMT/THT automation leads from inquiries, emails, LinkedIn messages, trade-show notes, or customer lists. Use when Codex needs to grade prospects A/B/C, summarize needs, recommend product direction, ask qualification questions, or suggest next actions for PCB assembly equipment sales.
---

# Qualify Lead

## Purpose

Evaluate whether a prospect is suitable for Southern Machinery SMT/THT automation equipment and decide the next sales action.

## Input To Look For

- Company, country, industry, and role.
- Inquiry text, message history, or trade-show note.
- PCB type, component type, monthly output, current process, worker count, timeline, and budget.
- Any mentioned machine model, production target, pain point, or catalog request.

## Workflow

1. Extract the available lead facts and mark missing fields.
2. Assign a lead grade:
   - `A`: mentions specific demand, production volume, factory scale, target machine, budget, timeline, or urgent automation pain.
   - `B`: shows buying or quotation intent but lacks technical or timeline detail.
   - `C`: only asks for catalog, general information, or has unclear fit.
3. Identify the most likely automation direction: radial insertion, axial insertion, odd-form insertion, LED mounting, lens mounting, wave soldering, board handling, spare parts, or full line.
4. Ask up to 3 high-value qualification questions when data is incomplete.
5. Recommend an action window: A within 24 hours, B within 48 hours, C with catalog and website link.

## Output Format

```markdown
## Lead Grade
A/B/C — one-sentence reason.

## Need Analysis
- Pain point:
- Current process:
- Production clue:
- Missing info:

## Recommended Direction
- Primary direction:
- Possible machines:

## Next Questions
1.
2.
3.

## Suggested Action
Clear next step and response channel.
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
