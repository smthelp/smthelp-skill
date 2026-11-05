#!/usr/bin/env python3
"""Contact sheet of every image under a folder, labelled by file name, so you can SEE images before choosing.
usage: python3 contact_sheet.py <folder> <out.jpg> [--min-kb 15]"""
import sys, os
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]; mk = int(sys.argv[sys.argv.index('--min-kb') + 1]) if '--min-kb' in sys.argv else 15
fs = [os.path.join(r, f) for r, _, n in os.walk(src) for f in sorted(n) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and os.path.getsize(os.path.join(r, f)) > mk * 1024]
ims = []
for f in fs:
    try: im = Image.open(f).convert('RGB'); im.thumbnail((240, 180)); ims.append((f, im))
    except Exception: pass
cols = 7; rows = max(1, (len(ims) + cols - 1) // cols)
W = Image.new('RGB', (cols * 250, rows * 200), 'white'); d = ImageDraw.Draw(W)
for k, (f, im) in enumerate(ims):
    x, y = (k % cols) * 250, (k // cols) * 200; W.paste(im, (x, y)); d.text((x + 2, y + 184), os.path.relpath(f, src)[-40:], fill='red')
W.save(out, quality=70); print(len(ims), 'images ->', out)
