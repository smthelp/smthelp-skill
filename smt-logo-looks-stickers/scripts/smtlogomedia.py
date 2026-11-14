#!/usr/bin/env python3
"""smt-logo-looks-stickers - logo STEP -> brand looks + GIF stickers.

usage: smtlogomedia.py <command> [job.json] [options]
commands:
  doctor                          check python modules, ffmpeg, renderer
  init <dir> --cad F [--brand D] [--png P]  scaffold a job folder from the example
  inspect <job>                   STEP -> GLB + work/parts.csv
  looks <job>                     render the static looks
  stickers <job>                  render the GIF stickers
  all <job>                       inspect + looks + stickers
  package                         build the skill zip (tools/package.sh)
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)
VERSION = open(os.path.join(SKILL, "VERSION")).read().strip()


def load_job(path):
    job = json.load(open(os.path.join(SKILL, "config", "defaults.json"), encoding="utf-8"))
    user = json.load(open(path, encoding="utf-8"))
    job.update(user)
    job["_file"] = os.path.abspath(path)
    base = os.path.dirname(os.path.abspath(path))

    def res(p):
        return p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))

    job["cad"] = res(job["cad"])
    if job.get("logo_png"):
        job["logo_png"] = res(job["logo_png"])
    bd = job.get("brand_dir", "../smt-brand-kit/assets/brand")
    if bd.startswith("../smt-brand-kit"):
        # repo default: resolve against the skill folder, not the job folder
        job["brand_dir"] = os.path.normpath(os.path.join(SKILL, bd))
    else:
        job["brand_dir"] = res(bd)
    job["out_dir"] = res(job.get("out_dir", "out"))
    job["work_dir"] = res(job.get("work_dir", "work"))
    job["glb"] = os.path.join(job["work_dir"], "model.glb")
    for d in (job["out_dir"], job["work_dir"]):
        os.makedirs(d, exist_ok=True)
    return job


def doctor():
    ok = True

    def chk(name, fn):
        nonlocal ok
        try:
            print(f"OK   {name}: {fn()}")
        except Exception as ex:
            ok = False
            print(f"FAIL {name}: {ex}")

    import importlib
    for mod in ("numpy", "PIL", "trimesh", "numba", "cascadio"):
        chk(mod, lambda m=mod: getattr(importlib.import_module(m), "__version__", "installed"))
    chk("ffmpeg", lambda: subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.split("\n")[0])
    chk("renderer", lambda: __import__("logo_render").render.__name__)
    chk("skill", lambda: VERSION)
    print("all good" if ok else "install: pip install -r requirements.txt")
    return 0 if ok else 2


def init(argv):
    d = argv[0]
    cad = argv[argv.index("--cad") + 1]
    brand = argv[argv.index("--brand") + 1] if "--brand" in argv else "../smt-brand-kit/assets/brand"
    os.makedirs(d, exist_ok=True)
    ex = os.path.join(SKILL, "examples", "sm-logo", "job.json")
    j = json.load(open(ex, encoding="utf-8"))
    j["cad"] = os.path.relpath(os.path.abspath(cad), d)
    if "--png" in argv:
        j["logo_png"] = os.path.relpath(os.path.abspath(argv[argv.index("--png") + 1]), d)
    j["brand_dir"] = os.path.relpath(os.path.abspath(brand), d) if os.path.isabs(brand) else brand
    j["_todo"] = "Run inspect, then edit texts/contacts/rollup_rows for this logo, then run all."
    p = os.path.join(d, "job.json")
    json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", p)
    return 0


def inspect(job):
    import logo_cad
    glb = logo_cad.convert_step_to_glb(job["cad"], job["glb"])
    info = logo_cad.inventory(glb, os.path.join(job["work_dir"], "parts.csv"))
    print(json.dumps(info, ensure_ascii=False))
    return info


def run_stage(job, stage):
    import produce
    e = produce.Engine(job)
    if stage == "looks":
        out = produce.run_looks(e, job.get("looks"))
    else:
        out = produce.run_stickers(e, job.get("stickers"))
    print(json.dumps(out, ensure_ascii=False, default=str))
    return out


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "doctor":
        return doctor()
    if cmd == "init":
        return init(argv[1:])
    if cmd == "--version":
        print(VERSION)
        return 0
    if cmd == "package":
        return subprocess.call([os.path.join(SKILL, "tools", "package.sh")])
    if len(argv) < 2:
        print(__doc__)
        return 2
    job = load_job(argv[1])
    if cmd == "inspect":
        inspect(job)
    elif cmd in ("looks", "stickers"):
        run_stage(job, cmd)
    elif cmd == "all":
        inspect(job)
        run_stage(job, "looks")
        run_stage(job, "stickers")
    else:
        print(__doc__)
        return 2
    print(json.dumps({"ok": True, "command": cmd, "skill_version": VERSION}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
