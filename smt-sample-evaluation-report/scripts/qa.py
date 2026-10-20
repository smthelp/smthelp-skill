#!/usr/bin/env python3
"""Quality gate for a sample evaluation report.

usage: qa.py <case_dir>          (reads out/calc.json, out/deck-*.json, out/render-*.log)
Writes out/qa.json and exits 1 on any error. Checks:
  E1 arithmetic: saving = manual - auto, yearly = 12 x monthly, operators = ceil(parts/h / rate)
  E2 every {placeholder} resolved in the specs
  E3 no price / lead-time / warranty figure (config forbidden_patterns); no 'price' key in case.json
  E4 test program points != BOM points -> a 'to be confirmed' line must be present
  E5 BOM parts outside machine limits (lead diameter, span) must be marked fit:false
  E6 renderer reported 0 overflow / missing-media errors
  W1 photos missing for a slide, W2 manual_ppm / efficiency left at default (flag as assumption)"""
import json, glob, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calc import load_case, SKILL


def run(case_dir):
    case, p, m = load_case(case_dir)
    out = os.path.join(case_dir, "out"); c = json.load(open(os.path.join(out, "calc.json"), encoding="utf-8"))
    E, Wn = [], []
    near = lambda a, b: abs(a - b) < 0.01
    if not near(c["saving_m"], c["manual_total"] - c["auto_total"]): E.append("E1 saving != manual - auto")
    if not near(c["saving_y"], c["saving_m"] * 12): E.append("E1 yearly != 12 x monthly")
    if c["ops_manual"] != math.ceil(c["parts_h"] / c["manual_rate"] - 1e-9): E.append("E1 operator count")
    raw = json.dumps(case, ensure_ascii=False).lower()
    if re.search(r'"(price|preco|preço|unit_price)"', raw): E.append("E3 case.json carries a price field - remove it")
    specs = sorted(glob.glob(os.path.join(out, "deck-*.json")))
    if not specs: E.append("no deck-*.json in out/")
    for sp in specs:
        txt = open(sp, encoding="utf-8").read(); d = json.loads(txt)
        body = json.dumps(d["slides"], ensure_ascii=False)
        left = re.findall(r"\{[a-z_0-9]+\}", body)
        if left: E.append(f"E2 {os.path.basename(sp)} unresolved {sorted(set(left))}")
        for pat in p.get("forbidden_patterns", []):
            mm = re.search(pat, body)
            if mm: E.append(f"E3 {os.path.basename(sp)} forbidden text: {mm.group(0)}")
        if c.get("prog_pts") and c["prog_pts"] != c["ppb"] and str(c["prog_pts"]) not in json.dumps(
                [s for s in d["slides"] if s["type"] == "bullets"], ensure_ascii=False):
            E.append(f"E4 {os.path.basename(sp)} test program {c['prog_pts']} pts vs BOM {c['ppb']} not flagged")
        for s in d["slides"]:
            for k in ("image",):
                if k in s and (not s[k] or not os.path.exists(s[k])): Wn.append(f"W1 {s['type']} slide without photo")
    bad = set(c["lead_over_limit"]) | set(c["span_unsupported"])
    for b in case["bom"]:
        if b["refs"] in bad and b.get("fit", True): E.append(f"E5 {b['refs']} outside machine limits but fit != false")
    for lg in glob.glob(os.path.join(out, "render-*.log")):
        t = open(lg, encoding="utf-8").read(); mm = re.search(r"errors (\d+)", t)
        if not mm or mm.group(1) != "0": E.append(f"E6 {os.path.basename(lg)}: {t.strip()[-300:]}")
    for k in ("efficiency", "manual_ppm", "manual_parts_per_operator_hour"):
        if k not in case.get("params", {}): Wn.append(f"W2 {k} = default {p[k]} (planning assumption - say so to the customer)")
    res = {"errors": E, "warnings": Wn, "ok": not E}
    json.dump(res, open(os.path.join(out, "qa.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    r = run(sys.argv[1])
    print(f"qa errors {len(r['errors'])} warnings {len(r['warnings'])}")
    for x in r["errors"] + r["warnings"]: print(" ", x)
    sys.exit(0 if r["ok"] else 1)
