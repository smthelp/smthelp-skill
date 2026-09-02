---
name: b2b-roi-one-pager
description: "Generate a single-page A4 ROI one-pager PDF for B2B sales — designed to be directly attached to a cold email, WhatsApp, or LinkedIn DM. Light/professional color scheme (NOT the PCB dark theme), inline SVG schematic of the machine (not factory photos with annotation clutter), industry-vertical-specific ROI model. Use when the user asks for a \"one-page PDF\" / \"PDF one-pager\" / \"ROI PDF\" / \"sales flyer\" / \"sales brochure\" / \"销售单页\" / \"PDF 报价单页\" / \"单页白皮书\" for a specific Southern Machinery machine + a specific industry vertical (white-goods, automotive, power supply, LED, IoT, etc.) + a specific region/labor market. Rendered via Playwright + Chromium headless shell to a single-page A4 PDF (~200 KB). Often used as a supporting deliverable inside the dormant-account-reactivation-ems 4-phase flow."
whenToUse: "make me a one-page PDF for [machine] in [industry]，ROI one-pager for [machine] targeting [region]，PDF sales flyer / PDF brochure / PDF datasheet one-page，单页 PDF / 销售单页 / PDF 报价单，PDF I can send directly to [customer]，PDF for the [reactivation] email，给客户发的 PDF / 客户能直接看的 PDF"
metadata:
  source: hermes
  origin: "sales-engineering/b2b-roi-one-pager"
---
## 技能指令（Skill Instructions）

When generating B2B ROI one-pager PDFs for Southern Machinery:
- USE LIGHT/PROFESSIONAL color scheme: Navy #0E2A47 + Orange #FF6B1A + Light Gray #F2F4F7 + Pastel Green #D4F1E0 for "savings" highlights. NOT the dark PCB theme (that's for HTML explainers).
- USE INLINE SVG for the machine schematic, NOT factory photos. Annotated factory photos look amateur. The stylized 3D-ish vector (vibratory bowl + tape feeder rail + Z-axis insertion head + PCB conveyor) is the proven pattern.
- USE THIS 6-SECTION LAYOUT in order: (1) Header band with brand + contact, (2) Hero with product title + value prop + industry pill tags + SVG schematic, (3) Challenge panel + Specs table side-by-side, (4) ROI comparison table (Today/With S-XXX/Annual Impact) + 3 KPI cards (Payback / 5-Year Savings / CapEx delta), (5) Why Us 3-card row + Line flow diagram, (6) CTA strip (Free 30-min Line Health Check, "send 1 Gerber") + Footer with assumptions + doc ref
- KEEP INDUSTRY TERMS IN UPPERCASE ENGLISH: SMT, THT, PCB, PCBA, CPH, Feeder, Nozzle, Reflow Oven, Wave Soldering, Pick and Place, SPI, AOI, MES
- ALWAYS use LOCAL labor cost in the ROI model. Never the default $3,600/yr. Spain €28-32/h, Poland €12-15/h, Vietnam $3-4/h, Mexico $5-7/h, Brazil R$25-35/h. Convert to fully-loaded annual cost (wages + benefits + management overhead, x 2080 hours x shifts).
- ALWAYS use a low-friction CTA: "Send us 1 Gerber + your current odd-form station headcount. We will return a written diagnostic + payback calculation in your local currency within 3 working days." This is the proven opener that converts dormant accounts.
- Save to /Users/jasonwu/Downloads/{Machine}_{Vertical}_{Region}_OnePager_v{N}.pdf. Example: S-70LD_WhiteGoods_Spain_OnePager_v2.pdf


# B2B ROI One-Pager PDF (Single-Page A4)

This skill produces a **print-ready, single-page A4 PDF** that Jason attaches to a cold email / WhatsApp / LinkedIn DM when reactivating a dormant account or pitching a new prospect. It is **not** an HTML explainer (different color scheme, different layout, different rendering path) and **not** a multi-page deck (it's literally one A4 page, intentionally dense).

The deliverable is designed to be opened, scanned in 30 seconds, and trigger an action (reply, download catalog, book a call). Every design decision serves that.

## When to Use This Skill

Use this skill when the user wants:

- A **single-page A4 PDF** (not HTML, not multi-page deck, not Word)
- A **sales one-pager** for a **specific Southern Machinery machine** (S-70LD, S3000, S-4000, S7020, S-WS450, SUL460, etc.)
- Targeted at a **specific industry vertical** (white-goods, automotive, power supply, LED, IoT, telecom, medical)
- Tuned to a **specific regional labor market** (Spain, Poland, Mexico, Vietnam, Brazil, India, etc.)
- "The kind I can send directly to the customer" — must be visually polished enough to forward to a procurement GM without embarrassment

Typical parent flow: this PDF is the **attachment to the email** in `dormant-account-reactivation-ems` Phase 4, or the **lead magnet** in `smt-html-product-explainer` for a LinkedIn DM. It can also stand alone as the only deliverable if the user just wants "a one-pager for the S-70LD in the Spanish white-goods market."

## When NOT to Use

- **Interactive HTML explainer** → use `smt-html-product-explainer`. Different format, different color scheme, different use case (web URL vs PDF attachment).
- **Multi-page proposal / white paper** → this skill is single-page. For 3-5 page proposals, generate a different artifact.
- **Internal spec sheet** (for engineering review) → the user wants specs, not ROI. Use `smthelp-knowledge-base` directly.
- **Trade-show booth handout** → still applies, but consider larger paper size (A3) and lower density. The skill's templates are A4.

## The 6-Section Single-Page Layout (MANDATORY order)

Every one-pager follows this exact structure. Reordering breaks the B2B sales-engineer narrative.

### Section 1: Header Band (Navy #0E2A47)
- Left: SM logo (orange "SM" square + "SOUTHERN MACHINERY" wordmark + tagline "Shenzhen · SMT · THT · Wave Soldering · Since 2011")
- Right: Contact block — Jason Wu, Senior Sales Engineer, email + WhatsApp + website
- **No menu, no nav, no fluff.** It's a sales sheet, not a website header.

### Section 2: Hero (Navy gradient with subtle orange wash)
- **Eyebrow line** (orange, all-caps, tracked): "2026 ROI Brief · [Industry Vertical]"
- **H1 title** (white, 18-22pt bold): Product full name + key adjective. e.g. "S-70LD Dual-Head Odd-Form Inserter"
- **Subhead** (light gray, 1-2 sentences): Specific value prop with hard numbers — "Replace 6-8 manual odd-form insertion operators on your [product type] line. Engineered in Shenzhen since 2011, 50% CapEx saving vs Japanese equivalents, 4-8 week delivery, 24-48h global service response."
- **Pill row** (4 pills, one orange): Industry × region × shift × certification. e.g. "For Spain · EU White-Goods EMS" / "2 Shifts · ~100k PCBA / month" / "IPC-A-610 Class 2 / 3" / "MES Ready"
- **Right side: Inline SVG schematic of the machine.** NOT a photo. The schematic shows: vibratory bowl + tape feeder rail + Z-axis insertion head + PCB conveyor with component dots. ~40-50mm tall.

### Section 3: Challenge + Specs (Side-by-side, light gray panels)

**Left panel — "The Challenge in Your [Line Type]"**
5 bullets, each with an orange dot. Bullets are quantified and specific to the vertical:
- "Manual odd-form bottleneck. [Component types] still inserted by hand on most 2015-2020 era THT lines."
- "EU labor cost squeeze. [Region] fully-loaded operator cost ≈ [local rate], pushing manual [station type] to [€/yr]/year each."
- "[Regulation] forces higher-mix, lower-volume production, where hand insertion ramp-up eats margin."
- "Yield & traceability gaps from manual stations — a single missed insertion triggers credit-note / rework penalties under strict PO terms."
- "[Old equipment brand] Feeder base is still solid (good!) — you don't need a rip-and-replace, you need a smart add-on."

**Right panel — "Key Specs at a Glance"**
10-row table, 2 columns. Specs are pulled directly from `smthelp-knowledge-base`. Format: `<key> <value with unit>`. Typical for S-70LD:
- Component range 3-25 mm
- Feeding cycle 0.8 s
- Placement accuracy ±0.5 mm
- Throughput ~4,500 pcs/hour
- PCB size 450×400 mm
- Feeder compatibility UIC / Universal + STF1003 tube
- Spring life 4 million cycles
- Power / Air 220V / 0.4-0.6 MPa
- Lead time 4-8 weeks
- Service response 24-48 hours

### Section 4: ROI Table + 3 KPI Cards (The Money Slide)

**Left — ROI comparison table** (4 columns, 5-6 rows)
- Column headers: Cost Driver | Today (Manual) | With S-XXX | Annual Impact
- 5-6 rows of quantified cost drivers
- Last row highlighted in pastel green: "5-Year Net Savings"
- Example rows for white-goods Spain (validated 2026-06-05):
  - Odd-form operators per shift: 4-5 → 1+1 feeder → **6-8 staff removed**
  - Fully-loaded operator cost / yr: €50,000 → €55,000 → -€55k
  - Annual direct labor (2 shifts): €800k-1.0M → €110k-165k → **-€690k**
  - First-pass yield: 96.5% → 99.2% → +2.7 pp
  - Credit-note / rework cost: €180k/yr → €55k/yr → -€125k
  - **5-Year Net Savings: — | — | €3.8M-4.5M** (green highlight)

**Right — 3 stacked KPI cards**
1. **Payback Period** (orange fill): big number + small note. e.g. "3-4 months" / "On a single S-70LD dual-head cell vs manual station labor in [region]"
2. **5-Year Net Savings** (pastel green fill): big number + small note. e.g. "€3.8-4.5 M" / "After S-70LD CapEx, training, integration & service"
3. **CapEx vs Japanese Equivalent** (white with orange left-border): "-50%" / "vs Yamaha YS24 / Fuji NXT odd-form head benchmark"

### Section 5: Why Us (3 cards) + Line Flow (process diagram)

**Left — 3 Why-Us cards** in a row. Each has: icon (inline SVG, 14x14), bold heading, 1-2 sentence body. The 3 winning differentiators for a Shenzhen-based OEM competitor are:
1. "15 Years of Shenzhen Engineering" — since 2011, 40+ countries
2. "100% [Old Brand] Feeder Reuse" — plug into existing base, no rip-and-replace
3. "3-4 Weeks Custom Delivery" — non-standard feeders/trays/bowls

**Right — "Where S-70LD Fits in Your THT Line"**
Horizontal process flow with 7 chips: Loader → SMT P&P + Reflow Oven → **S-70LD (orange highlight)** → S-3000 Radial → S-4000 Axial → Wave Soldering → AOI + Unloader. Below the flow, a 1-sentence summary: "All Southern Machinery — one throat to choke, one SLA to enforce."

### Section 6: CTA Strip + Footer

**CTA strip** (Navy gradient, full width):
- Left: "Next Step · Zero Cost · No Obligation" eyebrow + "Book a Free 30-Minute Remote Line Health Check" H3 + body "Send us 1 Gerber file + your current [station] headcount. We will deliver a written diagnostic & payback calculation in your local currency within 3 working days."
- Right: Orange button linking to mailto with pre-filled subject. Sub-line: "jasonwu@smthelp.com · Reply within 24h"

**Footer** (very dark navy):
- Left: copyright + URL + ROI assumptions disclaimer (e.g. "ROI assumptions: 2 shifts, fully-loaded operator cost €28-32/h, output ~100k PCBA / month. Your actual payback will be confirmed in the line health check.")
- Right: Orange "DOC-ROI-{MACHINE}-{VERTICAL}-{YEAR}-EN-{NN}" doc ref

## Design System Tokens (Light/Professional)

```css
--navy:    #0E2A47;    /* primary brand */
--navy2:   #1A3A5C;    /* gradient end, navy lighter */
--orange:  #FF6B1A;    /* primary accent, brand */
--orange2: #E55A0E;    /* darker for hover */
--gray-bg: #F2F4F7;    /* panel surface */
--gray-bd: #D8DCE3;    /* panel borders */
--green:   #D4F1E0;    /* savings highlight fill */
--green2:  #1B8A4A;    /* savings highlight text */
--text:    #1A1A1A;    /* body */
--muted:   #5A6573;    /* sub-text, labels */
```

Fonts: Inter / Helvetica Neue / Helvetica / Arial sans-serif fallback. KPI numbers use `font-variant-numeric: tabular-nums` so they align in columns.

## The Inline SVG Machine Schematic (CRITICAL — use this, not photos)

The hero SVG is the single most-imitated design element. It's a stylized 3D-ish schematic with 4 elements: vibratory bowl, tape feeder rail, Z-axis insertion head, PCB conveyor. The viewBox is 320x220. Color palette stays in the navy/orange/green family — no factory grays, no real photos.

```html
<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" class="machine-svg">
  <ellipse cx="160" cy="200" rx="130" ry="6" fill="rgba(0,0,0,0.25)"/>
  <rect x="40" y="60" width="240" height="130" rx="6" fill="#F4F1EC" stroke="#A8B0BB" stroke-width="1.2"/>
  <rect x="48" y="50" width="100" height="22" rx="2" fill="#1A3A5C" stroke="#0E2A47"/>
  <circle cx="58" cy="61" r="3" fill="#FF6B1A"/>
  <rect x="68" y="58" width="60" height="6" rx="1" fill="#4A6585"/>
  <circle cx="115" cy="125" r="34" fill="#1B4D2E" stroke="#0E2A47" stroke-width="1"/>
  <circle cx="115" cy="125" r="28" fill="none" stroke="#2D7A4A" stroke-width="0.5" stroke-dasharray="2 2"/>
  <circle cx="115" cy="125" r="6" fill="#FF6B1A"/>
  <rect x="160" y="100" width="105" height="50" rx="2" fill="#E8EBF0" stroke="#A8B0BB"/>
  <rect x="165" y="106" width="95" height="6" fill="#0E2A47"/>
  <rect x="165" y="116" width="95" height="6" fill="#0E2A47" opacity="0.7"/>
  <rect x="165" y="126" width="95" height="6" fill="#0E2A47" opacity="0.5"/>
  <rect x="165" y="136" width="95" height="6" fill="#0E2A47" opacity="0.3"/>
  <rect x="195" y="65" width="14" height="30" fill="#FF6B1A" stroke="#0E2A47" stroke-width="0.8"/>
  <rect x="192" y="92" width="20" height="10" fill="#1A1A1A"/>
  <line x1="202" y1="102" x2="202" y2="115" stroke="#1A1A1A" stroke-width="2"/>
  <rect x="60" y="175" width="200" height="14" fill="#1F8A3E" stroke="#0E2A47" stroke-width="0.5"/>
  <circle cx="100" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="140" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="180" cy="182" r="1.5" fill="#FF6B1A"/>
  <circle cx="220" cy="182" r="1.5" fill="#FF6B1A"/>
  <text x="160" y="206" text-anchor="middle" font-size="7" fill="#FF6B1A" font-weight="700">PCB INSPECTION · INSERTION ZONE</text>
  <line x1="202" y1="60" x2="202" y2="40" stroke="#FF6B1A" stroke-width="0.8" stroke-dasharray="2 2"/>
  <text x="202" y="36" text-anchor="middle" font-size="6.5" fill="#FF6B1A" font-weight="700">±0.5mm HEAD</text>
</svg>
```

**Why SVG, not photos?** Factory photos from the smthelp.com product pages have **green annotation ovals, arrows, and Chinese teaching text baked into the JPEG** (see S-70LD images on smthelp.com/desc/2019/05/). These look unprofessional in a B2B sales PDF — they scream "I grabbed this from a Chinese PowerPoint deck." The inline SVG schematic looks like a proper industrial design render and works at any zoom level. The trade-off is you don't show the actual machine — but the customer knows what an inserter looks like, what they need to see is the value prop and the ROI math.

## Rendering Pipeline (Playwright + Chromium Headless Shell)

**Why this path?** weasyprint is not installed. wkhtmltopdf is not installed. Chrome's headless --print-to-pdf command works but adds a 10s virtual-time-budget per render and doesn't let you control layout dimensions cleanly. Playwright's chromium PDF API gives precise control over A4 sizing, page margins, print backgrounds, and CSS page-size — and reuses the same chromium binary that powers the explainer skill's deployment.

**Setup (first time only):**
```bash
pip3 install playwright && python3 -m playwright install chromium
```
The `playwright` Python package is NOT pre-installed — this step is required on every new environment.

**The exact headless shell path (Mac, 2026-06-05 verified):**

```python
HEADLESS = "/Users/jasonwu/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell"
```

If the version number drifts (e.g. 1240, 1300), check `/Users/jasonwu/Library/Caches/ms-playwright/` for the latest `chromium_headless_shell-XXXX` directory. Don't hardcode the version — glob for it. See `scripts/render-a4-pdf.py` for the auto-discovery pattern.

**The render command:**

```python
from playwright.sync_api import sync_playwright
import os

HEADLESS_GLOB = "/Users/jasonwu/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"
import glob
HEADLESS = sorted(glob.glob(HEADLESS_GLOB))[-1]  # latest version

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=HEADLESS)
    page = browser.new_page(viewport={"width": 794, "height": 1123})  # A4 @ 96dpi
    page.goto(f"file://{html_path}", wait_until="networkidle")
    page.pdf(
        path=pdf_path,
        format="A4",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        prefer_css_page_size=True,
    )
    browser.close()
```

**Key flags:**
- `print_background=True` — preserves the navy/orange gradients and pastel green highlights. Without it, Chrome strips them.
- `margin={"top": "0", ...}` — the page controls its own padding via CSS. The page must include `@page { size: A4; margin: 0; }` and `body { ... }` with explicit `width: 210mm; height: 297mm;`.
- `prefer_css_page_size=True` — respects `@page { size: A4; }` in the CSS rather than forcing Chrome's default.

**A4 in pixels @ 96dpi:** 794 × 1123. Use this for the viewport so the screenshot for visual verification is 1:1 with the PDF.

## The One-Page Fit Problem (Common Pitfall)

A4 height = 1123px @ 96dpi. If your HTML is taller, Playwright **silently spills to page 2**, breaking the "single page" promise. Symptoms:
- The PDF is 2 pages but the visual preview in `screenshot` looks fine (screenshot only captures viewport).
- Customer complains "the bottom is cut off."

**Three defense layers:**

1. **Set `overflow: hidden` on the `.page` container.** Caps the layout. If content overflows, it gets clipped rather than spilling. This is the primary safety net — without it, Playwright silently generates 2-3 pages even if the screenshot looks fine (screenshot only captures the first viewport).
2. **Tighten paddings iteratively.** Start generous (5-6mm panel padding, 9-10mm section padding), then trim to 3-4mm panel, 5-6mm section. Drop font sizes 0.5-1pt at a time.
3. **HTML height check before rendering:**
   ```python
   h = page.evaluate("() => document.documentElement.scrollHeight")
   print(f"HTML height: {h}px, A4 @96dpi: 1123px")
   if h > 1123:
       print("WARN: will overflow to 2+ pages")
   ```
   A value of ~2786px produces ~2.5 pages (verified 2026-06-10 with Fitech report).

**Single-page verification after render:**
```python
import re
with open(pdf_path, "rb") as f:
    data = f.read()
pages = re.findall(rb'/Type\s*/Page[^s]', data)
print(f"Page count: {len(pages)}")  # must be 1
```

The validated v2 build for S-70LD white-goods Spain comes in at **exactly 1123px** with `overflow: hidden` as a safety net.

## Labor Cost Database (Local Rates, 2026-06-05)

Use these fully-loaded rates (wages + benefits + management overhead, x 2080 hours) when building the ROI model. Always state the source as an assumption in the footer.

| Region | Loaded Rate | Notes |
|--------|------------|-------|
| Spain (Catalonia) | €28-32 / hour | 2025-2026 manufacturing |
| Germany | €32-38 / hour | Southern Bavaria higher |
| Poland | €12-15 / hour | Skilled THT operator |
| Czechia | €11-14 / hour | |
| Vietnam (HCMC) | $3-4 / hour | Skilled in ZES/Hi-Tech zones |
| Mexico (Monterrey) | $5-7 / hour | IMMEX zone, near-shoring premium |
| Brazil (Manaus ZFM) | R$25-35 / hour | ZFM tax-incentivized |
| India (Tamil Nadu) | $2-3 / hour | Skilled in Chennai belt |
| USA (Texas) | $22-28 / hour | |

Convert to annual: rate × 2080 hours. Multiply by 2 for 2 shifts. Apply to the # of operators removed by the automation.

## ROI Content Patterns by Industry Vertical

| Vertical | Primary Pain | Typical Annual Saving | Headline KPI |
|----------|--------------|----------------------|--------------|
| White-goods controllers (washing machine main boards) | Manual odd-form bottleneck on inverter boards | €3-5M / 5yr per line | 3-4 month payback |
| Automotive electronics (BMS, ECU) | IGBT/connector insertion, traceable insertion force | €2-4M / 5yr | 4-6 month payback |
| Power supplies / EV chargers | Radial cap + transformer, high volume | €1-3M / 5yr | 4-8 month payback |
| LED drivers / lighting | High-mix, short runs, frequent changeover | €1-2M / 5yr | 5-8 month payback |
| IoT / connectivity modules | Small batch, high-mix, manual stations dominate | €0.5-1.5M / 5yr | 6-10 month payback |
| Telecom infrastructure (base station PSUs) | High-reliability THT, military-grade QC | €2-4M / 5yr | 4-6 month payback |
| Medical devices (PCBA) | IPC Class 3, full traceability | €1-3M / 5yr | 5-8 month payback |

## Output Location & Naming

Save to `/Users/jasonwu/Downloads/{Machine}_{Vertical}_{Region}_OnePager_v{N}.pdf`

Examples (validated 2026-06-05):
- `S-70LD_WhiteGoods_Spain_OnePager_v2.pdf`
- `S3000_PowerSupply_Mexico_OnePager_v1.pdf`
- `S7020_Automotive_Germany_OnePager_v1.pdf`

Keep version numbers ascending. The original v1 from previous sessions is in `/Users/jasonwu/Downloads/` and should be left in place — it's the version the user already shared with prospects.

## Pitfalls & Anti-Patterns

**NEVER do these:**

- **Use factory photos with annotation overlays** from smthelp.com — they have green ovals + Chinese teaching text baked in. The customer will think you sent them a Chinese PowerPoint screenshot. Use inline SVG.
- **Use the PCB dark theme** (`#050a13` etc.) from `smt-html-product-explainer` — that theme is for interactive web pages. A B2B sales one-pager needs the **light/professional** navy + orange + light gray + pastel green palette.
- **Default to a $3,600/yr operator cost** — this is the ROI calculator's default, but for a Spain white-goods reactivation that's off by 8-10x. Always use the local rate from the table above.
- **Quote a payback period without stating the labor-cost assumption** — auditors and procurement GMs will discount the entire document if they can't audit the math.
- **Skip the CTA's "send 1 Gerber" angle** — the highest-converting CTA is "send us 1 Gerber + your current station headcount, we return a written diagnostic in 3 working days." Generic "contact us" CTAs get 5-10x lower response rates.
- **Render to 2+ pages** — the whole point is single-page. Iterate on padding/font size until it fits.
- **Add decorative animations, scroll-reveals, or JS** — the PDF renderer doesn't run JS. Keep it static.
- **Use external image URLs** (logo, product photos) — the PDF may be forwarded through email systems that block remote image loads. Use inline SVG and data URIs.

**ALWAYS do these:**

- **Use inline SVG for the machine schematic** — works in any PDF reader, scales perfectly, looks professional.
- **Use the proven 6-section layout** — reordering breaks the sales narrative.
- **State the labor-cost assumption in the footer** — "ROI assumptions: 2 shifts, fully-loaded operator cost [local rate], output [local volume]. Your actual payback will be confirmed in the line health check."
- **Include a doc ref** in the footer — "DOC-ROI-{MACHINE}-{VERTICAL}-{YEAR}-EN-{NN}" lets you track which version went to which customer.
- **Verify the PDF with vision_analyze on the first page** before declaring it done. Catch truncated KPI numbers, clipped tables, missing pills.
- **Update MEMORY.md with the engagement** — what machine + what vertical + what region + what payback number, so future sessions can reference it.

## Verification Before Delivery

- [ ] PDF is **exactly 1 page** (verify with `python3 -c "import re; print(len(re.findall(rb'/Type\s*/Page[^s]', open('file.pdf','rb').read())))"` — must return 1)
- [ ] File size ~150-300 KB (the inline SVG and minimal CSS keep it lean)
- [ ] No text overflow or truncation in any section
- [ ] All 4 pill tags in the hero render fully
- [ ] The 3 KPI cards show their big numbers in full (no "3-4 mo..." truncation)
- [ ] The 5-Year Net Savings row in the ROI table is highlighted in pastel green
- [ ] The CTA strip button is an orange call-to-action
- [ ] The footer includes labor-cost assumption + doc ref
- [ ] Visual verify with `vision_analyze` on a screenshot of page 1

## Related Skills

- `dormant-account-reactivation-ems` — the parent flow that this one-pager is often attached to as the email attachment in Phase 4
- `smt-html-product-explainer` — for **interactive HTML explainers** (dark theme, animated, web URL). Different format, different use case, different color scheme.
- `smthelp-knowledge-base` — for exact machine specs (CPH, accuracy, component ranges). Load this FIRST.
- `smt_roi_calculator` — for the full ROI math validation. The one-pager uses the same formula but compresses it to a 5-row table.
- `cold-email-templates-ems-global` — for the email body that wraps the one-pager PDF attachment.

## Support Files

- `templates/roi-one-pager-base.html` — the base 6-section HTML with the inline SVG schematic and all CSS variables pre-defined. Copy → fill `{{MACHINE}}`, `{{VERTICAL}}`, `{{REGION}}`, `{{ROI_NUMBERS}}` slots → render. ~24 KB, self-contained.
- `scripts/render-a4-pdf.py` — the Playwright + Chromium headless shell renderer with auto-discovery of the latest chrome-headless-shell version. Run with `python3 scripts/render-a4-pdf.py path/to/one-pager.html` to produce `<name>.pdf` next to it. Includes the A4 height sanity check and the single-page-count verification.
- `references/roi-content-patterns.md` — full content templates for 6 industry verticals (white-goods, automotive, power supply, LED, IoT, medical) with labor cost, ROI numbers, challenge bullets, and spec callouts. Copy the relevant section into the base template.
- `references/svg-machine-library.md` — the inline SVG schematic patterns for S-70LD (odd-form), S-3000 (radial), S-4000 (axial), S-7020 (terminal), S-WS450 (wave soldering), SUL460 (unloader). Drop in the matching SVG when you switch machines.
