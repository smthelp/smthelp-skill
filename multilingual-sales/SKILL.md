---
name: multilingual-sales
description: Localize Southern Machinery sales content into multilingual customer-facing messages. Use when Codex needs English plus another language version for emails, WhatsApp, landing pages, product introductions, FAQs, or market-specific outreach while preserving SMT/THT technical accuracy and sales tone.
---

# Multilingual Sales

## Purpose

Create or localize sales content for non-English markets while keeping technical terms accurate and claims controlled.

## Workflow

1. Confirm target language, market, channel, and audience technical level.
2. Draft from the English source when possible, then localize rather than literal-translate.
3. Preserve model names, CPH figures, machine names, and contact details exactly.
4. Explain technical terms simply for non-engineering buyers.
5. If the target market needs cultural adaptation, adjust CTA tone and formality.

## Quality Rules

- Keep side-by-side versions when the user requests review.
- Do not translate brand names, model names, emails, URLs, or hashtags unless asked.
- Use English as fallback for technical nouns where local translation may be ambiguous.
- Mark any uncertain technical wording for human review.

## Output Format

```markdown
## English Version
[content]

## [Target Language] Version
[localized content]

## Localization Notes
- 
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
