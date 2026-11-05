#!/usr/bin/env python3
"""Build one self-contained landing page.

usage: python3 build.py <workdir>
<workdir> must contain: config.yaml, page.py, i18n/<lang>.json for every configured language,
optional emb.json (inline images), optional model.glb (glb mode) or the procedural js.
Writes <workdir>/<page.filename>.
"""
import json, re, html, os, sys, base64, copy
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(HERE)

def load_yaml(p):
    try:
        import yaml
        return yaml.safe_load(open(p, encoding='utf8')) or {}
    except ImportError:
        return json.load(open(p.replace('.yaml', '.json'), encoding='utf8'))

def merge(a, b):
    out = copy.deepcopy(a)
    for k, v in (b or {}).items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out

W = os.path.abspath(sys.argv[1]) + '/'
CFG = merge(load_yaml(SK + '/config/default.yaml'), load_yaml(W + 'config.yaml'))
P = CFG['page']; FN = P['filename']; assert FN.endswith('.html'), 'page.filename required'
CANON = P['canonical_base'] + FN
L = [l[0] for l in CFG['languages']]
I = {l: json.load(open(W + f'i18n/{l}.json', encoding='utf8')) for l in L}
en = I[L[0]]
for l in L:
    miss = set(en) - set(I[l]); assert not miss, (l, sorted(miss)[:8])
e = lambda s: html.escape(str(s), quote=True)
EM = json.load(open(W + 'emb.json')) if os.path.exists(W + 'emb.json') else {}
PH = 'https://ph.smthelp.com/images/'

# helpers available inside page.py
def ph(p): return (PH + p, PH + re.sub(r'\.md\.', '.', p))          # (thumb, full) from ph.smthelp.com path
def emb(k): return (EM[k][0], EM[k][0])                               # inline image (dedupe later)
V = lambda k: ('k', k)                                                # value cell that is an i18n key
NS = dict(ph=ph, emb=emb, V=V, EM=EM, PH=PH, en=en, CFG=CFG, e=e)
exec(open(W + 'page.py', encoding='utf8').read(), NS)
g = lambda k, d=None: NS.get(k, d)

t = open(SK + '/templates/template.html', encoding='utf8').read()
HERO = g('HERO'); hw, hh = g('HERO_SIZE', (1200, 800))
t = t.replace('width="1400" height="928" fetchpriority="high"', f'width="{hw}" height="{hh}" fetchpriority="high"')
C = CFG['content']
# stations
st = ''
for i in range(1, C['station_count'] + 1):
    img = g('STATION_IMG', {}).get(i)
    phh = f'<img src="{img}" data-i18n-alt="st{i}_n" alt="" loading="lazy">' if img else f'<i class="fa-solid {g("STATION_ICON", {}).get(i, "fa-gear")}"></i>'
    st += f'<article class="card st reveal"><div class="ph">{phh}<span class="num">{i}</span></div><div class="bd"><h3 data-i18n="st{i}_n"></h3><p data-i18n="st{i}_d"></p><div class="f" data-i18n="st{i}_f"></div></div></article>'
cell = lambda v: f'<td data-i18n="{v[1]}"></td>' if isinstance(v, tuple) else f'<td>{e(v)}</td>'
bom = ''.join('<tr>' + ''.join((f'<td><b>{e(c)}</b></td>' if j == 0 else cell(c)) for j, c in enumerate(r)) + '</tr>' for r in g('TABLE_ROWS', []))
spec = ''
for title, rows in g('SPECS', []):
    tr = ''.join(f'<tr><td data-i18n="{k}"></td>{cell(v)}<td class="src" data-i18n="{s}"></td></tr>' for k, v, s in rows)
    spec += f'<div class="card reveal"><h3><span data-i18n="{title}"></span><span class="ev v" data-i18n="ev_ver"></span></h3><div style="overflow-x:auto"><table><tbody>{tr}</tbody></table></div></div>'
ND, TBC = g('DISC_COUNT', 0), set(g('DISC_TBC', []))
disc = ''.join(f'<tr><td><b data-i18n="d{i}t"></b>' + ('<br><span class="ev t" data-i18n="ev_tbc"></span>' if i in TBC else '') + f'</td><td data-i18n="d{i}a"></td><td data-i18n="d{i}b"></td><td data-i18n="d{i}n"></td></tr>' for i in range(1, ND + 1))
gal = ''.join(f'<figure class="reveal" data-full="{f}"><img src="{s}" data-i18n-alt="g{i}" alt="" loading="lazy" style="background:#fff;object-fit:contain"><figcaption data-i18n="g{i}"></figcaption></figure>' for i, (s, f) in enumerate(g('GALLERY', []), 1))
VID = g('VIDEOS', [])
vids = ''.join(f'<article class="card vid reveal" data-vid="{v}" tabindex="0" role="button"><div class="th"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" data-i18n-alt="v{i}t" alt="" loading="lazy"><div class="pl"><i class="fa-solid fa-play"></i></div></div><div class="bd"><h3 data-i18n="v{i}t"></h3></div></article>' for i, v in enumerate(VID, 1))
clips = ''.join(f'<article class="card vid clip reveal" data-drive="{v}" tabindex="0" role="button"><div class="th"><img src="https://drive.google.com/thumbnail?id={v}&amp;sz=w640" data-i18n-alt="c{i}t" alt="" loading="lazy"><div class="pl"><i class="fa-solid fa-play"></i></div></div><div class="bd"><h3 data-i18n="c{i}t"></h3></div></article>' for i, v in enumerate(g('CLIPS', []), 1))
ic = {'dl_pdf': 'fa-file-pdf', 'dl_man': 'fa-book', 'dl_3d': 'fa-cube'}
dls = ''.join(f'<a class="card dl reveal" href="{u}" target="_blank" rel="noopener"><i class="fa-solid {ic.get(k, "fa-file")}"></i><div><b>{e(n)}</b><span data-i18n="{k}"></span></div></a>' for n, u, k in g('DOWNLOADS', []))
NB, NSt = C['blog_count'], C['blog_steps']
blogs = ''
for i in range(1, NB + 1):
    full = ''.join(f'<h3 data-i18n="b{i}_h{j}"></h3><p data-i18n="b{i}_p{j}"></p>' for j in range(1, NSt + 1))
    blogs += f'<article class="card post reveal" id="article-{i}"><div class="meta"><span data-i18n="b{i}_c"></span><span data-i18n="b{i}_m"></span></div><h3 data-i18n="b{i}_t"></h3><p data-i18n="b{i}_x"></p><div class="full">{full}</div><button type="button" data-i18n="blog_read"></button></article>'
NF = C['faq_count']
faq = ''.join(f'<details class="reveal"><summary data-i18n="fq{i}"></summary><p data-i18n="fa{i}"></p></details>' for i in range(1, NF + 1))
# 3D viewer
M = CFG['model']
if M['mode'] == 'glb':
    v = open(SK + '/templates/viewer_glb.js', encoding='utf8').read()
    src = M.get('url') or ''
    if os.path.exists(W + 'model.glb') and (M['embed'] == 'inline' or (M['embed'] == 'auto' and os.path.getsize(W + 'model.glb') <= M['max_inline_kb'] * 1024)):
        src = 'data:model/gltf-binary;base64,' + base64.b64encode(open(W + 'model.glb', 'rb').read()).decode()
    assert src, 'glb mode: provide model.glb within max_inline_kb or model.url'
    VIEWER = v.replace('%%MODEL_SRC%%', src).replace('%%VIEWS_JSON%%', json.dumps(M['views']))
    NMODES = len(M['views'])
else:
    VIEWER = open(W + M['procedural_js'], encoding='utf8').read()
    NMODES = g('N_MODES', 1)
# JSON-LD
D = P.get('date_modified') or '2026-01-01'
org = {"@type": "Organization", "@id": "https://www.smthelp.com/#organization", "name": "Shenzhen Southern Machinery Sales and Service Co., Ltd.", "alternateName": "Southern Machinery", "url": "https://www.smthelp.com", "logo": "https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png", "foundingDate": "2011",
       "address": {"@type": "PostalAddress", "streetAddress": "Rm 1806, Block 3, Jinyun COFCO, Qianjin 2nd Road, Xixiang, Bao'an District", "addressLocality": "Shenzhen", "addressRegion": "Guangdong", "postalCode": "518102", "addressCountry": "CN"},
       "contactPoint": [{"@type": "ContactPoint", "telephone": "+86-13602562576", "email": "info@smthelp.com", "contactType": "sales"}],
       "sameAs": ["https://www.linkedin.com/company/smtmachine", "https://www.linkedin.com/in/smtsupplier", "https://twitter.com/smtspecialist", "https://www.facebook.com/autoinsertion", "https://www.youtube.com/c/Smthelping"]}
page = {"@type": "WebPage", "@id": CANON + "#webpage", "url": CANON, "name": en['meta_title'], "description": en['meta_desc'], "inLanguage": L, "publisher": {"@id": "https://www.smthelp.com/#organization"}, "primaryImageOfPage": P['og_image'], "dateModified": D,
        "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#top h1", "#top .sub", "#faq summary"]}}
faqld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": en[f'fq{i}'], "acceptedAnswer": {"@type": "Answer", "text": en[f'fa{i}']}} for i in range(1, NF + 1)]}
howto = {"@type": "HowTo", "name": en['st_h2'], "step": [{"@type": "HowToStep", "position": i, "name": en[f'st{i}_n'], "text": en[f'st{i}_d']} for i in range(1, C['station_count'] + 1)]}
posts = [{"@type": "BlogPosting", "headline": en[f'b{i}_t'], "description": en[f'b{i}_x'], "url": CANON + f"#article-{i}", "author": {"@type": "Person", "name": "Jason Wu", "url": "https://www.linkedin.com/in/smtsupplier"}, "publisher": {"@id": "https://www.smthelp.com/#organization"}, "datePublished": D, "inLanguage": "en", "about": g('BLOG_ABOUT', '')} for i in range(1, NB + 1)]
vidld = [{"@type": "VideoObject", "name": en[f'v{i}t'], "description": en[f'v{i}t'] + " - Southern Machinery", "thumbnailUrl": f"https://i.ytimg.com/vi/{v}/hqdefault.jpg", "embedUrl": f"https://www.youtube-nocookie.com/embed/{v}", "contentUrl": f"https://www.youtube.com/watch?v={v}", "uploadDate": "2024-01-01"} for i, v in enumerate(VID, 1)]
crumb = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.smthelp.com/"}, {"@type": "ListItem", "position": 2, "name": g('CRUMB_SECTION', 'Products'), "item": "https://www.smthelp.com/"}, {"@type": "ListItem", "position": 3, "name": g('CRUMB_NAME', en['hero_h1']), "item": CANON}]}
graph = [org, page] + ([g('PRODUCT_LD')] if g('PRODUCT_LD') else []) + [faqld, howto, crumb] + posts + vidld
LD = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace('</', '<\\/')
hl = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{CANON}{"" if l == L[0] else "?lang=" + l}">' for l in L) + f'\n<link rel="alternate" hreflang="x-default" href="{CANON}">'
TH = CFG['theme']
rep = {'%%STATIONS%%': st, '%%BOM%%': bom, '%%SPECS%%': spec, '%%DISC%%': disc, '%%GALLERY%%': gal, '%%VIDEOS%%': vids, '%%CLIPS%%': clips, '%%DOWNLOADS%%': dls, '%%BLOGS%%': blogs, '%%FAQ%%': faq,
       '%%JSONLD%%': LD, '%%HREFLANG%%': hl, '%%CANON%%': CANON, '%%IMG_HERO%%': HERO, '%%meta_title%%': e(en['meta_title']), '%%meta_desc%%': e(en['meta_desc']),
       '%%KEYWORDS%%': e(P['keywords']), '%%OG_IMAGE%%': P['og_image'], '%%OG_ALT%%': e(P['og_alt']), '%%CANVAS_ARIA%%': e(P['canvas_aria']), '%%FULL3D_URL%%': P['full3d_url'] or '#',
       '%%MAIL_TO%%': P['mail_to'], '%%MAIL_SUBJECT%%': P['mail_subject'].replace(' ', '%20'), '%%LS_PREFIX%%': P['ls_prefix'], '%%LANGS%%': json.dumps(CFG['languages'], ensure_ascii=False), '%%RTL%%': json.dumps(CFG.get('rtl_languages', [])),
       '%%CHATWOOT_TOKEN%%': CFG['chatwoot']['token'], '%%CHATWOOT_HOST%%': CFG['chatwoot']['host'], '%%C_PRIMARY%%': TH['primary'], '%%C_PRIMARY_DARK%%': TH['primary_dark'], '%%C_ACCENT%%': TH['accent'], '%%C_WARN%%': TH['warn'],
       '%%TOOL_HTML%%': g('TOOL_HTML', ''), '%%TOOL_JS%%': g('TOOL_JS', ''), '%%N_MODES%%': str(NMODES), '%%VIEWER3D%%': VIEWER}
for k, v in rep.items(): t = t.replace(k, v)
if not g('CLIPS'): t = re.sub(r'<h3 style="margin:34px 0 6px" data-i18n="vid_clips"></h3><p class="small" data-i18n="vid_clips_p"></p>\s*<div class="grid g4" style="margin-top:14px"></div>', '', t, count=1)
if not P['full3d_url']: t = re.sub(r'<div class="acts" style="margin-top:14px"><a class="btn btn-o" href="#".*?</a></div>', '', t, count=1, flags=re.S)
t = t.replace('%%I18N%%', json.dumps(I, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
t = re.sub(r'(data-i18n="(\w+)"[^>]*>)(</)', lambda m: m.group(1) + e(en.get(m.group(2), '')) + m.group(3), t)
t = re.sub(r'data-i18n-alt="(\w+)" alt=""', lambda m: f'data-i18n-alt="{m.group(1)}" alt="{e(en.get(m.group(1), ""))}"', t)
t = re.sub(r'data-i18n-aria="(\w+)" aria-label=""', lambda m: f'data-i18n-aria="{m.group(1)}" aria-label="{e(en.get(m.group(1), ""))}"', t)
left = re.findall(r'%%[A-Za-z0-9_]+%%', t); assert not left, left
# dedupe inline images: each data URI stored once in window.EMB
U = {}
for u in re.findall(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', t):
    U.setdefault(u, 'e%d' % len(U))
for u, k in U.items():
    t = t.replace(f'src="{u}"', f'src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" data-emb="{k}"').replace(f'data-full="{u}"', f'data-full="#{k}"')
if U:
    js = '<script>window.EMB=' + json.dumps({k: u for u, k in U.items()}) + ';document.querySelectorAll("img[data-emb]").forEach(function(i){i.src=EMB[i.getAttribute("data-emb")];});document.querySelectorAll("[data-full^=\'#\']").forEach(function(f){f.setAttribute("data-full",EMB[f.getAttribute("data-full").slice(1)]);});</script>'
    t = t.replace('<script>window.I18N=', js + '\n<script>window.I18N=', 1)
used = set(re.findall(r'data-i18n(?:-alt|-aria)?="(\w+)"', t))
print('missing keys', sorted(used - set(en)))
open(W + FN, 'w', encoding='utf8').write(t)
print(FN, len(t.encode()) // 1024, 'KB')
