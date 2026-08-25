#!/usr/bin/env python3
"""Step 2 — Build ordered, normalized slides_sel/slide-NN.png.

From the page screenshots + downloaded key images, produce a clean set of
1920x1080 (or --w/--h) frames, zero-padded and ordered to match
narration.json. Uses cover-crop (no distortion) so portrait product
shots fill the 16:9 frame.

Usage:
  python3 normalize.py --base . --manifest frames.json
  python3 normalize.py --base . --manifest frames.json --w 1080 --h 1920

frames.json format (order = final video order):
  [
    {"label":"home",  "kind":"shot", "file":"slide-home.png"},
    {"label":"prod1", "kind":"img",  "file":"ab12cd-3f9a1b2c3.jpg"},
    {"label":"about", "kind":"shot", "file":"slide-about.png"}
  ]
"kind":"shot" -> <base>/slides/ ; "kind":"img" -> <base>/assets/
"""
import os, json, argparse
from PIL import Image

def cover_resize(im, target):
    """Resize to cover target box, crop center, no distortion."""
    im = im.convert("RGB")
    tw, th = target
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(round(sw * scale)), int(round(sh * scale))
    im = im.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return im.crop((left, top, left + tw, top + th))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".")
    ap.add_argument("--manifest", required=True, help="JSON: [{label,kind,file}]")
    ap.add_argument("--shots-dir", default="slides")
    ap.add_argument("--assets-dir", default="assets")
    ap.add_argument("--out", default="slides_sel")
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    args = ap.parse_args()

    BASE = os.path.abspath(args.base)
    SD = os.path.join(BASE, args.shots_dir)
    AD = os.path.join(BASE, args.assets_dir)
    OUT = os.path.join(BASE, args.out)
    os.makedirs(OUT, exist_ok=True)

    items = json.load(open(args.manifest, encoding="utf-8"))
    T = (args.w, args.h)
    n = 0
    for it in items:
        n += 1
        src = os.path.join(SD if it["kind"] == "shot" else AD, it["file"])
        im = Image.open(src)
        out_im = cover_resize(im, T)
        dst = os.path.join(OUT, f"slide-{n:02d}.png")
        out_im.save(dst)
        print(f"slide-{n:02d}.png  <- {it['label']} ({it['file']}) {im.size}->{T}")
    print(f"\nTOTAL {n} slides in {OUT}")

if __name__ == "__main__":
    main()
