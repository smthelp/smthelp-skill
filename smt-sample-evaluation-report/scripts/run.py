#!/usr/bin/env python3
"""One-command pipeline: case.json -> calc.json -> deck spec per language -> PPTX -> QA -> summary.

usage: run.py <case_dir> [--langs en,pt] [--layout 16x9|a4] [--no-preview]
Outputs in <case_dir>/out/:
  calc.json                 raw figures (+ skill version)
  deck-<lang>.json          slide spec (editable; re-render with render16.py)
  <slug>-<lang>.pptx        the evaluation report deck
  prev-<lang>/*.png         layout previews (check every one before delivery)
  render-<lang>.log, qa.json, summary.md (figures + assumptions for the chat reply / email)"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from calc import load_case, compute, SKILL
import make_spec, qa


def version():
    m = re.search(r"^\s*version:\s*([\d.]+)", open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read(), re.M)
    return m.group(1) if m else "?"


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    case_dir = a[0]; out = os.path.join(case_dir, "out"); os.makedirs(out, exist_ok=True)
    case, p, m = load_case(case_dir)
    langs = a[a.index("--langs") + 1].split(",") if "--langs" in a else case.get("languages", ["en"])
    layout = a[a.index("--layout") + 1] if "--layout" in a else p.get("layout", "16x9")
    c = compute(case, p, m); c["skill_version"] = version()
    json.dump(c, open(os.path.join(out, "calc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for lang in langs:
        spec = make_spec.build(case_dir, lang, c); spec["skill_version"] = c["skill_version"]
        sp = os.path.join(out, f"deck-{lang}.json"); json.dump(spec, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        pptx = os.path.join(out, f"{case['slug']}-{lang}.pptx")
        if layout == "a4":
            cmd = [sys.executable, os.path.join(SKILL, "..", "smt-brand-kit", "scripts", "make_deck.py"), sp, pptx]
        else:
            cmd = [sys.executable, os.path.join(HERE, "render16.py"), sp, pptx]
        if "--no-preview" not in a: cmd += ["--preview", os.path.join(out, f"prev-{lang}")]
        r = subprocess.run(cmd, capture_output=True, text=True)
        open(os.path.join(out, f"render-{lang}.log"), "w").write(r.stdout + r.stderr)
        print(lang, (r.stdout.strip().splitlines() or ["?"])[0], "->", pptx)
    res = qa.run(case_dir)
    F = make_spec.Fmt({"thousands": ",", "decimal": "."})
    lines = [f"# {case['customer']} {case['board']} - {m['name']} sample evaluation (skill v{c['skill_version']})", "",
             f"- Measured: {c['cycle']} s per {c['bpp']}-board panel; BOM {c['ppb']} parts/board, {c['ppp']}/panel"
             + (f"; test program {c['prog_pts']} pts/board (to be confirmed with full BOM)" if c['prog_pts'] and c['prog_pts'] != c['ppb'] else ""),
             f"- Theoretical: {F(c['panels_h'])} panels/h, {F(c['boards_h'])} boards/h, {F(c['cph'])} CPH",
             f"- At {F(c['eff']*100)} %: {F(c['boards_h_eff'])} boards/h, {F(c['boards_shift'])}/shift, {F(c['boards_month'])}/month (1 shift, {c['days']} days)",
             f"- ROI per shift: manual {c['ops_manual']} operators {c['cur']} {F(c['manual_total'])}/month vs machine {c['cur']} {F(c['auto_total'])}/month -> saving {c['cur']} {F(c['saving_m'])}/month, {c['cur']} {F(c['saving_y'])}/year",
             "- Shifts: " + "; ".join(f"{k}: {c['cur']} {F(v['saving'])}/month" for k, v in c["shifts"].items()),
             f"- Benefits: {c['released']} operators released/shift, {F(c['ratio'],1)}x boards per operator-hour, {F(c['defects_avoided'])} defects avoided/month",
             "- Payback = customer quote / monthly saving (price never shown)", "",
             f"QA: {len(res['errors'])} errors, {len(res['warnings'])} warnings"] + [f"- {x}" for x in res["errors"] + res["warnings"]]
    open(os.path.join(out, "summary.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if res["ok"] else 1)


if __name__ == "__main__":
    main()
