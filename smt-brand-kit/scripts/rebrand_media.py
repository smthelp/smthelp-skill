#!/usr/bin/env python3
"""Replace supplier marks on photos and videos with Southern Machinery branding.

photo:  rebrand_media.py photo <in> <out> --box x0,y0,x1,y1 [--text "SOUTHERN MACHINERY"] [--color auto|RRGGBB]
        paints the box with the colour sampled just outside it (or given) and writes the text in DejaVu Sans Bold,
        fitted to the box. Several --box flags allowed. Boxes in pixels of the input image.
video:  rebrand_media.py video <in> <out> [--box x,y,w,h] [--trim start,end] [--width 1280] [--keep-audio]
        covers the box with the SM logo on white, trims intro/end cards, drops audio (supplier voice/music)
        unless --keep-audio, re-encodes H.264 CRF 26 +faststart.
web:    rebrand_media.py web <in.mp4> <out.mp4>   540 px wide CRF 30 copy for the landing page + poster jpg
Find boxes from extract_sources.py frame/photo sheets; check the result visually every time."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageStat

BD = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "brand"))
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def opts(a):
    o = {"box": []}
    i = 0
    while i < len(a):
        if a[i].startswith("--"):
            k = a[i][2:]
            if k in ("keep-audio",): o[k] = True; i += 1; continue
            if k == "box": o["box"].append([int(float(v)) for v in a[i + 1].split(",")])
            else: o[k] = a[i + 1]
            i += 2
        else: i += 1
    return o


def run(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-2000:]); sys.exit(1)


cmd, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
o = opts(sys.argv[4:])
if cmd == "photo":
    im = Image.open(src).convert("RGB"); d = ImageDraw.Draw(im)
    for x0, y0, x1, y1 in o["box"]:
        if o.get("color", "auto") == "auto":
            ring = [im.crop((max(0, x0 - 6), y0, x0, y1)), im.crop((x1, y0, min(im.width, x1 + 6), y1))]
            ring = [r for r in ring if r.width > 0]
            col = tuple(int(sum(ImageStat.Stat(r).median[c] for r in ring) / len(ring)) for c in range(3))
        else:
            col = tuple(int(o["color"][i:i + 2], 16) for i in (0, 2, 4))
        d.rectangle((x0, y0, x1, y1), fill=col)
        t = o.get("text", "SOUTHERN MACHINERY")
        if t:
            lum = sum(col) / 3; fg = (20, 20, 20) if lum > 140 else (245, 245, 245)
            s = int((y1 - y0) * 0.7); f = ImageFont.truetype(FB, max(6, s))
            while d.textlength(t, font=f) > (x1 - x0) * 0.92 and f.size > 6: f = ImageFont.truetype(FB, f.size - 1)
            tw = d.textlength(t, font=f); d.text((x0 + (x1 - x0 - tw) / 2, y0 + (y1 - y0 - f.size) / 2 - 1), t, font=f, fill=fg)
    im.save(out, quality=92); print("photo ->", out)
elif cmd == "video":
    w = int(o.get("width", 1280)); flt = [f"scale={w}:-2"]
    ins = f'-i "{src}"'; fc = ""
    if o.get("trim"):
        a, b = o["trim"].split(","); ins = f'-ss {a} -to {b} -i "{src}"'
    if o["box"]:
        x, y, bw, bh = o["box"][0]
        lg = Image.open(os.path.join(BD, "sm-logo.png")).convert("RGBA")
        card = Image.new("RGBA", (bw, bh), (255, 255, 255, 255)); s = min((bw - 8) / lg.width, (bh - 6) / lg.height)
        l2 = lg.resize((max(1, int(lg.width * s)), max(1, int(lg.height * s))), Image.LANCZOS)
        card.paste(l2, ((bw - l2.width) // 2, (bh - l2.height) // 2), l2); card.save("/tmp/_smcard.png")
        fc = f'-i /tmp/_smcard.png -filter_complex "[0:v][1:v]overlay={x}:{y},{",".join(flt)}[v]" -map "[v]"'
    else:
        fc = f'-vf "{",".join(flt)}"'
    au = "-c:a aac -b:a 128k" if o.get("keep-audio") else "-an"
    if o.get("keep-audio") and o["box"]: fc += " -map 0:a?"
    run(f'ffmpeg -v error -y {ins} {fc} -c:v libx264 -preset veryfast -crf 26 -pix_fmt yuv420p {au} -movflags +faststart "{out}"')
    print("video ->", out)
elif cmd == "web":
    run(f'ffmpeg -v error -y -i "{src}" -vf "scale=540:-2" -c:v libx264 -preset veryfast -crf 30 -c:a aac -b:a 64k -movflags +faststart "{out}"')
    run(f'ffmpeg -v error -y -ss 2 -i "{src}" -frames:v 1 -vf scale=540:-2 -q:v 4 "{out[:-4]}-poster.jpg"')
    print("web ->", out)
else:
    print(__doc__)
