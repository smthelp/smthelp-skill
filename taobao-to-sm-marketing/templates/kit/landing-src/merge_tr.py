#!/usr/bin/env python3
"""tr/<lang>.txt = strings reused from squeegee-kit/landing-src/tr/<lang>.txt (same English text, map in tr/reuse-map.json)
+ new translations in tr/<lang>.new.txt. usage: merge_tr.py es pt fr ar ru zh"""
import json, os, sys
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQ = os.path.join(os.path.dirname(K), "squeegee-kit", "landing-src", "tr")
M = json.load(open(os.path.join(K, "landing-src/tr/reuse-map.json")))
def load(p):
    d = {}
    for ln in open(p, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if ln.strip(): k, v = ln.split("|", 1); d[k] = v
    return d
for l in sys.argv[1:]:
    old = load(os.path.join(SQ, l + ".txt")); new = load(os.path.join(K, "landing-src/tr", l + ".new.txt"))
    out = {k: old[src] for k, src in M.items()}
    dup = set(out) & set(new)
    if dup: print(l, "overlap", sorted(dup))
    out.update(new)
    with open(os.path.join(K, "landing-src/tr", l + ".txt"), "w", encoding="utf-8") as f:
        for k, v in out.items(): f.write(f"{k}|{v}\n")
    print(l, len(out))
