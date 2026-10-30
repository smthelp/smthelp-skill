#!/usr/bin/env python3
"""Render a deck spec (JSON) to a Southern Machinery A4 PPTX.
Same renderer for the marketing deck (deck.json) and the operation manual (manual.json).

usage: make_deck.py <spec.json> <out.pptx> [--preview DIR]
Media paths in the spec are relative to the spec file's folder (the kit dir).

Slide types (field "type"):
  cover      kicker, title, subtitle, image, metrics[{v,l}] (<=4), tagline
  section    kicker, title, text, items[], image        (chapter opener; manual chapters)
  toc        title, items[str]                          (auto-filled from section titles when items omitted)
  bullets    kicker, title, lead, bullets[], image, caption, layout "right"|"bottom"
  cards      kicker, title, lead, cards[{h,b}], cols 1|2, numbered, image, caption
  steps      kicker, title, lead, steps[{h,b}], image, caption   (numbered vertical steps + side photo)
  metrics    kicker, title, lead, metrics[{v,l}] (<=8), text, image, caption
  table      kicker, title, lead, colw[], rows[[...]] (row 0 = header), note, size
  gallery    kicker, title, images[{src,cap}] (2-6)
  warning    kicker, title, lead, cards[{h,b}], banner      (safety pages)
  cta        kicker, title, facts[{h,b}], text            (closing; contact slide follows from the template)
Every slide may carry "notes" (sources) and "focus" [x,y] for cover-cropping its image.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smdeck import Deck, X0, X1, Y0, Y1, W, DARK, GREEN, TEAL, GREY, LIGHT, WHITE, BRAND

args = sys.argv[1:]
prev = None
if "--preview" in args:
    i = args.index("--preview"); prev = args[i + 1]; del args[i:i + 2]
spec_path, out = args[0], args[1]
spec = json.load(open(spec_path, encoding="utf-8"))
D = Deck(os.path.dirname(os.path.abspath(spec_path)), spec.get("template"), prev)
ACC = [GREEN, TEAL]


def img_block(s, x, y, w, h):
    if s.get("image"):
        ch = 0.45 if s.get("caption") else 0
        D.pic(s["image"], x, y, w, h - ch, tuple(s.get("focus", (0.5, 0.5))), s.get("fit", "cover"))
        if ch: D.caption(x, y + h - ch + 0.02, w, s["caption"])


def lead(s, y, w=W, x=X0, size=11.5):
    if not s.get("lead"): return y
    h = D.measure(s["lead"], w, size, False, 1.25)
    D.text(x, y, w, h, s["lead"], size, False, GREY, lsp=1.25, name="lead")
    return y + h + 0.12


def cover(s):
    if s.get("image"): D.pic(s["image"], 0, 1.25, D.SW, 5.2, tuple(s.get("focus", (0.5, 0.5))))
    D.rect(0, 6.45, D.SW, 0.08, GREEN)
    y = 6.75
    if s.get("kicker"): D.text(X0, y, W, 0.35, s["kicker"].upper(), 11, True, GREEN, name="kicker"); y += 0.4
    h = D.measure(s["title"], W, 26, True, 1.08); D.text(X0, y, W, h, s["title"], 26, True, DARK, lsp=1.08, name="ctitle"); y += h + 0.05
    if s.get("subtitle"):
        h = D.measure(s["subtitle"], W, 14, False, 1.2); D.text(X0, y, W, h, s["subtitle"], 14, False, TEAL, lsp=1.2, name="csub"); y += h + 0.2
    m = s.get("metrics", [])[:4]
    if m:
        mw = W / len(m)
        D.rect(X0, y, W, 1.2, LIGHT)
        for i, it in enumerate(m): D.metric(X0 + i * mw, y + 0.06, mw, it["v"], it["l"])
        y += 1.35
    D.text(X0, max(y, Y1 - 0.45), W, 0.4, s.get("tagline", BRAND["short"] + " - " + BRAND["tagline"]), 9.5, False, GREY, name="tagline")


def section(s):
    D.title(s["title"], s.get("kicker"))
    D.rect(X0, Y0, W, 2.6, DARK); D.rect(X0, Y0 + 2.6, W, 0.08, GREEN)
    if s.get("kicker"): D.text(X0 + 0.35, Y0 + 0.3, W - 0.7, 0.45, s["kicker"].upper(), 14, True, GREEN, name="skick")
    D.text(X0 + 0.35, Y0 + 0.8, W - 0.7, 1.6, s["title"], 28, True, WHITE, anchor="m", lsp=1.1, name="stitle")
    y = Y0 + 2.95
    if s.get("text"):
        h = D.measure(s["text"], W, 13, False, 1.3); D.text(X0, y, W, h, s["text"], 13, False, GREY, lsp=1.3); y += h + 0.2
    if s.get("items"):
        h = D.measure(s["items"], W, 12, False, 1.25, True); D.text(X0, y, W, h, s["items"], 12, False, DARK, lsp=1.25, bullets=True, name="sitems"); y += h + 0.2
    if s.get("image") and Y1 - y > 1.5: img_block(s, X0, y, W, Y1 - y)


def toc(s, all_slides):
    D.title(s.get("title", "Contents"), s.get("kicker"))
    items = s.get("items") or [x["title"] for x in all_slides if x.get("type") == "section"]
    rows = [[f"{i:02d}", t] for i, t in enumerate(items, 1)]
    y = Y0 + 0.1
    for i, (n, t) in enumerate(rows):
        D.rect(X0, y, 0.6, 0.5, ACC[i % 2]); D.text(X0, y, 0.6, 0.5, n, 13, True, WHITE, "c", "m", name="tocn")
        D.text(X0 + 0.75, y, W - 0.75, 0.5, t, 12.5, True, DARK, anchor="m", name="toct"); y += 0.62
    if y > Y1: D.errors.append("toc overflow")


def bullets(s):
    D.title(s["title"], s.get("kicker")); y = lead(s, Y0)
    side = s.get("image") and s.get("layout", "right") == "right"
    bw = W * 0.55 if side else W
    h = D.measure(s["bullets"], bw, 11.5, False, 1.2, True)
    D.text(X0, y, bw, h, s["bullets"], 11.5, False, DARK, lsp=1.2, bullets=True, name="bullets")
    if side: img_block(s, X0 + W * 0.58, y, W * 0.42, min(Y1 - y, max(h, 4.5)))
    elif s.get("image"): img_block(s, X0, y + h + 0.2, W, Y1 - y - h - 0.2)


def cards(s, warn=False):
    D.title(s["title"], s.get("kicker")); y = lead(s, Y0)
    cols = s.get("cols", 2 if len(s["cards"]) > 3 else 1)
    cw = (W - 0.1 * (cols - 1)) / cols
    rows = [s["cards"][i:i + cols] for i in range(0, len(s["cards"]), cols)]
    k = 0
    for r in rows:
        h = max(D.card_height(cw, c.get("b", "")) for c in r)
        for j, c in enumerate(r):
            D.card(X0 + j * (cw + 0.1), y, cw, h, c["h"], c.get("b", ""), (k + 1) if s.get("numbered") else None, ACC[k % 2]); k += 1
        y += h + 0.12
    if warn and s.get("banner"):
        h = D.measure(s["banner"], W - 0.5, 13, True, 1.2) + 0.2
        D.rect(X0, y + 0.05, W, h, DARK); D.text(X0 + 0.25, y + 0.05, W - 0.5, h, s["banner"], 13, True, WHITE, "c", "m", lsp=1.2, name="banner"); y += h + 0.2
    if s.get("image") and Y1 - y > 1.5: img_block(s, X0, y + 0.05, W, Y1 - y - 0.05)
    if y > Y1 + 0.01: D.errors.append(f"{D.pages[-1][2]}: cards overflow")


def steps(s):
    D.title(s["title"], s.get("kicker")); y = lead(s, Y0)
    sw = W * 0.6 if s.get("image") else W; y0 = y
    for i, st in enumerate(s["steps"]):
        h = D.card_height(sw, st.get("b", ""), 9.5)
        D.card(X0, y, sw, h, st["h"], st.get("b", ""), i + 1, ACC[i % 2]); y += h + 0.1
    if s.get("image"): img_block(s, X0 + W * 0.63, y0, W * 0.37, min(Y1 - y0, max(y - y0, 4)))
    if y > Y1 + 0.01: D.errors.append(f"{D.pages[-1][2]}: steps overflow")


def metrics(s):
    D.title(s["title"], s.get("kicker")); y = lead(s, Y0)
    m = s["metrics"][:8]; per = 4 if len(m) > 4 else len(m); mw = W / per
    for i, it in enumerate(m):
        r, c = divmod(i, per)
        D.rect(X0 + c * mw + 0.04, y + r * 1.3, mw - 0.08, 1.2, LIGHT)
        D.metric(X0 + c * mw + 0.04, y + r * 1.3 + 0.05, mw - 0.08, it["v"], it["l"])
    y += 1.3 * ((len(m) + per - 1) // per) + 0.15
    if s.get("text"):
        h = D.measure(s["text"], W, 11, False, 1.25); D.text(X0, y, W, h, s["text"], 11, False, GREY, lsp=1.25); y += h + 0.15
    if s.get("image"): img_block(s, X0, y, W, Y1 - y)


def table(s):
    D.title(s["title"], s.get("kicker")); y = lead(s, Y0)
    rows = s["rows"]; colw = s.get("colw") or [1 / len(rows[0])] * len(rows[0])
    y = D.table(X0, y, W, colw, rows, s.get("size", 9.5)) + 0.12
    if s.get("note"):
        h = D.measure(s["note"], W, 9, False, 1.2); D.text(X0, y, W, h, s["note"], 9, False, GREY, lsp=1.2, name="note"); y += h + 0.1
    if s.get("image") and Y1 - y > 1.5: img_block(s, X0, y, W, Y1 - y)


def gallery(s):
    D.title(s["title"], s.get("kicker")); y = lead(s, Y0)
    ims = s["images"][:6]; cols = 2; rows = (len(ims) + 1) // 2
    cw = (W - 0.15) / 2; ch = (Y1 - y - 0.1 * (rows - 1)) / rows
    for i, it in enumerate(ims):
        r, c = divmod(i, cols); x, yy = X0 + c * (cw + 0.15), y + r * (ch + 0.1)
        D.pic(it["src"], x, yy, cw, ch - 0.45, tuple(it.get("focus", (0.5, 0.5))), it.get("fit", "cover"))
        D.caption(x, yy + ch - 0.42, cw, it.get("cap", ""))


def cta(s):
    D.title(s["title"], s.get("kicker")); y = lead(s, Y0)
    for i, f in enumerate(s.get("facts", [])):
        h = D.card_height(W, f.get("b", ""), 10)
        D.card(X0, y, W, h, f["h"], f.get("b", ""), i + 1, ACC[i % 2], 10); y += h + 0.1
    t = s.get("text", f"Send these facts to {BRAND['email']} or WhatsApp {BRAND['whatsapp']}. Price, lead time and warranty are quoted per order.")
    h = D.measure(t, W - 0.5, 12, True, 1.25) + 0.25
    D.rect(X0, y + 0.1, W, h, DARK); D.text(X0 + 0.25, y + 0.1, W - 0.5, h, t, 12, True, WHITE, "c", "m", lsp=1.25, name="ctabox")
    y += h + 0.3
    if s.get("image") and Y1 - y > 1.5: img_block(s, X0, y, W, Y1 - y)


slides = spec["slides"]
for i, s in enumerate(slides, 1):
    D.new_slide(f"{s['type']}")
    t = s["type"]
    if t == "cover": cover(s)
    elif t == "section": section(s)
    elif t == "toc": toc(s, slides)
    elif t == "bullets": bullets(s)
    elif t == "cards": cards(s)
    elif t == "warning": cards(s, warn=True)
    elif t == "steps": steps(s)
    elif t == "metrics": metrics(s)
    elif t == "table": table(s)
    elif t == "gallery": gallery(s)
    elif t == "cta": cta(s)
    else: D.errors.append(f"slide {i}: unknown type {t}")
    if s.get("notes"): D.notes(s["notes"])

n, errs = D.save(out, spec.get("contact_slide", True))
print("slides", n, "errors", len(errs))
for e in errs: print("  ", e)
sys.exit(1 if errs else 0)
