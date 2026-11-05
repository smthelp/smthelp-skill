#!/usr/bin/env python3
"""Static validation of a finished page. Exit code 1 when any hard check fails.
usage: python3 validate.py <workdir>
Hard: size <= budget; every <script> passes node --check; JSON-LD parses; no %%placeholders%%; all data-i18n keys exist
      in every language; no banned word in visible text or class names; no privacy term; blog/faq counts; hreflang per language;
      chatwoot token present; logo + 5 social links + WhatsApp present.
Soft (warn): http:// links, images without alt, external images not on ph.smthelp.com, more than 3 inline images > 60 KB."""
import sys, os, re, json, subprocess, copy, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); SK = os.path.dirname(HERE)
import yaml
def m(a, b):
    o = copy.deepcopy(a)
    for k, v in (b or {}).items(): o[k] = m(o[k], v) if isinstance(v, dict) and isinstance(o.get(k), dict) else v
    return o
W = os.path.abspath(sys.argv[1]) + '/'; C = m(yaml.safe_load(open(SK + '/config/default.yaml')), yaml.safe_load(open(W + 'config.yaml')))
F = W + C['page']['filename']; t = open(F, encoding='utf8').read(); L = [l[0] for l in C['languages']]
ok, warn = [], []
def chk(name, cond, detail=''): ok.append((name, bool(cond), detail))
kb = len(t.encode()) // 1024; chk('size', kb <= C['page']['size_budget_kb'], f'{kb} KB / {C["page"]["size_budget_kb"]}')
bad = 0
for i, s in enumerate(re.findall(r'<script(?: type="module")?>(.*?)</script>', t, re.S)):
    p = tempfile.mktemp(suffix='.mjs'); open(p, 'w').write(s)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True); bad += r.returncode != 0
chk('scripts', bad == 0, f'{bad} failing')
try:
    g = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)]
    types = sorted({n['@type'] for d in g for n in d['@graph']}); chk('json-ld', {'Organization', 'WebPage', 'FAQPage', 'BlogPosting'} <= set(types), ','.join(types))
except Exception as ex: chk('json-ld', False, str(ex))
chk('placeholders', not re.search(r'%%[A-Za-z0-9_]+%%', t))
I = json.loads(re.search(r'window\.I18N=(\{.*?\});</script>', t, re.S).group(1))
used = set(re.findall(r'data-i18n(?:-alt|-aria)?="(\w+)"', t))
chk('i18n keys', all(not (used - set(I[l])) for l in L), str({l: sorted(used - set(I[l]))[:3] for l in L if used - set(I[l])}))
chk('languages', sorted(I) == sorted(L), ','.join(I))
vis = re.sub(r'<script.*?</script>|<style.*?</style>|data:[^"]*', '', t, flags=re.S)
words = C['content']['banned_words'] + C['content']['banned_words_zh']
rx = re.compile('(?i)' + '|'.join(r'\b' + re.escape(w) if w.isalpha() else re.escape(w) for w in words))
txt = ' '.join(v for l in I for v in I[l].values()) + ' ' + re.sub(r'<[^>]+>', ' ', vis) + ' ' + ' '.join(re.findall(r'class="([^"]*)"', t))
chk('banned words', not rx.search(txt), str(rx.findall(txt)[:5]))
pv = [p for p in C['content']['privacy_terms'] if p and p.lower() in (txt + t).lower()]; chk('privacy', not pv, str(pv))
chk('blog count', len(re.findall(r'class="card post', t)) == C['content']['blog_count'])
chk('faq count', len(re.findall(r'<details', t)) == C['content']['faq_count'])
chk('hreflang', all(f'hreflang="{l}"' in t for l in L) and 'x-default' in t)
chk('chatwoot', C['chatwoot']['token'] in t)
need = ['Southern-Machinery-logo-300x83.png', 'linkedin.com/company/smtmachine', 'linkedin.com/in/smtsupplier', 'smtspecialist', 'facebook.com/autoinsertion', 'youtube.com/c/Smthelping', 'wa.me/8613602562576', 'file.autoinsertion.com', 'ph.smthelp.com']
miss = [n for n in need if n not in t]; chk('brand + footer', not miss, str(miss))
chk('3d viewer', 'id="c3d"' in t and ('__mode3d' in t))
chk('roi', 'id="rPrice"' in t or not C['roi']['enabled'])
if 'http://' in re.sub(r'"http://"', '', vis): warn.append('http:// link present')
ext = set(re.findall(r'<img[^>]+src="(https?://[^/"]+)', t)) - {'https://ph.smthelp.com', 'https://i.ytimg.com', 'https://drive.google.com'}
if ext: warn.append('images from ' + ','.join(ext))
big = [u for u in re.findall(r'"(data:image/[^"]{80000,})"', t)]
if len(big) > 3: warn.append(f'{len(big)} inline images over ~60 KB')
for n, c, d in ok: print(('PASS' if c else 'FAIL').ljust(5), n.ljust(16), d)
for w in warn: print('WARN ', w)
sys.exit(0 if all(c for _, c, _ in ok) else 1)
