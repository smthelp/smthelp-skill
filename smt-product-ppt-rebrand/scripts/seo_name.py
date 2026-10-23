#!/usr/bin/env python3
"""Make an SEO file name: seo_name.py "ESD PCB Magazine Rack" "anti static" "SMT loader unloader"
-> ESD-PCB-Magazine-Rack-Anti-Static-SMT-Loader-Unloader-Southern-Machinery.pptx"""
import json, os, re, sys
SKILL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
F = json.load(open(os.path.join(SKILL, "config", "brand.json"), encoding="utf-8"))["filename"]
KEEP_UPPER = {"ESD", "PCB", "PCBA", "SMT", "THT", "LED", "EMS", "AOI", "PP", "PPE", "DIP", "CE", "UL"}

def seo_name(*parts):
    words, seen = [], set()
    for p in parts:
        for w in re.split(r"[^A-Za-z0-9]+", p):
            if not w or w.lower() in seen or w.lower() in ("southern", "machinery"): continue
            seen.add(w.lower())
            words.append(w if (w.upper() in KEEP_UPPER and w.isalpha()) or any(ch.isdigit() for ch in w) else w.capitalize())
    name = F["pattern"].format(keywords=F["separator"].join(words))
    while len(name) > F["max_len"] and len(words) > 2:
        words.pop(); name = F["pattern"].format(keywords=F["separator"].join(words))
    return name

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    print(seo_name(*sys.argv[1:]))
