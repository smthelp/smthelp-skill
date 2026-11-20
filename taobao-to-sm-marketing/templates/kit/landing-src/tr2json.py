#!/usr/bin/env python3
"""Convert landing-src/tr/<lang>.txt (key|value per line) into landing/i18n/<lang>.json and check key parity with en."""
import json, sys, os
META = {"es": ("ltr", "Español", "ES"), "pt": ("ltr", "Português", "PT"), "fr": ("ltr", "Français", "FR"),
        "ar": ("rtl", "العربية", "AR"), "ru": ("ltr", "Русский", "RU"), "zh": ("ltr", "中文", "ZH")}
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
en = json.load(open(os.path.join(KIT, "landing/i18n/en.json"), encoding="utf-8"))
ok = True
for l in sys.argv[1:]:
    d = {"__meta": dict(zip(["dir", "label", "short"], META[l]))}
    for ln in open(os.path.join(KIT, "landing-src/tr", l + ".txt"), encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln.strip(): continue
        k, v = ln.split("|", 1)
        if k in d: print(l, "dup", k); ok = False
        d[k] = v.strip()
    miss, extra = set(en) - set(d), set(d) - set(en)
    if miss or extra: print(l, "missing", sorted(miss), "extra", sorted(extra)); ok = False
    d = {k: d[k] for k in en if k in d}
    json.dump(d, open(os.path.join(KIT, "landing/i18n", l + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(l, len(d))
sys.exit(0 if ok else 1)
