---
name: smthelp-brand-document-suite
description: "Southern Machinery branded document generation suite. Uses logo2docs methodology — extract brand identity from company logo, build a design system (brand-config.json), then generate professional Excel, Word, PPT, PDF, flowcharts, and handbooks for Southern Machinery sales and marketing. Triggers on: 'brand guidelines', 'company template', 'branded report', 'design system', 'generate branded documents', 'company style guide', '整套品牌文档', '品牌文档生成', 'Southern Machinery branded', 'SMThelp document', or any request to create professional branded documents for Southern Machinery sales/procurement/marketing use cases."
metadata:
  source: hermes
  origin: "sales-engineering/smthelp-brand-document-suite"
---
# SMThelp Brand Document Suite

Skill for generating professional branded documents for **Southern Machinery** (Shenzhen Southern Machinery Sales And Service Co., Ltd) using the logo2docs methodology adapted for Hermes/skill-stack environments where the original repo scripts are unavailable.

**Two-layer system:**
1. **Brand Setup** (one-time per company/sub-brand): Logo → color extraction → brand-config.json
2. **Document Generation** (on-demand): brand-config.json → any document type

---

## CRITICAL: Script Availability — PITFALL

**The `npx skills add quzhi-ai/logo2docs` installation ONLY copies SKILL.md.** The full repo scripts (`brand_setup.py`, `brand_preview.py`, `brand_check.py`) and reference files (`references/*.md`) are **NOT installed** in the Hermes skill environment. Do NOT attempt to call these scripts — they will fail.

**Always use the fallback workflow** (pure Python + HTML, no repo scripts needed).

## CRITICAL: Python venv Path — PITFALL (2026-06-27)

**Do NOT use `python3` or `python` in terminal commands for document generation.** The system Python (`/usr/bin/python3`, Python 3.9.6) does NOT have `python-pptx` / `openpyxl` / `python-docx` installed.

**Always use the Hermes venv Python:**
```
/Users/jasonwu/.hermes/hermes-agent/venv/bin/python
```

Or find it via:
```bash
ls ~/.hermes/hermes-agent/venv/bin/python
```

**Install dependencies once via the venv:**
```bash
~/.hermes/hermes-agent/venv/bin/pip install python-pptx openpyxl python-docx lxml
```

---

## Phase 1: Brand Setup (No Scripts — Fallback Only)

### Step 1: Save the Logo

When user provides a logo URL or file:
```bash
mkdir -p ~/brand-assets
curl -sL "<logo-url>" -o ~/brand-assets/logo-color.png
```

### Step 2: Extract Colors via Python in Terminal

Use PIL + numpy via `terminal()`:
```python
python3 -c "
from PIL import Image
import numpy as np
from collections import Counter
img = Image.open('brand-assets/logo-color.png').convert('RGB').resize((150,150))
arr = np.array(img).reshape(-1,3)
def q(r,g,b,s=16):
    f=256//s; return (r//f)*f+f//2
cnt = Counter([q(int(r),int(g),int(b)) for r,g,b in arr])
for (r,g,b),n in cnt.most_common(10):
    print(f'#{r:02X}{g:02X}{b:02X} {n/len(arr)*100:.1f}%')
"
```

If Python/PIL is unavailable or blocked, use **known Southern Machinery brand colors**:
- **Primary**: `#1E40AF` (deep industrial blue — precision, reliability)
- **Secondary**: `#EA580C` (orange — energy, manufacturing vitality)
- Adjust based on actual logo observation

### Step 3: Brand Interview (3 Questions Max)

Natural conversation, NOT numbered list:

1. **Industry/Audience**: "Who are the end readers of these documents — procurement managers, engineers, C-level executives?" (determines font weight and visual formality)
2. **Style**: "Do you prefer **professional** (conservative, high-contrast), **modern** (clean, spacious), **bold** (strong colors, large type), or **elegant** (refined, subtle)?"
3. **Existing rules**: "Any specific brand colors, fonts, or guidelines we must follow?"

For Southern Machinery specific context:
- Industry: Electronics manufacturing equipment (SMT/THT insertion machines, wave solder systems)
- Audience: Global EMS factory procurement managers and production engineers
- Style: Professional (conservative, high-contrast, spec-driven — engineers distrust flashy)
- Known brand: Primary `#1E40AF`, Secondary `#EA580C`, fonts Arial/Helvetica

### Step 4: Create brand-config.json

Write `~/brand-config.json` with this structure (minimum viable):

```json
{
  "brand": {
    "company_name": "Southern Machinery",
    "full_name": "Shenzhen Southern Machinery Sales And Service Co., Ltd",
    "website": "https://www.smthelp.com",
    "tagline": "Precision SMT/THT Equipment Solutions"
  },
  "colors": {
    "primary": "#1E40AF",
    "primary_dark": "#1E3A8A",
    "primary_light": "#3B82F6",
    "secondary": "#EA580C",
    "secondary_dark": "#C2410C",
    "secondary_light": "#FB923C",
    "background": {
      "page": "#FFFFFF",
      "card": "#F8FAFC",
      "subtle": "#F1F5F9"
    },
    "text": {
      "primary": "#1E293B",
      "secondary": "#475569",
      "muted": "#94A3B8",
      "on_primary": "#FFFFFF",
      "on_secondary": "#FFFFFF"
    },
    "functional": {
      "success": "#16A34A",
      "warning": "#D97706",
      "error": "#DC2626",
      "info": "#2563EB"
    },
    "chart": ["#1E40AF","#EA580C","#16A34A","#7C3AED","#0891B2","#DC2626","#CA8A04"]
  },
  "typography": {
    "heading": { "font_family": "Arial, Helvetica, sans-serif", "weight": "700" },
    "body": { "font_family": "Arial, Helvetica, sans-serif", "weight": "400" },
    "mono": { "font_family": "Courier New, monospace", "weight": "400" }
  },
  "layout": { "margin": "40px", "gap": "24px", "radius": "4px", "shadow": "0 1px 3px rgba(0,0,0,0.1)" },
  "logo": { "aspect_ratio": 1.33, "primary_color": "#1E40AF", "white_version": false },
  "style": "professional",
  "industry": "electronics manufacturing equipment"
}
```

### Step 5: Generate brand-preview.html

Write a pure HTML/CSS preview file (no script needed). Include:
- CSS `:root` variables matching brand-config.json
- Color swatches with hex labels
- Typography samples (heading + body + mono)
- Sample table with brand header styling
- Sample card component
- Header bar and footer bar examples

Open via `open ~/brand-preview.html` or deliver path to user.

---

## Phase 2: Document Generation (Pure Python Fallback)

When scripts are unavailable, generate Office files directly with Python libraries.

### For Excel (.xlsx) — Product Catalog / Spec Sheet

```python
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Products"

primary = "1E40AF"
white = "FFFFFF"
header_fill = PatternFill("solid", fgColor=primary)
header_font = Font(color=white, bold=True, size=11)
header_align = Alignment(horizontal="center", vertical="center")
thin = Side(style="thin", color="CCCCCC")
border = Border(bottom=thin)

# Headers
headers = ["Product", "Type", "CPH", "PCB Size", "Accuracy", "Status"]
ws.append(headers)
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = header_align

# Sample data
products = [
    ["S-70LD", "Odd Form Insertion", "18,000", "Min 80×50mm", "±0.05mm", "Flagship"],
    ["S-3010B", "Radial Insertion", "12,000", "Max 250×120mm", "±0.05mm", "Standard"],
    ["S-WS450", "Wave Soldering", "—", "Max 450mm wide", "—", "Standard"],
    ["S-WS350B", "Lead-Free Dual Wave", "—", "Max 350mm wide", "—", "Lead-Free"],
    ["S-100A", "Ultrasonic Cleaner", "—", "—", "—", "Maintenance"],
]
for row in products:
    ws.append(row)

# Style body rows
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    for cell in row:
        cell.font = Font(size=10)
        cell.alignment = Alignment(vertical="center")
        if cell.column == 1:
            cell.font = Font(bold=True, size=10)

# Column widths
ws.column_dimensions['A'].width = 14
ws.column_dimensions['B'].width = 20
ws.column_dimensions['C'].width = 12
ws.column_dimensions['D'].width = 18
ws.column_dimensions['E'].width = 14
ws.column_dimensions['F'].width = 12

wb.save("~/outputs/Southern-Machinery-Product-Catalog.xlsx")
```

### For Word (.docx) — Company One-Pager

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
primary = RGBColor(0x1E, 0x40, 0xAF)
secondary = RGBColor(0xEA, 0x58, 0x0C)

# Title
title = doc.add_heading("Southern Machinery", level=0)
title.runs[0].font.color.rgb = primary
title.runs[0].font.size = Pt(24)

# Subtitle
sub = doc.add_paragraph("Precision SMT/THT Equipment Solutions")
sub.runs[0].font.color.rgb = RGBColor(0x47, 0x55, 0x69)
sub.runs[0].font.size = Pt(12)

# Section
doc.add_heading("Company Overview", level=1).runs[0].font.color.rgb = primary
p = doc.add_paragraph(
    "Shenzhen Southern Machinery Sales And Service Co., Ltd specializes in "
    "SMT/THT automation equipment for global EMS factories. Founded 2011, "
    "serving 20+ years of electronics manufacturing clients worldwide."
)

# Products section
doc.add_heading("Core Products", level=1).runs[0].font.color.rgb = primary
products = [
    ("S-70LD Odd Form Insertion Machine", "18,000 CPH, ±0.05mm accuracy"),
    ("S-3010B Radial Insertion Machine", "12,000 CPH, wide PCB compatibility"),
    ("S-WS450 Wave Soldering Machine", "Standard wave, max 450mm PCB"),
    ("S-WS350B Lead-Free Dual Wave", "Lead-free compliant, dual wave"),
]
for name, desc in products:
    p = doc.add_paragraph(style="List Bullet")
    p.add_run(name + ": ").bold = True
    p.add_run(desc)

doc.save("~/outputs/Southern-Machinery-Company-Profile.docx")
```

### For PowerPoint (.pptx) — Sales Presentation

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

primary = RGBColor(0x1E, 0x40, 0xAF)
secondary = RGBColor(0xEA, 0x58, 0x0C)
white = RGBColor(0xFF, 0xFF, 0xFF)
dark = RGBColor(0x1E, 0x29, 0x3B)

def add_title_slide(prs, title_text, subtitle_text=""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    # Blue background bar
    from pptx.shapes.autoshape import Shape
    from pptx.enum.shapes import MSO_SHAPE
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(4))
    bg.fill.solid(); bg.fill.fore_color.rgb = primary
    bg.line.fill.background()
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.5), Inches(1.5))
    tf = title_box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = title_text
    p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = white
    # Subtitle
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.8), Inches(11.5), Inches(0.8))
        sp = sub_box.text_frame.paragraphs[0]; sp.text = subtitle_text
        sp.font.size = Pt(20); sp.font.color.rgb = RGBColor(0xBF, 0xDB, 0xFE)
    # Footer
    footer = slide.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.5), Inches(0.5))
    fp = footer.text_frame.paragraphs[0]; fp.text = "Southern Machinery — smthelp.com"
    fp.font.size = Pt(12); fp.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

add_title_slide(prs, "SMT/THT Equipment Solutions", "Precision Insertion Machines · Wave Soldering · Full Line Integration")

# Content slide
slide = prs.slides.add_slide(prs.slide_layouts[6])
header = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(1.2))
header.fill.solid(); header.fill.fore_color.rgb = primary
header.line.fill.background()
hbox = slide.shapes.add_textbox(Inches(0.6), Inches(0.3), Inches(12), Inches(0.8))
hp = hbox.text_frame.paragraphs[0]; hp.text = "Core Products"
hp.font.size = Pt(28); hp.font.bold = True; hp.font.color.rgb = white

products = [
    ("S-70LD Odd Form Insertion", "18,000 CPH · ±0.05mm · Radial & DIP"),
    ("S-3010B Radial Insertion", "12,000 CPH · Wide PCB Range"),
    ("S-WS450 Wave Soldering", "Standard Wave · Max 450mm PCB"),
    ("S-WS350B Lead-Free Dual Wave", "Lead-Free Compliant · Dual Wave System"),
]
y = 1.6
for name, spec in products:
    nb = slide.shapes.add_textbox(Inches(0.8), Inches(y), Inches(5), Inches(0.5))
    np_ = nb.text_frame.paragraphs[0]; np_.text = name
    np_.font.size = Pt(18); np_.font.bold = True; np_.font.color.rgb = primary
    sb = slide.shapes.add_textbox(Inches(0.8), Inches(y+0.4), Inches(11), Inches(0.4))
    sp_ = sb.text_frame.paragraphs[0]; sp_.text = spec
    sp_.font.size = Pt(14); sp_.font.color.rgb = dark
    y += 1.1

prs.save("~/outputs/Southern-Machinery-Sales-Deck.pptx")
```

### For HTML → PDF (No External Dependencies)

Write complete HTML file with inline CSS using brand CSS variables. Deliver as `.html` and instruct user to print to PDF via browser (Ctrl+P → Save as PDF).

For **Playwright PDF** (if available):
```bash
pip install playwright && playwright install chromium
```
Then:
```python
import asyncio
from playwright.async_api import async_playwright

async def html_to_pdf(html_path, pdf_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file://{html_path}")
        await page.pdf(format="A4", path=pdf_path, print_background=True)
        await browser.close()

asyncio.run(html_to_pdf("~/brand-preview.html", "~/outputs/brand-preview.pdf"))
```

---

## Document Type Routing

| User Request | Document Type | Output | Method |
|---|---|---|---|
| "Excel", "spreadsheet", "product catalog", "spec sheet" | .xlsx | Product/price table | openpyxl |
| "Word", "company profile", "one-pager", "capabilities" | .docx | Company intro document | python-docx |
| "PPT", "presentation", "sales deck", "pitch" | .pptx | Sales presentation | python-pptx |
| "PDF", "printable", "handbook", "catalog PDF" | .pdf | Print-ready document | HTML → Playwright or browser print |
| "flowchart", "diagram", "SMT line diagram" | .html/.svg | Inline SVG diagram | Write HTML+SVG |
| "整套" / "全套" / "all documents" | Multiple | All above types | Generate in sequence |

---

## Universal Design Rules (All Formats)

**Color Discipline:**
- Primary `#1E40AF`: headers, titles, table headers, emphasis — strategic use only (3-5 places per doc)
- Secondary `#EA580C`: accents, tags, highlights — never large areas
- Neutral text: body text always `#1E293B` or `#475569`, never brand colors

**Anti-AI Aesthetic:**
- ✗ No gradient backgrounds (except cover page)
- ✗ No emoji as decoration
- ✗ No rounded-corner cards with left color bars
- ✗ No 3D chart effects
- ✓ Large whitespace (40% empty is good)
- ✓ High contrast (dark titles + light body)
- ✓ Solid colors, thin line separators
- ✓ Data labels directly on charts

**Logo Placement:**
- Set only ONE dimension (width OR height), auto-scale the other
- Logo placeholder text (e.g. "SM") acceptable for Word/Excel when logo image unavailable

---

## File Organization

```
~/brand-assets/
  logo-color.png              ← Company logo
  logo-white.png              ← White version (if available)
~/brand-config.json           ← Brand design system (source of truth)
~/brand-preview.html          ← Visual brand preview
~/outputs/                   ← All generated documents
  Southern-Machinery-Product-Catalog.xlsx
  Southern-Machinery-Company-Profile.docx
  Southern-Machinery-Sales-Deck.pptx
  ...
```

---

## Southern Machinery — Specific Context

**Company**: Shenzhen Southern Machinery Sales And Service Co., Ltd
**Founded**: 2011, Shenzhen Baoan District
**Core Products**:
- S-70LD Odd Form Insertion Machine (flagship, 18,000 CPH)
- S-3010B Radial Insertion Machine (12,000 CPH)
- S3000 PCB Dip Assembly (radial/DIP)
- S-WS450 Wave Soldering Machine
- S-WS350B Lead-Free Dual Wave Soldering
- S-100A Ultrasonic Cleaner, S-1688 Stencil Cleaner
- S-6200 Nozzle Cleaning Machine, S-680A Reel Scrap Cutter
- S-D601 LED MCPCB Separator

**Key Selling Points**: 30-50% CapEx savings vs. Fuji/Yamaha/Panasonic, full SMT/THT line integration, 20+ years expertise, global service

**Contact**: jasonwu@smthelp.com | +86-136-0256-2576 | smthelp.com
