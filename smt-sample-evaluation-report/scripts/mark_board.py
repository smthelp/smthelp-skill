#!/usr/bin/env python3
"""Draw component markers on a PCB/panel photo: circles = process A (e.g. radial), boxes = process B (odd-form/axial).

usage: mark_board.py <photo> <markers.json|-> <out.jpg>
markers: [{"type": "radial"|"oddform"|"axial", "x": 0-1, "y": 0-1, "w": 0-1, "h": 0-1}] (fractions of the photo).
Also used by make_spec.py for case boards[].markers. Colours: radial red circle, oddform blue box, axial amber box.
Tip: markers can be read from an old PPT where an engineer drew ellipses/rectangles over the photo
(shape position minus picture position, divided by picture size) - see references/input-spec.md."""
import json, sys
from PIL import Image, ImageDraw

STYLE = {"radial": ("ellipse", (230, 30, 30)), "oddform": ("rect", (0, 110, 230)), "axial": ("rect", (236, 160, 0))}


def mark(photo, markers, out, max_w=2000):
    im = Image.open(photo).convert("RGB")
    if im.width > max_w: im = im.resize((max_w, int(im.height * max_w / im.width)))
    W, H = im.size; d = ImageDraw.Draw(im); lw = max(3, W // 300)
    for m in markers:
        shape, col = STYLE.get(m["type"], ("rect", (0, 160, 0)))
        b = [m["x"] * W, m["y"] * H, (m["x"] + m["w"]) * W, (m["y"] + m["h"]) * H]
        (d.ellipse if shape == "ellipse" else d.rectangle)(b, outline=col, width=lw)
    im.save(out, quality=88)
    return out


if __name__ == "__main__":
    if len(sys.argv) != 4: sys.exit(__doc__)
    mk = json.load(sys.stdin if sys.argv[2] == "-" else open(sys.argv[2]))
    print(mark(sys.argv[1], mk, sys.argv[3]))
