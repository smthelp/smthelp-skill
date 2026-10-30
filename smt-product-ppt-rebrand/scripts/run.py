#!/usr/bin/env python3
"""Pipeline: validate spec -> build pptx -> QA gate -> (optional) render + contact sheets.

usage: run.py <spec.json> <assets_dir> <out_dir> [--name "<SEO-file-name>.pptx"] [--render]
       run.py --example            (builds assets/examples/esd-storage-board-fjd250 into ./out-example)
Writes <out_dir>/<name>.pptx, <name>.qa.json and build-log.json (skill version, brand version, result).
Stops with exit 1 at the first failing gate; nothing is uploaded by this script (use upload.sh)."""
import datetime, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); SKILL = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import validate_spec, qa, smbuild

def main(argv):
    if "--example" in argv:
        ex = os.path.join(SKILL, "assets", "examples", "esd-storage-board-fjd250")
        argv = [os.path.join(ex, "spec.json"), os.path.join(ex, "images"), "out-example",
                "--name", "ESD-PCB-Storage-Board-L-Type-Anti-Static-Stand-FJD250-95-Southern-Machinery.pptx"] + (["--render"] if "--render" in argv else [])
    if len(argv) < 3: sys.exit(__doc__)
    spec_p, assets, out = argv[0], argv[1].rstrip("/") + "/", argv[2]
    name = argv[argv.index("--name") + 1] if "--name" in argv else os.path.splitext(os.path.basename(spec_p))[0] + ".pptx"
    os.makedirs(out, exist_ok=True); spec = json.load(open(spec_p, encoding="utf-8"))
    log = {"time": datetime.datetime.now().isoformat(timespec="seconds"),
           "skill_version": open(os.path.join(SKILL, "VERSION")).read().strip(),
           "brand_version": smbuild.BRAND["brand_version"], "spec": spec_p, "output": os.path.join(out, name)}
    errs, warns = validate_spec.validate(spec, assets)
    for w in warns: print("WARN ", w)
    if errs:
        for e in errs: print("ERROR", e)
        log.update(stage="validate", result="fail", errors=errs); json.dump(log, open(os.path.join(out, "build-log.json"), "w"), indent=1); return 1
    deck = os.path.join(out, name)
    tpl = os.path.join(SKILL, smbuild.BRAND["template"]["file"])
    try:
        smbuild.build(tpl, spec, assets, deck)
    except Exception as e:
        print("ERROR B01 build failed:", repr(e)); log.update(stage="build", result="fail", errors=[repr(e)])
        json.dump(log, open(os.path.join(out, "build-log.json"), "w"), indent=1); return 1
    r = qa.qa(deck, spec); json.dump(r, open(os.path.splitext(deck)[0] + ".qa.json", "w"), indent=1, ensure_ascii=False)
    for w in r["warnings"]: print("WARN ", w)
    for e in r["errors"]: print("ERROR", e)
    log.update(stage="qa", result="pass" if r["pass"] else "fail", slides=r["slides"], warnings=warns + r["warnings"], errors=r["errors"])
    if r["pass"] and "--render" in argv:
        try:
            subprocess.run([os.path.join(HERE, "render.sh"), deck], check=True)
            subprocess.run([sys.executable, os.path.join(HERE, "sheet.py"), os.path.splitext(deck)[0]], check=True)
            log["render"] = "ok"
        except Exception as e:
            log["render"] = f"skipped: {e}"; print("WARN R01 render unavailable:", e)
    json.dump(log, open(os.path.join(out, "build-log.json"), "w"), indent=1, ensure_ascii=False)
    print(("PASS" if r["pass"] else "FAIL"), deck, f"({r['slides']} slides)")
    return 0 if r["pass"] else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
