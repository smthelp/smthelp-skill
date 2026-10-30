"""Southern Machinery video graphics engine (PIL).
All coordinates are 4K design units (3840x2160 frame, 1400x1680 footage window) multiplied by S
(S=1.0 for 4K, 0.25 for previews). Colours, fonts, logo and contacts come from config/brand.json
(+ project brand_overrides); product labels from project.json -> product.
Slide types usable from content SLIDES dicts: rows, stat, formula, flow, split, table, grid, bars.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cfg

FD = cfg.FONT_DIR
LOGO = cfg.LOGO
C = dict(cfg.B['colors'])
FONTS = cfg.B['fonts']
W4, H4 = cfg.W4, cfg.H4
WIN = (160, 220, 1400, 1680)      # footage window x, y, w, h
CO = (1720, 600, 1960, 900)       # callout card box
RAD = 44
X0, X1 = 90, 1310                 # slide content margins inside the window
PRODUCT = cfg.PRODUCT
CT = cfg.CONTACT


def set_layout(mirror=False):
    """batch 2: mirror=True puts the footage window on the right, callouts on the left"""
    global WIN, CO
    if mirror:
        WIN = (2280, 220, 1400, 1680); CO = (160, 600, 1960, 900)
    else:
        WIN = (160, 220, 1400, 1680); CO = (1720, 600, 1960, 900)

def hexa(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

_fc = {}

def F(name, size, S):
    key = (name, int(size * S))
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FD + FONTS[name], max(6, int(size * S)))
    return _fc[key]

def wrap(d, text, font, maxw):
    out = []
    for para in text.split('\n'):
        words = para.split(' '); cur = ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=font) <= maxw or not cur:
                cur = t
            else:
                out.append(cur); cur = w
        out.append(cur)
    return out

def text_block(d, xy, text, font, fill, maxw, lh=1.18, spacing=0):
    x, y = xy
    lines = wrap(d, text, font, maxw)
    asc = font.size
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += asc * lh
    return y

def spaced(d, xy, text, font, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return x

def grid_bg(w, h, S, top=None, bottom=None, step=80, alpha=10):
    top = top or C['grid_top']; bottom = bottom or C['grid_bottom']
    im = Image.new('RGBA', (w, h))
    px = Image.linear_gradient('L').resize((w, h))
    a = Image.new('RGBA', (w, h), hexa(top)); b = Image.new('RGBA', (w, h), hexa(bottom))
    im = Image.composite(b, a, px)
    g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    st = max(4, int(step * S))
    for x in range(0, w, st): gd.line([(x, 0), (x, h)], fill=(255, 255, 255, alpha), width=max(1, int(2 * S)))
    for y in range(0, h, st): gd.line([(0, y), (w, y)], fill=(255, 255, 255, alpha), width=max(1, int(2 * S)))
    return Image.alpha_composite(im, g)

def logo_plate(S, h=110):
    lg = Image.open(LOGO).convert('RGBA')
    lh = int(h * S); lw = int(lg.width * lh / lg.height)
    lg = lg.resize((lw, lh), Image.LANCZOS)
    pad = int(h * 0.28 * S)
    pl = Image.new('RGBA', (lw + 2 * pad, lh + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle([0, 0, pl.width - 1, pl.height - 1], radius=int(18 * S), fill=(255, 255, 255, 255))
    pl.alpha_composite(lg, (pad, pad))
    return pl

def glow(im, box, color, radius, S):
    g = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle(box, radius=int(RAD * S), fill=color)
    g = g.filter(ImageFilter.GaussianBlur(radius * S))
    return Image.alpha_composite(im, g)

def make_bg(v, S, path):
    w, h = int(W4 * S), int(H4 * S)
    im = grid_bg(w, h, S)
    x, y, ww, wh = [int(c * S) for c in WIN]
    im = glow(im, [x, y, x + ww, y + wh], hexa(C['brand2'], 70), 60, S)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x, y, x + ww, y + wh], radius=int(RAD * S), fill=hexa(C['deep']))
    # logo bug top-left
    pl = logo_plate(S, 74)
    im.alpha_composite(pl, (int(160 * S), int(70 * S)))
    d = ImageDraw.Draw(im)
    # top-right product tag
    f = F('monom', 34, S)
    tag = PRODUCT['tag']
    tw = d.textlength(tag, font=f) + 0
    d.text((w - int(160 * S) - tw - int(len(tag) * 2 * S), int(100 * S)), tag, font=f, fill=hexa(C['fg3']))
    # right panel title
    rx = int(CO[0] * S)
    spaced(d, (rx, int(250 * S)), v['kicker'], F('mono', 40, S), hexa(C['gold']), int(4 * S))
    d.line([(rx, int(318 * S)), (rx + int(120 * S), int(318 * S))], fill=hexa(C['brand2']), width=max(1, int(6 * S)))
    text_block(d, (rx, int(350 * S)), v['title'], F('bold', 92, S), hexa(C['fg']), int(CO[2] * S), lh=1.12)
    # footer
    fy = int(1985 * S)
    d.line([(int(160 * S), fy), (w - int(160 * S), fy)], fill=hexa(C['line2']), width=max(1, int(3 * S)))
    ff = F('med', 44, S)
    d.text((int(160 * S), fy + int(36 * S)), v.get('footer_cta', PRODUCT['footer_cta']), font=ff, fill=hexa(C['gold']))
    right = f"WhatsApp {CT['whatsapp_display']}   ·   {CT['web']}"
    d.text((w - int(160 * S) - d.textlength(right, font=ff), fy + int(36 * S)), right, font=ff, fill=hexa(C['fg2']))
    im.save(path)
    return im

def make_frame(bg, S, path):
    """corner mask + border to sit over the window footage"""
    m = int(24 * S)
    x, y, ww, wh = [int(c * S) for c in WIN]
    box = (x - m, y - m, x + ww + m, y + wh + m)
    crop = bg.crop(box)
    mask = Image.new('L', crop.size, 255)
    ImageDraw.Draw(mask).rounded_rectangle([m, m, m + ww - 1, m + wh - 1], radius=int(RAD * S), fill=0)
    out = Image.new('RGBA', crop.size, (0, 0, 0, 0))
    out.paste(crop, (0, 0), mask)
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([m, m, m + ww - 1, m + wh - 1], radius=int(RAD * S), outline=hexa(C['brand2'], 150), width=max(1, int(5 * S)))
    out.save(path)
    return (x - m, y - m)

def make_callout(co, S, path):
    w, h = int(CO[2] * S), int(CO[3] * S)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pad = int(70 * S)
    # measure content first
    def draw(dry, scale):
        y = int(60 * S)
        if not dry:
            spaced(d, (pad, y), co['k'], F('mono', 40 * scale, S), hexa(C['brand2']), int(4 * S))
        y += int(90 * S * scale)
        if co.get('stat'):
            f = F('xbold', 210 * scale, S)
            if not dry: d.text((pad, y - int(20 * S)), co['stat'], font=f, fill=hexa(C['gold']))
            y += int(225 * S * scale)
            f2 = F('semi', 60 * scale, S)
            for ln in wrap(d, co['h'], f2, w - 2 * pad):
                if not dry: d.text((pad, y), ln, font=f2, fill=hexa(C['fg']))
                y += int(74 * S * scale)
        else:
            f = F('bold', 82 * scale, S)
            for ln in wrap(d, co['h'], f, w - 2 * pad):
                if not dry: d.text((pad, y), ln, font=f, fill=hexa(C['fg']))
                y += int(98 * S * scale)
        y += int(30 * S * scale)
        fb = F('med', 54 * scale, S)
        for b in co.get('b', []):
            col = C['fg2']; mark = 'dot'
            if b.startswith('+ '): b = b[2:]; mark = 'plus'
            elif b.startswith('– '): b = b[2:]; mark = 'minus'
            lines = wrap(d, b, fb, w - 2 * pad - int(70 * S))
            if not dry:
                cy = y + int(32 * S * scale)
                r = int(13 * S * scale)
                if mark == 'dot':
                    d.ellipse([pad + int(8 * S), cy - r, pad + int(8 * S) + 2 * r, cy + r], fill=hexa(C['brand2']))
                elif mark == 'plus':
                    fm = F('bold', 60 * scale, S); d.text((pad, y - int(6 * S)), '+', font=fm, fill=hexa(C['ok']))
                else:
                    fm = F('bold', 60 * scale, S); d.text((pad + int(4 * S), y - int(8 * S)), '–', font=fm, fill=hexa(C['red']))
                for i, ln in enumerate(lines):
                    d.text((pad + int(70 * S), y + i * int(66 * S * scale)), ln, font=fb, fill=hexa(C['fg2']))
            y += int(66 * S * scale) * len(lines) + int(22 * S * scale)
        return y + int(40 * S)
    scale = 1.22
    while draw(True, scale) > h and scale > 0.6:
        scale -= 0.05
    hh = min(h, draw(True, scale))
    d.rounded_rectangle([0, 0, w - 1, hh - 1], radius=int(32 * S), fill=hexa(C['card'], 235), outline=hexa(C['line2']), width=max(1, int(3 * S)))
    d.rounded_rectangle([0, int(40 * S), int(10 * S), int(40 * S) + int(120 * S)], radius=int(5 * S), fill=hexa(C['gold']))
    draw(False, scale)
    im.save(path)

def make_intro(v, S, path_bg, path_txt, still=None):
    w, h = int(W4 * S), int(H4 * S)
    im = grid_bg(w, h, S, top=C['hero_top'], bottom=C['grid_bottom'])
    # still on the right in rounded window
    if still:
        st = Image.open(still).convert('RGBA')
        bw, bh = int(1200 * S), int(1440 * S)
        st = st.resize((bw, bh), Image.LANCZOS)
        bx, by = int(2420 * S), int(360 * S)
        im = glow(im, [bx, by, bx + bw, by + bh], hexa(C['brand2'], 90), 70, S)
        m = Image.new('L', (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=int(RAD * S), fill=255)
        im.paste(st, (bx, by), m)
        ImageDraw.Draw(im).rounded_rectangle([bx, by, bx + bw - 1, by + bh - 1], radius=int(RAD * S), outline=hexa(C['brand2'], 160), width=max(1, int(5 * S)))
    im.save(path_bg)
    t = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    pl = logo_plate(S, 130)
    t.alpha_composite(pl, (int(240 * S), int(330 * S)))
    d = ImageDraw.Draw(t)
    spaced(d, (int(240 * S), int(640 * S)), PRODUCT['tag'], F('mono', 48, S), hexa(C['gold']), int(5 * S))
    y = int(760 * S)
    for ln in v['intro_title'].split('\n'):
        d.text((int(240 * S), y), ln, font=F('black', 150, S), fill=hexa(C['fg']))
        y += int(180 * S)
    d.rectangle([int(240 * S), y + int(40 * S), int(560 * S), y + int(56 * S)], fill=hexa(C['brand2']))
    d.text((int(240 * S), y + int(110 * S)), cfg.B['tagline'], font=F('med', 56, S), fill=hexa(C['fg2']))
    t.save(path_txt)

def make_outro(S, path, headline=None):
    headline = headline or PRODUCT['outro_headline']
    w, h = int(W4 * S), int(H4 * S)
    im = grid_bg(w, h, S, top=C['hero_top'], bottom=C['grid_bottom'])
    im = glow(im, [int(520 * S), int(330 * S), int(3320 * S), int(1650 * S)], hexa(C['brand2'], 50), 90, S)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([int(520 * S), int(330 * S), int(3320 * S), int(1650 * S)], radius=int(48 * S), fill=hexa(C['card'], 245), outline=hexa(C['line2']), width=max(1, int(4 * S)))
    pl = logo_plate(S, 120)
    im.alpha_composite(pl, ((w - pl.width) // 2, int(420 * S)))
    d = ImageDraw.Draw(im)
    def ctr(y, text, font, fill):
        d.text(((w - d.textlength(text, font=font)) / 2, y), text, font=font, fill=fill)
    ctr(int(720 * S), headline, F('black', 132, S), hexa(C['fg']))
    # whatsapp pill
    ft = F('bold', 96, S)
    txt = f"WhatsApp {CT['whatsapp_display']}"
    tw = d.textlength(txt, font=ft)
    px, py = (w - tw) / 2 - int(70 * S), int(960 * S)
    d.rounded_rectangle([px, py, px + tw + int(140 * S), py + int(170 * S)], radius=int(85 * S), fill=hexa(C['whatsapp']))
    d.text((px + int(70 * S), py + int(30 * S)), txt, font=ft, fill=hexa('#04110f'))
    ctr(int(1210 * S), f"{CT['web']}   ·   {CT['email']}", F('semi', 80, S), hexa(C['brand3']))
    ctr(int(1420 * S), PRODUCT['outro_line'], F('med', 50, S), hexa(C['fg3']))
    im.putalpha(255)  # card was drawn with alpha<255 (ImageDraw replaces pixels); keep outro opaque
    im.save(path)

def slide_base(S, kicker, heading):
    w, h = int(WIN[2] * S), int(WIN[3] * S)
    im = grid_bg(w, h, S, top=C['slide_top'], bottom=C['slide_bottom'], step=70, alpha=12)
    d = ImageDraw.Draw(im)
    spaced(d, (int(90 * S), int(100 * S)), kicker, F('mono', 40, S), hexa(C['brand2']), int(4 * S))
    y = text_block(d, (int(90 * S), int(170 * S)), heading, F('bold', 84, S), hexa(C['fg']), int(1220 * S), lh=1.15)
    return im, d, y + int(40 * S)

def rows_slide(S, kicker, heading, rows, numbered=False, icon=None, footer=None):
    """returns list of build images: one per row revealed"""
    builds = []
    for n in range(0, len(rows) + 1):
        if n == 0 and len(rows) > 0:
            continue
        im, d, y = slide_base(S, kicker, heading)
        if icon: y = icon(im, d, y)
        for i, r in enumerate(rows[:n]):
            bh = int(178 * S)
            x0, x1 = int(90 * S), int(1310 * S)
            d.rounded_rectangle([x0, y, x1, y + bh], radius=int(24 * S), fill=hexa(C['card'], 230), outline=hexa(C['line2']), width=max(1, int(3 * S)))
            lab = str(i + 1).zfill(2) if numbered else '✓'
            if numbered:
                d.text((x0 + int(40 * S), y + int(38 * S)), lab, font=F('mono', 64, S), fill=hexa(C['gold']))
            else:
                cx, cy = x0 + int(75 * S), y + bh // 2
                d.ellipse([cx - int(32 * S), cy - int(32 * S), cx + int(32 * S), cy + int(32 * S)], fill=hexa(C['brand']))
                d.line([(cx - int(14 * S), cy), (cx - int(3 * S), cy + int(12 * S)), (cx + int(16 * S), cy - int(12 * S))], fill=hexa('#ffffff'), width=max(1, int(7 * S)))
            fr = F('semi', 60, S)
            lines = wrap(d, r, fr, x1 - x0 - int(220 * S))
            ty = y + (bh - len(lines) * int(68 * S)) // 2 - int(4 * S)
            for ln in lines:
                d.text((x0 + int(170 * S), ty), ln, font=fr, fill=hexa(C['fg']))
                ty += int(68 * S)
            y += bh + int(26 * S)
        if footer:
            d.text((int(90 * S), int(1560 * S)), footer, font=F('med', 40, S), fill=hexa(C['fg3']))
        builds.append(im)
    return builds

def reel(d, cx, cy, r, S, col=None, parts=True):
    col = col or C['fg2']
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=hexa(col), width=max(1, int(8 * S)))
    d.ellipse([cx - r * 0.25, cy - r * 0.25, cx + r * 0.25, cy + r * 0.25], outline=hexa(col), width=max(1, int(6 * S)))
    if parts:
        for k in range(3):
            rr = r * (0.45 + 0.15 * k)
            n = int(18 + 10 * k)
            for i in range(n):
                a = 2 * math.pi * i / n
                x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
                s = max(1, int(7 * S))
                d.rectangle([x - s, y - s, x + s, y + s], fill=hexa(C['gold'], 230))

def big_stat_slide(S, kicker, heading, stat, sub, foot):
    im, d, y = slide_base(S, kicker, heading)
    cx = int(700 * S); cy = int(900 * S); r = int(380 * S)
    for k in range(4):
        rr = r + k * int(70 * S)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=hexa(C['brand2'], 160 - 35 * k), width=max(1, int(5 * S)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hexa(C['card'], 240))
    f = F('xbold', 170, S)
    d.text((cx - d.textlength(stat, font=f) / 2, cy - int(130 * S)), stat, font=f, fill=hexa(C['gold']))
    f2 = F('semi', 52, S)
    for i, ln in enumerate(wrap(d, sub, f2, int(600 * S))):
        d.text((cx - d.textlength(ln, font=f2) / 2, cy + int(70 * S) + i * int(62 * S)), ln, font=f2, fill=hexa(C['fg2']))
    if foot:
        d.text((int(90 * S), int(1530 * S)), foot, font=F('med', 40, S), fill=hexa(C['fg3']))
    return [im]

def formula_slide(S, kicker, heading, lines, foot=None, hl_last=False):
    builds = []
    for n in range(1, len(lines) + 1):
        im, d, y = slide_base(S, kicker, heading)
        y += int(20 * S)
        for i, (lab, val) in enumerate(lines[:n]):
            last = hl_last and i == len(lines) - 1
            bh = int(190 * S)
            d.rounded_rectangle([int(90 * S), y, int(1310 * S), y + bh], radius=int(24 * S), fill=hexa(C['brand'] if last else C['card'], 235), outline=hexa(C['gold'] if last else C['line2']), width=max(1, int(3 * S)))
            d.text((int(140 * S), y + int(26 * S)), lab, font=F('med', 44, S), fill=hexa(C['fg2'] if not last else '#ffffff'))
            vs = 70
            while vs > 40 and d.textlength(val, font=F('bold', vs, S)) > int(1120 * S): vs -= 2
            d.text((int(140 * S), y + int(86 * S) + int((70 - vs) * 0.5 * S)), val, font=F('bold', vs, S), fill=hexa(C['gold'] if not last else '#ffffff'))
            y += bh + int(24 * S)
        if foot:
            for i, ln in enumerate(wrap(d, foot, F('med', 40, S), int(1220 * S))):
                d.text((int(90 * S), int(1500 * S) + i * int(50 * S)), ln, font=F('med', 40, S), fill=hexa(C['fg3']))
        builds.append(im)
    return builds

def _i(v, S):
    return int(v * S)

def arrow_down(d, cx, y0, y1, S, col=None):
    col = hexa(col or C['brand2'])
    d.line([(cx, y0), (cx, y1 - _i(22, S))], fill=col, width=max(1, _i(8, S)))
    k = _i(24, S)
    d.polygon([(cx - k, y1 - k), (cx + k, y1 - k), (cx, y1)], fill=col)

def arrow_right(d, x0, x1, cy, S, col=None):
    col = hexa(col or C['brand2'])
    d.line([(x0, cy), (x1 - _i(22, S), cy)], fill=col, width=max(1, _i(8, S)))
    k = _i(24, S)
    d.polygon([(x1 - k, cy - k), (x1 - k, cy + k), (x1, cy)], fill=col)

def flow_slide(S, kicker, heading, steps, hl=None, foot=None):
    """steps: list of (title, sub). hl: index highlighted in gold."""
    builds = []
    n = len(steps)
    for k in range(1, n + 1):
        im, d, y = slide_base(S, kicker, heading)
        avail = _i(1560, S) - y
        bh = min(_i(200, S), int((avail - (n - 1) * _i(70, S)) / n))
        gap = _i(70, S)
        for i, (t, sub) in enumerate(steps[:k]):
            yy = y + i * (bh + gap)
            on = (hl == i)
            d.rounded_rectangle([_i(X0, S), yy, _i(X1, S), yy + bh], radius=_i(28, S),
                                fill=hexa(C['brand'] if on else C['card'], 240), outline=hexa(C['gold'] if on else C['line2']), width=max(1, _i(4, S)))
            cx, cy = _i(X0 + 95, S), yy + bh // 2
            r = _i(52, S)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hexa(C['gold'] if not on else '#ffffff'))
            num = str(i + 1)
            f = F('black', 60, S)
            d.text((cx - d.textlength(num, font=f) / 2, cy - _i(38, S)), num, font=f, fill=hexa(C['deep']))
            ft = F('bold', 58, S)
            fs = F('med', 42, S)
            tx = _i(X0 + 190, S)
            if sub:
                d.text((tx, cy - _i(62, S)), t, font=ft, fill=hexa('#ffffff' if on else C['fg']))
                d.text((tx, cy + _i(8, S)), sub, font=fs, fill=hexa('#e6fffa' if on else C['fg3']))
            else:
                d.text((tx, cy - _i(34, S)), t, font=ft, fill=hexa('#ffffff' if on else C['fg']))
            if i < k - 1:
                arrow_down(d, cx, yy + bh + _i(6, S), yy + bh + gap - _i(6, S), S)
        if foot:
            d.text((_i(X0, S), _i(1590, S)), foot, font=F('med', 38, S), fill=hexa(C['fg3']))
        builds.append(im)
    return builds

def split_slide(S, kicker, heading, left, right, foot=None):
    im, d, y = slide_base(S, kicker, heading)
    y += _i(10, S)
    colw = _i(590, S)
    for j, (title, items, col) in enumerate([left + (C['brand2'],), right + (C['gold'],)]):
        x0 = _i(X0, S) + j * (colw + _i(40, S))
        fb = F('semi', 46, S)
        hh = _i(190, S)
        for it in items:
            hh += len(wrap(d, it, fb, colw - _i(120, S))) * _i(56, S) + _i(40, S)
        y1 = max(y + _i(1000, S), y + hh + _i(40, S))
        d.rounded_rectangle([x0, y, x0 + colw, y1], radius=_i(30, S), fill=hexa(C['card'], 235), outline=hexa(col, 200), width=max(1, _i(4, S)))
        d.rounded_rectangle([x0, y, x0 + colw, y + _i(140, S)], radius=_i(30, S), fill=hexa(col, 230))
        d.rectangle([x0, y + _i(100, S), x0 + colw, y + _i(140, S)], fill=hexa(col, 230))
        ft = F('black', 64, S)
        d.text((x0 + (colw - d.textlength(title, font=ft)) / 2, y + _i(32, S)), title, font=ft, fill=hexa(C['deep']))
        yy = y + _i(190, S)
        fb = F('semi', 46, S)
        for it in items:
            lines = wrap(d, it, fb, colw - _i(120, S))
            d.ellipse([x0 + _i(40, S), yy + _i(16, S), x0 + _i(64, S), yy + _i(40, S)], fill=hexa(col))
            for li, ln in enumerate(lines):
                d.text((x0 + _i(90, S), yy + li * _i(56, S)), ln, font=fb, fill=hexa(C['fg']))
            yy += len(lines) * _i(56, S) + _i(40, S)
    if foot:
        for li, ln in enumerate(wrap(d, foot, F('med', 38, S), _i(1220, S))):
            d.text((_i(X0, S), _i(1520, S) + li * _i(50, S)), ln, font=F('med', 38, S), fill=hexa(C['fg3']))
    return [im]

def table_slide(S, kicker, heading, header, rows, foot=None, widths=None):
    builds = []
    for k in (2, len(rows)):
        im, d, y = slide_base(S, kicker, heading)
        y += _i(10, S)
        x0, x1 = _i(X0, S), _i(X1, S)
        n = len(header)
        widths_ = widths or [1] * n
        tot = sum(widths_)
        xs = [x0]
        for w in widths_:
            xs.append(xs[-1] + int((x1 - x0) * w / tot))
        rh = _i(118, S)
        d.rounded_rectangle([x0, y, x1, y + rh * (len(rows) + 1)], radius=_i(22, S), fill=hexa('#08100f', 240), outline=hexa(C['line2']), width=max(1, _i(3, S)))
        d.rounded_rectangle([x0, y, x1, y + rh], radius=_i(22, S), fill=hexa(C['brand'], 255))
        fh = F('mono', 36, S); fr = F('monom', 36, S)
        for i, h in enumerate(header):
            d.text((xs[i] + _i(24, S), y + _i(38, S)), h, font=fh, fill=hexa('#ffffff'))
        for r, row in enumerate(rows[:k]):
            yy = y + rh * (r + 1)
            if r % 2:
                d.rectangle([x0 + 2, yy, x1 - 2, yy + rh], fill=hexa(C['bg3'], 200))
            for i, c in enumerate(row):
                col = C['gold'] if i == len(row) - 1 else C['fg2']
                d.text((xs[i] + _i(24, S), yy + _i(38, S)), c, font=fr, fill=hexa(col))
        if foot:
            for li, ln in enumerate(wrap(d, foot, F('med', 38, S), _i(1220, S))):
                d.text((_i(X0, S), _i(1500, S) + li * _i(50, S)), ln, font=F('med', 38, S), fill=hexa(C['fg3']))
        builds.append(im)
    return builds

def grid_slide(S, kicker, heading, cards, foot=None, icons=None):
    """cards: list of (big, label). 2 columns."""
    im, d, y = slide_base(S, kicker, heading)
    y += _i(10, S)
    n = len(cards); rows = (n + 1) // 2
    cw = _i(590, S); gap = _i(40, S)
    ch = min(_i(560, S), int((_i(1500, S) - y - (rows - 1) * gap) / rows))
    for i, (big, lab) in enumerate(cards):
        cx0 = _i(X0, S) + (i % 2) * (cw + gap); cy0 = y + (i // 2) * (ch + gap)
        d.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=_i(30, S), fill=hexa(C['card'], 240), outline=hexa(C['line2']), width=max(1, _i(3, S)))
        d.rectangle([cx0 + _i(40, S), cy0 + _i(40, S), cx0 + _i(120, S), cy0 + _i(48, S)], fill=hexa(C['gold']))
        if icons and icons[i]:
            icons[i](d, cx0 + cw // 2, cy0 + int(ch * 0.36), int(ch * 0.2), S)
            fl = F('semi', 46, S)
            lines = wrap(d, lab, fl, cw - _i(60, S))
            ly = cy0 + ch - _i(40, S) - len(lines) * _i(54, S)
            for ln in lines:
                d.text((cx0 + (cw - d.textlength(ln, font=fl)) / 2, ly), ln, font=fl, fill=hexa(C['fg']))
                ly += _i(54, S)
        else:
            fb = F('xbold', 92, S)
            while d.textlength(big, font=fb) > cw - _i(80, S) and fb.size > 30:
                fb = F('xbold', fb.size / S - 6, S)
            d.text((cx0 + _i(40, S), cy0 + _i(80, S)), big, font=fb, fill=hexa(C['gold']))
            fl = F('semi', 44, S)
            ly = cy0 + _i(80, S) + int(fb.size * 1.25)
            for ln in wrap(d, lab, fl, cw - _i(80, S)):
                d.text((cx0 + _i(40, S), ly), ln, font=fl, fill=hexa(C['fg2']))
                ly += _i(54, S)
    if foot:
        for li, ln in enumerate(wrap(d, foot, F('med', 38, S), _i(1220, S))):
            d.text((_i(X0, S), _i(1570, S) + li * _i(48, S)), ln, font=F('med', 38, S), fill=hexa(C['fg3']))
    return [im]

def ic_reel(d, cx, cy, r, S):
    reel(d, cx, cy, r, S)

def ic_tube(d, cx, cy, r, S):
    w = int(r * 2.2); h = int(r * 0.55)
    d.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], radius=int(h * 0.3), outline=hexa(C['fg2']), width=max(1, _i(7, S)))
    for i in range(6):
        x = cx - w // 2 + int(w * (i + 0.6) / 6.4)
        d.rectangle([x, cy - h // 4, x + int(w / 11), cy + h // 4], fill=hexa(C['gold']))

def ic_tray(d, cx, cy, r, S):
    w = int(r * 2.2); h = int(r * 1.5)
    d.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], radius=_i(14, S), outline=hexa(C['fg2']), width=max(1, _i(7, S)))
    for gx in range(4):
        for gy in range(3):
            x = cx - w // 2 + int(w * (gx + 0.5) / 4); y = cy - h // 2 + int(h * (gy + 0.5) / 3)
            s = int(r * 0.18)
            d.rectangle([x - s, y - s, x + s, y + s], fill=hexa(C['gold']))

def ic_bag(d, cx, cy, r, S):
    w = int(r * 1.7); h = int(r * 2.0)
    d.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], radius=_i(20, S), outline=hexa(C['brand3']), width=max(1, _i(7, S)))
    d.line([(cx - w // 2, cy - h // 2 + _i(30, S)), (cx + w // 2, cy - h // 2 + _i(30, S))], fill=hexa(C['brand3']), width=max(1, _i(5, S)))
    reel(d, cx, cy + _i(14, S), int(r * 0.62), S, parts=True)

def ic_loose(d, cx, cy, r, S):
    import random
    rnd = random.Random(3)
    for _ in range(26):
        x = cx + rnd.uniform(-r, r); y = cy + rnd.uniform(-r * 0.8, r * 0.8)
        s = r * 0.09; a = rnd.uniform(0, math.pi)
        pts = [(x + s * 2 * math.cos(a) - s * math.sin(a), y + s * 2 * math.sin(a) + s * math.cos(a)),
               (x - s * 2 * math.cos(a) - s * math.sin(a), y - s * 2 * math.sin(a) + s * math.cos(a)),
               (x - s * 2 * math.cos(a) + s * math.sin(a), y - s * 2 * math.sin(a) - s * math.cos(a)),
               (x + s * 2 * math.cos(a) + s * math.sin(a), y + s * 2 * math.sin(a) - s * math.cos(a))]
        d.polygon(pts, fill=hexa(C['gold']))

def ic_tape(d, cx, cy, r, S):
    w = int(r * 2.3); h = int(r * 0.7)
    d.rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], outline=hexa(C['fg2']), width=max(1, _i(6, S)))
    for i in range(7):
        x = cx - w // 2 + int(w * (i + 0.5) / 7)
        d.ellipse([x - _i(6, S), cy - h // 2 + _i(8, S), x + _i(6, S), cy - h // 2 + _i(20, S)], fill=hexa(C['fg3']))
        d.rectangle([x - int(r * 0.11), cy - int(r * 0.08), x + int(r * 0.11), cy + int(r * 0.2)], fill=hexa(C['gold']))

def ic_chip(d, cx, cy, r, S):
    w = int(r * 1.3)
    d.rounded_rectangle([cx - w // 2, cy - w // 2, cx + w // 2, cy + w // 2], radius=_i(10, S), fill=hexa('#1d2c2a'), outline=hexa(C['fg2']), width=max(1, _i(5, S)))
    for i in range(5):
        o = -w // 2 + int(w * (i + 0.5) / 5)
        for (a, b) in [((cx + o, cy - w // 2), (cx + o, cy - w // 2 - int(r * 0.3))), ((cx + o, cy + w // 2), (cx + o, cy + w // 2 + int(r * 0.3))),
                       ((cx - w // 2, cy + o), (cx - w // 2 - int(r * 0.3), cy + o)), ((cx + w // 2, cy + o), (cx + w // 2 + int(r * 0.3), cy + o))]:
            d.line([a, b], fill=hexa(C['gold']), width=max(1, _i(6, S)))

def ic_cable(d, cx, cy, r, S):
    for k, col in enumerate([C['gold'], C['brand3'], C['fg2']]):
        pts = [(cx - r * 1.1 + t * r * 2.2 / 20, cy + (k - 1) * r * 0.35 + math.sin(t / 3 + k) * r * 0.18) for t in range(21)]
        d.line(pts, fill=hexa(col), width=max(1, _i(10, S)))
    d.rounded_rectangle([cx + r * 0.9, cy - r * 0.6, cx + r * 1.25, cy + r * 0.6], radius=_i(8, S), fill=hexa(C['fg3']))

def ic_bolt(d, cx, cy, r, S):
    d.regular_polygon((cx, cy - int(r * 0.55), int(r * 0.42)), 6, fill=hexa(C['fg2']))
    d.rectangle([cx - int(r * 0.2), cy - int(r * 0.2), cx + int(r * 0.2), cy + r], fill=hexa(C['fg3']))
    for k in range(5):
        y = cy - int(r * 0.1) + k * int(r * 0.22)
        d.line([(cx - int(r * 0.24), y), (cx + int(r * 0.24), y + int(r * 0.1))], fill=hexa(C['deep']), width=max(1, _i(4, S)))

def ic_plastic(d, cx, cy, r, S):
    d.rounded_rectangle([cx - r, cy - int(r * 0.6), cx + r, cy + int(r * 0.6)], radius=int(r * 0.3), outline=hexa(C['brand3']), width=max(1, _i(7, S)))
    d.ellipse([cx - int(r * 0.3), cy - int(r * 0.3), cx + int(r * 0.3), cy + int(r * 0.3)], outline=hexa(C['brand3']), width=max(1, _i(7, S)))

def ic_honey(d, cx, cy, r, S):
    s = r * 0.32
    for gy in range(-2, 3):
        for gx in range(-2, 3):
            x = cx + gx * s * 1.75 + (gy % 2) * s * 0.875; y = cy + gy * s * 1.5
            if abs(x - cx) > r * 1.1: continue
            d.regular_polygon((x, y, s), 6, rotation=30, outline=hexa(C['gold']), width=max(1, _i(4, S)))

def bars_slide(S, kicker, heading, bars, foot=None):
    """bars: list of (label, frac, note) — horizontal 'lower is safer' bars"""
    builds = []
    for k in range(1, len(bars) + 1):
        im, d, y = slide_base(S, kicker, heading)
        y += _i(20, S)
        for i, (lab, frac, note) in enumerate(bars[:k]):
            yy = y + i * _i(230, S)
            d.text((_i(X0, S), yy), lab, font=F('bold', 54, S), fill=hexa(C['fg']))
            d.text((_i(X1, S) - d.textlength(note, font=F('med', 40, S)), yy + _i(12, S)), note, font=F('med', 40, S), fill=hexa(C['brand3']))
            by = yy + _i(90, S)
            d.rounded_rectangle([_i(X0, S), by, _i(X1, S), by + _i(70, S)], radius=_i(35, S), fill=hexa(C['bg3']))
            xe = _i(X0, S) + int((_i(X1, S) - _i(X0, S)) * frac)
            d.rounded_rectangle([_i(X0, S), by, xe, by + _i(70, S)], radius=_i(35, S), fill=hexa(C['gold']))
            arrow_right(d, xe + _i(30, S), xe + _i(160, S), by + _i(35, S), S, C['ok']) if False else None
        if foot:
            for li, ln in enumerate(wrap(d, foot, F('med', 38, S), _i(1220, S))):
                d.text((_i(X0, S), _i(1480, S) + li * _i(50, S)), ln, font=F('med', 38, S), fill=hexa(C['fg3']))
        builds.append(im)
    return builds


# ---------------------------------------------------------------- data-driven slides
ICONS = dict(reel=ic_reel, tube=ic_tube, tray=ic_tray, bag=ic_bag, loose=ic_loose, tape=ic_tape, chip=ic_chip,
             cable=ic_cable, bolt=ic_bolt, plastic=ic_plastic, honey=ic_honey)


def slide_from_spec(sp, S):
    """sp = dict(type=..., kicker=..., heading=..., ...) - see references/design-copy-standard.md"""
    t = sp['type']; k = sp.get('kicker', ''); h = sp.get('heading', ''); foot = sp.get('foot')
    if t == 'rows':
        return rows_slide(S, k, h, sp['rows'], numbered=sp.get('numbered', False), footer=foot)
    if t == 'stat':
        return big_stat_slide(S, k, h, sp['stat'], sp.get('sub', ''), foot or '')
    if t == 'formula':
        return formula_slide(S, k, h, [tuple(x) for x in sp['lines']], foot=foot, hl_last=sp.get('hl_last', False))
    if t == 'flow':
        return flow_slide(S, k, h, [tuple(x) for x in sp['steps']], hl=sp.get('hl'), foot=foot)
    if t == 'split':
        return split_slide(S, k, h, (sp['left'][0], sp['left'][1]), (sp['right'][0], sp['right'][1]), foot=foot)
    if t == 'table':
        return table_slide(S, k, h, sp['header'], [tuple(r) for r in sp['rows']], foot=foot, widths=sp.get('widths'))
    if t == 'grid':
        icons = [ICONS.get(i) if i else None for i in sp['icons']] if sp.get('icons') else None
        return grid_slide(S, k, h, [tuple(c) for c in sp['cards']], foot=foot, icons=icons)
    if t == 'bars':
        return bars_slide(S, k, h, [tuple(b) for b in sp['bars']], foot=foot)
    raise ValueError(f'E21 unknown slide type {t}')


def make_slide(sid, S):
    """'blank' -> empty branded panel; else content SLIDES[sid] (data), else content/slides.py make_slide (custom drawing)."""
    if sid == 'blank':
        im, d, y = slide_base(S, PRODUCT['chip'], '')
        return [im]
    if sid in cfg.SLIDES:
        return slide_from_spec(cfg.SLIDES[sid], S)
    if cfg.HAS_CUSTOM_SLIDES:
        r = cfg.custom_slides().make_slide(sid, S)
        if r is not None:
            return r
    raise KeyError(f'E20 slide id not defined: {sid}')
