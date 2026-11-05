#!/usr/bin/env python3
"""Build ONE self-contained English-first, 7-language landing page from job.json + content.json.

usage: build_lp.py <job.json> [--out file.html]

Everything (CSS, JS, images, 3D model, animation) is inlined. The only network requests are user-initiated:
YouTube iframes load on click, Chatwoot loads only on http/https, links open other pages.
Every text node carries data-i18n="<content path>" so translations in content.i18n.<lang>.<path> switch it.
"""
import os, sys, json, html, base64, io, re, argparse, urllib.request, mimetypes
sys.path.insert(0, os.path.dirname(__file__))
from common import load_job, W, SKILL

TPL = os.path.join(SKILL, 'templates', 'landing')
ap = argparse.ArgumentParser(); ap.add_argument('job'); ap.add_argument('--out'); a = ap.parse_args()
job = load_job(a.job); cfg = job['_cfg']; P = job['_P']; B = cfg['brand']
C = json.load(open(P(job['content']), encoding='utf8'))
E = lambda s: html.escape(str(s), quote=True)
EN = {}

def T(path, text, tag=None, attrs=''):
    """register an i18n string and return escaped text, optionally wrapped in a tag carrying data-i18n"""
    EN[path] = str(text)
    if tag is None: return f'<span data-i18n="{path}">{E(text)}</span>'
    return f'<{tag}{attrs} data-i18n="{path}">{E(text)}</{tag}>'

_cache = {}
def img(src, maxw=1400):
    """inline an image (local path or URL) as a data URI, resized to webp when Pillow is available"""
    if not src: return ''
    if src.startswith('data:'): return src
    if src in _cache: return _cache[src]
    if '://' in src:
        loc = W(job, 'assets', re.sub(r'[^A-Za-z0-9._-]', '_', src.split('/')[-1])[-80:] or 'img')
        if not os.path.exists(loc):
            req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
            open(loc, 'wb').write(urllib.request.urlopen(req, timeout=60).read())
    else:
        loc = P(src)
    raw = open(loc, 'rb').read()
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw)); keep_alpha = im.mode in ('RGBA', 'LA', 'P')
        im = im.convert('RGBA' if keep_alpha else 'RGB'); im.thumbnail((maxw, maxw))
        b = io.BytesIO(); im.save(b, 'WEBP', quality=80, method=6); uri = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    except Exception:
        uri = f'data:{mimetypes.guess_type(loc)[0] or "image/png"};base64,' + base64.b64encode(raw).decode()
    _cache[src] = uri; return uri

def sec(id_, inner, cls=''):
    return f'<section id="{id_}"{(" class=" + chr(34) + cls + chr(34)) if cls else ""}><div class="wrap">{inner}</div></section>\n'

def head_block(p, kicker, title, lead=None):
    h = T(f'{p}.kicker', kicker, 'span', ' class="kick"') + T(f'{p}.title', title, 'h2', ' class="sec"')
    if lead: h += T(f'{p}.lead', lead, 'p', ' class="lead"')
    return h

wa = f'https://wa.me/{B["whatsapp"]}'
S = {}
# ---------------- sections ----------------
def s_hero():
    h = C['hero']
    stats = ''.join(f'<div class="stat">{T(f"hero.stats.{i}.v", s["v"], "b")}{T(f"hero.stats.{i}.l", s["l"], "span")}</div>' for i, s in enumerate(h.get('stats', [])))
    ims = ''.join(f'<figure><img src="{img(x["src"])}" alt="{E(x["alt"])}" loading="eager">{T(f"hero.images.{i}.alt", x["alt"], "figcaption")}</figure>' for i, x in enumerate(h.get('images', [])[:2]))
    return (f'<section class="hero" id="top"><div class="wrap"><div>{T("hero.badge", h.get("badge", ""), "span", " class=\"vsb\"") if h.get("badge") else ""}'
            f'{T("hero.h1", h["h1"], "h1")}{T("hero.lead", h["lead"], "p", " class=\"lead\"")}'
            f'<div class="ctas"><a class="btn p" href="#{"duel" if C.get("duel") else "model3d"}">{T("ui.watch", h.get("cta_primary", "Watch the animation"))}</a>'
            f'<a class="btn g" href="{wa}?text={urllib.request.quote(h.get("wa_text", "Hi, I am interested in " + C["meta"]["product"]))}" target="_blank" rel="noopener">{T("ui.whatsapp", "WhatsApp an engineer")}</a></div>'
            f'<div class="stats">{stats}</div></div><div class="hph">{ims}</div></div></section>\n')

def s_duel():
    d = C.get('duel')
    if not d or not job.get('duel'): return ''
    sides = d['sides']; keys = job['duel']['keys']
    cards = ''
    for i, k in enumerate(keys):
        cards += (f'<div class="dcard {"bowl" if i == 0 else "belt"}" data-fd-card="{k}"><div class="dhead"><b><em>{"AB"[i]}</em>{T(f"duel.sides.{k}", sides[k])}</b>'
                  f'<span class="dbadge" data-badge></span><small>{T("ui.picks", "PICKS") if (i or not d.get("left_illustrative")) else T("ui.illustrative", "ILLUSTRATIVE")}'
                  f'{"<strong data-fd-count=" + chr(34) + k + chr(34) + ">0</strong>" if (i or not d.get("left_illustrative")) else ""}</small></div>'
                  f'<div class="dsvg" data-fd="{k}"></div><div class="fd-metrics" data-fd-metrics="{k}"></div></div>')
    for i, c in enumerate(d['chapters']):
        T(f'duel.chapters.{i}.tab', c['tab']); T(f'duel.chapters.{i}.text', c['text'])
    return sec('duel', head_block('duel', d.get('kicker', 'Side-by-side animation'), d['title'], d.get('lead')) +
               f'<div class="tabs" role="tablist" id="tabs"></div><div class="duel" id="duelRoot">{cards}</div><div class="prog"><i id="prog"></i></div>'
               f'<div class="dexp"><p id="dexp" aria-live="polite"></p><div class="ctls"><button class="ctl" id="bPlay" aria-pressed="true">{T("ui.pause", "❚❚ Pause")}</button>'
               f'<button class="ctl" id="bSlow" aria-pressed="false">{T("ui.slow", "Slow motion")}</button></div></div>' +
               (T('duel.note', d['note'], 'p', ' class="dnote"') if d.get('note') else ''))

def s_why():
    w = C.get('why')
    if not w: return ''
    cards = ''.join(f'<div class="card"><div class="num">{i+1:02d}</div>{T(f"why.cards.{i}.h", c["h"], "h3")}{T(f"why.cards.{i}.p", c["p"], "p")}</div>' for i, c in enumerate(w['cards']))
    return sec('why', head_block('why', w.get('kicker', 'Why it matters'), w['title'], w.get('lead')) + f'<div class="grid g3" style="margin-top:28px">{cards}</div>')

def s_how():
    h = C.get('how')
    if not h: return ''
    cols = ''
    for i, c in enumerate(h['cols']):
        steps = ''.join(f'<li><b data-i18n="how.cols.{i}.steps.{j}.b">{E(s["b"])}</b>{T(f"how.cols.{i}.steps.{j}.t", s["t"])}</li>' for j, s in enumerate(c['steps']))
        for j, s in enumerate(c['steps']): EN[f'how.cols.{i}.steps.{j}.b'] = s['b']
        cols += f'<div class="col {"bowl" if i == 0 else "belt"}">{T(f"how.cols.{i}.tag", c["tag"], "span", " class=\"tag\"")}{T(f"how.cols.{i}.h", c["h"], "h3")}<ol class="steps">{steps}</ol></div>'
    return sec('how', head_block('how', h.get('kicker', 'Working principle'), h['title'], h.get('lead')) + f'<div class="vs2" style="margin-top:28px">{cols}</div>', 'alt')

def s_model3d():
    m = C.get('model3d')
    if not m: return ''
    mc = cfg['model']
    mats = ''.join(f'<button type="button" data-mat="{k}" aria-pressed="{str(i == 0).lower()}">{T(f"ui.mat.{k}", k.capitalize() if k != "xray" else "X-ray")}</button>' for i, k in enumerate(mc['material_presets']))
    lts = ''.join(f'<button type="button" data-light="{k}" aria-pressed="{str(i == 0).lower()}">{T(f"ui.light.{k}", k.capitalize())}</button>' for i, k in enumerate(mc['lighting_presets']))
    fb = img(m['fallback_image']) if m.get('fallback_image') else ''
    bullets = ''.join(f'<li>{T(f"model3d.bullets.{i}", b)}</li>' for i, b in enumerate(m.get('bullets', [])))
    link = f'<a class="btn o" href="{E(m["drawing_url"])}" target="_blank" rel="noopener">{T("ui.open3d", "Open the original 3D drawing")}</a>' if m.get('drawing_url') else ''
    return sec('model3d', head_block('model3d', m.get('kicker', 'Interactive 3D model'), m['title'], m.get('lead')) +
               f'<div class="v3d" style="margin-top:24px"><div class="v3d-stage" id="v3d"><div class="fallback">{"<img src=" + chr(34) + fb + chr(34) + " alt=" + chr(34) + E(m.get("fallback_alt", "3D model")) + chr(34) + ">" if fb else ""}</div>'
               f'{T("ui.hint3d", "Drag to rotate · scroll or pinch to zoom · double-click to reset", "span", " class=\"hint\"")}</div>'
               f'<div class="v3d-ctl"><div class="grp">{T("ui.material", "Material", "b")}<div class="seg">{mats}</div></div>'
               f'<div class="grp">{T("ui.lighting", "Lighting", "b")}<div class="seg">{lts}</div></div>'
               f'<div class="grp">{T("ui.explode", "Explode view", "b")}<input id="v3dEx" type="range" min="0" max="100" value="0" aria-label="Explode"></div>'
               f'<div class="grp seg"><button type="button" id="v3dAuto" aria-pressed="true">{T("ui.autorotate", "Auto-rotate")}</button><button type="button" id="v3dReset">{T("ui.reset", "Reset view")}</button></div>'
               f'<ul class="chk3">{bullets}</ul>{link}</div></div>')

def s_specs():
    s = C.get('specs')
    if not s: return ''
    rows = ''.join(f'<tr><td>{T(f"specs.rows.{i}.0", r[0]) if r[0] else ""}</td><td>{T(f"specs.rows.{i}.1", r[1])}</td><td>{T(f"specs.rows.{i}.2", r[2])}</td></tr>' for i, r in enumerate(s['rows']))
    hd = s.get('header', ['Category', 'Parameter', 'Value'])
    return sec('specs', head_block('specs', s.get('kicker', 'Specification'), s['title'], s.get('lead')) +
               f'<div class="tw" style="margin-top:22px"><table class="cmp"><thead><tr>{"".join(T(f"specs.header.{i}", h, "th") for i, h in enumerate(hd))}</tr></thead><tbody>{rows}</tbody></table></div>' +
               (T('specs.source', s['source'], 'p', ' class="src"') if s.get('source') else ''), 'alt')

def s_fit():
    f = C.get('fit')
    if not f: return ''
    inp = ''
    for i, x in enumerate(f['inputs']):
        EN[f'fit.inputs.{i}.label'] = x['label']
        inp += f'<label for="fit_{x["id"]}" data-i18n="fit.inputs.{i}.label">{E(x["label"])}</label><input id="fit_{x["id"]}" type="number" step="any" value="{x["value"]}" data-min="{x.get("min", "")}" data-max="{x.get("max", "")}" data-unit="{E(x.get("unit", ""))}" data-name="{E(x["label"])}">'
    return sec('fit', head_block('fit', f.get('kicker', 'Fit check'), f['title'], f.get('lead')) +
               f'<div class="calc fit" style="margin-top:22px"><div class="card">{inp}</div><div><ul class="chk" id="fitOut"></ul><p class="disc" id="fitNote"></p>'
               f'<a class="btn p" id="fitCta" href="{wa}" target="_blank" rel="noopener">{T("fit.cta", f.get("cta", "Send us a sample for a trial"))}</a></div></div>')

def s_roi():
    r = C.get('roi', {}); dfl = dict(cfg['roi']['defaults'], **r.get('defaults', {}))
    labels = {'operators_saved': 'Operators freed per shift', 'hourly_cost': f'Loaded labour cost per hour ({cfg["roi"]["currency"]})', 'hours_per_shift': 'Hours per shift',
              'shifts_per_day': 'Shifts per day', 'days_per_year': 'Working days per year', 'extra_output_per_hour': 'Extra good parts per hour (optional)',
              'margin_per_unit': f'Contribution per extra part ({cfg["roi"]["currency"]}, optional)', 'investment': f'Your quoted investment ({cfg["roi"]["currency"]})'}
    labels.update(r.get('labels', {}))
    inp = ''.join(f'<label for="roi_{k}">{T(f"roi.labels.{k}", labels[k])}</label><input id="roi_{k}" type="number" min="0" step="any" value="{dfl[k]}">' for k in labels)
    res = ''.join(f'<div><b id="roiR_{k}">–</b>{T(f"roi.out.{k}", v, "span")}</div>' for k, v in
                  [('labour', 'Labour saving per year'), ('output', 'Extra output value per year'), ('total', 'Total benefit per year'), ('payback', 'Payback (months)')])
    return sec('roi', head_block('roi', r.get('kicker', 'ROI calculator'), r.get('title', 'Estimate your payback'), r.get('lead', 'Enter your own figures. No price is published here: ask us for a quotation and enter it to see the payback.')) +
               f'<div class="roi" style="margin-top:22px"><div class="card">{inp}</div><div><div class="res">{res}</div>' +
               T('roi.disc', r.get('disclaimer', 'Estimate only, based on the values you enter; it is not a performance guarantee.'), 'p', ' class="disc"') + '</div></div>', 'alt')

def s_benefits():
    b = C.get('benefits')
    if not b: return ''
    cards = ''.join(f'<div class="card"><h3><span class="ic">{E(c.get("icon", "✓"))}</span>{T(f"benefits.cards.{i}.h", c["h"])}</h3>{T(f"benefits.cards.{i}.p", c["p"], "p")}</div>' for i, c in enumerate(b['cards']))
    return sec('benefits', head_block('benefits', b.get('kicker', 'What it changes'), b['title']) + f'<div class="grid g4" style="margin-top:26px">{cards}</div>', 'ben')

def s_gallery():
    g = C.get('gallery')
    if not g: return ''
    items = ''.join(f'<button type="button" data-full="{img(x["src"], 1800)}" aria-label="{E(x["alt"])}"><img src="{img(x["src"], 900)}" alt="{E(x["alt"])}" loading="lazy"></button>' for x in g['items'])
    return sec('gallery', head_block('gallery', g.get('kicker', 'Gallery'), g['title']) + f'<div class="gal" style="margin-top:22px" id="gal">{items}</div>') + \
        '<dialog id="lb" aria-label="Image viewer"><button type="button" aria-label="Close">×</button><img class="dialog-image" alt=""></dialog>\n'

def s_videos():
    v = C.get('videos')
    if not v: return ''
    items = ''.join(f'<div class="vc{" big" if len(v["items"]) == 1 else ""}"><div class="vst"><img src="{img("https://i.ytimg.com/vi/" + x["id"] + "/hqdefault.jpg", 960)}" alt="" loading="lazy"><button class="vld" type="button" data-id="{x["id"]}" aria-label="Play: {E(x["title"])}"><span><svg width="26" height="26" viewBox="0 0 24 24" fill="#fff"><path d="M8 5v14l11-7z"/></svg></span></button></div>{T(f"videos.items.{i}.title", x["title"], "p")}</div>' for i, x in enumerate(v['items']))
    return sec('videos', head_block('videos', v.get('kicker', 'Video'), v['title']) + f'<div class="vids" style="margin-top:22px">{items}</div>', 'alt')

def s_blogs():
    bl = C.get('blogs')
    if not bl: return ''
    n = cfg['blog_count']
    if len(bl['items']) != n: sys.exit(f'content.blogs.items has {len(bl["items"])} articles, config.blog_count = {n}')
    items = ''
    for i, b in enumerate(bl['items']):
        body = ''.join(T(f'blogs.items.{i}.body.{j}', p, 'p') for j, p in enumerate(b['body']))
        items += (f'<article class="blog" id="blog-{i+1}">{T(f"blogs.items.{i}.tag", b.get("tag", "Engineering"), "span", " class=\"tg\"")}{T(f"blogs.items.{i}.title", b["title"], "h3")}'
                  f'{T(f"blogs.items.{i}.summary", b["summary"], "p")}<details><summary>{T("ui.readmore", "Read the article")}</summary>{body}</details></article>')
    return sec('blogs', head_block('blogs', bl.get('kicker', 'Insights'), bl['title'], bl.get('lead')) + f'<div class="blogs" style="margin-top:22px">{items}</div>')

def s_docs():
    d = C.get('docs')
    if not d: return ''
    items = ''.join(f'<a class="doc" href="{E(x["href"])}" target="_blank" rel="noopener">{T(f"docs.items.{i}.t", x["t"], "b")}{T(f"docs.items.{i}.d", x["d"], "span")}<em>{T("ui.open", "Open →")}</em></a>' for i, x in enumerate(d['items']))
    return sec('docs', head_block('docs', d.get('kicker', 'Documents'), d['title']) + f'<div class="docs" style="margin-top:22px">{items}</div>', 'alt')

def s_faq():
    f = C.get('faq')
    if not f: return ''
    items = ''.join(f'<details{" open" if i == 0 else ""}><summary data-i18n="faq.items.{i}.q">{E(x["q"])}</summary>{T(f"faq.items.{i}.a", x["a"], "p")}</details>' for i, x in enumerate(f['items']))
    for i, x in enumerate(f['items']): EN[f'faq.items.{i}.q'] = x['q']
    return sec('faq', head_block('faq', f.get('kicker', 'FAQ'), f['title']) + f'<div style="margin-top:22px;max-width:920px">{items}</div>', 'faq')

def s_contact():
    c = C['contact']
    return (f'<section id="contact" style="padding-bottom:0"><div class="wrap"><div class="cta"><div>{T("contact.kicker", c.get("kicker", "Next step"), "span", " class=\"kick\" style=\"color:#b8e563\"")}'
            f'{T("contact.h", c["h"], "h2")}{T("contact.p", c["p"], "p")}</div><div class="ctas">'
            f'<a class="btn g" href="{wa}?text={urllib.request.quote(c.get("wa_text", "Hi, I would like a quotation"))}" target="_blank" rel="noopener">WhatsApp {E(B["phone"])}</a>'
            f'<a class="btn l" href="mailto:{B["email"]}?subject={urllib.request.quote(C["meta"]["product"])}">Email {E(B["email"])}</a>'
            f'<a class="btn l" href="{B["website"]}" target="_blank" rel="noopener">{E(B["website"].split("//")[-1])}</a></div></div></div></section>\n')

FN = {k[2:]: v for k, v in globals().items() if k.startswith('s_')}
order = job.get('sections') or cfg['sections']
body = ''.join(FN[s]() for s in order if s in FN)

# ---------------- header / footer ----------------
meta = C['meta']; th = cfg['theme']
nav_items = [(s, C.get(s, {}).get('nav')) for s in order if isinstance(C.get(s), dict) and C.get(s, {}).get('nav')]
nav = ''.join(f'<a href="#{s}">{T(f"{s}.nav", n)}</a>' for s, n in nav_items)
langs = cfg['languages']
lang_sel = '<select class="lang" id="lang" aria-label="Language">' + ''.join(f'<option value="{l}">{E(cfg["language_labels"].get(l, l))}</option>' for l in langs) + '</select>'
logo = img(B['logo_url'], 600)
soc = B['social']
footer_products = ''.join(f'<a href="{E(x["href"])}">{T(f"footer.products.{i}", x["t"])}</a>' for i, x in enumerate(C.get('footer', {}).get('products', [])))
footer = f'''<footer><div class="wrap"><div class="fg">
<div><img class="fl" src="{logo}" alt="{E(B['company'])}">{T('footer.about', B['about'], 'p')}
<div class="soc"><a href="{soc['linkedin']}" target="_blank" rel="noopener" aria-label="LinkedIn Company Page">in</a><a href="{soc['linkedin_profile']}" target="_blank" rel="noopener" aria-label="LinkedIn Profile">in</a><a href="{soc['twitter']}" target="_blank" rel="noopener" aria-label="Twitter">X</a><a href="{soc['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">f</a><a href="{soc['youtube']}" target="_blank" rel="noopener" aria-label="YouTube Channel">YT</a></div></div>
<div>{T('footer.h_products', 'Products', 'h4')}{footer_products}<a href="{B['catalog_url']}" target="_blank" rel="noopener">{T('footer.catalog', 'Machine catalog')}</a></div>
<div>{T('footer.h_resources', 'Resources', 'h4')}<a href="{soc['linkedin']}" target="_blank" rel="noopener">LinkedIn Company Page</a><a href="{soc['linkedin_profile']}" target="_blank" rel="noopener">LinkedIn Profile</a><a href="{soc['twitter']}" target="_blank" rel="noopener">Twitter</a><a href="{soc['facebook']}" target="_blank" rel="noopener">Facebook</a><a href="{soc['youtube']}" target="_blank" rel="noopener">YouTube Channel</a></div>
<div>{T('footer.h_contact', 'Contact', 'h4')}<a href="mailto:{B['email']}">{B['email']}</a><a href="{wa}" target="_blank" rel="noopener">WhatsApp {E(B['phone'])}</a><a href="tel:{B['phone'].replace(' ', '')}">Tel {E(B['phone'])}</a><a href="{B['website']}" target="_blank" rel="noopener">{B['website'].split('//')[-1]}</a><p>{E(B['address'])}</p></div>
</div><div class="bot"><p>Browse our machine catalog at <a href="{B['catalog_url']}" target="_blank" rel="noopener">{B['catalog_url'].split('//')[-1]}</a> and find machine photos at <a href="{B['photos_url']}" target="_blank" rel="noopener">{B['photos_url'].split('//')[-1]}</a>.</p>
<p>© {meta.get('year', 2026)} {E(B['company'])} · {E(B['legal_name'])}. {E(C.get('footer', {}).get('disclaimer', 'Specifications are subject to change; confirm the final configuration on your quotation.'))}</p></div></div></footer>
<a class="fabbtn" href="{wa}" target="_blank" rel="noopener" aria-label="WhatsApp" style="color:#fff">{open(os.path.join(TPL, 'wa_svg.txt')).read().strip()}/></svg></a>
'''
header = f'''<div class="util"><div class="wrap"><span>{E(B['legal_name'])}</span><span><a href="tel:{B['phone'].replace(' ', '')}">{E(B['phone'])}</a> · <a href="mailto:{B['email']}">{B['email']}</a></span></div></div>
<header class="hdr" id="hdr"><div class="wrap"><a class="brand" href="#top"><img src="{logo}" alt="{E(B['company'])}" width="218" height="60"></a>
<nav class="nav" id="nav">{nav}</nav><div class="tools">{lang_sel}{'<button class="thm" id="thm" type="button" aria-label="Dark mode">◐</button>' if th.get('dark_mode_toggle') else ''}</div>
<a class="btn p" href="#contact">{T('ui.quote', 'Get a quote')}</a><button class="navt" id="navt" aria-label="Menu" aria-expanded="false">☰</button></div></header>
'''
css = open(os.path.join(TPL, 'style.css'), encoding='utf8').read()
for k, v in th.items(): css = css.replace('%%' + k + '%%', str(v))
css = css.replace('%%', '%')

# ---------------- scripts ----------------
I18N = {cfg['default_language']: EN}
for l, d in (C.get('i18n') or {}).items():
    if l in langs: I18N[l] = d
if job.get('i18n_dir') and os.path.isdir(P(job['i18n_dir'])):
    for fn in os.listdir(P(job['i18n_dir'])):
        l = fn.split('.')[0]
        if fn.endswith('.json') and l in langs and l != cfg['default_language']:
            I18N.setdefault(l, {}).update(json.load(open(os.path.join(P(job['i18n_dir']), fn), encoding='utf8')))
model_js = ''
if C.get('model3d') and job.get('model'):
    mp = P(job['model'])
    if os.path.exists(mp):
        model_js = f'<script type="application/json" id="smt3d-data">{open(mp).read()}</script>\n<script>\n{open(os.path.join(TPL, "viewer3d.js"), encoding="utf8").read()}\n</script>\n'
    else:
        print('WARN model file missing, 3D section falls back to image:', mp)
duel_js = ''
if job.get('duel') and C.get('duel'):
    duel_js = '<script>\n' + open(P(job['duel']['script']), encoding='utf8').read() + '\n</script>\n'
BOOT = {'langs': langs, 'rtl': cfg['rtl_languages'], 'def': cfg['default_language'], 'wa': wa, 'currency': cfg['roi']['currency'],
        'duel': ({'cls': job['duel']['class'], 'keys': job['duel']['keys'], 'cycle': job['duel'].get('cycle_s', 13.4),
                  'chapters': [c['id'] for c in C['duel']['chapters']]} if duel_js else None),
        'model': {'material': cfg['model']['material_presets'][0], 'light': cfg['model']['lighting_presets'][0]},
        'fitTpl': C.get('fit', {}).get('wa_text', 'Hi, fit check for ' + meta['product'] + ': ')}
app = open(os.path.join(TPL, 'app.js'), encoding='utf8').read()
jsonld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Product", "name": meta['product'], "brand": {"@type": "Brand", "name": B['company']}, "description": meta['description']},
    {"@type": "Organization", "name": B['company'], "url": B['website'], "email": B['email'], "telephone": B['phone']},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x['q'], "acceptedAnswer": {"@type": "Answer", "text": x['a']}} for x in C.get('faq', {}).get('items', [])]}]}
chat = B['chatwoot']
chat_js = '' if not chat.get('website_token') else f'''<script>
window.chatwootSettings={{"position":"right","type":"standard","launcherTitle":"{E(B['company'])} Support"}};
(function(d,t){{if(location.protocol!=="http:"&&location.protocol!=="https:")return;var BASE_URL="{chat['base_url']}";
var g=d.createElement(t),s=d.getElementsByTagName(t)[0];g.src=BASE_URL+"/packs/js/sdk.js";g.async=true;s.parentNode.insertBefore(g,s);
g.onload=function(){{window.chatwootSDK.run({{websiteToken:'{chat['website_token']}',baseUrl:BASE_URL}})}}}})(document,"script");
</script>'''
page = f'''<!DOCTYPE html>
<html lang="{cfg['default_language']}" dir="ltr">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(meta['title'])}</title><meta name="description" content="{E(meta['description'])}"><meta name="keywords" content="{E(meta.get('keywords', ''))}">
<meta property="og:title" content="{E(meta['title'])}"><meta property="og:description" content="{E(meta['description'])}"><meta property="og:type" content="website"><meta name="theme-color" content="{th['brand']}">
<meta name="generator" content="smt-3d-animation-landing-kit {cfg['skill_version']}">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<style>{css}</style></head>
<body>
{header}{body}{footer}
<script type="application/json" id="smt-i18n">{json.dumps(I18N, ensure_ascii=False).replace('</', '<\\/')}</script>
<script type="application/json" id="smt-boot">{json.dumps(BOOT, ensure_ascii=False)}</script>
{model_js}{duel_js}<script>
{app}
</script>
{chat_js}
</body></html>
'''
out = a.out or W(job, 'out', job.get('slug', meta.get('slug', 'landing')) + '.html')
open(out, 'w', encoding='utf8').write(page)
cov = {l: (round(100 * sum(1 for k in EN if k in I18N.get(l, {})) / max(1, len(EN)))) for l in langs}
json.dump({'keys': len(EN), 'coverage_pct': cov}, open(W(job, 'build', 'i18n_report.json'), 'w'))
json.dump(EN, open(W(job, 'build', 'i18n_en_keys.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(f'written {out} ({len(page)/1e6:.2f} MB), {len(EN)} i18n keys, coverage {cov}')
if len(page.encode('utf-8')) > 2_000_000: print('WARNING: page is over 2,000,000 bytes; file.autoinsertion.com has served pages truncated at 2 MiB. Shrink images or the mesh before publishing.')
print('external <img src="http" left:', page.count('src="http'))
