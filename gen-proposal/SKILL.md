---
name: gen-proposal
description: Generate complete Southern Machinery automation proposal drafts. Use when Codex needs structured English proposals for SMT/THT production lines, equipment recommendations, parameter tables, ROI assumptions, implementation steps, cover letters, quotation narratives, or customer-facing solution documents for PCB assembly automation projects.
---

# Gen Proposal

## Purpose

Create a structured proposal draft that can be reviewed by the sales engineer before sending to a customer.

## Workflow

1. Summarize customer background, PCB type, component mix, target output, current bottleneck, worker count, and timeline.
2. Recommend a machine or line configuration using only known Southern Machinery equipment and catalog-backed values.
3. Include assumptions and data gaps before ROI or capacity calculations.
4. Provide a clear equipment table; leave price fields blank or marked `To be confirmed` unless the user provides prices.
5. End with next steps for sample testing, technical confirmation, layout, quotation, or online meeting.

## Proposal Structure

```markdown
# Proposal For [Customer]

## 1. Executive Summary
[Concise customer-specific solution overview]

## 2. Customer Requirements
| Item | Details | Status |
|---|---|---|

## 3. Recommended Solution
| Step | Equipment | Key Specification | Purpose |
|---|---|---|---|

## 4. Expected Benefits
- Labor reduction:
- Throughput improvement:
- Quality stability:
- ROI logic:

## 5. Assumptions And Items To Confirm
- 

## 6. Next Steps
1.
2.
3.
```

## Southern Machinery Rules

- Do not invent prices, delivery time, or unsupported specs.
- Keep ROI transparent and assumption-based.
- Default to English for customer-facing proposals.
- Include contact details: `jasonwu@smthelp.com`, `www.smthelp.com`, `+8613602562576`.
