#!/usr/bin/env python3
"""Curation aid for the Doc->Promo pipeline (Step 1.5).

When the source PDF/PPTX is image-heavy (only some pages carry text), the model
cannot eyeball the rendered PNGs. This script profiles every slide-NN.png and
emits a data-driven view to help pick a ~N-slide curated set:

  - detail  : grayscale std (photos/diagrams high, blank/flat low)
  - color%  : fraction of pixels with saturation > 0.18 (finds real photos)
  - hue     : dominant hue of saturated pixels (brand teal/green detection)
  - blank   : True if near-uniform (detail very low)
  - dup_of  : near-duplicate page(s) via perceptual hash (dhash, delta <= 12)

It also lists the most "visually interesting" non-blank, non-duplicate pages
(ranked by detail * (1 + color%/100)) so you can fill remaining slots with real
machine/line photos after locking in the narrative (text) pages.

Usage:
    python3 profile_slides.py slides_1080
    python3 profile_slides.py slides_1080 --keep 13
"""
import argparse, glob, os, warnings
from PIL import Image

# Pillow 14 deprecates Image.getdata(); keep output clean until then.
warnings.filterwarnings("ignore", category=DeprecationWarning)


def page_of(path):
    return int("".join(ch for ch in os.path.basename(path) if ch.isdigit()))


def dhash(img, size=16):
    img = img.convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(img.getdata())
    w = size + 1
    bits = []
    for y in range(size):
        for x in range(size):
            bits.append(1 if px[y * w + x] < px[y * w + x + 1] else 0)
    return "".join(map(str, bits))


def detail_std(img, w=120, h=68):
    im = img.convert("L").resize((w, h))
    px = list(im.getdata())
    m = sum(px) / len(px)
    return (sum((x - m) ** 2 for x in px) / len(px)) ** 0.5


def color_profile(img, small=(160, 90)):
    im = img.convert("RGB").resize(small)
    px = list(im.getdata())
    sat = 0
    hues = []
    for r, g, b in px:
        mx = max(r, g, b)
        mn = min(r, g, b)
        s = 0 if mx == 0 else (mx - mn) / mx
        if s > 0.18:
            sat += 1
            rr, gg, bb = [x / 255 for x in (r, g, b)]
            mx2 = max(rr, gg, bb)
            mn2 = min(rr, gg, bb)
            dd = mx2 - mn2
            if dd == 0:
                h = 0
            elif mx2 == rr:
                h = ((gg - bb) / dd) % 6
            elif mx2 == gg:
                h = (bb - rr) / dd + 2
            else:
                h = (rr - gg) / dd + 4
            hues.append(h * 60)
    return 100 * sat / len(px), (sum(hues) / len(hues) if hues else -1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides", help="directory of slide-NN.png")
    ap.add_argument("--keep", type=int, default=13,
                    help="how many photo slots to suggest filling")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.slides, "slide-*.png")),
                   key=page_of)
    if not files:
        sys.exit("No slide-*.png found in " + args.slides)

    rows = []
    for f in files:
        im = Image.open(f).convert("RGB")
        d = detail_std(im)
        cp, hue = color_profile(im)
        rows.append(dict(page=page_of(f),
                         file=os.path.basename(f),
                         detail=round(d, 1),
                         color_pct=round(cp, 1),
                         hue=round(hue, 1),
                         blank=d < 8,
                         hash=dhash(im)))

    # near-duplicate detection
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            dd = sum(a != b for a, b in zip(rows[i]["hash"], rows[j]["hash"]))
            if dd <= 12:
                rows[i].setdefault("dup_of", []).append(rows[j]["file"])
                rows[j].setdefault("dup_of", []).append(rows[i]["file"])

    print(f"{'page':>4} {'file':<14} {'detail':>7} {'color%':>7} {'hue':>7} {'blank':>5} dups")
    for r in rows:
        dups = ",".join(r.get("dup_of", []))[:30]
        print(f"{r['page']:>4} {r['file']:<14} {r['detail']:>7} {r['color_pct']:>7} {r['hue']:>7} {str(r['blank']):>5} {dups}")

    # Photo candidates: non-blank, non-duplicate, ranked by visual interest
    candidates = [r for r in rows if not r["blank"] and "dup_of" not in r]
    candidates.sort(key=lambda r: r["detail"] * (1 + r["color_pct"] / 100),
                    reverse=True)
    top = candidates[:args.keep]
    print(f"\nTop {args.keep} photo candidates (high detail + color, non-dup):")
    print("  " + " ".join(f"{c['page']:02d}" for c in top))
    print("\nCuration recipe: keep ALL narrative/text pages + fill remaining")
    print("slots from the photo candidates above. Then copy into slides_sel/:")
    print("  cp slides_1080/slide-PP.png slides_sel/slide-NN.png")


if __name__ == "__main__":
    import sys
    main()
