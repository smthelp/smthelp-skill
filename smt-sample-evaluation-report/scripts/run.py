#!/usr/bin/env python3
"""One-command pipeline: case.json -> calc.json -> deck spec per language -> PPTX -> QA -> summary.

usage: run.py <case_dir> [--langs en,pt] [--layout 16x9|a4] [--no-preview] [--html] [--no-pptx]
              [--customer-alias "LED Driver Manufacturer"] [--slug NAME]
--customer-alias  replaces the customer name everywhere (spec, notes, file names) for anonymous/public use;
                  QA E8 fails if the real name is left in any output. --slug sets the output file stem.
--board-alias     boards become "Board 1..n"; PCB and model numbers are dropped (line_evaluation).
--web             multilingual marketing page from <case_dir>/web/ (render_web.py): exports web/strings_en.json
                  (translate to web/i18n/<lang>.json with identical keys) and builds out/<page.json file>.
--html            also writes <slug>-<lang>.html: one self-contained HTML report (render_html.py).
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
    alias = a[a.index("--customer-alias") + 1] if "--customer-alias" in a else None
    if "--board-alias" in a:   # Board 1..n instead of the customer's PCB / model numbers
        for i, b in enumerate(case["boards"], 1): b["id"], b["pcb"], b["model"] = f"Board {i}", "", ""
        c = compute(case, p, m); c["skill_version"] = version()
    real = case["customer"]; hide = []
    if alias:
        w = real.split()
        hide = [" ".join(w[:k]) for k in range(len(w), 0, -1) if len(" ".join(w[:k])) > 3]
        case["customer"] = alias
    stem = a[a.index("--slug") + 1] if "--slug" in a else (re.sub(r"[^A-Za-z0-9]+", "-", alias).strip("-") + "-" + case.get("type", "sample_test").replace("_", "-") if alias else case["slug"])
    def redact(o, k=None):
        """Replace the real name in every text value; file paths (image/src/photo keys, absolute paths) stay as they are."""
        if isinstance(o, dict): return {kk: redact(v, kk) for kk, v in o.items()}
        if isinstance(o, list): return [redact(v, k) for v in o]
        if isinstance(o, str) and k not in ("image", "src", "photo") and not o.startswith("/"):
            for h in hide: o = re.sub(re.escape(h), alias, o, flags=re.I)
        return o
    json.dump(c, open(os.path.join(out, "calc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for lang in langs:
        spec = make_spec.build(case_dir, lang, c, case); spec["skill_version"] = c["skill_version"]
        if alias: spec = redact(spec)
        sp = os.path.join(out, f"deck-{lang}.json"); json.dump(spec, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        pptx = os.path.join(out, f"{stem}-{lang}.pptx")
        if "--html" in a:
            hp = os.path.join(out, f"{stem}-{lang}.html")
            r = subprocess.run([sys.executable, os.path.join(HERE, "render_html.py"), sp, hp], capture_output=True, text=True); print(r.stdout.strip() or r.stderr[-800:])
            if alias and any(h.lower() in open(hp, encoding="utf-8").read().lower() for h in hide): print("QA E8 real customer name left in HTML"); sys.exit(1)
        if "--web" in a and lang == "en" and os.path.isdir(os.path.join(case_dir, "web")):
            wd = os.path.join(case_dir, "web")
            for mode in ("export", "build"):
                r = subprocess.run([sys.executable, os.path.join(HERE, "render_web.py"), mode, sp, wd] + ([out] if mode == "build" else []), capture_output=True, text=True)
                print(r.stdout.strip() or r.stderr[-800:])
        if "--no-pptx" in a: continue
        if layout == "a4":
            cmd = [sys.executable, os.path.join(SKILL, "..", "smt-brand-kit", "scripts", "make_deck.py"), sp, pptx]
        else:
            cmd = [sys.executable, os.path.join(HERE, "render16.py"), sp, pptx]
        if "--no-preview" not in a: cmd += ["--preview", os.path.join(out, f"prev-{lang}")]
        r = subprocess.run(cmd, capture_output=True, text=True)
        open(os.path.join(out, f"render-{lang}.log"), "w").write(r.stdout + r.stderr)
        print(lang, (r.stdout.strip().splitlines() or ["?"])[0], "->", pptx)
    res = qa.run(case_dir)
    if alias:
        res = redact(res)
        for f in os.listdir(out):
            if f.startswith(stem) and f.endswith(".pptx"):
                from pptx import Presentation
                pr = Presentation(os.path.join(out, f)); txt = []
                for sl in pr.slides:
                    txt += [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame]
                    if sl.has_notes_slide: txt.append(sl.notes_slide.notes_text_frame.text)
                if any(h.lower() in " ".join(txt).lower() for h in hide): res["errors"].append(f"E8 real customer name left in {f}"); res["ok"] = False
    F = make_spec.Fmt({"thousands": ",", "decimal": "."})
    if c.get("type") == "line_evaluation":
        if alias: c = redact(c)
        lines = [f"# {case['customer']} - line evaluation (skill v{c['skill_version']})", "",
                 "- Line: " + " + ".join(f"{g['qty']} x {g['name']} ({g['process']}, ~{F(g['cph'])} CPH)" for g in c["line"])]
        for b in c["boards"]:
            lines.append(f"- {b['id']} {b['pcb']}: " + ", ".join(f"{g['name']} {F(g['cycle'],1)} s" for g in b["groups"])
                         + f" -> {F(b['line_boards_h'])} boards/h (bottleneck {b['bottleneck_name']}; +1 {b['alt_add']}: {F(b['alt_boards_h'])})")
        lines += ["", f"QA: {len(res['errors'])} errors, {len(res['warnings'])} warnings"] + [f"- {x}" for x in res["errors"] + res["warnings"]]
        open(os.path.join(out, "summary.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n"); print("\n".join(lines))
        sys.exit(0 if res["ok"] else 1)
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
