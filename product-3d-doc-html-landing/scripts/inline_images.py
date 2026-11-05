#!/usr/bin/env python3
"""Make emb.json: images that are NOT hosted on ph.smthelp.com, inlined as small WebP data URIs.
usage: python3 inline_images.py <workdir> key=path[:maxpx[:quality]] ...
       python3 inline_images.py <workdir> --hero out_key path1 path2 path3 path4   (2x2 white-trimmed hero grid)
Existing keys in emb.json are kept unless overwritten. Prints KB per image; keep the sum small (page budget 1 MB)."""
import sys, os, json, base64
from PIL import Image, ImageChops
W = os.path.abspath(sys.argv[1]); J = os.path.join(W, 'emb.json'); out = json.load(open(J)) if os.path.exists(J) else {}
def trim(f):
    im = Image.open(f).convert('RGB'); bg = Image.new('RGB', im.size, (255, 255, 255))
    bb = ImageChops.difference(im, bg).convert('L').point(lambda p: 255 if p > 22 else 0).getbbox(); return im.crop(bb) if bb else im
def put(k, im, q):
    p = os.path.join(W, k + '.webp'); im.save(p, 'WEBP', quality=q, method=6)
    out[k] = ['data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode(), list(im.size)]; print(k, im.size, os.path.getsize(p) // 1024, 'KB')
a = sys.argv[2:]
if a and a[0] == '--hero':
    k, fs = a[1], a[2:6]; C = Image.new('RGB', (900, 900), 'white')
    for i, f in enumerate(fs):
        im = trim(f); im.thumbnail((420, 420)); C.paste(im, ((i % 2) * 450 + (450 - im.width) // 2, (i // 2) * 450 + (450 - im.height) // 2))
    put(k, C, 72)
else:
    for s in a:
        k, rest = s.split('=', 1); parts = rest.split(':'); px = int(parts[1]) if len(parts) > 1 else 720; q = int(parts[2]) if len(parts) > 2 else 66
        im = Image.open(parts[0]).convert('RGB'); im.thumbnail((px, px)); put(k, im, q)
json.dump(out, open(J, 'w'))
