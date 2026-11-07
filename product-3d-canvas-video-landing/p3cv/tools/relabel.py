"""Replace the model name printed on a machine label in a real photo (e.g. "S7020T" -> "S7040P").

Used when a new model/variant shares the body of an existing machine and only the badge differs.
The text box is painted with the label's own background (85th-percentile colour of the box, blended
with the columns either side so gradients survive) and the new text is drawn bold, stretched to the
old text's box, in the old text's colour, with a light blur to match the photo's softness.

    python -m p3cv relabel IN.jpg --bbox 592,556,683,578 --text S7040P [--out OUT.jpg] [--color 3c5fa0] [--blur 0.5]

--bbox is the tight box of the OLD text (x0,y0,x1,y1, inclusive). Find it by cropping/zooming the photo.
Always look at the result at 300% before using it, and say in the deliverable notes that the badge
was edited.
"""
import argparse
from pathlib import Path

FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
         "C:/Windows/Fonts/arialbd.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]


def _font(path=None):
    for f in ([path] if path else []) + FONTS:
        if f and Path(f).exists():
            return f
    return None


def relabel(src, dst, bbox, text, color=None, pad=3, blur=0.5, font=None):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    im = Image.open(src).convert("RGB"); W, H = im.size; px = im.load()
    x0, y0, x1, y1 = bbox
    X0, Y0, X1, Y1 = max(1, x0 - pad), max(0, y0 - pad), min(W - 2, x1 + pad), min(H - 1, y1 + pad)
    box = [px[x, y] for y in range(Y0, Y1 + 1) for x in range(X0, X1 + 1)]
    lum = sorted(box, key=sum)
    bg = tuple(sorted(c[i] for c in box)[int(len(box) * 0.85)] for i in range(3))  # per-channel 85th pct
    if color is None:  # darkest 8 % of the box = the old text
        dark = lum[:max(1, len(lum) // 12)]
        color = tuple(sum(c[i] for c in dark) // len(dark) for i in range(3))
    for y in range(Y0, Y1 + 1):
        L, R = px[X0 - 1, y], px[X1 + 1, y]
        for x in range(X0, X1 + 1):
            t = (x - X0) / max(1, X1 - X0)
            px[x, y] = tuple(int(0.75 * bg[i] + 0.25 * (L[i] * (1 - t) + R[i] * t)) for i in range(3))
    w, h = x1 - x0 + 1, y1 - y0 + 1; S = 4
    fp = _font(font)
    fnt = ImageFont.truetype(fp, int(h * S * 1.36)) if fp else ImageFont.load_default()
    tb = fnt.getbbox(text)
    layer = Image.new("L", (tb[2] - tb[0] + 4, tb[3] - tb[1] + 4), 0)
    ImageDraw.Draw(layer).text((2 - tb[0], 2 - tb[1]), text, font=fnt, fill=255)
    layer = layer.resize((w, h), Image.LANCZOS)
    if blur:
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.new("RGB", (w, h), tuple(color)), (x0, y0), layer)
    im.save(dst, quality=93)
    return {"out": str(dst), "bbox": list(bbox), "text": text, "color": "#%02x%02x%02x" % tuple(color), "bg": "#%02x%02x%02x" % tuple(bg)}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="p3cv relabel")
    ap.add_argument("image"); ap.add_argument("--bbox", required=True); ap.add_argument("--text", required=True)
    ap.add_argument("--out"); ap.add_argument("--color"); ap.add_argument("--pad", type=int, default=3)
    ap.add_argument("--blur", type=float, default=0.5); ap.add_argument("--font")
    a = ap.parse_args(argv)
    bb = tuple(int(v) for v in a.bbox.split(","))
    col = tuple(int(a.color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) if a.color else None
    print(relabel(a.image, a.out or a.image, bb, a.text, col, a.pad, a.blur, a.font))


if __name__ == "__main__":
    main()
