# Southern Machinery PPT Generation — Working Reference Script

Generated: 2026-06-27 | Tested on: Southern Machinery S-70LD + Wave Soldering sales deck
Python: `/Users/jasonwu/.hermes/hermes-agent/venv/bin/python`

## Quick Start

```bash
# 1. Install dependencies (once)
~/.hermes/hermes-agent/venv/bin/pip install python-pptx lxml

# 2. Write the script to ~/generate_smt_ppt.py
# 3. Run
/Users/jasonwu/.hermes/hermes-agent/venv/bin/python ~/generate_smt_ppt.py
```

## Full Working PPT Generator

```python
#!/usr/bin/env python3
"""
Southern Machinery — S-70LD & Wave Soldering Sales Presentation Generator
Brand: Primary #1E40AF (Deep Blue) | Secondary #EA580C (Orange)
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ─── Brand Colors ──────────────────────────────────────────────────────────────
C_PRIMARY      = RGBColor(0x1E, 0x40, 0xAF)
C_PRIMARY_DARK = RGBColor(0x1E, 0x3A, 0x8A)
C_PRIMARY_LIGHT= RGBColor(0x3B, 0x82, 0xF6)
C_SECONDARY    = RGBColor(0xEA, 0x58, 0x0C)
C_SEC_DARK     = RGBColor(0xC2, 0x41, 0x0C)
C_SEC_LIGHT    = RGBColor(0xFB, 0x92, 0x3C)
C_WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
C_LIGHT_GRAY   = RGBColor(0xF8, 0xFA, 0xFC)
C_MID_GRAY     = RGBColor(0xE2, 0xE8, 0xF0)
C_TEXT         = RGBColor(0x1E, 0x29, 0x3B)
C_TEXT_SEC     = RGBColor(0x47, 0x55, 0x69)
C_TEXT_MUTED   = RGBColor(0x94, 0xA3, 0xB8)
C_SUCCESS      = RGBColor(0x16, 0xA3, 0x4A)
C_ERROR        = RGBColor(0xDC, 0x26, 0x26)
C_INFO         = RGBColor(0x25, 0x63, 0xEB)

W = Inches(13.33)  # 16:9 widescreen
H = Inches(7.5)

def new_prs():
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H
    return prs

def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

def add_rect(slide, left, top, width, height, fill_color=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    shape.line.fill.background()
    return shape

def add_text(slide, left, top, width, height, text, font_size=14, bold=False,
             color=C_TEXT, align=PP_ALIGN.LEFT, font_name="Arial"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_name
    return txBox

# ─── Slide Builders ────────────────────────────────────────────────────────────

def slide_cover(prs):
    s = blank_slide(prs)
    add_rect(s, 0, 0, W, H, C_PRIMARY_DARK)
    add_rect(s, 0, H - Inches(0.6), W, Inches(0.6), C_SECONDARY)
    add_rect(s, 0, H * 0.45, W, H * 0.55, C_WHITE)
    add_rect(s, 0, H * 0.45 - Pt(3), W, Pt(3), C_SECONDARY)
    add_text(s, Inches(0.8), Inches(0.5), Inches(8), Inches(0.6),
             "SHENZHEN SOUTHERN MACHINERY", font_size=16, bold=True,
             color=C_PRIMARY_LIGHT, align=PP_ALIGN.LEFT)
    add_text(s, Inches(0.8), Inches(1.3), Inches(10), Inches(1.2),
             "S-70LD Odd-Form Inserter\n& Wave Soldering Solutions",
             font_size=40, bold=True, color=C_WHITE, align=PP_ALIGN.LEFT)
    add_text(s, Inches(0.8), Inches(2.8), Inches(9), Inches(0.8),
             "High-Speed THT Automation for Global EMS Factories",
             font_size=22, color=C_PRIMARY_LIGHT, align=PP_ALIGN.LEFT)
    add_rect(s, Inches(0.8), Inches(3.8), Inches(6), Inches(0.9), C_SECONDARY)
    add_text(s, Inches(0.8), Inches(3.8), Inches(6), Inches(0.9),
             "Precision · Speed · ROI", font_size=20, bold=True,
             color=C_WHITE, align=PP_ALIGN.CENTER)
    stats = [("18,000 CPH","Radial Insertion"),("4,500 CPH","Odd-Form (S-70LD)"),
             ("450mm PCB","Wave Solder Width"),("14–18 Mo","Payback Period")]
    for i, (num, label) in enumerate(stats):
        x = Inches(0.8 + i * 3.1)
        add_text(s, x, Inches(4.4), Inches(2.8), Inches(0.5),
                 num, font_size=26, bold=True, color=C_PRIMARY, align=PP_ALIGN.LEFT)
        add_text(s, x, Inches(4.95), Inches(2.8), Inches(0.4),
                 label, font_size=13, color=C_TEXT_SEC, align=PP_ALIGN.LEFT)
    add_text(s, Inches(0.8), Inches(6.9), Inches(10), Inches(0.4),
             "www.SMThelp.com  |  jasonwu@smthelp.com  |  +86-136-0256-2576",
             font_size=11, color=C_TEXT_MUTED, align=PP_ALIGN.LEFT)

# ─── Save ────────────────────────────────────────────────────────────────────
prs = new_prs()
slide_cover(prs)
# ... add more slides ...
import os; os.makedirs("~/outputs", exist_ok=True)
prs.save("~/outputs/SM_Sales_Deck.pptx")
```

## PPT Slide Structure for SM Sales Decks

| # | Slide Type | Content |
|---|-----------|---------|
| 1 | Cover | Dark blue + orange, 4 KPI stats |
| 2 | Company Overview | 3 differentiator boxes + values list |
| 3 | Product Line Flow | Horizontal flow diagram: S-70LD→S-4000→S-3000→S-WS450→SUL460 |
| 4 | S-70LD Features | Spec callout boxes + feature list |
| 5 | ROI Analysis | Manual vs Automated comparison table |
| 6 | Wave Solder Specs | S-WS450 spec boxes + temp profile |
| 7 | Competitive Positioning | vs Japanese brands comparison table |
| 8 | Line Configurations | 2方案 (方案A性价比/方案B汽车电子) |
| 9 | CTA | 5 reasons + contact info |

## Key Hex Colors for SM Brand

```
Primary:       #1E40AF  (Deep industrial blue)
Primary Dark:  #1E3A8A
Primary Light: #3B82F6
Secondary:     #EA580C  (Orange — energy)
Secondary Dark: #C2410C
Success:       #16A34A
Error:         #DC2626
Info:          #2563EB
Chart palette: ["#1E40AF","#EA580C","#16A34A","#7C3AED","#0891B2","#DC2626","#CA8A04"]
```

## Product Specs Quick Reference (for PPT content)

| Model | Type | Speed | Accuracy | Key Spec |
|-------|------|-------|---------|---------|
| S-70LD | Odd Form Inserter | ~4,500 CPH | ±0.5mm | 3-25mm元件, 0.8s供料周期 |
| S-4000 | Axial Inserter | 22,000 CPH | ±0.001mm | 轴向+跳线同插 |
| S-3000 | Radial Inserter | 18,000 CPH | 高可靠 | 1000ppm, 不停机补料 |
| S-WS450 | Wave Soldering | — | — | PCB 450mm, 280°C, 460KG锡炉, 双波峰 |
| S-7900 | High-End Odd Form | 4,000 CPH | ±0.05mm | AI Vision + Active Clinching |

## ROI Numbers to Include

- 30-50% CapEx savings vs Fuji/Yamaha/Panasonic
- 4-8 weeks delivery (vs 16-24 weeks Japanese)
- 24-48h after-sales response
- S-70LD: 替代6-8人, 14-18月 payback
- 5年 TCO 节省 49%
