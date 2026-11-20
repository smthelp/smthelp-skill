#!/usr/bin/env python3
"""Fail if any never-publish term appears in marketing outputs (html, pptx, srt, txt, json copy).
usage: scrub_check.py <kit_dir> [--terms config/never_publish.txt] [--extra term ...]
Skips the quote/ folder (prices belong there) and embedded base64 data in html."""
import sys, os, re, zipfile, argparse
here = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument("kit"); ap.add_argument("--terms", default=os.path.join(here, "..", "config", "never_publish.txt")); ap.add_argument("--extra", nargs="*", default=[])
a = ap.parse_args()
terms = [l.strip() for l in open(a.terms, encoding="utf-8") if l.strip() and not l.startswith("#")] + a.extra
def texts(p):
    if p.endswith(".pptx"):
        with zipfile.ZipFile(p) as z:
            return " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.endswith(".xml"))
    t = open(p, encoding="utf-8", errors="ignore").read()
    return re.sub(r"data:[a-z/+-]+;base64,[A-Za-z0-9+/=]+", "", t)
bad = 0; out = os.path.join(a.kit, "out")
for root, _, files in os.walk(out):
    if os.sep + "quote" in root: continue
    for f in files:
        if not f.endswith((".html", ".pptx", ".srt", ".txt", ".json")): continue
        p = os.path.join(root, f); t = texts(p).lower()
        hits = sorted({x for x in terms if x.lower() in t})
        if hits: bad += 1; print(f"FAIL {os.path.relpath(p, a.kit)}: {', '.join(hits)}")
print("OK: no never-publish terms" if not bad else f"{bad} file(s) failed"); sys.exit(1 if bad else 0)
