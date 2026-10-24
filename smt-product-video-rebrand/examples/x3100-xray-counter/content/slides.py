"""X3100 custom slides (drawn in code). The engine calls make_slide(sid, S) for any slide id that is
not 'blank' and not in the batch's SLIDES dict. Return a list of PIL images (build steps) or None.
New products: prefer data-driven SLIDES in the batch module; write code here only for bespoke diagrams."""
import math
from PIL import Image, ImageDraw
from gfx import *          # engine primitives: F, hexa, C, wrap, slide_base, rows_slide, flow_slide, grid_slide, ic_* ...
import gfx
from gfx import _i

def method_icon(kind):
    def f(im, d, y, S=None):
        return y
    return f

def compare_table(S):
    im, d, y = slide_base(S, 'COMPARISON', 'Four ways to count SMD parts')
    cols = ['Hand', 'Tape wheel', 'Weighing', 'X-ray']
    rowsd = [('No opening', ['–', '–', '±', '+']), ('Several reels at once', ['–', '–', '–', '+']), ('Reads reel ID', ['–', '–', '–', '+']),
             ('Trays, tubes, loose', ['±', '–', '+', '+']), ('Low investment', ['+', '+', '+', '–'])]
    x0 = int(90 * S); cw = int(215 * S); lw = int(360 * S)
    y += int(20 * S)
    fh = F('semi', 40, S)
    for i, c in enumerate(cols):
        cx = x0 + lw + i * cw + cw // 2
        for j, part in enumerate(c.split(' ')):
            d.text((cx - d.textlength(part, font=fh) / 2, y + j * int(48 * S)), part, font=fh, fill=hexa(C['gold'] if c == 'X-ray' else C['fg2']))
    y += int(130 * S)
    xr = x0 + lw + 3 * cw
    d.rounded_rectangle([xr + int(8 * S), y - int(150 * S), xr + cw - int(8 * S), y + len(rowsd) * int(170 * S)], radius=int(24 * S), outline=hexa(C['gold'], 200), width=max(1, int(4 * S)))
    for lab, vals in rowsd:
        d.line([(x0, y), (x0 + lw + 4 * cw, y)], fill=hexa(C['line2']), width=max(1, int(2 * S)))
        for i, ln in enumerate(wrap(d, lab, F('med', 44, S), lw - int(20 * S))):
            d.text((x0, y + int(30 * S) + i * int(52 * S)), ln, font=F('med', 44, S), fill=hexa(C['fg']))
        for i, vv in enumerate(vals):
            cx = x0 + lw + i * cw + cw // 2; cy = y + int(85 * S)
            col = {'+': C['ok'], '–': C['red'], '±': C['gold']}[vv]
            sym = {'+': '✓', '–': '✕', '±': '~'}[vv]
            r = int(36 * S)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hexa(col))
            colx = col; col = C['deep']
            fs = F('bold', 46, S)
            if sym == '✓':
                d.line([(cx - int(15 * S), cy), (cx - int(3 * S), cy + int(13 * S)), (cx + int(17 * S), cy - int(13 * S))], fill=hexa(col), width=max(1, int(7 * S)))
            elif sym == '✕':
                k = int(13 * S); d.line([(cx - k, cy - k), (cx + k, cy + k)], fill=hexa(col), width=max(1, int(7 * S))); d.line([(cx - k, cy + k), (cx + k, cy - k)], fill=hexa(col), width=max(1, int(7 * S)))
            else:
                d.line([(cx - int(16 * S), cy), (cx + int(16 * S), cy)], fill=hexa(col), width=max(1, int(7 * S)))
        y += int(170 * S)
    d.text((x0, int(1560 * S)), 'General comparison. Accuracy depends on parts and settings.', font=F('med', 38, S), fill=hexa(C['fg3']))
    return [im]

def method_slide(S, kind):
    titles = {'hand': ('01 · HAND COUNT', 'Counting by hand'), 'wheel': ('02 · TAPE-WHEEL COUNTER', 'Tape-wheel counter'), 'scale': ('03 · WEIGHING', 'Counting by weight')}
    k, hd = titles[kind]
    im, d, y = slide_base(S, k, hd)
    cx, cy = int(700 * S), int(860 * S)
    if kind == 'hand':
        reel(d, cx, cy - int(60 * S), int(300 * S), S)
        for i, t in enumerate(['1', '2', '3', '…']):
            d.text((int(260 * S) + i * int(250 * S), int(1250 * S)), t, font=F('black', 120, S), fill=hexa(C['fg3']))
        d.text((int(90 * S), int(1440 * S)), 'One part at a time, by eye', font=F('semi', 56, S), fill=hexa(C['fg2']))
    elif kind == 'wheel':
        reel(d, int(420 * S), cy, int(240 * S), S)
        wx, wy = int(1000 * S), cy + int(60 * S)
        d.rounded_rectangle([wx - int(170 * S), wy - int(170 * S), wx + int(170 * S), wy + int(170 * S)], radius=int(30 * S), outline=hexa(C['fg2']), width=max(1, int(8 * S)))
        d.ellipse([wx - int(90 * S), wy - int(90 * S), wx + int(90 * S), wy + int(90 * S)], outline=hexa(C['gold']), width=max(1, int(10 * S)))
        d.line([(int(420 * S), cy + int(240 * S)), (wx - int(90 * S), wy + int(90 * S))], fill=hexa(C['gold']), width=max(1, int(10 * S)))
        d.text((wx - int(150 * S), wy - int(320 * S)), '0 1 5 2 2', font=F('mono', 64, S), fill=hexa(C['brand2']))
        d.text((int(90 * S), int(1440 * S)), 'Tape pulled through, one reel at a time', font=F('semi', 56, S), fill=hexa(C['fg2']))
    else:
        px0, px1, py = int(300 * S), int(1100 * S), int(1080 * S)
        d.rounded_rectangle([px0, py, px1, py + int(60 * S)], radius=int(20 * S), fill=hexa(C['fg3']))
        d.rounded_rectangle([px0 + int(80 * S), py + int(60 * S), px1 - int(80 * S), py + int(260 * S)], radius=int(20 * S), outline=hexa(C['fg3']), width=max(1, int(8 * S)))
        d.rounded_rectangle([int(560 * S), py + int(110 * S), int(840 * S), py + int(210 * S)], radius=int(10 * S), fill=hexa(C['deep']))
        d.text((int(585 * S), py + int(115 * S)), '----- g', font=F('mono', 56, S), fill=hexa(C['ok']))
        reel(d, int(700 * S), py - int(250 * S), int(240 * S), S)
        d.text((int(90 * S), int(1440 * S)), 'Count estimated from weight', font=F('semi', 56, S), fill=hexa(C['fg2']))
    return [im]

def tray_slide(S):
    im, d, y = slide_base(S, 'STEP 2 · X-RAY SHOT', 'One image, four reels')
    x0, y0, sz = int(210 * S), int(480 * S), int(980 * S)
    d.rounded_rectangle([x0, y0, x0 + sz, y0 + sz], radius=int(30 * S), fill=hexa('#0a0f0e'), outline=hexa(C['brand2']), width=max(1, int(6 * S)))
    r = int(230 * S)
    for i, (gx, gy) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
        cx = x0 + sz // 4 + gx * sz // 2; cy = y0 + sz // 4 + gy * sz // 2
        reel(d, cx, cy, r, S, col=C['fg2'])
        d.text((cx - int(20 * S), cy - int(40 * S)), str(i + 1), font=F('black', 70, S), fill=hexa(C['gold']))
    d.text((x0, y0 + sz + int(30 * S)), '427 x 427 mm flat panel · 3072 x 3072 px', font=F('semi', 50, S), fill=hexa(C['brand3']))
    return [im]

def _make_slide_b1(sid, S):
    if sid == 'methods': return compare_table(S)
    if sid in ('hand', 'wheel', 'scale'): return method_slide(S, sid)
    if sid == 'tray': return tray_slide(S)
    if sid == 'costperreel':
        return formula_slide(S, 'DECIDE ON NUMBERS', 'Cost per reel, per method', [
            ('Minutes per reel', 'measured, not brochure'), ('× reels per month', 'your volume'), ('× labour cost per hour', 'your rate'), ('+ cost of errors left behind', 'line stops, freight, audits')])
    if sid == 'checklist':
        return rows_slide(S, 'BUYER CHECKLIST', 'X-ray counter: 8 checks', ['Smallest part size', 'Reel and package range', 'Speed at your peak', 'Barcode and MES link', 'Offline or inline', 'Radiation safety', 'Software and records', 'Installation and service'], numbered=True)[-1:] \
            if False else rows_slide_compact(S)
    if sid == 'safety' or sid == 'dose':
        return big_stat_slide(S, 'RADIATION SAFETY', 'Test value at the cabinet', '< 1', 'µSv/h radiation test value', 'Source: X3100 brochure and operation manual')
    if sid == 'service':
        return rows_slide(S, 'AFTER DELIVERY', 'What Southern Machinery does', ['Installation and set-up, on site or remote', 'Operator training in English', 'MES / ERP / WMS link agreed with IT', 'Whole-line SMT / THT support'])
    if sid == 'fivefacts':
        return rows_slide(S, 'BEFORE YOU ORDER', 'Five facts for the right proposal', ['Reels per day and size mix', 'Smallest part and packages', 'MES / ERP / WMS and label format', 'Mains voltage', 'Floor space and route in'], numbered=True)
    if sid == 'tube':
        return formula_slide(S, 'THE SOURCE', 'Closed X-ray tube', [('Tube type', 'Closed'), ('Voltage', '80 kV, limited to 50 kV'), ('Current', '0.01 – 0.089 mA'), ('Spatial resolution', '30 µm')])
    if sid == 'circuits':
        return rows_slide(S, 'SAFETY CIRCUITS', 'Layers that stop X-ray', ['Door interlocks 1 and 2', 'Double safety circuit', 'Over-voltage / over-current protection', 'Emergency stop', 'Anti-pinch sensor'])
    if sid == 'rules':
        return rows_slide(S, 'OPERATING RULES', 'From the X3100 manual', ['Only trained staff operate it', 'Door never opened while X-ray is on', 'Interlocks and warning labels stay in place', 'Safety lock checked every day'])
    if sid == 'training':
        return rows_slide(S, 'YOUR COUNTRY', 'Registration and training', ['Local registration rules for X-ray equipment apply', 'X-ray safety rules in operator training', 'Remote set-up and training in English'])
    if sid == 'power':
        return formula_slide(S, 'SITE PLANNING', 'Power, size and weight', [('Power', 'AC 110–220 V · 50–60 Hz · 1200 W'), ('Offline cabinet', '734 x 1456 x 1934 mm'), ('With printer', '949 mm long'), ('Weight', '450 kg')])
    if sid == 'care':
        return rows_slide(S, 'MAINTENANCE CARD', 'Daily and monthly care', ['Daily: no dust, water or oil in or on the cabinet', 'Daily: test safety lock and interlocks', 'Power and ground tight; cabinet earthed', 'Monthly: clean and re-oil guide rails', 'Keep 5 cm free at fan exhausts'])
    if sid == 'faults':
        return formula_slide(S, 'FAULT TO CHECK', 'Software first, settings second', [('Wrong count', '→ adjust brightness'), ('No barcode read', '→ auto scan + code type'), ('Panel / X-ray init failure', '→ restart the software'), ('Not confirmed', '→ tag it, call service')])
    if sid == 'askplan':
        return rows_slide(S, 'ASK US', 'Quoted per order', ['Price and lead time', 'Warranty and service terms', 'Running cost and service plan for your version'])
    if sid == 'tally':
        return formula_slide(S, 'STEP 1 · MEASURE', 'One week at the return shelf', [('Reels per day', 'tally sheet'), ('Minutes per reel', 'start and end time'), ('Method', 'hand · tape wheel · scale'), ('Share counted at all', '% of returned reels')])
    if sid == 'formula':
        return formula_slide(S, 'STEP 2 · FORMULA', 'Payback from your numbers', [('Hours freed per month', 'hand-counted reels × min ÷ 60'), ('Labour value', 'hours × your labour rate'), ('Minus X3100 time', 'load + label minutes'), ('Payback', 'quoted price ÷ net value / month')], hl_last=True)
    if sid == 'ex1':
        return formula_slide(S, 'EXAMPLE · ASSUMPTIONS', 'For example, assume…', [('Reels per month', '4,000'), ('Counted by hand today', '75% = 3,000 reels'), ('Minutes per reel · labour', '3 min · $10 per hour'), ('Hand counting today', '150 h = $1,500 / month')], foot='Example assumptions only. Your numbers will differ.', hl_last=True)
    if sid == 'ex2':
        return formula_slide(S, 'EXAMPLE · X3100 TIME', 'Subtract the X3100 handling', [('Handling at the X3100', 'assume 0.5 min per reel'), ('3,000 reels × 0.5 min', '25 h = $250 / month'), ('Net value per month', '$1,500 – $250 = $1,250')], foot='Example assumptions only. Your numbers will differ.', hl_last=True)
    if sid == 'ex3':
        return formula_slide(S, 'EXAMPLE · PAYBACK', 'Quoted price ÷ net value', [('Net value (example)', '$1,250 per month'), ('Per $10,000 of quoted price', '10,000 ÷ 1,250 = 8 months')], foot='Labour only, example assumptions. Southern Machinery publishes no savings figure; price is quoted per order.', hl_last=True)
    if sid == 'sendnumbers':
        return rows_slide(S, 'YOUR NUMBERS', 'Send these three numbers', ['Reels per month', 'Minutes per reel today', 'Labour cost per hour'], numbered=True)
    raise KeyError(sid)

def rows_slide_compact(S):
    items = ['Smallest part size', 'Reel and package range', 'Speed at your peak', 'Barcode and MES link', 'Offline or inline', 'Radiation safety', 'Software and records', 'Installation and service']
    builds = []
    for n in (2, 4, 6, 8):
        im, d, y = slide_base(S, 'BUYER CHECKLIST', 'X-ray counter: 8 checks')
        for i, t in enumerate(items[:n]):
            bh = int(118 * S)
            d.rounded_rectangle([int(90 * S), y, int(1310 * S), y + bh], radius=int(20 * S), fill=hexa(C['card'], 230), outline=hexa(C['line2']), width=max(1, int(3 * S)))
            d.text((int(130 * S), y + int(28 * S)), str(i + 1).zfill(2), font=F('mono', 54, S), fill=hexa(C['gold']))
            d.text((int(280 * S), y + int(30 * S)), t, font=F('semi', 54, S), fill=hexa(C['fg']))
            y += bh + int(18 * S)
        builds.append(im)
    return builds

def ghost_slide(S):
    im, d, y = slide_base(S, 'GHOST INVENTORY', 'System vs shelf')
    y += _i(20, S)
    for j, (lab, num, col, sub) in enumerate([('ERP / MES', '5,000', C['brand3'], 'parts on record'), ('ON THE SHELF', '1,200', C['red'], 'parts on the reel')]):
        yy = y + j * _i(520, S)
        d.rounded_rectangle([_i(X0, S), yy, _i(X1, S), yy + _i(440, S)], radius=_i(30, S), fill=hexa(C['card'], 240), outline=hexa(col, 220), width=max(1, _i(5, S)))
        spaced(d, (_i(X0 + 60, S), yy + _i(50, S)), lab, F('mono', 44, S), hexa(col), _i(4, S))
        d.text((_i(X0 + 60, S), yy + _i(130, S)), num, font=F('black', 190, S), fill=hexa(C['fg']))
        d.text((_i(X0 + 60, S), yy + _i(350, S)), sub, font=F('med', 44, S), fill=hexa(C['fg3']))
        if j == 0:
            # tiny database icon
            cx, cy = _i(1120, S), yy + _i(220, S)
            for k in range(3):
                d.ellipse([cx - _i(90, S), cy - _i(110, S) + k * _i(70, S), cx + _i(90, S), cy - _i(60, S) + k * _i(70, S)], outline=hexa(col), width=max(1, _i(6, S)))
        else:
            reel(d, _i(1120, S), yy + _i(220, S), _i(140, S), S)
    d.text((_i(X0, S), _i(1530, S)), 'Illustration — numbers for example only', font=F('med', 38, S), fill=hexa(C['fg3']))
    return [im]

def mbb_slide(S):
    im, d, y = slide_base(S, 'MOISTURE-SENSITIVE DEVICES', 'Opening the bag costs floor life')
    cx, cy = _i(700, S), _i(900, S)
    w, h = _i(640, S), _i(760, S)
    d.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], radius=_i(40, S), fill=hexa('#1a2a28', 230), outline=hexa(C['brand3']), width=max(1, _i(8, S)))
    d.line([(cx - w // 2, cy - h // 2 + _i(70, S)), (cx + w // 2, cy - h // 2 + _i(70, S))], fill=hexa(C['brand3']), width=max(1, _i(6, S)))
    reel(d, cx, cy + _i(30, S), _i(230, S), S)
    d.rounded_rectangle([cx - _i(200, S), cy + _i(290, S), cx + _i(200, S), cy + _i(350, S)], radius=_i(10, S), fill=hexa(C['fg2']))
    # clock
    kx, ky, kr = _i(1130, S), _i(560, S), _i(120, S)
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=hexa(C['card']), outline=hexa(C['gold']), width=max(1, _i(8, S)))
    d.line([(kx, ky), (kx, ky - _i(80, S))], fill=hexa(C['gold']), width=max(1, _i(8, S)))
    d.line([(kx, ky), (kx + _i(60, S), ky + _i(30, S))], fill=hexa(C['gold']), width=max(1, _i(8, S)))
    d.text((_i(X0, S), _i(1400, S)), 'Opened  →  floor-life clock starts', font=F('semi', 52, S), fill=hexa(C['gold']))
    d.text((_i(X0, S), _i(1480, S)), 'Then: bake or re-seal before returning to stock', font=F('med', 44, S), fill=hexa(C['fg2']))
    return [im]

def vt_slide(S):
    im, d, y = slide_base(S, 'THE MECHANISM', 'Threshold voltage can shift')
    # two distributions (programmed vs erased) with a shift arrow
    x0, x1 = _i(X0 + 30, S), _i(X1 - 30, S)
    base = _i(1250, S)
    d.line([(x0, base), (x1, base)], fill=hexa(C['fg3']), width=max(1, _i(4, S)))
    def curve(mu, col, sig=0.07, amp=480):
        pts = []
        for i in range(201):
            t = i / 200
            yv = math.exp(-((t - mu) ** 2) / (2 * sig ** 2))
            pts.append((x0 + (x1 - x0) * t, base - _i(amp, S) * yv))
        d.line(pts, fill=hexa(col), width=max(1, _i(9, S)))
    curve(0.22, C['brand3'])
    curve(0.72, C['gold'])
    curve(0.6, C['red'], sig=0.09, amp=380)
    ref = x0 + int((x1 - x0) * 0.47)
    for yy in range(base - _i(560, S), base, _i(40, S)):
        d.line([(ref, yy), (ref, yy + _i(20, S))], fill=hexa(C['fg2']), width=max(1, _i(4, S)))
    d.text((x0, base + _i(30, S)), 'erased  "1"', font=F('semi', 44, S), fill=hexa(C['brand3']))
    t = 'programmed  "0"'
    d.text((x1 - d.textlength(t, font=F('semi', 44, S)), base + _i(30, S)), t, font=F('semi', 44, S), fill=hexa(C['gold']))
    d.text((ref - _i(120, S), base - _i(620, S)), 'read level', font=F('med', 38, S), fill=hexa(C['fg2']))
    d.text((_i(X0, S), _i(1400, S)), 'High dose: programmed cells drift (red)', font=F('semi', 48, S), fill=hexa(C['red']))
    d.text((_i(X0, S), _i(1470, S)), 'and can read as the wrong value.', font=F('semi', 48, S), fill=hexa(C['fg2']))
    d.text((_i(X0, S), _i(1580, S)), 'Schematic illustration, after NXP AN13412 / SkyHigh AN98527', font=F('med', 34, S), fill=hexa(C['fg3']))
    return [im]

def lightsout_slide(S):
    builds = []
    nodes = [('AGV / conveyor', 'brings reels in'), ('X3100 Inline', 'counts + labels'), ('Smart shelf', 'reel storage')]
    for k in range(1, 5):
        im, d, y = slide_base(S, 'INTEGRATION CONCEPT', 'A lights-out reel flow')
        # MES bar
        my = y + _i(20, S)
        if k >= 4:
            d.rounded_rectangle([_i(X0, S), my, _i(X1, S), my + _i(150, S)], radius=_i(26, S), fill=hexa(C['brand'], 240), outline=hexa(C['gold']), width=max(1, _i(4, S)))
            t = 'MES / WMS directs the flow'
            d.text(((_i(X0, S) + _i(X1, S) - d.textlength(t, font=F('bold', 56, S))) / 2, my + _i(42, S)), t, font=F('bold', 56, S), fill=hexa('#ffffff'))
        ny = my + _i(260, S)
        bh = _i(250, S)
        for i, (a, b) in enumerate(nodes[:min(k, 3)]):
            yy = ny + i * (bh + _i(90, S))
            gold = i == 1
            d.rounded_rectangle([_i(X0 + 120, S), yy, _i(X1 - 120, S), yy + bh], radius=_i(30, S), fill=hexa(C['card'], 240), outline=hexa(C['gold'] if gold else C['line2']), width=max(1, _i(5 if gold else 3, S)))
            fa = F('black', 66, S); fb = F('med', 46, S)
            cx = _i(700, S)
            d.text((cx - d.textlength(a, font=fa) / 2, yy + _i(55, S)), a, font=fa, fill=hexa(C['gold'] if gold else C['fg']))
            d.text((cx - d.textlength(b, font=fb) / 2, yy + _i(150, S)), b, font=fb, fill=hexa(C['fg3']))
            if i < min(k, 3) - 1:
                arrow_down(d, cx, yy + bh + _i(8, S), yy + bh + _i(82, S), S)
            if k >= 4:
                d.line([(_i(X0 + 60, S), my + _i(150, S)), (_i(X0 + 60, S), yy + bh // 2), (_i(X0 + 120, S), yy + bh // 2)], fill=hexa(C['gold'], 160), width=max(1, _i(4, S)))
        d.text((_i(X0, S), _i(1590, S)), 'Concept only — engineered per project with your automation partners', font=F('med', 34, S), fill=hexa(C['fg3']))
        builds.append(im)
    return builds

def mesflow_slide(S, kicker, heading):
    builds = []
    for k in range(1, 4):
        im, d, y = slide_base(S, kicker, heading)
        y += _i(30, S)
        # left: reel + label ; right: system
        bw = _i(520, S); bh = _i(380, S)
        lx, rx = _i(X0, S), _i(X1, S) - bw
        d.rounded_rectangle([lx, y, lx + bw, y + bh], radius=_i(30, S), fill=hexa(C['card'], 240), outline=hexa(C['line2']), width=max(1, _i(3, S)))
        reel(d, lx + _i(170, S), y + bh // 2, _i(120, S), S)
        # barcode
        bx = lx + _i(320, S)
        for i in range(16):
            ww = _i(4 + (i * 7) % 9, S)
            d.rectangle([bx + i * _i(11, S), y + _i(130, S), bx + i * _i(11, S) + ww // 2, y + _i(250, S)], fill=hexa(C['fg']))
        d.text((lx + _i(40, S), y + bh - _i(70, S)), 'REEL ID + QTY', font=F('mono', 36, S), fill=hexa(C['gold']))
        if k >= 2:
            arrow_right(d, lx + bw + _i(20, S), rx - _i(20, S), y + bh // 2, S, C['gold'])
            d.rounded_rectangle([rx, y, rx + bw, y + bh], radius=_i(30, S), fill=hexa(C['brand'], 240), outline=hexa(C['gold']), width=max(1, _i(4, S)))
            for j, t in enumerate(['MES', 'ERP', 'WMS']):
                d.text((rx + _i(60, S), y + _i(50, S) + j * _i(105, S)), t, font=F('black', 80, S), fill=hexa('#ffffff'))
        if k >= 3:
            yy = y + bh + _i(80, S)
            rows = [('Barcode read', '20 MP camera'), ('Count', 'up to 4 reels per shot'), ('Upload', 'fields agreed with IT'), ('Label', 'built-in printer')]
            for i, (a, b) in enumerate(rows):
                ry = yy + i * _i(150, S)
                d.rounded_rectangle([_i(X0, S), ry, _i(X1, S), ry + _i(125, S)], radius=_i(20, S), fill=hexa(C['card'], 230), outline=hexa(C['line2']), width=max(1, _i(2, S)))
                d.text((_i(X0 + 40, S), ry + _i(34, S)), a, font=F('bold', 50, S), fill=hexa(C['fg']))
                d.text((_i(X1 - 40, S) - d.textlength(b, font=F('med', 44, S)), ry + _i(40, S)), b, font=F('med', 44, S), fill=hexa(C['brand3']))
        builds.append(im)
    return builds

def interlock_slide(S):
    builds = []
    for k in range(1, 4):
        im, d, y = slide_base(S, 'MES INTERLOCK · EXAMPLE', 'No count, no release')
        y += _i(30, S)
        cx = _i(700, S)
        # node 1
        def box(yy, t, sub, col):
            d.rounded_rectangle([_i(X0 + 80, S), yy, _i(X1 - 80, S), yy + _i(200, S)], radius=_i(30, S), fill=hexa(C['card'], 240), outline=hexa(col), width=max(1, _i(4, S)))
            d.text((cx - d.textlength(t, font=F('bold', 60, S)) / 2, yy + _i(40, S)), t, font=F('bold', 60, S), fill=hexa(C['fg']))
            d.text((cx - d.textlength(sub, font=F('med', 42, S)) / 2, yy + _i(118, S)), sub, font=F('med', 42, S), fill=hexa(C['fg3']))
        box(y, 'Reel returns from line', 'scanned at the counter', C['line2'])
        if k >= 2:
            arrow_down(d, cx, y + _i(210, S), y + _i(300, S), S)
            # diamond
            dy = y + _i(310, S); r = _i(190, S)
            d.polygon([(cx, dy), (cx + int(r * 1.6), dy + r), (cx, dy + 2 * r), (cx - int(r * 1.6), dy + r)], fill=hexa(C['brand'], 240), outline=hexa(C['gold']), width=max(1, _i(4, S)))
            t = 'Count received?'
            d.text((cx - d.textlength(t, font=F('bold', 54, S)) / 2, dy + r - _i(34, S)), t, font=F('bold', 54, S), fill=hexa('#ffffff'))
        if k >= 3:
            by = y + _i(310, S) + 2 * _i(190, S) + _i(90, S)
            for j, (t, col, sub) in enumerate([('YES', C['ok'], 'release to stock'), ('NO', C['red'], 'hold the reel')]):
                x0 = _i(X0, S) + j * _i(640, S)
                d.rounded_rectangle([x0, by, x0 + _i(580, S), by + _i(260, S)], radius=_i(30, S), fill=hexa(C['card'], 240), outline=hexa(col), width=max(1, _i(5, S)))
                d.text((x0 + _i(50, S), by + _i(40, S)), t, font=F('black', 90, S), fill=hexa(col))
                d.text((x0 + _i(50, S), by + _i(160, S)), sub, font=F('semi', 46, S), fill=hexa(C['fg2']))
            arrow_down(d, _i(X0 + 290, S), by - _i(120, S), by - _i(10, S), S, C['ok'])
            arrow_down(d, _i(X0 + 930, S), by - _i(120, S), by - _i(10, S), S, C['red'])
        d.text((_i(X0, S), _i(1590, S)), 'Example rule configured in your MES; the X3100 supplies the count', font=F('med', 34, S), fill=hexa(C['fg3']))
        builds.append(im)
    return builds

def _make_slide_b2(sid, S):
    if sid == 'mesflow':
        return mesflow_slide(S, 'DATA FLOW', 'From the reel to your system')
    if sid == 'mesflow2':
        return mesflow_slide(S, 'FIX 3 · RECORDS', 'The system holds the truth')
    if sid == 'interlock':
        return interlock_slide(S)
    if sid == 'csvlog':
        return table_slide(S, 'DAILY RECORD · SAMPLE LAYOUT', 'Every count saved', ['TIME', 'REEL ID', 'QTY'],
                           [('08:02', 'R-240117-0031', '3,855'), ('08:02', 'R-240117-0032', '306'), ('08:03', 'R-240117-0047', '1,624'), ('08:03', 'R-240117-0050', '10,000'), ('08:05', 'R-240117-0063', '3,794'), ('08:05', 'R-240117-0064', '849')],
                           foot='Illustrative layout. Saved daily as TXT, CSV or XLS; fields agreed per order.', widths=[1, 2.2, 1.2])
    if sid == 'csvlog2':
        return table_slide(S, 'STOCKTAKE REPORT · SAMPLE', 'Counted, not estimated', ['LOCATION', 'REEL ID', 'QTY'],
                           [('A-01-03', 'R-0031', '3,855'), ('A-01-04', 'R-0032', '306'), ('A-02-01', 'R-0047', '1,624'), ('A-02-02', 'R-0050', '10,000'), ('B-01-01', 'R-0063', '3,794')],
                           foot='Illustrative layout from daily TXT / CSV / XLS records.', widths=[1.4, 1.4, 1.2])
    if sid == 'itlist':
        return flow_slide(S, 'INTEGRATION CALL', 'What to bring', [('Your MES / ERP / WMS', 'system and version'), ('Barcode format', 'on incoming reel labels'), ('Label layout', 'what the new label shows'), ('Data per reel', 'fields to upload'), ('Remote set-up', 'training in English')], hl=4)
    if sid == 'usecases':
        return grid_slide(S, 'INSPECTION MODE', 'When to take a look inside', [('', 'Suspicious batch at goods-in'), ('', 'Supplier lot under question'), ('', 'Cables and parts: broken wires?'), ('', 'First check before deeper analysis')],
                          icons=[ic_reel, ic_chip, ic_cable, ic_tray])
    if sid == 'limits':
        return split_slide(S, 'KNOW THE LIMITS', 'What it is, and is not', ('IT IS', ['A component counter', 'With X-ray inspection mode', 'Shows hidden faults such as broken wires']),
                           ('IT IS NOT', ['A dedicated inspection X-ray system', 'A promise for BGA voids or solder joints', 'Send samples: we test']))
    if sid == 'dose2':
        return big_stat_slide(S, 'SAFETY', 'Radiation test value at the cabinet', '< 1', 'µSv/h at the cabinet', 'Closed tube: 80 kV, limited to 50 kV · 0.01–0.089 mA')
    if sid == 'invsoff':
        return split_slide(S, 'COMPARE', 'Offline vs Inline', ('OFFLINE', ['Operator loads the tray', 'Up to 4 reels per shot', '6–10 s per 4 reels (0201)', 'Reels, tubes, bags, loose parts']),
                           ('INLINE', ['Automatic loading', 'One reel at a time', 'About 9–15 s per reel', 'Auto label and unload']), foot='Both: 20 MP barcode camera · MES / ERP / WMS · daily records')
    if sid == 'lightsout':
        return lightsout_slide(S)
    if sid == 'choose':
        return flow_slide(S, 'YOUR PATH', 'Start where the reels are', [('Offline at goods-in', 'incoming reels, IQC'), ('Offline at returns', 'recount before stock'), ('Inline as volume grows', 'automatic cycle'), ('Connect to automation', 'AGV, shelves, MES / WMS')], hl=2)
    if sid == 'stocktake':
        return grid_slide(S, 'MONTHLY STOCKTAKE', 'The usual routine', [('', 'Reels pulled off the shelves'), ('', 'Counted by hand'), ('', 'Quantities typed in'), ('', 'Lines wait')], icons=[ic_reel, ic_loose, ic_tape, ic_tray])
    if sid == 'stockcalc':
        return formula_slide(S, 'EXAMPLE CALCULATION', 'Assume 2,000 reels', [('Reels to count (assumption)', '2,000'), ('Shots of 4 reels', '2,000 ÷ 4 = 500 shots'), ('X-ray time at 10 s per shot', '500 × 10 s ≈ 83 min'), ('Plus your handling time', 'loading + labeling, site-specific')],
                             foot='Example only, not a guarantee. 6–10 s per 4 reels is the brochure figure for 0201 chips (offline).', hl_last=True)
    if sid == 'yourstock':
        return grid_slide(S, 'YOUR ESTIMATE', 'Send us three things', [('01', 'Reels in stock'), ('02', 'Part and reel size mix'), ('03', 'A few reels for a trial count'), ('→', 'We calculate with your numbers')])
    if sid == 'packages':
        return grid_slide(S, 'PACKAGES', 'Beyond full reels', [('', '01005 chips'), ('', 'Tubes'), ('', 'Trays'), ('', 'Bags'), ('', 'Loose parts'), ('', 'Cut tape')],
                          icons=[ic_chip, ic_tube, ic_tray, ic_bag, ic_loose, ic_tape])
    if sid == 'res01005':
        return big_stat_slide(S, 'SMALLEST PARTS', 'Down to 01005', '01005', 'smallest chip size counted', '3072 x 3072 px flat panel · 30 µm spatial resolution')
    if sid == 'accuracy':
        return big_stat_slide(S, 'ACCURACY', 'Brochure example', '99.99%', 'example figure from the brochure', 'Depends on part, package and settings — test with your own reels')
    if sid == 'sendsamples':
        return flow_slide(S, 'FREE TEST COUNT', 'How the test works', [('Send your hardest parts', 'chips, tubes, trays, loose'), ('We count them', 'on the X3100'), ('You get the result', 'images and counts'), ('Decide on facts', 'not brochure numbers')], hl=3)
    if sid == 'mbb':
        return mbb_slide(S)
    if sid == 'msdsteps':
        return split_slide(S, 'MSD HANDLING', 'Counting: open vs X-ray', ('OPEN TO COUNT', ['Bag opened', 'Floor-life clock starts', 'Bake or re-seal may follow', 'More handling']),
                           ('X-RAY COUNT', ['Bag stays closed', 'No opening just to count', 'No re-bake or re-seal from counting', 'Less handling']), foot='Confirm with your own packaging and procedure.')
    if sid == 'testmsd':
        return flow_slide(S, 'TRY IT FIRST', 'Test with your dry packs', [('Send a sealed reel', 'in your usual dry pack'), ('We count it closed', 'through bag and tape'), ('You review the result', 'before changing procedure')], hl=1)
    if sid == 'newpart':
        return flow_slide(S, 'NEW PART TYPE', 'Checking a new part', [('Load and start', 'as usual'), ('Check the image', 'are parts clearly visible?'), ('Check the count', 'plausible for this reel?'), ('Adjust if needed', 'with remote engineer support')], hl=3)
    if sid == 'training2':
        return grid_slide(S, 'SUPPORT', 'Remote, in English', [('Remote', 'installation and set-up'), ('English', 'operator training'), ('Your parts', 'learn on your own reels'), ('Since 2011', 'Southern Machinery, Shenzhen')])
    if sid == 'ghost':
        return ghost_slide(S)
    if sid == 'ghostsrc':
        return flow_slide(S, 'ROOT CAUSES', 'Where ghost stock comes from', [('Returns not recounted', 'label quantity assumed'), ('Short incoming reels', 'less than the label says'), ('Typed quantities', 'one typo, wrong stock'), ('Result', 'system and shelf disagree')], hl=3)
    if sid == 'ghostcheck':
        return flow_slide(S, 'FIRST STEP', 'Measure before you invest', [('Pick returned reels', 'a normal week'), ('Count them', 'trial count with us'), ('Compare with ERP', 'how far off?'), ('Choose counting points', 'goods-in and returns')], hl=3)
    if sid == 'vtshift':
        return vt_slide(S)
    if sid == 'dosefactors':
        return bars_slide(S, 'DOSE', 'What drives the dose', [('Tube voltage', 0.3, 'keep as low as practical'), ('Tube current', 0.3, 'keep as low as practical'), ('Exposure time', 0.3, 'keep as short as practical'), ('Distance + filtering', 0.3, 'per maker guidance')],
                          foot='General guidance from component makers (NXP AN13412, SkyHigh AN98527). Bars are schematic.')
    if sid == 'tube2':
        return formula_slide(S, 'X3100 SOURCE', 'Closed X-ray tube', [('Rated', '80 kV'), ('Limited to', '50 kV'), ('Tube current', '0.01 – 0.089 mA'), ('Exposure', 'one short shot per count')], hl_last=False)
    if sid == 'studies':
        return split_slide(S, 'PUBLISHED STUDIES', 'What the research reports', ('HIGHER RISK', ['Higher dose', 'Repeated exposure', 'Dense multi-level NAND', 'Pre-programmed data']),
                           ('LOWER RISK', ['Lower kV and current', 'Short exposure', 'Single count', 'Maker guidance followed']), foot='General findings; no dose figure is published for the X3100. Validate with your parts.')
    if sid == 'validate':
        return flow_slide(S, 'OUR ADVICE', 'Validate with your own parts', [('Count sample reels', 'on the X3100'), ('Test or read back', 'electrical / data check'), ('Ask the component maker', 'its X-ray limits'), ('Then roll out', 'with confidence')], hl=1)
    if sid == 'samples':
        return grid_slide(S, 'ASK US TO TEST', 'Send samples first', [('', 'Plastic parts'), ('', 'Metal parts'), ('', 'Wire harnesses'), ('', 'Composite parts')],
                          icons=[ic_plastic, ic_bolt, ic_cable, ic_honey], foot='No promises before a test — results depend on material and size.')
    if sid == 'twojobs':
        return split_slide(S, 'ONE CABINET', 'Two jobs', ('COUNT', ['Up to 4 reels per shot', 'Tubes, bags, loose parts', 'Barcode + label + MES']), ('INSPECT', ['Look inside parts', 'Hidden defects', 'Broken wires']))
    raise KeyError(sid)


def make_slide(sid, S):
    try:
        return _make_slide_b1(sid, S)
    except KeyError:
        pass
    try:
        return _make_slide_b2(sid, S)
    except KeyError:
        return None
