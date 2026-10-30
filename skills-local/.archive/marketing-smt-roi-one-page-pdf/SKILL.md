---
name: smt-roi-one-page-pdf
description: Generate single-page A4 ROI / leave-behind PDF collateral for SMT + THT B2B sales. Use when Jason or the sales team needs a printable, emailable one-pager showing machine specs + payback math + CTA, ready to attach to a cold email, hand out at a trade show, or send via WhatsApp as a PDF file. Triggers include "ROI PDF", "leave-behind", "one-pager", "single page A4 PDF", "客户单页", "单页 ROI 报告", "打印版 ROI", "PDF sales sheet", "ROI brochure for [machine/industry]". Output is a single .pdf (5-15 KB, A4, exactly 1 page) plus a PNG preview. Distinct from the smt-html-product-explainer (which is HTML, animated, multi-section) and the dormant-customer-reactivation-brief (which is a 4-section bilingual KAM brief, not a one-pager).
---

# SMT/THT Single-Page A4 ROI PDF

## When to use this skill

Use this when the user wants a **printable, email-attachable, single-page A4 PDF** that consolidates one machine's specs + ROI math + CTA into a leave-behind for a specific industry vertical. Typical signals:

- "给我 X 机器在 Y 行业的 ROI 单页 PDF" / "single page ROI PDF for X"
- "客户单页" / "leave-behind for the meeting"
- "PDF brochure" / "one-pager"
- "打印版 ROI" / "printer-ready ROI sheet"
- "ready-to-send PDF for E.G.O. / Bosch / Whirlpool"
- "WhatsApp PDF" (need PNG preview alongside for mobile viewing)

This is **not** for:
- A 4-section bilingual KAM brief → use `dormant-customer-reactivation-brief`
- A 7-section animated HTML explainer → use `smt-html-product-explainer`
- A full product datasheet (multi-page PDF) → use `smthelp-knowledge-base` + manual authoring
- A blog article → use `smthelp-admin-blog-publishing`

## The mandatory 7-section structure

The single A4 page must follow this exact top-to-bottom order. Skipping or reordering breaks the sales-engineer narrative flow.

1. **Header bar (dark navy, full-width, ~28mm tall)**
   - Left: orange accent block + "SOUTHERN MACHINERY" wordmark + 1-line tagline + contact row (web / email / phone)
   - Right: machine model + bold (e.g. "S-70LD Dual-Head Odd-Form Inserter") + subtitle ("ROI Analysis · {Industry}") + 1-line italic application scope

2. **The Challenge (left ~62%, white background)**
   - 4-5 bullet points quantifying the buyer's pain with **hard numbers**: % of line labor, €/hr fully loaded, age of legacy equipment, regulatory drivers
   - Always include at least one **regulatory hook** (EU ESPR, IATF 16949, ISO 50001, RoHS) when targeting EU/automotive verticals

3. **Key Specs (right ~34%, light gray card)**
   - 7-8 spec rows with label / right-aligned value: Component height, Cycle time, Placement accuracy, PCB size, Feeder base compatibility, Non-std Feeder lead time, Throughput, Power/Air

4. **Payback Model table (full-width, prominent)**
   - 4 columns: Line Item / Manual Today / With {Machine} / Δ Annual Impact
   - 7-9 rows: stations, labor cost, first-pass yield, credit-note exposure, changeover time, energy, machine investment
   - **Last 2 rows MUST be highlighted** in distinct colors:
     - Row N-1 (orange): "PAYBACK PERIOD — X-Y MONTHS"
     - Row N (green): "5-YEAR NET SAVINGS — €X.XM - Y.YM"
   - These two rows are the visual climax — they prove the math

5. **Why Southern Machinery (3 equal columns)**
   - 3 trust pillars, each with orange left-accent bar:
     - 15-year Shenzhen engineering (1,000+ THT lines shipped, CE certified, 20+ years average engineering tenure)
     - Re-use existing {Feeder-brand} base (no rip-and-replace, e.g. "100% UIC Feeder compatible")
     - Non-std Feeder 3-4 wk lead time (custom tooling + spare-parts stock)

6. **CTA banner (full-width dark navy strip)**
   - Left: orange headline "FREE 30-MIN REMOTE LINE HEALTH CHECK" + 2-3 short body lines ("Send 1 Gerber + THT OEE / We return written diagnostic + EUR ROI in 3 working days / No obligation, no quotation.")
   - Right: email (orange bold) + WhatsApp/Mobile + website booking link, right-aligned

7. **Footer (2 short lines, gray italic)**
   - Line 1: "Figures are conservative engineering estimates for a representative {vertical} plant..."
   - Line 2: "© 2026 Southern Machinery (Shenzhen) Sales & Service Co., Ltd. CE certified." + right-aligned doc ref

## Brand palette (hardcode these tokens, do not improvise)

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

## PDF generation pipeline (the proven recipe)

**Do not** use `pdflatex`, `wkhtmltopdf`, or any non-reportlab path — they all have font / layout / encoding issues for the mixed CJK + boxed layouts in this skill. The exact recipe (sandboxed, venv-based to bypass PEP 668):

```bash
# 1. Create isolated venv (Homebrew Python 3.14+ blocks system pip with PEP 668)
python3 -m venv /tmp/pdfenv

# 2. Install reportlab (the only dep needed)
/tmp/pdfenv/bin/pip install reportlab --quiet

# 3. Generate the PDF from the template (see templates/roi-one-pager-template.py)
/tmp/pdfenv/bin/python3 build_pdf.py

# 4. Render preview PNG for visual QA
/tmp/pdfenv/bin/pip install pypdfium2 --quiet
/tmp/pdfenv/bin/python3 -c "import pypdfium2 as pdfium; pdfium.PdfDocument('out.pdf')[0].render(scale=2.0).to_pil().save('preview.png')"
```

The whole pipeline runs in < 10 seconds end-to-end.

## Mandatory visual QA loop (3 iterations expected)

After generating, **always** render the PDF to PNG and run `vision_analyze` to catch layout problems. Common issues that survive a first pass:

1. **Footer text overlap** — disclaimer + doc ref on the same y line. **Fix:** place disclaimer at y=9mm, copyright at y=6mm, doc ref right-aligned at y=6mm.
2. **CTA banner too short** — 3 body lines + 3 right-column lines need ~18mm height, not 16mm. **Fix:** `cta_h = 18*mm`.
3. **"Why Us" card body too long for card height** — 3-4 wrapped lines need ≥ 36mm card height. **Fix:** `col_h = 36*mm` minimum.
4. **ROI table column widths sum > 168mm** — the 4-column table needs to fit in 168mm (PAGE_W − 2·MARGIN). Use 56/36/44/32 mm as a starting point.
5. **Right-aligned text vs left-aligned text collision** in CTA banner — measure: if left body line at 8.2pt is > 90mm wide, shorten it or move right column further right.

**Always re-render and re-check after every fix.** A "looks fine to me" self-assessment is not sufficient.

## ROI data template (white-goods / EU controller vertical — proven numbers)

These figures were verified against E.G.O. Spain 2026 and apply broadly to other EU white-goods controller plants. Use them as defaults; replace only when the buyer gives different inputs.

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

For non-EU verticals (Mexico, Vietnam, India), operator cost drops 50-70% — **always re-anchor the math to the buyer's actual local labor cost** or the ROI pitch falls flat. See the existing `ROI Calculator` memory note for the operator-cost sensitivity bug.

## Output location & file naming

Save to `/Users/jasonwu/Downloads/{Machine}_ROI_{Vertical}.pdf`. Always also drop a `{Machine}_ROI_{Vertical}_preview.png` alongside — Jason pastes the PNG into WhatsApp when the buyer is on mobile.

Examples:
- `S-70LD_ROI_WhiteGoods_Controller.pdf`
- `S3000_ROI_Automotive_Tier1.pdf`
- `S-WS450_ROI_PowerSupply_Wave.pdf`

## CTA copy templates (drop in verbatim)

### Email attachment one-liner
> Attached: 1-page ROI breakdown for the {Machine} in {vertical} assembly. If the payback math looks interesting for your THT section, reply with a recent Gerber and your current OEE figures and I'll prepare a custom line-layout in PDF within 3 working days.

### WhatsApp Hook (96 chars, English, with legacy hook)
> Hi {FirstName} — Jason from Southern Machinery (your {legacy-equipment} spare parts supplier, PO {year}). Quick question: in 2026, is {Customer} still running manual insertion for the new {product-type} boards? I just released a free {vertical} ROI PDF. Want me to send it?

## SPIN follow-up questions (plant at the end of the email/WhatsApp follow-up, not in the PDF)

After the PDF is sent, the next conversation turn should plant 1-2 of these:

- **Situation**: "On the {product} line in {City} today, how many manual odd-form stations are still running, and across how many shifts?"
- **Problem**: "When a new board revision comes in with 5+ new odd-form parts, how long does it usually take your team to reach steady first-pass yield — and what does that ramp-up cost in credit notes under your PO terms?"
- **Implication**: "If we quantified that ramp-up loss across 4-5 board revisions per year, would the number change {Customer}'s 2026 capex priority for THT automation?"
- **Need-payoff**: "If a single {Machine} could replace 3-4 of those manual stations, re-use 100% of your existing {Feeder-brand} base, and pay back in under 4 months at {local} labor rates — would that be worth a 30-min video audit this month?"

## Pitfalls

1. **DO NOT** use `pdflatex` / `wkhtmltopdf` / `weasyprint` for this layout. `reportlab` is the only library that gives you precise canvas-level control over the 7-section boxed layout with proper CJK fallback.

2. **DO NOT** install reportlab into the system Python — Homebrew Python 3.12+ enforces PEP 668 and the install will fail with "pass the --user flag" / "override by passing --break-system-packages". Always use the `/tmp/pdfenv` venv recipe above. This is the single most common failure mode.

3. **DO NOT** skip the visual QA loop. Reportlab will not warn you that the CTA banner is overflowing the page bottom or that two text blocks collide. Render to PNG, `vision_analyze` it, fix, re-render. Budget 3 iterations.

4. **DO NOT** use Helvetica for CJK characters — Helvetica is a Latin-only font. If you need to mix English machine names with Chinese industry terms, register a TTF (e.g. `STHeiti` or `Noto Sans CJK`) via `pdfmetrics.registerFont`. For pure-English one-pagers, Helvetica + Helvetica-Bold is correct.

5. **DO NOT** claim the ROI numbers are "industry standard" or "conservative across the board" without disclosing the source scenario. The footer MUST say "Figures are conservative engineering estimates for a representative EU {vertical} plant" — auditors and procurement check the disclaimers.

6. **DO NOT** lead with the price. Lead with the **labor cost avoided** (€400,000-500,000/yr for 4-5 manual stations) and let the machine investment (€30,000-50,000) sit quietly in the table. Price-led pitches lose to Japanese competitors; ROI-led pitches win on week 1.

7. **DO NOT** include a literal machine photo placeholder that says "TODO: insert image here". The one-pager is meant to be sent as-is. If a photo is essential, generate one with the `smt-machine-marketing-image-prompts` skill FIRST and embed it with `c.drawImage(...)` — but for a 1-page A4 with 7 sections, no image usually fits cleanly. Skip the image, lean on the spec card.

8. **DO** mirror the **legacy equipment hook** from `dormant-customer-reactivation-brief/references/legacy-equipment-hook-pattern.md` — if the buyer's historical PO mentions UIC / Panasonic / Yamaha, name that brand in the "Why Us" card and the email subject. The "100% {brand} Feeder compatible" angle is the single highest-conversion trust signal for EU reactivation.

## Related Skills

- `dormant-customer-reactivation-brief` — for the **4-section bilingual KAM brief** that PRECEDES the one-pager in a reactivation sequence (the PDF is typically Deliverable C from the brief's CTA)
- `smt-html-product-explainer` — for the **animated HTML version** of the same ROI pitch (use HTML for web sharing, PDF for email/print/WhatsApp)
- `smthelp-knowledge-base` — load FIRST for exact model numbers, CPH numbers, and certified specs before authoring the specs card
- `improved-pitch-ems-global-smt-line` — for the verbal/email pitch structure that the PDF is a visual artifact of
- `jason-wu-sales-engineer` — for the B2B sales methodology and ROI-framing principles the one-pager is built on
- `smt-machine-marketing-image-prompts` — for generating product images IF a real machine photo is needed in the header

## Support files

- `references/pdf-generation-pipeline.md` — the exact reportlab + venv + pypdfium2 + vision_analyze recipe, with copy-paste commands and known failure modes
- `templates/roi-one-pager-template.py` — a known-good A4 7-section template, all sections wired, all layout pitfalls pre-fixed. Copy → fill {PLACEHOLDER} slots → ship.
- `references/white-goods-roi-data.md` — the verified ROI figures (labor cost, payback, 5-year savings) for the white-goods controller vertical, with sources
