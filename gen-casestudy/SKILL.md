---
name: gen-casestudy
description: Generate anonymized Southern Machinery customer success case studies and before/after automation stories. Use when Codex needs EMS factory case studies, ROI narratives, labor-saving stories, industry examples, blog drafts, LinkedIn proof posts, or marketing material based on SMT/THT automation outcomes without exposing confidential customer information.
---

# Gen Casestudy

## Purpose

Turn customer outcomes into credible case-study narratives that support Southern Machinery sales and marketing.

## Workflow

1. Anonymize customer identity by default unless the user explicitly provides publishable approval.
2. Extract industry, country/region, production challenge, current manual process, selected machines, implementation scope, and measured or assumed outcomes.
3. Separate verified results from estimated ROI or marketing assumptions.
4. Structure the story around challenge, solution, implementation, measurable impact, and next step.
5. Keep customer-facing claims conservative and review-ready.

## Output Format

```markdown
## Title
[Industry + automation outcome]

## Customer Profile
- Region:
- Industry:
- Production type:

## Challenge
[manual labor, quality, speed, expansion, or cost issue]

## Southern Machinery Solution
| Equipment | Role | Reason |
|---|---|---|

## Results
- Labor:
- Throughput:
- Quality:
- ROI:

## Customer-Ready Summary
[English summary suitable for website or LinkedIn]

## Review Notes
- Verified facts:
- Items needing confirmation:
```

## Southern Machinery Rules

- Protect customer information and anonymize by default.
- Do not invent numeric outcomes; label estimates clearly.
- Use catalog-backed machine specs only.
- Keep the tone practical, credible, and non-hype.
