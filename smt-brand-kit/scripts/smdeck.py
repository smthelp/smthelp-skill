#!/usr/bin/env python3
"""Southern Machinery A4-portrait PPTX renderer (python-pptx) with a PIL preview
and overflow checks. Used by make_deck.py for both the marketing deck and the
operation manual. Design tokens come from assets/brand/brand.json."""
import json, os
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.opc.packuri import PackURI
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.normpath(os.path.join(HERE, "..", "assets", "brand"))
BRAND = json.load(open(os.path.join(BRAND_DIR, "brand.json"), encoding="utf-8"))
C = BRAND["colors"]
DARK, GREEN, TEAL, GREY, LIGHT, WHITE = C["navy"], C["green"], C["teal"], C["grey"], C["light"], C["white"]
FONT = BRAND["fonts"]["pptx"]
FREG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FBOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DPI = 100
X0, X1, Y0, Y1 = 0.45, 7.82, 1.3, 10.85   # safe content area (inches) inside template chrome
W = X1 - X0
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


class Deck:
    def __init__(self, base_dir, template=None, preview_dir=None):
        self.base = base_dir                      # media paths in specs are relative to this
        self.prs = Presentation(template or os.path.join(BRAND_DIR, "sm-template-2025-a4.pptx"))
        self.SW, self.SH = self.prs.slide_width / 914400, self.prs.slide_height / 914400
        # template = 3 blank slides + contact slide (index 3); keep contact, move it to the end on save
        self.contact = self.prs.slides[3]
        self.contact.part.partname = PackURI("/ppt/slides/slide99.xml")
        lst = self.prs.slides._sldIdLst
        for sid in list(lst)[:3]:
            self.prs.part.drop_rel(sid.rId); lst.remove(sid)
        self.errors, self.pages = [], []
        self.preview_dir = preview_dir
        self._m = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    # ---------- primitives ----------
    def path(self, p):
        return p if os.path.isabs(p) else os.path.join(self.base, p)

    def new_slide(self, name):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[0])
        im = Image.new("RGB", (int(self.SW * DPI), int(self.SH * DPI)), "white")
        d = ImageDraw.Draw(im)
        d.rectangle([9, 15, 265, 87], outline="#" + GREEN); d.text((14, 40), "SM LOGO (template)", fill="#" + GREEN)
        d.rectangle([0, int(11.08 * DPI), int(self.SW * DPI), int(self.SH * DPI)], fill="#F3F3F3")
        self.pages.append((s, im, name))
        self.sd = (s, d, im)
        return self.sd

    def font(self, size, bold=False):
        return ImageFont.truetype(FBOLD if bold else FREG, int(size * DPI / 72 * 0.97))

    def wrap(self, text, font, maxw):
        lines = []
        for para in str(text).split("\n"):
            cur = ""
            for w in para.split(" "):
                t = (cur + " " + w).strip()
                if self._m.textlength(t, font=font) <= maxw or not cur: cur = t
                else: lines.append(cur); cur = w
            lines.append(cur)
        return lines

    def measure(self, s, w, size=12, bold=False, lsp=1.2, bullets=False):
        """Height in inches a text block needs (DejaVu is wider than YaHei -> conservative)."""
        paras = s if isinstance(s, list) else [s]
        f = self.font(size, bold); lh = size * lsp / 72
        n = 0.0
        for i, p in enumerate(paras):
            n += len(self.wrap(("• " if bullets else "") + p, f, (w - 0.1) * DPI)) * lh + (lh * 0.35 if i else 0)
        return n + 0.08

    def text(self, x, y, w, h, s, size=12, bold=False, color=DARK, align="l", anchor="t", lsp=1.2, name="text", bullets=False):
        slide, d, im = self.sd
        if (x < X0 - 0.01 or x + w > X1 + 0.01 or y < 0.15 or y + h > Y1 + 0.01) and name != "title":
            self.errors.append(f"{self.pages[-1][2]}: {name} outside safe area")
        paras = s if isinstance(s, list) else [s]
        paras = [str(p) for p in paras]
        f = self.font(size, bold); lh = size * lsp / 72 * DPI
        lines = []
        for p in paras:
            lines += self.wrap(("• " if bullets else "") + p, f, (w - 0.1) * DPI); lines.append(None)
        lines = lines[:-1]
        need = sum(lh if l is not None else lh * 0.35 for l in lines)
        if need > (h - 0.05) * DPI + 1:
            self.errors.append(f"{self.pages[-1][2]}: {name} overflow ({need/DPI:.2f}in > {h:.2f}in): {paras[0][:40]}")
        ty = y * DPI + (0 if anchor == "t" else ((h * DPI - need) / 2 if anchor == "m" else h * DPI - need))
        for l in lines:
            if l is None: ty += lh * 0.35; continue
            tw = d.textlength(l, font=f)
            tx = x * DPI + 5 + (0 if align == "l" else ((w * DPI - tw) / 2 - 5 if align == "c" else w * DPI - tw - 10))
            d.text((tx, ty), l, font=f, fill="#" + color); ty += lh
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = Inches(0.02)
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            para.line_spacing = lsp * 0.85
            if i: para.space_before = Pt(size * 0.35)
            r = para.add_run(); r.text = ("• " if bullets else "") + p
            r.font.size = Pt(size); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = RGBColor.from_string(color)
            rPr = r._r.get_or_add_rPr(); rPr.append(rPr.makeelement(A_NS + "ea", {"typeface": FONT}))
        return tb

    def rect(self, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
        slide, d, im = self.sd
        sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        sp.fill.solid(); sp.fill.fore_color.rgb = RGBColor.from_string(fill)
        if line: sp.line.color.rgb = RGBColor.from_string(line); sp.line.width = Pt(0.75)
        else: sp.line.fill.background()
        sp.shadow.inherit = False
        if shape == MSO_SHAPE.ROUNDED_RECTANGLE: sp.adjustments[0] = 0.08
        if shape == MSO_SHAPE.OVAL: d.ellipse([x * DPI, y * DPI, (x + w) * DPI, (y + h) * DPI], fill="#" + fill)
        else: d.rectangle([x * DPI, y * DPI, (x + w) * DPI, (y + h) * DPI], fill="#" + fill, outline=("#" + line) if line else None)
        return sp

    def pic(self, path, x, y, w, h, focus=(0.5, 0.5), fit="cover"):
        slide, d, im = self.sd
        fp = self.path(path)
        if not os.path.exists(fp):
            self.errors.append(f"{self.pages[-1][2]}: missing image {path}"); self.rect(x, y, w, h, LIGHT); return
        src = Image.open(fp).convert("RGB"); iw, ih = src.size; ar = w / h
        if fit == "cover":
            if iw / ih > ar:
                cw = ih * ar; l = max(0, min(iw - cw, iw * focus[0] - cw / 2)); box = (l, 0, l + cw, ih)
            else:
                ch = iw / ar; t = max(0, min(ih - ch, ih * focus[1] - ch / 2)); box = (0, t, iw, t + ch)
            p = slide.shapes.add_picture(fp, Inches(x), Inches(y), Inches(w), Inches(h))
            p.crop_left, p.crop_top, p.crop_right, p.crop_bottom = box[0] / iw, box[1] / ih, 1 - box[2] / iw, 1 - box[3] / ih
            im.paste(src.crop(tuple(int(v) for v in box)).resize((max(1, int(w * DPI)), max(1, int(h * DPI)))), (int(x * DPI), int(y * DPI)))
        else:
            s = min(w / iw, h / ih); pw, ph = iw * s, ih * s; px, py = x + (w - pw) / 2, y + (h - ph) / 2
            slide.shapes.add_picture(fp, Inches(px), Inches(py), Inches(pw), Inches(ph))
            im.paste(src.resize((max(1, int(pw * DPI)), max(1, int(ph * DPI)))), (int(px * DPI), int(py * DPI)))

    # ---------- components ----------
    def title(self, t, kicker=None):
        if kicker: self.text(2.85, 0.22, 4.97, 0.3, kicker.upper(), 10, True, GREEN, name="title")
        size = 19 if len(t) <= 34 else (17 if len(t) <= 60 else 15)
        self.text(2.85, 0.48 if kicker else 0.3, 4.97, 0.7 if kicker else 0.8, t, size, True, DARK, name="title", lsp=1.1)
        if self.measure(t, 4.97, size, True, 1.1) > (0.75 if kicker else 0.85):
            self.errors.append(f"{self.pages[-1][2]}: title too long: {t[:50]}")
        self.rect(X0, 1.15, W, 0.03, GREEN)

    def caption(self, x, y, w, t):
        self.text(x, y, w, 0.42, t, 8.5, False, GREY, name="caption", lsp=1.1)

    def table(self, x, y, w, colw, rows, size=9, rowh=None, head=True, name="table"):
        slide, d, im = self.sd
        f, fb = self.font(size), self.font(size, True)
        cws = [w * c for c in colw]
        heights = []
        for ri, r in enumerate(rows):
            mx = 1
            for ci, c in enumerate(r):
                mx = max(mx, len(self.wrap(c, fb if (head and ri == 0) or ci == 0 else f, (cws[ci] - 0.14) * DPI)))
            heights.append(max(rowh or 0, mx * size * 1.18 / 72 + 0.12))
        total = sum(heights)
        if y + total > Y1 + 0.01: self.errors.append(f"{self.pages[-1][2]}: {name} overflow ends at {y+total:.2f}in")
        tbl = slide.shapes.add_table(len(rows), len(colw), Inches(x), Inches(y), Inches(w), Inches(total)).table
        tblPr = tbl._tbl.tblPr
        for k in ("bandRow", "firstRow"): tblPr.set(k, "0")
        st = tblPr.find(A_NS + "tableStyleId")
        if st is not None: st.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"
        for ci, cw in enumerate(cws): tbl.columns[ci].width = Inches(cw)
        yy = y
        for ri, r in enumerate(rows):
            tbl.rows[ri].height = Inches(heights[ri]); hdr = head and ri == 0
            bg = DARK if hdr else (LIGHT if ri % 2 == 0 else WHITE); xx = x
            for ci, c in enumerate(r):
                cell = tbl.cell(ri, ci); cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor.from_string(bg)
                cell.margin_left = cell.margin_right = Inches(0.07); cell.margin_top = cell.margin_bottom = Inches(0.04)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = cell.text_frame.paragraphs[0]; cell.text_frame.word_wrap = True; p.text = ""
                run = p.add_run(); run.text = str(c); run.font.size = Pt(size); run.font.name = FONT
                run.font.bold = hdr or ci == 0
                run.font.color.rgb = RGBColor.from_string(WHITE if hdr else (DARK if ci == 0 else "222222"))
                d.rectangle([xx * DPI, yy * DPI, (xx + cws[ci]) * DPI, (yy + heights[ri]) * DPI], fill="#" + bg, outline="#C9D6DB")
                ls = self.wrap(c, fb if hdr or ci == 0 else f, (cws[ci] - 0.14) * DPI)
                ty = yy * DPI + (heights[ri] * DPI - len(ls) * size * 1.18 / 72 * DPI) / 2
                for l in ls:
                    d.text((xx * DPI + 7, ty), l, font=fb if hdr or ci == 0 else f, fill="#FFFFFF" if hdr else "#" + DARK); ty += size * 1.18 / 72 * DPI
                xx += cws[ci]
            yy += heights[ri]
        return y + total

    def card(self, x, y, w, h, head, body, num=None, accent=GREEN, size=9.5):
        self.rect(x, y, w, h, LIGHT); self.rect(x, y, 0.06, h, accent)
        hx = x + 0.15
        if num:
            self.rect(hx, y + 0.12, 0.36, 0.36, accent, shape=MSO_SHAPE.OVAL)
            self.text(hx, y + 0.12, 0.36, 0.36, str(num), 11, True, WHITE, "c", "m", name="num"); hx += 0.45
        self.text(hx, y + 0.1, x + w - hx - 0.08, 0.42, head, 11, True, DARK, anchor="m", name="cardhead", lsp=1.05)
        if body: self.text(x + 0.15, y + 0.55, w - 0.25, h - 0.6, body, size, False, GREY, name="cardbody", lsp=1.15)

    def card_height(self, w, body, size=9.5):
        return 0.6 + (self.measure(body, w - 0.25, size, False, 1.15) if body else 0)

    def metric(self, x, y, w, v, l):
        self.text(x, y, w, 0.5, v, 20 if len(v) < 10 else 16, True, TEAL, "c", "m", name="mval")
        self.text(x, y + 0.52, w, 0.55, l, 8.5, False, GREY, "c", name="mlbl", lsp=1.1)

    def notes(self, t):
        self.sd[0].notes_slide.notes_text_frame.text = t

    # ---------- save ----------
    def save(self, out, keep_contact=True):
        lst = self.prs.slides._sldIdLst
        first = list(lst)[0]; lst.remove(first)
        if keep_contact: lst.append(first)
        else: self.prs.part.drop_rel(first.rId)
        if self.preview_dir:
            os.makedirs(self.preview_dir, exist_ok=True)
            for i, (s, im, name) in enumerate(self.pages, 1): im.save(os.path.join(self.preview_dir, f"{i:02d}-{name}.png"))
        for i, sl in enumerate(self.prs.slides, 1):
            sl.part.partname = PackURI(f"/ppt/slides/slide{i}.xml")
            if sl.has_notes_slide: sl.notes_slide.part.partname = PackURI(f"/ppt/notesSlides/notesSlide{i}.xml")
        self.prs.save(out)
        return len(self.prs.slides), self.errors
