"""Southern Machinery deck builder (smt-product-ppt-rebrand).

usage: smbuild.py <spec.json> <template.pptx> <assets_dir> <out.pptx>
Builds a product deck on the official SM 16:9 template. Brand values come from config/brand.json
(override with env SM_BRAND). Slide types: overview, metrics, pains, fab, process, gallery,
beforeafter, specs, brands, table, summary (see references/slide-types.md)."""
import copy, json, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image

import os
SKILL_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BRAND = json.load(open(os.environ.get("SM_BRAND", os.path.join(SKILL_DIR, "config", "brand.json")), encoding="utf-8"))

def _rgb(h):
    h = h.lstrip("#"); return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

_C = BRAND["colors"]
TEAL = _rgb(_C["primary"])        # 00A3B4 template teal
GREEN = _rgb(_C["secondary"])     # 98B341 template green
NAVY = _rgb(_C["title"])          # 2F5597 = accent1 4472C4 lumMod 75% (template title colour)
GREY = _rgb(_C["muted"])          # 6E747A
LIGHT = _rgb(_C["light_green"])   # E9EFD6
LTEAL = _rgb(_C["light_teal"])    # E5F6F8
WHITE = _rgb(_C["white"])
INK = _rgb(_C["ink"])
FONT = BRAND["fonts"]["latin_and_ea"]

def _font(run, size, bold=False, color=INK):
    f = run.font
    f.size = Pt(size); f.bold = bold; f.color.rgb = color; f.name = FONT
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea",):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", FONT)

def text(slide, x, y, w, h, paras, size=14, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, spacing=None, bullet=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = Inches(0.03)
    tf.vertical_anchor = anchor
    if isinstance(paras, str): paras = [paras]
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        if spacing: para.space_after = Pt(spacing)
        segs = p if isinstance(p, list) else [(p, bold, color)]
        for seg in segs:
            if isinstance(seg, str): seg = (seg, bold, color)
            t, b, c = seg
            r = para.add_run(); r.text = (("■  " if bullet and seg is segs[0] else "") + t) if False else t
            _font(r, size, b, c)
        if bullet:
            pPr = para._p.get_or_add_pPr()
            pPr.set("marL", str(Inches(0.25))); pPr.set("indent", str(-Inches(0.25)))
            bu = etree.SubElement(pPr, qn("a:buClr")); s = etree.SubElement(bu, qn("a:srgbClr")); s.set("val", "00A3B4")
            bf = etree.SubElement(pPr, qn("a:buFont")); bf.set("typeface", "Arial")
            bc = etree.SubElement(pPr, qn("a:buChar")); bc.set("char", "■")
    return tb

def title(slide, t, size=None):
    if size is None:
        size = 28 if len(t) <= 30 else (24 if len(t) <= 36 else 22)
    """Template title style: 微软雅黑 bold, accent1 75% (navy), soft shadow, in the header band."""
    tb = slide.shapes.add_textbox(Inches(1.85), Inches(0.05), Inches(7.6), Inches(0.58))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t; _font(r, size, True, NAVY)
    rPr = r._r.get_or_add_rPr()
    eff = etree.fromstring('<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:outerShdw blurRad="38100" dist="19050" dir="2700000" algn="tl" rotWithShape="0"><a:prstClr val="black"><a:alpha val="40000"/></a:prstClr></a:outerShdw></a:effectLst>')
    # effectLst must follow solidFill
    sf = rPr.find(qn("a:solidFill")); sf.addnext(eff)
    return tb

def box(slide, x, y, w, h, fill=WHITE, line=TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, lw=1.0, adj=0.08):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None: s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None: s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(lw)
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try: s.adjustments[0] = adj
        except Exception: pass
    s.text_frame.text = ""
    return s

def shape_text(s, t, size=14, color=WHITE, bold=True, align=PP_ALIGN.CENTER):
    tf = s.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.08)
    lines = t if isinstance(t, list) else [t]
    for i, l in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = l; _font(r, size if i == 0 else size - 3, bold if i == 0 else False, color)

def picture(slide, path, x, y, w, h, border=True):
    im = Image.open(path); iw, ih = im.size
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    tr, br = w / h, iw / ih
    if br > tr:  # too wide: crop sides
        c = (1 - tr / br) / 2; pic.crop_left = c; pic.crop_right = c
    else:
        c = (1 - br / tr) / 2; pic.crop_top = c; pic.crop_bottom = c
    if border:
        pic.line.color.rgb = TEAL; pic.line.width = Pt(1)
    return pic

def picture_fit(slide, path, x, y, w, h):
    im = Image.open(path); iw, ih = im.size
    s = min(w / iw, h / ih); pw, ph = iw * s, ih * s
    return slide.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))

def notes(slide, t):
    slide.notes_slide.notes_text_frame.text = t

def chevron(slide, x, y, w, h, t, fill=TEAL, size=13, first=False):
    s = box(slide, x, y, w, h, fill=fill, line=None, shape=MSO_SHAPE.PENTAGON if first else MSO_SHAPE.CHEVRON)
    shape_text(s, t, size=size)
    return s

# ---------------- slide types ----------------
def s_title(prs, L, d, A):
    s = prs.slides.add_slide(L)
    text(s, 0.75, 1.25, 6.9, 0.4, d["eyebrow"], size=14, color=TEAL, bold=True)
    text(s, 0.75, 1.7, 6.9, 1.6, d["name"], size=38, color=NAVY, bold=True)
    bar = box(s, 0.8, 3.35, 1.2, 0.07, fill=GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
    text(s, 0.75, 3.55, 6.6, 1.1, d["subtitle"], size=17, color=INK)
    text(s, 0.75, 4.75, 6.6, 0.4, d["tagline"], size=14, color=TEAL, bold=True)
    text(s, 1.6, 5.75, 6.3, 0.6, [BRAND["company"]["legal_name"],
         BRAND["company"]["deck_label"] + "  |  " + d["date"]], size=11, color=GREY)
    picture_fit(s, A + d["image"], 7.55, 1.35, 4.3, 4.6)
    notes(s, d.get("notes", ""))

def s_contents(prs, L, items):
    s = prs.slides.add_slide(L)
    title(s, "Contents")
    n = len(items); top = 1.2; gap = 0.12; h = min(0.72, (5.0 - gap * (n - 1)) / n)
    for i, (head, sub) in enumerate(items):
        y = top + i * (h + gap)
        num = box(s, 1.6, y, 1.0, h, fill=TEAL, line=None, shape=MSO_SHAPE.PENTAGON)
        shape_text(num, f"{i+1:02d}", size=20)
        bx = box(s, 2.75, y, 7.6, h, fill=WHITE, line=TEAL, lw=0.75)
        text(s, 2.95, y, 4.7, h, head, size=17, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, 7.7, y, 2.6, h, sub, size=12, color=GREY, anchor=MSO_ANCHOR.MIDDLE)
    notes(s, "Agenda for the presentation.")

def s_overview(prs, L, d, A):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    text(s, 0.75, 1.0, 6.4, 1.3, d["lead"], size=15, color=INK)
    y = 2.35
    head = box(s, 0.75, y, 6.4, 0.42, fill=TEAL, line=None, shape=MSO_SHAPE.RECTANGLE)
    text(s, 0.85, y, 2.0, 0.42, "Application", size=12.5, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 2.85, y, 4.2, 0.42, "Typical parts / materials", size=12.5, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    rh = (3.75 - 0.42) / len(d["apps"])
    for i, (a, b) in enumerate(d["apps"]):
        yy = y + 0.42 + i * rh
        box(s, 0.75, yy, 6.4, rh, fill=LIGHT if i % 2 == 0 else WHITE, line=None, shape=MSO_SHAPE.RECTANGLE)
        text(s, 0.85, yy, 2.0, rh, a, size=13.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, 2.85, yy, 4.25, rh, b, size=13, anchor=MSO_ANCHOR.MIDDLE)
    picture(s, A + d["image"], 7.5, 1.45, 4.2, 3.9)
    if d.get("caption"):
        text(s, 7.5, 5.4, 4.2, 0.4, d["caption"], size=11, color=GREY, align=PP_ALIGN.CENTER)
    notes(s, d.get("notes", ""))

def s_metrics(prs, L, d):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    if d.get("lead"):
        text(s, 0.75, 1.0, 10.9, 0.6, d["lead"], size=15)
    n = len(d["items"]); w = (10.9 - 0.3 * (n - 1)) / n
    for i, (v, lab, sub) in enumerate(d["items"]):
        x = 0.75 + i * (w + 0.3)
        box(s, x, 1.9, w, 3.3, fill=WHITE, line=TEAL, lw=1.25)
        box(s, x, 1.9, w, 0.12, fill=TEAL if i % 2 == 0 else GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
        text(s, x + 0.1, 2.25, w - 0.2, 1.0, v, size=(34 if len(v) <= 5 else (28 if len(v) <= 8 else 24)), color=NAVY, bold=True, align=PP_ALIGN.CENTER)
        text(s, x + 0.1, 3.3, w - 0.2, 0.5, lab, size=14, color=TEAL, bold=True, align=PP_ALIGN.CENTER)
        text(s, x + 0.15, 3.85, w - 0.3, 1.2, sub, size=11.5, color=GREY, align=PP_ALIGN.CENTER)
    if d.get("footer"):
        text(s, 0.75, 5.5, 10.9, 0.6, d["footer"], size=13, color=INK, align=PP_ALIGN.CENTER)
    notes(s, d.get("notes", ""))

def s_pains(prs, L, d):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    text(s, 0.75, 0.95, 10.9, 0.55, d["lead"], size=15)
    items = d["items"]; cols = 4 if len(items) > 6 else 3
    rows = (len(items) + cols - 1) // cols
    w = (10.9 - 0.25 * (cols - 1)) / cols; h = (4.35 - 0.25 * (rows - 1)) / rows
    for i, (head, body) in enumerate(items):
        x = 0.75 + (i % cols) * (w + 0.25); y = 1.65 + (i // cols) * (h + 0.25)
        box(s, x, y, w, h, fill=WHITE, line=GREY, lw=0.75)
        badge = box(s, x + 0.15, y + 0.18, 0.45, 0.45, fill=GREEN, line=None, shape=MSO_SHAPE.OVAL)
        shape_text(badge, "!", size=16)
        text(s, x + 0.7, y + 0.13, w - 0.8, 0.6, head, size=14.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, x + 0.15, y + 0.8, w - 0.3, h - 0.9, body, size=13, color=INK)
    if d.get("footer"):
        bar = box(s, 0.75, 6.15, 10.9, 0.45, fill=LTEAL, line=None, shape=MSO_SHAPE.RECTANGLE)
        text(s, 0.85, 6.15, 10.7, 0.45, d["footer"], size=13, color=TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    notes(s, d.get("notes", ""))

def s_fab(prs, L, d):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    x0, top = 0.95, 1.0
    cw = [3.5, 3.5, 3.5]; gap = 0.12
    heads = [("FEATURES", "What it has", TEAL), ("ADVANTAGES", "What it does", GREEN), ("BENEFITS", "What you gain", NAVY)]
    xs = [x0, x0 + cw[0] + gap, x0 + cw[0] + cw[1] + 2 * gap]
    for i, (hd, sub, c) in enumerate(heads):
        hb = box(s, xs[i], top, cw[i], 0.55, fill=c, line=None, shape=MSO_SHAPE.PENTAGON if i < 2 else MSO_SHAPE.RECTANGLE)
        text(s, xs[i] + 0.12, top, cw[i] - 0.4, 0.55, [[(hd, True, WHITE), ("   " + sub, False, WHITE)]], size=14, anchor=MSO_ANCHOR.MIDDLE)
    rows = d["rows"]; rh = (4.85 - 0.15 * (len(rows) - 1)) / len(rows); y = top + 0.7
    for r in rows:
        for i in range(3):
            fill = LTEAL if i == 0 else (LIGHT if i == 1 else WHITE)
            line = TEAL if i == 0 else (GREEN if i == 1 else NAVY)
            box(s, xs[i], y, cw[i], rh, fill=fill, line=line, lw=0.75, adj=0.06)
            hd, body = r[i] if isinstance(r[i], (list, tuple)) else (None, r[i])
            paras = []
            if hd: paras.append([(hd, True, line)])
            paras.append([(body, False, INK)])
            text(s, xs[i] + 0.12, y + 0.06, cw[i] - 0.24, rh - 0.12, paras, size=13.5, anchor=MSO_ANCHOR.MIDDLE, spacing=3)
        y += rh + 0.15
    notes(s, d.get("notes", ""))

def s_process(prs, L, d, A):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    if d.get("lead"): text(s, 0.75, 0.95, 10.9, 0.5, d["lead"], size=15)
    steps = d["steps"]; per = d.get("per_row", len(steps))
    rows = [steps[i:i + per] for i in range(0, len(steps), per)]
    y = 1.6
    for ri, row in enumerate(rows):
        n = len(row); w = (10.9 + 0.12 * (n - 1)) / n
        for i, (hd, sub) in enumerate(row):
            x = 0.75 + i * (w - 0.12)
            chevron(s, x, y, w, 0.85, hd, fill=TEAL if (i + ri) % 2 == 0 else GREEN, size=12.5, first=(i == 0 and ri == 0))
            text(s, x + 0.2, y + 0.92, w - 0.35, 0.85, sub, size=12.5, color=INK, align=PP_ALIGN.CENTER)
        y += 1.95
    if d.get("images"):
        ims = d["images"]; n = len(ims); top = y + 0.05; hh = 6.45 - top
        w = (10.9 - 0.3 * (n - 1)) / n
        for i, (p, cap) in enumerate(ims):
            x = 0.75 + i * (w + 0.3)
            picture(s, A + p, x, top, w, hh - 0.38)
            text(s, x, top + hh - 0.36, w, 0.35, cap, size=11, color=GREY, align=PP_ALIGN.CENTER)
    if d.get("footer"):
        text(s, 0.75, y + 0.1, 10.9, 0.5, d["footer"], size=14, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    notes(s, d.get("notes", ""))

def s_gallery(prs, L, d, A):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    if d.get("lead"): text(s, 0.75, 0.95, 10.9, 0.5, d["lead"], size=15)
    items = d["items"]; n = len(items); top = 1.6 if d.get("lead") else 1.1
    w = (10.9 - 0.3 * (n - 1)) / n; imgh = d.get("imgh", 2.9)
    for i, it in enumerate(items):
        x = 0.75 + i * (w + 0.3)
        if it.get("fit"):
            box(s, x, top, w, imgh, fill=WHITE, line=TEAL, shape=MSO_SHAPE.RECTANGLE)
            picture_fit(s, A + it["image"], x + 0.05, top + 0.05, w - 0.1, imgh - 0.1)
        else:
            picture(s, A + it["image"], x, top, w, imgh)
        text(s, x, top + imgh + 0.1, w, 0.4, it["head"], size=14, color=NAVY, bold=True)
        text(s, x, top + imgh + 0.5, w, 6.45 - (top + imgh + 0.5), it["body"], size=13, bullet=True)
    notes(s, d.get("notes", ""))

def s_beforeafter(prs, L, d, A):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    text(s, 0.75, 0.95, 10.9, 0.5, d["lead"], size=15)
    # left: before/after pair; right: extra image
    lw = 6.6 if d.get("side") else 10.9
    pw = (lw - 0.25) / 2
    for i, (p, lab, c) in enumerate([(d["before"], "BEFORE", GREY), (d["after"], "AFTER", TEAL)]):
        x = 0.75 + i * (pw + 0.25)
        picture(s, A + p, x, 1.65, pw, 4.0)
        tag = box(s, x, 1.65, 1.2, 0.4, fill=c, line=None, shape=MSO_SHAPE.RECTANGLE)
        shape_text(tag, lab, size=12)
    text(s, 0.75, 5.75, lw, 0.6, d["caption"], size=12, color=GREY, align=PP_ALIGN.CENTER)
    if d.get("side"):
        p, cap = d["side"]
        picture_fit(s, A + p, 7.65, 1.65, 4.0, 3.7)
        text(s, 7.65, 5.45, 4.0, 0.9, cap, size=12, color=GREY, align=PP_ALIGN.CENTER)
    notes(s, d.get("notes", ""))

def s_specs(prs, L, d):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    rows = d["rows"]; half = (len(rows) + 1) // 2
    pairs = [rows[i:i + 1] + rows[half + i:half + i + 1] for i in range(half)]
    nrow = half + 1
    rhh = max(0.42, min(0.62, 5.0 / nrow)); fs = 13 if nrow <= 7 else 11.5
    top = 1.0; height = min(5.35, rhh * nrow)
    tbl = s.shapes.add_table(nrow, 4, Inches(0.75), Inches(top), Inches(10.9), Inches(height)).table
    widths = [2.2, 3.25, 2.2, 3.25]
    for i, w in enumerate(widths): tbl.columns[i].width = Inches(w)
    hdr = ["Parameter", "Specification", "Parameter", "Specification"]
    def cell(c, t, size, bold, color, fill):
        c.fill.solid(); c.fill.fore_color.rgb = fill
        c.margin_left = c.margin_right = Inches(0.08); c.margin_top = c.margin_bottom = Inches(0.03)
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = c.text_frame; tf.word_wrap = True; tf.paragraphs[0].text = ""
        r = tf.paragraphs[0].add_run(); r.text = t; _font(r, size, bold, color)
    for j, h in enumerate(hdr): cell(tbl.cell(0, j), h, 12.5, True, WHITE, TEAL)
    for i, pr in enumerate(pairs, 1):
        fill = LIGHT if i % 2 else WHITE
        for k in range(2):
            if k < len(pr):
                cell(tbl.cell(i, 2 * k), pr[k][0], fs, True, NAVY, fill)
                cell(tbl.cell(i, 2 * k + 1), pr[k][1], fs, False, INK, fill)
            else:
                cell(tbl.cell(i, 2 * k), "", 11, False, INK, fill); cell(tbl.cell(i, 2 * k + 1), "", 11, False, INK, fill)
    for i in range(nrow): tbl.rows[i].height = Inches(height / nrow)
    # disable banding style id to keep our fills
    tblPr = tbl._tbl.tblPr; tblPr.set("firstRow", "0"); tblPr.set("bandRow", "0")
    if d.get("footer"):
        text(s, 0.75, top + height + 0.12, 10.9, 0.4, d["footer"], size=11, color=GREY)
    notes(s, d.get("notes", ""))

def s_brands(prs, L, d, A):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    text(s, 0.75, 0.95, 10.9, 0.5, d["lead"], size=15)
    picture(s, A + d["image"], 0.75, 1.65, 4.0, 4.6)
    items = d["items"]; cols = 2; rows = (len(items) + 1) // 2
    w = (6.6 - 0.2) / 2; h = (4.6 - 0.18 * (rows - 1)) / rows
    for i, (b, part) in enumerate(items):
        x = 5.05 + (i % cols) * (w + 0.2); y = 1.65 + (i // cols) * (h + 0.18)
        box(s, x, y, w, h, fill=WHITE, line=TEAL, lw=0.75)
        box(s, x, y, 0.1, h, fill=TEAL if i % 2 == 0 else GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
        text(s, x + 0.22, y + 0.05, w - 0.3, 0.4, b, size=14, color=NAVY, bold=True)
        text(s, x + 0.22, y + 0.45, w - 0.3, h - 0.5, part, size=13, color=INK)
    notes(s, d.get("notes", ""))

def s_summary(prs, L, d):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    text(s, 0.75, 0.95, 10.9, 0.55, d["lead"], size=16, color=NAVY, bold=True)
    items = d["items"]; n = len(items)
    rh = (3.9 - 0.15 * (n - 1)) / n
    for i, (hd, body) in enumerate(items):
        y = 1.65 + i * (rh + 0.15)
        num = box(s, 0.75, y, 0.65, rh, fill=TEAL if i % 2 == 0 else GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
        shape_text(num, "✓", size=18)
        box(s, 1.4, y, 10.25, rh, fill=LTEAL if i % 2 == 0 else LIGHT, line=None, shape=MSO_SHAPE.RECTANGLE)
        text(s, 1.6, y, 3.4, rh, hd, size=17, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(s, 4.9, y, 6.65, rh, body, size=15, anchor=MSO_ANCHOR.MIDDLE)
    cta = box(s, 1.4, 5.7, 10.0, 0.66, fill=NAVY, line=None)
    shape_text(cta, d["cta"], size=15)
    notes(s, d.get("notes", ""))

def s_table(prs, L, d):
    s = prs.slides.add_slide(L)
    title(s, d["title"])
    top = 1.0
    if d.get("lead"):
        text(s, 0.75, 0.95, 10.9, 0.5, d["lead"], size=14); top = 1.5
    cols = d["columns"]; rows = d["rows"]; nrow = len(rows) + 1
    avail = 6.3 - top - (0.45 if d.get("footer") else 0)
    rhh = max(0.3, min(0.55, avail / nrow)); fs = 12.5 if rhh >= 0.42 else (11 if rhh >= 0.34 else 10)
    height = rhh * nrow
    tbl = s.shapes.add_table(nrow, len(cols), Inches(0.75), Inches(top), Inches(10.9), Inches(height)).table
    ws = d.get("widths") or [10.9 / len(cols)] * len(cols)
    k = 10.9 / sum(ws)
    for i, w in enumerate(ws): tbl.columns[i].width = Inches(w * k)
    def cell(c, t, size, bold, color, fill, align=PP_ALIGN.LEFT):
        c.fill.solid(); c.fill.fore_color.rgb = fill
        c.margin_left = c.margin_right = Inches(0.07); c.margin_top = c.margin_bottom = Inches(0.02)
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = c.text_frame; tf.word_wrap = True; tf.paragraphs[0].text = ""; tf.paragraphs[0].alignment = align
        r = tf.paragraphs[0].add_run(); r.text = str(t); _font(r, size, bold, color)
    for j, h in enumerate(cols): cell(tbl.cell(0, j), h, fs, True, WHITE, TEAL, PP_ALIGN.CENTER)
    for i, row in enumerate(rows, 1):
        fill = LIGHT if i % 2 else WHITE
        for j, v in enumerate(row):
            cell(tbl.cell(i, j), v, fs, j == 0, NAVY if j == 0 else INK, fill, PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER)
    for i in range(nrow): tbl.rows[i].height = Inches(rhh)
    tblPr = tbl._tbl.tblPr; tblPr.set("firstRow", "0"); tblPr.set("bandRow", "0")
    if d.get("footer"):
        text(s, 0.75, top + height + 0.1, 10.9, 0.4, d["footer"], size=11, color=GREY)
    notes(s, d.get("notes", ""))

TYPES = {"overview": s_overview, "metrics": s_metrics, "pains": s_pains, "fab": s_fab, "process": s_process,
         "gallery": s_gallery, "beforeafter": s_beforeafter, "specs": s_specs, "brands": s_brands, "summary": s_summary, "table": s_table}
NEEDS_A = {"overview", "process", "gallery", "beforeafter", "brands"}

def build(template, spec, assets, out):
    prs = Presentation(template)
    # layout used by template content slides 2-4 ("1_标题幻灯片", master 3)
    T = BRAND["template"]
    L = prs.slides[T["content_layout_from_slide"]].slide_layout
    orig = list(prs.slides._sldIdLst)
    s_title(prs, L, spec["title"], assets)
    s_contents(prs, L, spec["contents"])
    for sl in spec["slides"]:
        f = TYPES[sl["type"]]
        f(prs, L, sl, assets) if sl["type"] in NEEDS_A else f(prs, L, sl)
    # keep template slide 5 (After-sales) and 6 (Welcome Inquiry) at the end; drop blank slides 1-4
    lst = prs.slides._sldIdLst
    for sid in [orig[i] for i in T["keep_slides_at_end"]]:
        lst.remove(sid); lst.append(sid)
    for sid in [orig[i] for i in T["drop_slides"]]:
        prs.part.drop_rel(sid.get(qn("r:id"))); lst.remove(sid)
    prs.core_properties.title = spec["meta"]["title"]
    prs.core_properties.subject = spec["meta"]["subject"]
    prs.core_properties.keywords = spec["meta"]["keywords"]
    prs.core_properties.author = BRAND["company"]["short_name"]
    prs.save(out)

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    build(sys.argv[2], spec, sys.argv[3], sys.argv[4])
    print("ok", sys.argv[4])
