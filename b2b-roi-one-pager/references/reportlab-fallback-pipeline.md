---
name: reportlab-fallback-pipeline
description: Reportlab + venv + pypdfium2 fallback recipe for generating the A4 ROI one-pager when Playwright + Chromium headless shell is unavailable or the Playwright render produces layout artifacts. Use ONLY as a fallback — the primary path (Playwright + inline SVG schematic) is preferred.
---

# Reportlab Fallback Pipeline

This is the older generation path (v1 of the ROI one-pager). It produces a smaller PDF (5-15 KB vs ~200 KB) using Reportlab's canvas-level control. Use it when:

- Playwright + Chromium headless shell is not installed (no `ms-playwright` cache)
- The customer needs a tiny PDF (email size limits, archival)
- The one-pager has heavy CJK / mixed-language content (Reportlab + registered TTF handles it cleanly)
- The Playwright render has layout artifacts that won't go away after 3 iterations

## Why Reportlab, not pdflatex / wkhtmltopdf / weasyprint

- `pdflatex` — handles CJK well but the layout DSL is hostile for a 7-section boxed design
- `wkhtmltopdf` — abandoned by upstream, QtWebEngine version skews cause rendering differences
- `weasyprint` — not installed in this environment
- `reportlab` — canvas-level control, precise, works in any Python venv

## The proven recipe (sandboxed, venv-based to bypass PEP 668)

Homebrew Python 3.12+ blocks system pip with PEP 668. Always use a venv:

```bash
# 1. Create isolated venv
python3 -m venv /tmp/pdfenv

# 2. Install reportlab
/tmp/pdfenv/bin/pip install reportlab --quiet

# 3. Generate the PDF
/tmp/pdfenv/bin/python3 build_pdf.py

# 4. Render preview PNG for visual QA
/tmp/pdfenv/bin/pip install pypdfium2 --quiet
/tmp/pdfenv/bin/python3 -c "import pypdfium2 as pdfium; pdfium.PdfDocument('out.pdf')[0].render(scale=2.0).to_pil().save('preview.png')"
```

End-to-end: < 10 seconds.

## Color tokens (v1 palette)

```
NAVY    = #0A2540   (header bar, table header, CTA banner, dark text)
ORANGE  = #FF6B35   (accent bars, payback row highlight, CTA headline)
LIGHT   = #F4F6F8   (specs card background, alt table row)
GRID    = #D8DEE5   (table cell borders)
TEXT    = #1A1A1A   (body text)
MUTED   = #5A6A7B   (disclaimers, secondary)
GREEN   = #2E8B57   (5-year savings row highlight)
```

Page setup: A4 portrait, 12mm margins on all 4 sides. Always 1 page, no overflow.

## CJK font registration (mandatory for mixed English + Chinese)

Helvetica is Latin-only. If the one-pager mixes English machine names with Chinese industry terms (typical for `给客户单页` deliverables targeting Asia), register a TTF:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# macOS ships these out of the box
pdfmetrics.registerFont(TTFont('STHeiti', '/System/Library/Fonts/STHeiti Medium.ttc'))
pdfmetrics.registerFont(TTFont('STHeiti-Bold', '/System/Library/Fonts/STHeiti Bold.ttc'))

# Use in styles
title_style = ParagraphStyle(
    name='CNTitle',
    fontName='STHeiti-Bold',
    fontSize=14,
    leading=18,
)
```

For Linux servers, install `fonts-noto-cjk` and register `NotoSansCJK-Regular.ttc`.

## 7-section structure (v1 layout — slightly different from v2)

The v1 Reportlab layout is 7 sections (vs v2's 6). Differences:

- v1 has a "Payback Model" table as a full-width dedicated section (Section 4) with **orange + green** highlight rows for payback period + 5-year savings
- v1 has separate "Why Southern Machinery" 3-column cards (Section 5) — no inline process flow
- v1 uses Helvetica throughout; v2 uses Inter/Helvetica Neue with `font-variant-numeric: tabular-nums`

If you're generating a v1-style deliverable for an existing customer expecting that exact layout, use this pipeline. Otherwise, prefer v2.

## Visual QA loop (3 iterations expected)

After generating, render the PDF to PNG and run `vision_analyze` to catch layout problems. Common issues that survive a first pass:

1. **Footer text overlap** — disclaimer + doc ref on the same y line. Fix: disclaimer at y=9mm, copyright at y=6mm, doc ref right-aligned at y=6mm.
2. **CTA banner too short** — 3 body lines + 3 right-column lines need ~18mm height. Fix: `cta_h = 18*mm`.
3. **"Why Us" card body too long for card height** — 3-4 wrapped lines need ≥ 36mm card height. Fix: `col_h = 36*mm` minimum.
4. **ROI table column widths sum > 168mm** — 4-column table fits in 168mm (PAGE_W − 2·MARGIN). Start with 56/36/44/32 mm.
5. **Right-aligned text vs left-aligned text collision** in CTA banner.

Always re-render and re-check after every fix. Budget 3 iterations minimum.

## SPIN follow-up questions (plant AFTER the PDF, not in it)

After the PDF is sent, the next conversation turn should plant 1-2 of these:

- **Situation**: "On the {product} line in {City} today, how many manual odd-form stations are still running, and across how many shifts?"
- **Problem**: "When a new board revision comes in with 5+ new odd-form parts, how long does it usually take your team to reach steady first-pass yield — and what does that ramp-up cost in credit notes under your PO terms?"
- **Implication**: "If we quantified that ramp-up loss across 4-5 board revisions per year, would the number change {Customer}'s 2026 capex priority for THT automation?"
- **Need-payoff**: "If a single {Machine} could replace 3-4 of those manual stations, re-use 100% of your existing {Feeder-brand} base, and pay back in under 4 months at {local} labor rates — would that be worth a 30-min video audit this month?"

## WhatsApp hook (96 chars, English, with legacy hook)

> Hi {FirstName} — Jason from Southern Machinery (your {legacy-equipment} spare parts supplier, PO {year}). Quick question: in 2026, is {Customer} still running manual insertion for the new {product-type} boards? I just released a free {vertical} ROI PDF. Want me to send it?

This hook is below WhatsApp's 160-char preview limit and works for the first message in a reactivation sequence.

## ROI data template (white-goods / EU controller vertical)

Verified against E.G.O. Spain 2026. Apply to other EU white-goods controller plants; re-anchor the math for non-EU verticals (Mexico / Vietnam / India operator cost drops 50-70%).

| Field | Conservative | Aggressive |
|---|---|---|
| Odd-form stations per line | 4-5 | 3-4 |
| Fully-loaded operator cost (€/yr, EU) | €45,000 | €55,000 |
| Labor savings with 1 dual-head odd-form inserter | €150,000/yr | €370,000/yr |
| Manual first-pass yield (odd-form zone) | 94% | 96% |
| Machine first-pass yield | 98.5% | 99.2% |
| Credit-note exposure (€/mo with strict PO terms) | €25,000 | €50,000 |
| Machine investment (FOB Shenzhen) | €30,000 | €50,000 |
| Payback period (months) | 3 | 4 |
| 5-year net savings (conservative scenario) | €1.0M | €1.5M |

## CTA copy templates (drop in verbatim)

### Email attachment one-liner
> Attached: 1-page ROI breakdown for the {Machine} in {vertical} assembly. If the payback math looks interesting for your THT section, reply with a recent Gerber and your current OEE figures and I'll prepare a custom line-layout in PDF within 3 working days.

## The legacy equipment hook (the highest-conversion angle)

If the buyer's historical PO mentions UIC / Panasonic / Yamaha, name that brand in:
- The "Why Us" card ("100% {brand} Feeder compatible")
- The email subject
- The first WhatsApp message

This is the single highest-conversion trust signal for EU reactivation. "Re-use your existing {brand} base, no rip-and-replace" beats any spec sheet.

## Pitfalls (carried over from v1)

1. DO NOT use `pdflatex` / `wkhtmltopdf` / `weasyprint` for this layout.
2. DO NOT install reportlab into the system Python — always use `/tmp/pdfenv`.
3. DO NOT skip the visual QA loop. Reportlab will not warn you about overflows.
4. DO NOT use Helvetica for CJK characters — register a TTF first.
5. DO NOT claim ROI numbers are "industry standard" without disclosing source scenario.
6. DO NOT lead with the price. Lead with labor cost avoided.
7. DO NOT include a literal machine photo placeholder that says "TODO: insert image here".
