#!/usr/bin/env python3
"""Pre-delivery QA for a page built by build_page.py.
usage: check_page.py <page.html> [--case <case_dir>]   -> prints PASS/FAIL per check, exit 1 on any FAIL"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1:]
if not a: sys.exit(__doc__)
fp = a[0]; case = a[a.index("--case") + 1] if "--case" in a else None
t = open(fp, encoding="utf-8").read(); s = re.sub(r"data:[^\"')]+", "data:", t)
brand = json.load(open(os.path.join(ROOT, "config", "brand.json"), encoding="utf-8"))
pg = json.load(open(os.path.join(case, "web", "page.json"), encoding="utf-8")) if case else {}
if pg.get("brand"): brand.update(pg["brand"])
res = []
def chk(name, ok, info=""): res.append((ok, name, info))
chk("single file, no external stylesheet/script src", not re.search(r"<link[^>]+rel=.stylesheet|<script[^>]+src=", s))
hosts = set(re.findall(r"https?://([^/\"' )]+)", s))
bad = sorted(h for h in hosts if h not in brand["cdn_whitelist"])
chk("only whitelisted hosts", not bad, ", ".join(bad))
imgs = re.findall(r"<img[^>]+src=['\"]([^'\"]*)", t)
ext = [u for u in imgs if not u.startswith("data:") and "i.ytimg.com" not in u and "ph.smthelp.com" not in u]
chk("images inlined (except YouTube/photo-site thumbs)", not ext, str(ext[:3]))
chk("viewport meta", 'name="viewport"' in t)
chk("semantic tags", all(f"<{x}" in t for x in ("header", "nav", "main", "section", "footer")))
m = re.search(r"var I18N=(\{.*?\});var CFG=", t, re.S)
I = json.loads(m.group(1)) if m else {}
langs = (pg.get("langs") or list(I))
chk("languages present", all(l in I for l in langs), ",".join(l for l in langs if l not in I))
en = I.get("en", {})
miss = {l: len([k for k in en if k not in I[l]]) for l in I if l != "en"}
chk("translation coverage 100 %", not any(miss.values()), str(miss))
numre = re.compile(r"\d+(?:[.,]\d+)?")
nm = []
for l in I:
    if l == "en": continue
    for k, v in I[l].items():
        if k in en and sorted(numre.findall(en[k])) != sorted(numre.findall(v)) and not k.startswith(("ui_", "foot_")): nm.append(f"{l}:{k}")
chk("numbers identical across languages", not nm, ", ".join(nm[:8]) + (f" (+{len(nm)-8})" if len(nm) > 8 else ""))
fw = brand["forbidden_title_words"]
badre = re.compile(r"\b(" + "|".join(w for w in fw if w.isascii()) + r")\b|" + "|".join(w for w in fw if not w.isascii()), re.I)
hk = re.compile(r"(_title|_kicker|_h2|^bl\d+t|^seo_title|^v\d+t|^cat\d+t)$")
fh = [f"{l}:{k}" for l in I for k, v in I[l].items() if hk.search(k) and badre.search(v)]
chk("no forbidden words in headings", not fh, ", ".join(fh[:6]))
red = [w for w in pg.get("redact", []) if re.search(re.escape(w), s, re.I)]
chk("no redact terms", not red, ", ".join(red))
txt = re.sub(r"<script>(?!var I18N).*?</script>", "", s, flags=re.S)
money = re.findall(r"(?:US\$|\$|¥|€|RMB|USD|CNY)\s?\d[\d,.]*", txt)
chk("no prices", not money, ", ".join(money[:5]))
cw = brand.get("chatwoot", {})
chk("Chatwoot configured", not cw.get("enabled") or cw.get("token", "x") in t)
chk("hreflang for every language", all(f"hreflang='{l}'" in t for l in langs))
try:
    json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S).group(1).replace("<\\/", "</")); ok = True
except Exception: ok = False
chk("JSON-LD parses", ok)
kb = os.path.getsize(fp) // 1024
chk("size < 3 MB", kb < 3072, f"{kb} KB")
for ok, n, i in res: print(("PASS " if ok else "FAIL ") + n + (f"  [{i}]" if i and not ok else ""))
print(f"{sum(1 for r in res if r[0])}/{len(res)} checks passed")
sys.exit(0 if all(r[0] for r in res) else 1)
