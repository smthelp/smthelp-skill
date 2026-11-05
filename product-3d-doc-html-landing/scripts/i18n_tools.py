#!/usr/bin/env python3
"""i18n helpers.
  mk-en   <workdir>                 en_ui.py (EN dict) + en_blog.py (B list) -> i18n/en.json; checks blog count and banned words
  reuse   <workdir> <old_dir> ...   for each language: pre_<l>.json = translations reused from earlier pages for identical EN strings,
                                    todo_<l>.json = strings still to translate (send each to one translator subagent -> out_<l>.json)
  merge   <workdir>                 pre_<l>.json + out_<l>.json -> i18n/<l>.json; reports missing, untranslated, banned
  add-lang <workdir> <code>         creates todo_<code>.json with every EN string (new language upgrade path)
Languages and banned words come from config (default.yaml merged with <workdir>/config.yaml)."""
import sys, os, json, re, importlib.util, copy
HERE = os.path.dirname(os.path.abspath(__file__)); SK = os.path.dirname(HERE)
def cfg(W):
    import yaml
    def m(a, b):
        o = copy.deepcopy(a)
        for k, v in (b or {}).items(): o[k] = m(o[k], v) if isinstance(v, dict) and isinstance(o.get(k), dict) else v
        return o
    c = yaml.safe_load(open(SK + '/config/default.yaml'))
    p = os.path.join(W, 'config.yaml'); return m(c, yaml.safe_load(open(p)) if os.path.exists(p) else {})
def mod(p, name):
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
cmd, W = sys.argv[1], os.path.abspath(sys.argv[2]) + '/'; C = cfg(W); L = [l[0] for l in C['languages']]; os.makedirs(W + 'i18n', exist_ok=True)
bad = re.compile('(?i)' + '|'.join([r'\b' + re.escape(w) if w.isalpha() else re.escape(w) for w in C['content']['banned_words'] + C['content']['banned_words_zh']]))
if cmd == 'mk-en':
    EN = mod(W + 'en_ui.py', 'en_ui').EN; B = mod(W + 'en_blog.py', 'en_blog').B
    assert len(B) == C['content']['blog_count'], f"blog_count {C['content']['blog_count']} but en_blog has {len(B)}"
    d = dict(EN)
    for i, b in enumerate(B, 1):
        for k, v in b.items(): d[f'b{i}_{k}'] = v
    hits = [(k, v[:60]) for k, v in d.items() if bad.search(v)]
    json.dump(d, open(W + f'i18n/{L[0]}.json', 'w'), ensure_ascii=False, indent=0); print(len(d), 'keys; banned:', hits)
elif cmd == 'reuse':
    en = json.load(open(W + f'i18n/{L[0]}.json'))
    for l in L[1:]:
        m = {}
        for s in sys.argv[3:]:
            if os.path.exists(f'{s}/{l}.json'):
                E = json.load(open(f'{s}/{L[0]}.json')); T = json.load(open(f'{s}/{l}.json'))
                for k, v in E.items():
                    if k in T and v not in m: m[v] = T[k]
        pre = {k: m[v] for k, v in en.items() if v in m}; todo = {k: v for k, v in en.items() if v not in m}
        json.dump(pre, open(W + f'pre_{l}.json', 'w'), ensure_ascii=False, indent=0); json.dump(todo, open(W + f'todo_{l}.json', 'w'), ensure_ascii=False, indent=1)
        print(l, 'reused', len(pre), 'todo', len(todo))
elif cmd == 'merge':
    en = json.load(open(W + f'i18n/{L[0]}.json'))
    for l in L[1:]:
        d = json.load(open(W + f'pre_{l}.json')) if os.path.exists(W + f'pre_{l}.json') else {}
        if not os.path.exists(W + f'out_{l}.json'): print(l, 'pending'); continue
        d.update(json.load(open(W + f'out_{l}.json'))); d = {k: d[k] for k in en if k in d}
        miss = set(en) - set(d); same = [k for k in en if d.get(k) == en[k] and len(en[k]) > 25]
        hits = [(k, v[:40]) for k, v in d.items() if bad.search(v) or '<' in v]
        print(l, len(d), 'missing', sorted(miss)[:5], 'same-as-en', same[:4], 'banned', hits[:3])
        json.dump(d, open(W + f'i18n/{l}.json', 'w'), ensure_ascii=False, indent=0)
elif cmd == 'add-lang':
    code = sys.argv[3]; en = json.load(open(W + f'i18n/{L[0]}.json'))
    json.dump(en, open(W + f'todo_{code}.json', 'w'), ensure_ascii=False, indent=1)
    print(f'todo_{code}.json written; add [{code}, <native name>] to config.languages (and to rtl_languages if RTL)')
