"""1280x720 YouTube thumbnails. Usage: python3 thumbs.py [slug ...]
SEO[slug] keys used: thumb (text, \n = line break), thumb_hi (word drawn in gold), thumb_shot (shot id, seconds)."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import cfg, gfx
from gfx import hexa, C
from build import shot_still

VIDEOS, SEO = cfg.VIDEOS, cfg.SEO


def thumb(v):
    seo = SEO[v['slug']]
    S = 1280 / 3840
    W, H = 1280, 720
    im = gfx.grid_bg(W, H, S * 1.5, top=C['hero_top'], bottom=C['grid_bottom'], step=80, alpha=14)
    sid, t = seo['thumb_shot']
    fp = f'/tmp/th_{v["slug"]}.png'
    shot_still(sid, t, fp)                     # cropped + blurred + zoomed like the video
    st = Image.open(fp).convert('RGBA')
    bh = 620; bw = int(bh * st.width / st.height)
    st = st.resize((bw, bh), Image.LANCZOS)
    bx, by = W - bw - 50, 50
    im = gfx.glow(im, [bx, by, bx + bw, by + bh], hexa(C['brand2'], 110), 28 / S * 0.33, S)
    m = Image.new('L', (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=26, fill=255)
    im.paste(st, (bx, by), m)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([bx, by, bx + bw - 1, by + bh - 1], radius=26, outline=hexa(C['brand2']), width=4)
    im.alpha_composite(gfx.logo_plate(1.0, 46), (50, 46))
    d = ImageDraw.Draw(im)
    maxw = bx - 90
    lines = seo['thumb'].split('\n')
    size = 104
    while True:
        f = gfx.F('black', size, 1.0)
        if all(d.textlength(l, font=f) <= maxw for l in lines) or size < 40: break
        size -= 4
    y = 360 - (len(lines) * size * 1.08) / 2 + 20
    hi = seo.get('thumb_hi', '')
    for ln in lines:
        x = 50
        if hi and hi in ln:
            a, b = ln.split(hi, 1)
            for part, col in ((a, C['fg']), (hi, C['gold']), (b, C['fg'])):
                if part:
                    d.text((x, y), part, font=f, fill=hexa(col)); x += d.textlength(part, font=f)
        else:
            d.text((x, y), ln, font=f, fill=hexa(C['fg']))
        y += size * 1.08
    chip = cfg.PRODUCT['chip']
    fc = gfx.F('mono', 30, 1.0)
    tw = d.textlength(chip, font=fc)
    d.rounded_rectangle([50, H - 100, 50 + tw + 40, H - 48], radius=26, fill=hexa(C['brand']))
    d.text((70, H - 94), chip, font=fc, fill=hexa('#ffffff'))
    out = os.path.join(cfg.OUT, cfg.out_name(v['slug'], 'thumb'))
    im.convert('RGB').save(out)
    return out


if __name__ == '__main__':
    only = sys.argv[1:]
    for v in VIDEOS:
        if not only or v['slug'] in only:
            print(thumb(v))
