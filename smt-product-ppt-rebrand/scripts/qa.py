#!/usr/bin/env python3
"""Post-build QA gate on the generated .pptx.

usage: qa.py <deck.pptx> [spec.json]  -> prints report, writes <deck>.qa.json, exit 1 on errors.
Checks: slide count, brand closing slides present, font = brand font on every run, no empty
text boxes/placeholders, text boxes inside the 16:9 safe area, core properties, file name pattern."""
import json, os, re, sys
from pptx import Presentation
from pptx.util import Emu

SKILL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BRAND = json.load(open(os.path.join(SKILL, "config", "brand.json"), encoding="utf-8"))

def qa(path, spec=None):
    errs, warns = [], []
    prs = Presentation(path); n = len(prs.slides)
    if spec:
        exp = 2 + len(spec["slides"]) + len(BRAND["template"]["keep_slides_at_end"])
        if n != exp: errs.append(f"Q01 slide count {n}, expected {exp}")
    texts_last = " ".join(sh.text_frame.text for s in list(prs.slides)[-2:] for sh in s.shapes if sh.has_text_frame).lower()
    for name in BRAND["template"]["keep_slides_names"]:
        if name.split()[0].lower() not in texts_last: errs.append(f"Q02 closing slide '{name}' missing")
    font = BRAND["fonts"]["latin_and_ea"]; W, H = prs.slide_width, prs.slide_height
    bad_font = 0
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.is_placeholder and sh.has_text_frame and not sh.text_frame.text.strip():
                errs.append(f"Q03 slide {i}: empty placeholder '{sh.name}'")
            if sh.left is not None and (sh.left < 0 or sh.top < 0 or sh.left + sh.width > W * 1.001 or sh.top + sh.height > H * 1.001):
                warns.append(f"Q04 slide {i}: '{sh.name}' extends beyond the slide")
            if sh.has_text_frame and i <= n - 2:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.text.strip() and r.font.name not in (None, font): bad_font += 1
    if bad_font: errs.append(f"Q05 {bad_font} text runs not in brand font {font}")
    cp = prs.core_properties
    for k in BRAND["metadata"]["required"]:
        if not getattr(cp, k): errs.append(f"Q06 core property '{k}' empty")
    fn = os.path.basename(path)
    if not fn.startswith(("out", "deck")) and not re.match(r"^[A-Za-z0-9][A-Za-z0-9-]*-Southern-Machinery\.pptx$", fn):
        warns.append("Q07 file name does not follow the SEO pattern (run seo_name.py)")
    size_mb = os.path.getsize(path) / 1e6
    if size_mb > 40: warns.append(f"Q08 file is {size_mb:.0f} MB; compress images")
    return {"file": path, "slides": n, "errors": errs, "warnings": warns, "pass": not errs}

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    spec = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else None
    r = qa(sys.argv[1], spec)
    json.dump(r, open(os.path.splitext(sys.argv[1])[0] + ".qa.json", "w"), indent=1, ensure_ascii=False)
    for w in r["warnings"]: print("WARN ", w)
    for e in r["errors"]: print("ERROR", e)
    print(("QA PASS" if r["pass"] else "QA FAIL"), f"- {r['slides']} slides")
    sys.exit(0 if r["pass"] else 1)
