"""Content gate before any rendering. Usage: (SMV_PROJECT=...) python3 lint.py
Checks structure, shot/slide references, copy limits, claim policy and SEO fields.
Exit 0 = pass (warnings allowed), 2 = errors. Error codes: references/error-handling.md"""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg

E, W = [], []
FORBID = [re.compile(x, re.I) for x in cfg.P.get('forbidden_claims', [])]
REQ_EXAMPLE = [re.compile(x, re.I) for x in cfg.P.get('example_only_patterns', [])]
SEO_REQ = ['title', 'kw', 'summary', 'tags', 'hashtags', 'thumb', 'thumb_shot']
WPS = 2.55     # en-US-AndrewNeural at +3% speaks ~2.5-2.6 words/s


def texts_of(v):
    for sc in v['scenes']:
        yield 'scene', sc['text']
        co = sc.get('co') or {}
        for k in ('k', 'h', 'stat'):
            if co.get(k): yield 'callout', co[k]
        for b in co.get('b', []): yield 'callout', b
    seo = cfg.SEO.get(v['slug'], {})
    for k in ('title', 'kw', 'summary', 'thumb'):
        if seo.get(k): yield 'seo', seo[k]


slugs = set()
for v in cfg.VIDEOS:
    s = v.get('slug', '?')
    if s in slugs: E.append(f'E10 {s}: duplicate slug')
    slugs.add(s)
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', s): E.append(f'E10 {s}: slug must be kebab-case')
    for k in ('topic', 'kicker', 'title', 'intro_title', 'scenes'):
        if k not in v: E.append(f'E11 {s}: missing {k}')
    if s not in cfg.SEO: E.append(f'E12 {s}: no SEO entry'); continue
    seo = cfg.SEO[s]
    for k in SEO_REQ:
        if k not in seo: E.append(f'E12 {s}: SEO missing {k}')
    if not v['scenes'][0].get('ch'): E.append(f'E13 {s}: first scene needs a chapter label (ch)')
    words = 0; use = {}
    for i, sc in enumerate(v['scenes']):
        words += len(sc['text'].split())
        n = len(sc['text'].split())
        if n > 70: W.append(f'W14 {s} scene {i}: {n} words (keep <= 60 for pace)')
        for vid in sc.get('vis', []):
            if vid.startswith('slide:'):
                sid = vid[6:]
                if sid != 'blank' and sid not in cfg.SLIDES and not cfg.HAS_CUSTOM_SLIDES:
                    E.append(f'E20 {s}: slide {sid} not defined')
            else:
                if vid not in cfg.SHOTS: E.append(f'E15 {s}: shot {vid} not in shots.py')
                use[vid] = use.get(vid, 0) + 1
        co = sc.get('co')
        if co:
            if len(co.get('k', '')) > 30: W.append(f"W16 {s} scene {i}: callout kicker > 30 chars")
            if len(co.get('h', '')) > 60: E.append(f"E16 {s} scene {i}: callout headline > 60 chars")
            if len(co.get('b', [])) > 4: E.append(f"E16 {s} scene {i}: > 4 bullets")
            for b in co.get('b', []):
                if len(b) > 48: W.append(f"W16 {s} scene {i}: bullet > 48 chars: {b}")
            if co.get('stat') and len(co['stat']) > 10: E.append(f"E16 {s} scene {i}: stat > 10 chars")
    words += len(v.get('outro', cfg.OUTRO_TEXT).split())
    est = words / WPS + len(v['scenes']) * 0.6 + 8
    if not 60 <= est <= 175: E.append(f'E17 {s}: estimated length {est:.0f}s outside 60-175 s ({words} words)')
    for vid, n in use.items():
        if n > 2: W.append(f'W18 {s}: shot {vid} used {n}x')
    for kind, t in texts_of(v):
        for rx in FORBID:
            if rx.search(t): E.append(f'E30 {s} [{kind}]: forbidden claim /{rx.pattern}/ in: {t[:90]}')
        for rx in REQ_EXAMPLE:
            m = rx.search(t)
            if m and not re.search(r'example|e\.g\.|for example|assum|illustrat|brochure', t, re.I):
                W.append(f'W31 {s} [{kind}]: "{m.group(0)}" should be labelled as an example/brochure figure')
    t = seo.get('title', '')
    if not 40 <= len(t) <= 70: E.append(f'E40 {s}: title length {len(t)} (40-70)')
    if not 13 <= len(seo.get('tags', [])) <= 15: E.append(f"E41 {s}: {len(seo.get('tags', []))} tags (13-15)")
    if cfg.P.get('primary_keyword') and cfg.P['primary_keyword'].lower() not in ' '.join(seo.get('tags', [])).lower():
        W.append(f"W42 {s}: primary keyword '{cfg.P['primary_keyword']}' not in tags")
    if len(seo.get('kw', '')) > 160: E.append(f'E43 {s}: description first line > 160 chars')
    if re.search(r'[<>]', seo.get('kw', '') + seo.get('summary', '') + seo.get('title', '')):
        E.append(f'E45 {s}: < or > in title/description (YouTube rejects them; write "below" / "above")')
    sid, _ = seo.get('thumb_shot', (None, 0))
    if sid and sid not in cfg.SHOTS: E.append(f'E15 {s}: thumb_shot {sid} not in shots.py')

titles = [cfg.SEO[v['slug']]['title'] for v in cfg.VIDEOS if v['slug'] in cfg.SEO]
if len(set(titles)) != len(titles): E.append('E44 duplicate titles in batch')
print('\n'.join(W + E) or 'no findings')
print(f"lint: {len(cfg.VIDEOS)} videos, {len(E)} errors, {len(W)} warnings")
sys.exit(2 if E else 0)
