"""YouTube metadata + copy document. Usage: python3 meta.py [4k|prev]
Writes final/<batch>/metadata.json and copy.html (upload as a Google Doc). Enforces the SEO rules
(references/output-spec.md); exits non-zero on violation."""
import json, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg

VIDEOS, SEO, OUTRO_TEXT, P, CT = cfg.VIDEOS, cfg.SEO, cfg.OUTRO_TEXT, cfg.P, cfg.CONTACT
NOTES = getattr(cfg.content, 'NOTES', [])
SOURCES = getattr(cfg.content, 'SOURCES', [])     # list of (name, url, what it supports)


def mmss(t):
    t = int(t); return f"{t // 60}:{t % 60:02d}"


def description(v, seo, plan):
    url = f"{v.get('page', P['landing_page'])}?utm_source=youtube&utm_medium=video&utm_campaign={P['utm_prefix']}-{v['topic']}"
    chap = '\n'.join(f"{mmss(t)} {l}" for t, l in plan['chapters'])
    cta = v.get('desc_cta', P['desc_cta'])
    foot = '\n'.join(cfg.fmt(x) for x in cfg.B['description_footer'])
    parts = [f"{seo['kw']}\n{cta}: WhatsApp {CT['whatsapp_desc']} (https://wa.me/{CT['whatsapp_digits']})",
             seo['summary'], f"Chapters:\n{chap}", f"{P['landing_label']}:\n{url}", foot]
    if P.get('desc_disclaimer'):
        parts[-1] += '\n' + P['desc_disclaimer']
    parts.append(' '.join(seo['hashtags']))
    return '\n\n'.join(parts), url


def check(v, seo, desc):
    errs = []
    t = seo['title']
    if not (40 <= len(t) <= 70): errs.append(f'title length {len(t)} (40-70)')
    if not (13 <= len(seo['tags']) <= 15): errs.append(f'{len(seo["tags"])} tags (13-15)')
    if sum(len(x) for x in seo['tags']) + 2 * len(seo['tags']) > 480: errs.append('tags over ~480 chars')
    if not (2 <= len(seo['hashtags']) <= 5): errs.append('hashtags 2-5')
    if len(desc) > 4900: errs.append('description > 4900 chars')
    if len(seo['kw']) > 160: errs.append('first line > 160 chars (shown above the fold)')
    if '<' in desc or '>' in desc: errs.append('angle brackets not allowed in YouTube description')
    return [f"{v['slug']}: {e}" for e in errs]


def build(tag='4k'):
    allm, errs = [], []
    for v in VIDEOS:
        seo = SEO[v['slug']]
        p = f"{cfg.BUILD}/{v['slug']}/{tag}/plan.json"
        if not os.path.exists(p): p = f"{cfg.BUILD}/{v['slug']}/prev/plan.json"
        if not os.path.exists(p):
            errs.append(f"{v['slug']}: not rendered yet (no plan.json)"); continue
        plan = json.load(open(p))
        desc, url = description(v, seo, plan)
        errs += check(v, seo, desc)
        script = [s['text'] for s in v['scenes']] + [v.get('outro', OUTRO_TEXT)]
        allm.append(dict(slug=v['slug'], file=cfg.out_name(v['slug'], 'mp4'), title=seo['title'], title_len=len(seo['title']),
                         description=desc, tags=seo['tags'], thumbnail_text=seo['thumb'].replace('\n', ' '),
                         duration=plan['T'], script=script, url=url))
    json.dump(allm, open(f"{cfg.OUT}/metadata.json", 'w'), indent=1, ensure_ascii=False)
    title = P.get('doc_title', f"{P['product']['model']} YouTube Video Copy - {cfg.BATCH}")
    h = [f'<html><head><meta charset="utf-8"><title>{html.escape(title)}</title></head><body>', f'<h1>{html.escape(title)}</h1>']
    if NOTES:
        h.append('<h2>Production notes</h2>'); h += [f"<p>{html.escape(n)}</p>" for n in NOTES]
    if SOURCES:
        h.append('<h2>Sources</h2>')
        h += [f"<p><b>{html.escape(a)}</b><br>{html.escape(b)}<br>{html.escape(c)}</p>" for a, b, c in SOURCES]
    h.append('<h2>Contents</h2><ol>' + ''.join(f"<li>{html.escape(m['title'])} ({mmss(m['duration'])})</li>" for m in allm) + '</ol>')
    for i, m in enumerate(allm, 1):
        h.append(f"<h2>Video {i}: {html.escape(m['title'])}</h2>")
        h.append(f"<p><b>File:</b> {html.escape(m['file'])} · <b>Duration:</b> {mmss(m['duration'])}</p>")
        h.append(f"<h3>YouTube title ({m['title_len']} characters)</h3><p>{html.escape(m['title'])}</p><h3>Description</h3>")
        for para in m['description'].split('\n\n'):
            h.append('<p>' + '<br>'.join(html.escape(x) for x in para.split('\n')) + '</p>')
        h.append(f"<h3>Tags ({len(m['tags'])})</h3><p>{html.escape(', '.join(m['tags']))}</p>")
        h.append(f"<h3>Thumbnail</h3><p>Text: {html.escape(m['thumbnail_text'])}<br>File: {html.escape(cfg.out_name(m['slug'], 'thumb'))}</p>")
        h.append(f"<p><b>Subtitles:</b> {html.escape(cfg.out_name(m['slug'], 'srt'))}</p><h3>Narration script</h3>")
        h += [f"<p>{html.escape(s)}</p>" for s in m['script']]
    h.append('</body></html>')
    open(f"{cfg.OUT}/copy.html", 'w').write('\n'.join(h))
    return allm, errs


if __name__ == '__main__':
    allm, errs = build(sys.argv[1] if len(sys.argv) > 1 else '4k')
    for m in allm:
        print(m['title_len'], m['title'], round(m['duration'], 1))
    if errs:
        print('\n'.join('E40 ' + e for e in errs)); sys.exit(2)
