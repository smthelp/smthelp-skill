#!/usr/bin/env python3
"""usage: sheet.py <deck_basename>  -> <base>_sheetN.png, 4 rendered slides per sheet for review."""
import glob, sys
from PIL import Image
b = sys.argv[1]; fs = sorted(glob.glob(b + "_p-*.png"))
for k in range(0, len(fs), 4):
    ims = [Image.open(f) for f in fs[k:k + 4]]; w, h = ims[0].size
    c = Image.new("RGB", (w * 2, h * 2), "white")
    for i, im in enumerate(ims): c.paste(im, ((i % 2) * w, (i // 2) * h))
    c.save(f"{b}_sheet{k // 4 + 1}.png")
print(len(fs), "pages")
