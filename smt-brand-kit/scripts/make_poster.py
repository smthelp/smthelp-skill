#!/usr/bin/env python3
"""Southern Machinery product poster from poster.json -> PNG (+ PDF for print sizes).

usage: make_poster.py <poster.json> <out_basename>   (writes <out>-<format>.png/.pdf for every format listed)
poster.json:
 {"formats": ["a3", "social", "story"],          a3/a4 = print 300 dpi, social = 1080x1350, story = 1080x1920
  "product_label": "Smart EMS X3100 X-ray Counter",
  "kicker": "SMART EMS WAREHOUSE", "headline": "Count 4 reels\\nin one X-ray shot", "sub": "...",
  "image": "photos/hero.jpg", "focus": [0.5, 0.5],
  "metrics": [{"v": "6 - 10 s", "l": "per 4 reels"}],        up to 4
  "benefits": ["...", "..."],                                up to 4, one line each
  "cta": "Send your reel mix for a trial count", "qr": "https://..."(optional), "footnote": "evidence note"}
Paths are relative to the json's folder. Fails (exit 1) when a text block does not fit."""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
BD = os.path.normpath(os.path.join(HERE, "..", "assets", "brand"))
BRAND = json.load(open(os.path.join(BD, "brand.json"), encoding="utf-8"))
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
C = {k: rgb(v) for k, v in BRAND["colors"].items()}
SIZES = {"a3": (3508, 4961), "a4": (2480, 3508), "social": (1080, 1350), "story": (1080, 1920)}
errors = []


def F(w, s): return ImageFont.truetype(os.path.join(BD, "fonts", f"Montserrat-{w}.ttf"), max(8, int(s)))


def cover(img, w, h, fx=0.5, fy=0.5):
    s = max(w / img.width, h / img.height); img = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    l = int((img.width - w) * fx); t = int((img.height - h) * fy); return img.crop((l, t, l + w, t + h))


def fit_lines(d, text, font_w, size, maxw, minsize):
    lines = text.split("\n"); f = F(font_w, size)
    while any(d.textlength(l, font=f) > maxw for l in lines) and f.size > minsize: f = F(font_w, f.size - 2)
    if any(d.textlength(l, font=f) > maxw for l in lines): errors.append(f"too wide: {text[:40]}")
    return lines, f


def wrap(d, text, f, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur: cur = t
        else: out.append(cur); cur = w
    return out + [cur]


def render(p, base, fmt):
    W, H = SIZES[fmt]; u = W / 1080.0; tall = H / W > 1.6
    im = Image.new("RGB", (W, H), C["navy_deep"])
    g = Image.linear_gradient("L").rotate(-35, expand=True).resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), C["navy_mid"]), im, g)
    cir = Image.open(os.path.join(BD, "circuit.png")).convert("RGBA")
    cir = cir.resize((int(cir.width * 2.6 * u), int(cir.height * 2.6 * u)))
    cir.putalpha(cir.split()[3].point(lambda v: int(v * 0.15)))
    im.paste(cir, (W - cir.width + int(40 * u), int(250 * u)), cir)
    d = ImageDraw.Draw(im)
    M = int(64 * u)
    # header: logo card + product label
    d.rounded_rectangle((M, M, M + int(330 * u), M + int(96 * u)), int(14 * u), fill=C["white"])
    lg = Image.open(os.path.join(BD, "sm-logo.png")).convert("RGBA"); lw = int(296 * u)
    lg = lg.resize((lw, int(lw * lg.height / lg.width)), Image.LANCZOS)
    im.paste(lg, (M + int(17 * u), M + (int(96 * u) - lg.height) // 2), lg)
    pl = p.get("product_label", "")
    if pl:
        f = F("SemiBold", 22 * u)
        while d.textlength(pl, font=f) > W - 2 * M - 360 * u and f.size > 10: f = F("SemiBold", f.size - 1)
        x = W - M - d.textlength(pl, font=f); d.text((x, M + 30 * u), pl, font=f, fill=C["muted"])
        d.rectangle((x, M + 64 * u, W - M, M + 68 * u), fill=C["green"])
    y = M + int(150 * u)
    d.text((M, y), p.get("kicker", "").upper(), font=F("Bold", 30 * u), fill=C["green"]); y += int(52 * u)
    lines, fh = fit_lines(d, p["headline"], "ExtraBold", (92 if H / W >= 1.4 else 80) * u, W - 2 * M, 50 * u)
    for l in lines: d.text((M, y), l, font=fh, fill=C["white"]); y += int(fh.size * 1.12)
    if p.get("sub"):
        y += int(14 * u); fs = F("SemiBold", 32 * u)
        for l in wrap(d, p["sub"], fs, W - 2 * M): d.text((M, y), l, font=fs, fill=C["muted"]); y += int(fs.size * 1.35)
    y += int(30 * u)
    # footer height
    foot_h = int(170 * u)
    met = p.get("metrics", [])[:4]; ben = p.get("benefits", [])[:4] if H / W >= 1.4 else []   # 4:5 social drops benefits
    met_h = int(170 * u) if met else 0
    fb = F("SemiBold", 31 * u); ben_h = len(ben) * int(fb.size * 1.7) + (int(20 * u) if ben else 0)
    img_h = H - foot_h - y - met_h - ben_h - int(90 * u)
    if tall: img_h = int(img_h * 0.95)
    if img_h < 300 * u: errors.append(f"{fmt}: too much text, image area {img_h}px")
    if p.get("image") and img_h > 100:
        bx, by, bw, bh = M, y, W - 2 * M, img_h
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((bx + 10 * u, by + 18 * u, bx + bw + 10 * u, by + bh + 18 * u), int(30 * u), fill=(0, 0, 0, 130))
        sh = sh.filter(ImageFilter.GaussianBlur(18 * u)); im.paste(sh, (0, 0), sh)
        d.rounded_rectangle((bx - 7 * u, by - 7 * u, bx + bw + 7 * u, by + bh + 7 * u), int(32 * u), fill=C["green"])
        src = Image.open(os.path.join(base, p["image"])).convert("RGB")
        fx, fy = p.get("focus", [0.5, 0.5]); ph = cover(src, bw, bh, fx, fy)
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, bh - 1), int(26 * u), fill=255)
        im.paste(ph, (bx, by), m)
        y = by + bh + int(40 * u)
    if met:
        n = len(met); gap = int(18 * u); tw = (W - 2 * M - gap * (n - 1)) // n
        for i, it in enumerate(met):
            x = M + i * (tw + gap)
            d.rounded_rectangle((x, y, x + tw, y + met_h - int(20 * u)), int(18 * u), fill=C["white"])
            d.rectangle((x, y + 24 * u, x + 7 * u, y + met_h - 44 * u), fill=C["green"] if i % 2 == 0 else C["teal"])
            fv = F("ExtraBold", 50 * u)
            while d.textlength(it["v"], font=fv) > tw - 40 * u and fv.size > 14: fv = F("ExtraBold", fv.size - 2)
            d.text((x + 26 * u, y + 24 * u), it["v"], font=fv, fill=C["navy"])
            fl = F("SemiBold", 21 * u); ll = wrap(d, it["l"], fl, tw - 40 * u)
            if len(ll) > 2: errors.append(f"metric label too long: {it['l']}")
            yy = y + 92 * u
            for l in ll[:2]: d.text((x + 26 * u, yy), l, font=fl, fill=C["grey"]); yy += fl.size * 1.2
        y += met_h + int(10 * u)
    for b in ben:
        d.ellipse((M, y + 10 * u, M + 24 * u, y + 34 * u), fill=C["green"])
        if d.textlength(b, font=fb) > W - 2 * M - 46 * u: errors.append(f"benefit too long: {b}")
        d.text((M + 46 * u, y), b, font=fb, fill=(230, 240, 244)); y += int(fb.size * 1.7)
    # footer band
    fy0 = H - foot_h
    d.rectangle((0, fy0, W, H), fill=C["white"]); d.rectangle((0, fy0, W, fy0 + 8 * u), fill=C["green"])
    qr_w = 0
    if p.get("qr"):
        try:
            import qrcode
            q = qrcode.make(p["qr"], border=1).convert("RGB"); qs = int(foot_h - 40 * u)
            im.paste(q.resize((qs, qs)), (W - M - qs, fy0 + int(24 * u))); qr_w = qs + int(24 * u)
        except Exception as e:
            errors.append(f"qr skipped: {e}")
    fc = F("ExtraBold", 34 * u)
    cta = p.get("cta", BRAND["closing_line"])
    if d.textlength(cta, font=fc) > W - 2 * M - qr_w:
        fc = F("ExtraBold", 28 * u)
        if d.textlength(cta, font=fc) > W - 2 * M - qr_w: errors.append("cta too long")
    d.text((M, fy0 + 30 * u), cta, font=fc, fill=C["navy"])
    contact = f"{BRAND['web']}   ·   {BRAND['email']}   ·   WhatsApp {BRAND['whatsapp']}"
    fcn = F("SemiBold", 25 * u)
    while d.textlength(contact, font=fcn) > W - 2 * M - qr_w and fcn.size > 10: fcn = F("SemiBold", fcn.size - 1)
    d.text((M, fy0 + 86 * u), contact, font=fcn, fill=C["teal"])
    if p.get("footnote"):
        fn = F("Regular", 16 * u); d.text((M, fy0 + 128 * u), p["footnote"], font=fn, fill=C["grey"])
    return im


def main():
    spec, out = sys.argv[1], sys.argv[2]
    p = json.load(open(spec, encoding="utf-8")); base = os.path.dirname(os.path.abspath(spec))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    for fmt in p.get("formats", ["a3", "social"]):
        im = render(p, base, fmt)
        im.save(f"{out}-{fmt}.png", optimize=True)
        if fmt in ("a3", "a4"): im.save(f"{out}-{fmt}.pdf", resolution=300)
        print("wrote", f"{out}-{fmt}.png", im.size)
    for e in errors: print("  ERROR", e)
    sys.exit(1 if [e for e in errors if not e.startswith("qr skipped")] else 0)


if __name__ == "__main__":
    main()
