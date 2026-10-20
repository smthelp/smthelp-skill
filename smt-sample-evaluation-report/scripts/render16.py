#!/usr/bin/env python3
"""Render a slide spec (from make_spec.py) on a 16:9 Southern Machinery PPT template.

usage: render16.py <spec.json> <out.pptx> [--template assets/template/template.json] [--preview DIR]
template.json names the .pptx, the chrome layout index, the template slides to drop and to keep at
the end (keep slides are translated with spec["template_text"]), the safe area and colours.
Slide types: cover, cards (cols 1|2, numbered), steps, table, metrics, gallery, bullets, cta.
Exit code 1 when any text overflows or media is missing (shorten copy; never shrink fonts).
Needs smt-brand-kit/scripts/smdeck.py (sibling skill) for text/table/picture primitives."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SKILL = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.normpath(os.path.join(SKILL, "..", "smt-brand-kit", "scripts")))
import smdeck
from smdeck import Deck
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.opc.packuri import PackURI
from PIL import Image, ImageDraw
import io

args = sys.argv[1:]
prev = None; tcfg = os.path.join(SKILL, "assets", "template", "template.json")
if "--preview" in args: i = args.index("--preview"); prev = args[i + 1]; del args[i:i + 2]
if "--template" in args: i = args.index("--template"); tcfg = args[i + 1]; del args[i:i + 2]
if len(args) != 2: sys.exit(__doc__)
spec_path, out = args
spec = json.load(open(spec_path, encoding="utf-8"))
TC = json.load(open(tcfg, encoding="utf-8")); tpl = os.path.join(os.path.dirname(os.path.abspath(tcfg)), TC["file"])
sf, col = TC["safe"], TC["colors"]
smdeck.X0, smdeck.X1, smdeck.Y0, smdeck.Y1 = sf["x0"], sf["x1"], sf["y0"], sf["y1"]
X0, X1, Y1 = sf["x0"], sf["x1"], sf["y1"]
W = X1 - X0
NAVY, TEAL, GREEN, GOLD, GREY, LIGHT, PALE, WHITE = col["navy"], col["teal"], col["green"], col["gold"], col["grey"], col["light"], col["pale"], "FFFFFF"
smdeck.DARK, smdeck.TEAL, smdeck.GREY, smdeck.LIGHT = NAVY, TEAL, GREY, LIGHT
PT = spec.get("template_text", {})


class D16(Deck):
    def __init__(self, base, tpl, prev):
        self.base = base
        self.prs = Presentation(tpl)
        self.SW, self.SH = self.prs.slide_width / 914400, self.prs.slide_height / 914400
        lst = self.prs.slides._sldIdLst; ids = list(lst)
        self.keep = [ids[i] for i in TC["keep"]]
        for i in TC["drop"]: self.prs.part.drop_rel(ids[i].rId); lst.remove(ids[i])
        self.errors, self.pages, self.preview_dir = [], [], prev
        self._m = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        self.layout = self.prs.slide_layouts[TC["layout"]]
        self.logo = None
        for sh in self.layout.shapes:
            if sh.shape_type == 13:
                self.logo = (Image.open(io.BytesIO(sh.image.blob)).convert("RGB"), sh.left / 914400, sh.top / 914400, sh.width / 914400, sh.height / 914400)

    def new_slide(self, name):
        s = self.prs.slides.add_slide(self.layout)
        P = smdeck.DPI
        im = Image.new("RGB", (int(self.SW * P), int(self.SH * P)), "white"); d = ImageDraw.Draw(im, "RGBA")
        d.pieslice([int(10.26 * P), int(-3.07 * P), int(16.4 * P), int(3.07 * P)], 90, 180, fill=(0, 163, 180, 40))
        d.pieslice([int(-2.05 * P), int(5.45 * P), int(2.05 * P), int(9.55 * P)], 270, 360, fill=(152, 179, 65, 45))
        d.rectangle([0, int(0.64 * P), int(self.SW * P), int(0.75 * P)], fill="#E9EFD6"); d.rectangle([0, int(0.64 * P), int(2.83 * P), int(0.75 * P)], fill="#00A3B4")
        if self.logo:
            lg, lx, ly, lw, lh = self.logo; im.paste(lg.resize((int(lw * P), int(lh * P))), (int(lx * P), int(ly * P)))
        d.text((int(10.97 * P), int(6.98 * P)), "www.smthelp.com", fill="#6E747A")
        self.pages.append((s, im, name)); self.sd = (s, d, im)
        for ph in list(s.placeholders): ph._element.getparent().remove(ph._element)
        return self.sd

    def title(self, t, kicker=None):
        if kicker: self.text(*TC["kicker_box"], kicker.upper(), 12, True, TEAL, anchor="m", name="title")
        h = self.measure(t, 9.0, 24, True, 1.08)
        self.text(X0, 0.88, 9.0, h, t, 24, True, NAVY, lsp=1.08, name="title")
        if h > 0.95: self.errors.append(f"{self.pages[-1][2]}: title 3 lines")
        return 0.88 + h + 0.2

    def save(self, out):
        lst = self.prs.slides._sldIdLst
        for sid in self.keep: lst.remove(sid); lst.append(sid)
        if self.preview_dir:
            os.makedirs(self.preview_dir, exist_ok=True)
            for i, (s, im, name) in enumerate(self.pages, 1): im.save(os.path.join(self.preview_dir, f"{i:02d}-{name}.png"))
        for i, sl in enumerate(self.prs.slides, 1):
            sl.part.partname = PackURI(f"/ppt/slides/slide{i}.xml")
            if sl.has_notes_slide: sl.notes_slide.part.partname = PackURI(f"/ppt/notesSlides/notesSlide{i}.xml")
        self.prs.save(out)
        return len(self.prs.slides), self.errors


D = D16(os.path.dirname(os.path.abspath(spec_path)), tpl, prev)
KB = TC["kicker_box"]
ACC = [GREEN, TEAL]


def img(s, x, y, w, h):
    if not s.get("image"): return
    ch = 0.4 if s.get("caption") else 0
    D.pic(s["image"], x, y, w, h - ch, tuple(s.get("focus", (0.5, 0.5))))
    if ch: D.text(x, y + h - ch + 0.03, w, 0.36, s["caption"], 10, False, GREY, name="caption", lsp=1.05)


def lead(s, y, w=W, x=X0):
    if not s.get("lead"): return y
    h = D.measure(s["lead"], w, 14, False, 1.2); D.text(x, y, w, h, s["lead"], 14, False, GREY, lsp=1.2, name="lead")
    return y + h + 0.1


def metric(x, y, w, h, v, l):
    D.rect(x, y, w, h, LIGHT)
    D.text(x, y + 0.06, w, 0.55, v, 24 if len(v) < 9 else 19, True, TEAL, "c", "m", name="mval")
    D.text(x + 0.05, y + 0.62, w - 0.1, h - 0.66, l, 12, False, GREY, "c", name="mlbl", lsp=1.05)


def card(x, y, w, h, head, body, num=None, acc=GREEN, bs=12.5):
    D.rect(x, y, w, h, LIGHT); D.rect(x, y, 0.07, h, acc)
    hx = x + 0.2
    if num:
        D.rect(hx, y + 0.12, 0.4, 0.4, acc, shape=MSO_SHAPE.OVAL)
        D.text(hx, y + 0.12, 0.4, 0.4, str(num), 13, True, WHITE, "c", "m", name="num"); hx += 0.5
    D.text(hx, y + 0.1, x + w - hx - 0.1, 0.44, head, 14.5, True, NAVY, anchor="m", name="cardhead", lsp=1.05)
    if body: D.text(x + 0.2, y + 0.58, w - 0.32, h - 0.62, body, bs, False, GREY, name="cardbody", lsp=1.18)


def cardh(w, body, bs=12.5): return 0.66 + D.measure(body, w - 0.32, bs, False, 1.15)


def stack(items, x, y, w, ybot, numbered=False):
    hs = [cardh(w, c["b"]) for c in items]; gap = 0.14
    extra = max(0, (ybot - y - sum(hs) - gap * (len(hs) - 1)) / len(hs)); extra = min(extra, 0.35)
    for i, c in enumerate(items):
        h = hs[i] + extra; card(x, y, w, h, c["h"], c["b"], i + 1 if numbered else None, ACC[i % 2]); y += h + gap
    if y - gap > ybot + 0.01: D.errors.append(f"{D.pages[-1][2]}: cards overflow {y:.2f}")


for s in spec["slides"]:
    t = s["type"]; D.new_slide(t)
    if t == "cover":
        if s.get("kicker"): D.text(*KB, "SOUTHERN MACHINERY · SMART EMS", 12, True, TEAL, anchor="m", name="title")
        D.pic(s["image"], 6.75, 1.05, 6.05, 5.45, tuple(s.get("focus", (0.5, 0.5))))
        D.rect(6.75, 6.5, 6.05, 0.08, GREEN)
        y = 1.2
        D.text(X0, y, 5.9, 0.35, s["kicker"].upper(), 12, True, GREEN, name="kicker"); y += 0.45
        h = D.measure(s["title"], 5.9, 30, True, 1.06); D.text(X0, y, 5.9, h, s["title"], 30, True, NAVY, lsp=1.06, name="ctitle"); y += h + 0.1
        h = D.measure(s["subtitle"], 5.9, 15, False, 1.2); D.text(X0, y, 5.9, h, s["subtitle"], 15, False, TEAL, lsp=1.2, name="csub"); y += h + 0.25
        m = s["metrics"]; mw = (5.9 - 0.1 * (len(m) - 1)) / len(m)
        for i, mm in enumerate(m): metric(X0 + i * (mw + 0.1), max(y, 4.2), mw, 1.4, mm["v"], mm["l"])
    elif t == "cards":
        y = D.title(s["title"], s.get("kicker")); y = lead(s, y)
        if s.get("cols", 1) == 2:
            cs = s["cards"]; cw = (W - 0.25) / 2; rows = [cs[i:i + 2] for i in range(0, len(cs), 2)]
            rh = [max(cardh(cw, c["b"]) for c in r) for r in rows]; ex = min(0.3, max(0, (Y1 - y - sum(rh) - 0.15 * (len(rows) - 1)) / len(rows)))
            k = 0
            for r, h in zip(rows, rh):
                for j, c in enumerate(r):
                    k += 1; card(X0 + j * (cw + 0.25), y, cw, h + ex, c["h"], c["b"], k if s.get("numbered") else None, ACC[(k - 1) % 2])
                y += h + ex + 0.15
        else:
            stack(s["cards"], X0, y, 6.7, Y1, s.get("numbered")); img(s, 7.6, y, X1 - 7.6, Y1 - y)
    elif t == "steps":
        y = D.title(s["title"], s.get("kicker")); y = lead(s, y)
        stack(s["steps"], X0, y, 6.9, Y1, True); img(s, 7.8, y, X1 - 7.8, Y1 - y)
    elif t == "table":
        y = D.title(s["title"], s.get("kicker")); y = lead(s, y)
        nr = len(s["rows"]); rh = min(0.55, max(0.36, (Y1 - y - 0.7) / nr))
        y = D.table(X0, y, W, s["colw"], s["rows"], size=s.get("size", 14 if nr <= 9 else 13), rowh=rh) + 0.15
        if s.get("note"):
            h = D.measure(s["note"], W, 12, False, 1.15); D.text(X0, y, W, h, s["note"], 12, False, GREY, lsp=1.15, name="note")
            if y + h > Y1: D.errors.append(f"table note overflow {y+h:.2f}")
    elif t == "metrics":
        y = D.title(s["title"], s.get("kicker")); y = lead(s, y)
        m = s["metrics"]; per = 4; ww = 8.3 if s.get("image") else W
        mw = (ww - 0.15 * (per - 1)) / per; mh = 1.45
        for i, mm in enumerate(m): metric(X0 + (i % per) * (mw + 0.15), y + (i // per) * (mh + 0.15), mw, mh, mm["v"], mm["l"])
        yt = y + ((len(m) + per - 1) // per) * (mh + 0.15) + 0.1
        if s.get("text"):
            h = D.measure(s["text"], ww, 13.5, False, 1.2); D.text(X0, yt, ww, h, s["text"], 13.5, False, GREY, lsp=1.2, name="mtext")
            if yt + h > Y1: D.errors.append("metrics text overflow")
        if s.get("image"): img(s, X0 + ww + 0.3, y, X1 - X0 - ww - 0.3, Y1 - y)
    elif t == "gallery":
        y = D.title(s["title"], s.get("kicker")); ims = s["images"]; cols = 3 if len(ims) > 4 else len(ims); rows = (len(ims) + cols - 1) // cols
        gw = (W - 0.2 * (cols - 1)) / cols; gh = (Y1 - y - 0.15 * (rows - 1)) / rows
        for i, g in enumerate(ims):
            x = X0 + (i % cols) * (gw + 0.2); yy = y + (i // cols) * (gh + 0.15)
            D.pic(g["src"], x, yy, gw, gh - 0.36); D.text(x, yy + gh - 0.34, gw, 0.32, g["cap"], 10.5, False, GREY, name="caption")
    elif t == "bullets":
        y = D.title(s["title"], s.get("kicker")); y = lead(s, y)
        bw = 7.4; h = D.measure(s["bullets"], bw, 14.5, False, 1.25, True)
        D.text(X0, y, bw, h, s["bullets"], 14.5, False, NAVY, lsp=1.25, name="bullets", bullets=True)
        if y + h > Y1: D.errors.append("bullets overflow")
        img(s, X0 + bw + 0.35, y, X1 - X0 - bw - 0.35, Y1 - y)
    elif t == "cta":
        y = D.title(s["title"], s.get("kicker")) + 0.1
        fs = s["facts"]; cw = (W - 0.25 * (len(fs) - 1)) / len(fs); h = max(cardh(cw, f["b"], 13.5) for f in fs) + 0.2
        for i, f in enumerate(fs): card(X0 + i * (cw + 0.25), y, cw, h, f["h"], f["b"], i + 1, ACC[i % 2], 13.5)
        y += h + 0.4
        D.rect(X0 + 2.4, y, W - 2.4, 0.7, NAVY); D.text(X0 + 2.4, y, W - 2.4, 0.7, s["text"], 16, True, WHITE, "c", "m", name="ctabar")
    if s.get("notes"): D.notes(s["notes"])

if PT:
    for sid in D.keep:
        sl = D.prs.slides.get(int(sid.get("id")))
        for sh in sl.shapes:
            frames = [sh] if sh.has_text_frame else ([c for c in sh.shapes if c.has_text_frame] if sh.shape_type == 6 else [])
            for f in frames:
                for p in f.text_frame.paragraphs:
                    full = "".join(r.text for r in p.runs).strip()
                    key = next((k for k in PT if k.replace(" ", "") == full.replace(" ", "")), None)
                    if key and p.runs:
                        p.runs[0].text = PT[key]
                        for r in p.runs[1:]: r.text = ""
                    else:
                        for r in p.runs:
                            k = r.text.strip()
                            if k in PT: r.text = r.text.replace(k, PT[k])

n, errs = D.save(out)
print("slides", n, "errors", len(errs)); [print(" ", e) for e in errs]
sys.exit(1 if errs else 0)
