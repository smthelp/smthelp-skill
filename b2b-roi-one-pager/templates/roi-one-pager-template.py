"""
SMT/THT Single-Page A4 ROI PDF — Reusable Template
====================================================

Copy this file, replace the {PLACEHOLDER} slots with your specific
machine + industry data, run, and ship. Pre-fixed for all 5 common
layout pitfalls (footer overlap, CTA overflow, card height, column
width, right-column collision).

Usage:
    /tmp/pdfenv/bin/python3 this_file.py

Output:
    /Users/jasonwu/Downloads/{MACHINE}_ROI_{VERTICAL}.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import simpleSplit
import os

# ============================================================
# {PLACEHOLDER} — fill these in for the specific deliverable
# ============================================================
MACHINE_MODEL    = "S-70LD"            # e.g. "S-70LD", "S3000", "S-WS450"
MACHINE_NAME     = "Dual-Head Odd-Form Inserter"
INDUSTRY         = "White-Goods Controller"   # e.g. "Automotive Tier-1", "LED Tube"
INDUSTRY_LOC     = "EU / Spain"        # shown in the payback section
SHIFT_PATTERN    = "2 shifts"
FOB_LOW          = 30_000
FOB_HIGH         = 50_000
PAYBACK_LOW_MO   = 3
PAYBACK_HIGH_MO  = 4
SAVINGS_5Y_LOW   = "1.0M"
SAVINGS_5Y_HIGH  = "1.5M"
LEGGACY_FEEDER   = "UIC"               # "UIC" / "Panasonic" / "Yamaha" / "TDK"

OUT_PATH = f"/Users/jasonwu/Downloads/{MACHINE_MODEL.replace('-', '')}_ROI_{INDUSTRY.replace(' ', '_').replace('-', '')}.pdf"

# ============================================================
# Brand palette (DO NOT change — these are the proven tokens)
# ============================================================
NAVY    = HexColor("#0A2540")
ORANGE  = HexColor("#FF6B35")
LIGHT   = HexColor("#F4F6F8")
GRID    = HexColor("#D8DEE5")
TEXT    = HexColor("#1A1A1A")
MUTED   = HexColor("#5A6A7B")
GREEN   = HexColor("#2E8B57")

PAGE_W, PAGE_H = A4
M = 12 * mm  # page margin on all 4 sides

# ============================================================
# Spec card data (right column, ~8 rows)
# ============================================================
SPECS = [
    ("Component height",   "5 – 30 mm"),
    ("Cycle time",         "1.2 – 1.8 sec / part"),
    ("Placement accuracy", "±0.05 mm"),
    ("PCB size",           "50 × 50 – 460 × 460 mm"),
    ("Feeder base",        f"100% {LEGGACY_FEEDER} compatible"),
    ("Non-std Feeder",     "3-4 wk custom lead time"),
    ("Throughput",         "up to 3,000 CPH"),
    ("Power / Air",        "220V · 0.5 MPa"),
]

# ============================================================
# Challenge bullets (left column, 4-5 bullets)
# ============================================================
CHALLENGES = [
    "• 25-30% of line labor still spent on manual odd-form insertion",
    "  (relays, terminal blocks, transformers, large e-caps, IGBT modules)",
    "• EU labor cost €28-32/hr fully loaded → 1 station = €45-55k/yr",
    f"• {LEGGACY_FEEDER}-era Feeder base 10-15 yrs old, throwing parts up, yield drift",
    "• EU ESPR + Right-to-Repair → higher-mix, lower-volume runs",
]

# ============================================================
# ROI table data
# ============================================================
ROI_ROWS = [
    ["Line Item", "Manual Station Today", f"With 1 × {MACHINE_MODEL}", "Δ Annual Impact"],
    ["Odd-form stations per line",       "4 – 5",              "1 (machine) + 1 (supervisor)",      "– 3 to 4 FTE"],
    ["Labor cost per year (2 shifts)",   "€400,000 – 500,000", "€100,000 – 130,000",                  "SAVE €300k – 370k"],
    ["First-pass yield (odd-form zone)", "94 – 96 %",          "98.5 – 99.2 %",                       "+ 3 – 4 pts"],
    ["Credit-note exposure (PO penalty)","€25,000 – 50,000 / mo",  "€5,000 – 10,000 / mo",            "SAVE €240k – 480k / yr"],
    ["Line changeover (new board rev.)", "2 – 3 days",         "4 – 6 hours (program + Feeder)",     "– 75 % setup time"],
    ["Energy per board (THT section)",   "Baseline",           "– 25 % (servo + standby)",            "ISO 50001 friendly"],
    [f"{MACHINE_MODEL} investment (FOB Shenzhen)", "—", f"€{FOB_LOW:,} – {FOB_HIGH:,}",        "—"],
    ["PAYBACK PERIOD",                   "—",                  "—",                                  f"{PAYBACK_LOW_MO} – {PAYBACK_HIGH_MO} MONTHS"],
    ["5-YEAR NET SAVINGS (conservative)","—",                  "—",                                  f"€{SAVINGS_5Y_LOW} – {SAVINGS_5Y_HIGH}"],
]

# ============================================================
# Why-Us pillars
# ============================================================
PILLARS = [
    ("15-YEAR SHENZHEN ENGINEERING",
     "Founded 2011. 1,000+ THT lines shipped to EU, LATAM, SEA, MENA. CE certified. 20+ years average engineering tenure on staff."),
    (f"RE-USE YOUR {LEGGACY_FEEDER} FEEDER BASE",
     f"{MACHINE_MODEL} accepts 100% of {LEGGACY_FEEDER} mechanical feeders. No rip-and-replace. Your existing Feeder inventory stays in production."),
    ("NON-STD FEEDER, 3-4 WK LEAD",
     "Custom tooling for relays, terminal blocks, transformers, IGBT. Spare-parts and Nozzle stock in EU + Shenzhen for fast dispatch."),
]

# ============================================================
# Build the PDF
# ============================================================
c = canvas.Canvas(OUT_PATH, pagesize=A4)
c.setTitle(f"{MACHINE_MODEL} ROI — {INDUSTRY} Industry")
c.setAuthor("Southern Machinery")
c.setSubject(f"{MACHINE_MODEL} {MACHINE_NAME} — ROI One-Pager")

# --- HEADER BAR (28mm tall, full width) ---
c.setFillColor(NAVY)
c.rect(0, PAGE_H - 28*mm, PAGE_W, 28*mm, fill=1, stroke=0)
c.setFillColor(ORANGE)
c.rect(M, PAGE_H - 22*mm, 4*mm, 16*mm, fill=1, stroke=0)
c.setFillColor("white")
c.setFont("Helvetica-Bold", 14)
c.drawString(M + 7*mm, PAGE_H - 14*mm, "SOUTHERN MACHINERY")
c.setFont("Helvetica", 8)
c.drawString(M + 7*mm, PAGE_H - 18*mm, "Shenzhen · Est. 2011 · SMT + THT + Wave Soldering Full-Line Solutions")
c.drawString(M + 7*mm, PAGE_H - 22*mm, "www.SMThelp.com  |  jasonwu@smthelp.com  |  +86-136-0256-2576")
c.setFont("Helvetica-Bold", 18)
c.drawRightString(PAGE_W - M, PAGE_H - 12*mm, f"{MACHINE_MODEL} {MACHINE_NAME}")
c.setFont("Helvetica", 10)
c.drawRightString(PAGE_W - M, PAGE_H - 17*mm, f"ROI Analysis · {INDUSTRY} Industry")
c.setFont("Helvetica-Oblique", 8)
c.setFillColor(HexColor("#FFD8C7"))
c.drawRightString(PAGE_W - M, PAGE_H - 22*mm, "Main Control Board · Inverter Motor Control · IoT Modules")

# --- TOP-LEFT CHALLENGE BLOCK + TOP-RIGHT SPECS CARD ---
y0 = PAGE_H - 28*mm
left_w = (PAGE_W - 2*M) * 0.62
right_w = (PAGE_W - 2*M) * 0.34
right_x = M + left_w + 4*mm

c.setFillColor(ORANGE)
c.rect(M, y0 - 4*mm, 3*mm, 4*mm, fill=1, stroke=0)
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 11)
c.drawString(M + 5*mm, y0 - 3*mm, "THE CHALLENGE IN YOUR THT LINE")

c.setFillColor(TEXT)
c.setFont("Helvetica", 8.5)
y = y0 - 9*mm
for line in CHALLENGES:
    c.drawString(M, y, line)
    y -= 4.2*mm

# Specs card
specs_y = y0
c.setFillColor(LIGHT)
c.rect(right_x, specs_y - 50*mm, right_w, 50*mm, fill=1, stroke=0)
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 10)
c.drawString(right_x + 3*mm, specs_y - 5*mm, f"{MACHINE_MODEL} KEY SPECS")
c.setStrokeColor(ORANGE)
c.setLineWidth(0.8)
c.line(right_x + 3*mm, specs_y - 6.5*mm, right_x + right_w - 3*mm, specs_y - 6.5*mm)
sy = specs_y - 11*mm
c.setFont("Helvetica", 8)
for k, v in SPECS:
    c.setFillColor(MUTED)
    c.drawString(right_x + 3*mm, sy, k)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(right_x + right_w - 3*mm, sy, v)
    c.setFont("Helvetica", 8)
    sy -= 4.2*mm

# --- ROI TABLE (full width, prominent) ---
roi_y = y0 - 56*mm
c.setFillColor(ORANGE)
c.rect(M, roi_y - 4*mm, 3*mm, 4*mm, fill=1, stroke=0)
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 11)
c.drawString(M + 5*mm, roi_y - 3*mm, f"PAYBACK MODEL — TYPICAL {INDUSTRY.upper()} PLANT ({INDUSTRY_LOC}, {SHIFT_PATTERN.upper()})")

t = Table(ROI_ROWS, colWidths=[56*mm, 36*mm, 44*mm, 32*mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",  (0,0), (-1,0), "white"),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,0), 8.5),
    ("ALIGN",      (0,0), (-1,0), "LEFT"),
    ("BOTTOMPADDING", (0,0), (-1,0), 4),
    ("TOPPADDING", (0,0), (-1,0), 4),
    ("FONTNAME",   (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",   (0,1), (-1,-1), 8),
    ("TEXTCOLOR",  (0,1), (-1,-1), TEXT),
    ("ALIGN",      (1,1), (-1,-1), "CENTER"),
    ("ALIGN",      (0,1), (0,-1),  "LEFT"),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), ["white", LIGHT]),
    ("LINEBELOW",  (0,0), (-1,-1), 0.3, GRID),
    ("LEFTPADDING",  (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING",   (0,1), (-1,-1), 3),
    ("BOTTOMPADDING",(0,1), (-1,-1), 3),
    ("BACKGROUND", (0,-2), (-1,-2), HexColor("#FFF1E8")),
    ("FONTNAME",   (0,-2), (-1,-2), "Helvetica-Bold"),
    ("TEXTCOLOR",  (0,-2), (-1,-2), ORANGE),
    ("BACKGROUND", (0,-1), (-1,-1), HexColor("#E8F5EE")),
    ("FONTNAME",   (0,-1), (-1,-1), "Helvetica-Bold"),
    ("TEXTCOLOR",  (0,-1), (-1,-1), GREEN),
]))
w, h = t.wrapOn(c, PAGE_W - 2*M, 200)
t.drawOn(c, M, roi_y - 8*mm - h)

# --- WHY US (3 equal columns, 36mm tall cards) ---
why_y = roi_y - 12*mm - h
c.setFillColor(ORANGE)
c.rect(M, why_y - 4*mm, 3*mm, 4*mm, fill=1, stroke=0)
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 11)
c.drawString(M + 5*mm, why_y - 3*mm, "WHY SOUTHERN MACHINERY")

col_w = (PAGE_W - 2*M - 6*mm) / 3
col_y = why_y - 9*mm
col_h = 36*mm
cx = M
for title, body in PILLARS:
    c.setFillColor(LIGHT)
    c.rect(cx, col_y - col_h, col_w, col_h, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(cx, col_y - col_h, 2*mm, col_h, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(cx + 4*mm, col_y - 5*mm, title)
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 7.5)
    lines = simpleSplit(body, "Helvetica", 7.5, col_w - 8*mm)
    ly = col_y - 9*mm
    for ln in lines:
        c.drawString(cx + 4*mm, ly, ln)
        ly -= 3.4*mm
    cx += col_w + 3*mm

# --- CTA BANNER (full width, 18mm tall) ---
cta_y = col_y - col_h - 6*mm
cta_h = 18*mm
c.setFillColor(NAVY)
c.rect(M, cta_y - cta_h, PAGE_W - 2*M, cta_h, fill=1, stroke=0)
c.setFillColor(ORANGE)
c.setFont("Helvetica-Bold", 11)
c.drawString(M + 4*mm, cta_y - 5*mm, "FREE 30-MIN REMOTE LINE HEALTH CHECK")
c.setFillColor("white")
c.setFont("Helvetica", 8.2)
for i, ln in enumerate([
    "Send 1 recent Gerber + your current THT OEE.",
    "We return a written diagnostic + EUR ROI within 3 working days.",
    "No obligation, no quotation.",
]):
    c.drawString(M + 4*mm, cta_y - 9*mm - i*3.2*mm, ln)
c.setFillColor(ORANGE)
c.setFont("Helvetica-Bold", 9.5)
c.drawRightString(PAGE_W - M - 4*mm, cta_y - 6*mm, "jasonwu@smthelp.com")
c.setFillColor("white")
c.setFont("Helvetica", 8.2)
c.drawRightString(PAGE_W - M - 4*mm, cta_y - 10*mm, "WhatsApp / Mobile: +86-136-0256-2576")
c.drawRightString(PAGE_W - M - 4*mm, cta_y - 14*mm, "Book a slot: www.SMThelp.com /contact")

# --- FOOTER (2 short lines, no overlap) ---
c.setFillColor(MUTED)
c.setFont("Helvetica-Oblique", 6.5)
c.drawString(M, 9*mm, f"Figures are conservative engineering estimates for a representative {INDUSTRY.lower()} plant. Actual ROI depends on board mix, shift pattern and existing line layout.")
c.drawString(M, 6*mm, "© 2026 Southern Machinery (Shenzhen) Sales & Service Co., Ltd.  CE certified.  All trademarks belong to their respective owners.")
c.setFont("Helvetica", 6.5)
c.drawRightString(PAGE_W - M, 6*mm, f"Doc ref: {MACHINE_MODEL.replace('-', '')}-ROI-{INDUSTRY.replace(' ', '').replace('-', '')}-2026-EN-v1.0")

c.showPage()
c.save()

print(f"PDF created: {OUT_PATH}")
print(f"Size: {os.path.getsize(OUT_PATH):,} bytes")
