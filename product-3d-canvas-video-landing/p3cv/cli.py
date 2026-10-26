"""Command line:  python -m p3cv <command> ...

  init  DIR [--example juki-gripper-nozzle]   create a project folder with product.json (+ example anim)
  check PRODUCT_JSON                          validate config, tools and Python packages
  run   PRODUCT_JSON [stage ...] [--force] [--wait] [--timeout S]
  preview PRODUCT_JSON [--times 5,30,60] [--ar 169]
  status PRODUCT_JSON                         stage table + render chunk progress
  stages                                      list stages and dependencies
  download URL [URL ...] --out DIR            stand-alone downloader (no product.json needed)
"""
import argparse, importlib, json, shutil, sys
from pathlib import Path
from . import __version__, log
from .config import Config, SKILL_ROOT
from .errors import P3VError


def cmd_init(a):
    d = Path(a.dir); d.mkdir(parents=True, exist_ok=True)
    ex = SKILL_ROOT / "examples" / a.example if a.example else None
    if ex and not ex.exists():
        raise P3VError("E_CONFIG", f"example {a.example} not found")
    src = (ex / "product.json") if ex else (SKILL_ROOT / "config" / "product.example.json")
    if (d / "product.json").exists() and not a.overwrite:
        raise P3VError("E_CONFIG", f"{d/'product.json'} exists (use --overwrite)")
    shutil.copy(src, d / "product.json")
    if ex:
        for f in ex.glob("*.js"):
            shutil.copy(f, d / f.name)
    else:
        shutil.copy(SKILL_ROOT / "templates" / "anim-template.js", d / "anim.js")
    print(f"created {d/'product.json'} - edit it, then: python -m p3cv check {d/'product.json'}")


def cmd_check(a):
    cfg = Config(a.config); ok = True
    for t in ("ffmpeg", "ffprobe"):
        if not shutil.which(t):
            print("MISSING tool", t); ok = False
    for m in ("playwright", "edge_tts", "PIL"):
        try:
            importlib.import_module(m)
        except ImportError:
            print("MISSING python package", m); ok = False
    if not cfg.resolve(cfg["anim"]["module"]).exists():
        print("MISSING anim module", cfg["anim"]["module"]); ok = False
    print(f"config OK: {cfg['product_name']} | {len(cfg['segments'])} segments | {len(cfg['video']['scenes'])} scenes")
    print("environment OK" if ok else "fix the items above (scripts/setup_env.sh)")
    return 0 if ok else 1


def cmd_run(a):
    from . import pipeline
    cfg = Config(a.config); log.setup(cfg.proj, "DEBUG" if a.verbose else "INFO")
    res = pipeline.run(cfg, a.stages or None, force=a.force, wait=a.wait or None, timeout=a.timeout)
    print(json.dumps(res, indent=1, ensure_ascii=False, default=str))


def cmd_preview(a):
    from .stages import video
    cfg = Config(a.config); log.setup(cfg.proj)
    html, tl = video.build(cfg)
    times = [float(x) for x in a.times.split(",")] if a.times else None
    for f in video.preview(cfg, html, tl, times, [a.ar] if a.ar else None):
        print(f)


def cmd_status(a):
    from .state import State
    from .stages import load_all, ORDER
    from .stages.render import chunk_status
    cfg = Config(a.config); st = State(cfg.proj); load_all()
    for s in ORDER:
        r = st.d.get(s, {}); err = r.get("error", {})
        print(f"{s:10s} {r.get('status','pending'):9s} {r.get('at',''):19s} {err.get('code','')} {err.get('message','')[:80]}")
    if (cfg.proj / "vo" / "timeline.json").exists():
        for k, v in chunk_status(cfg).items():
            print(f"  render {k}: {'DONE' if v['done'] else v['last'][-70:] or 'not started'}")


def cmd_stages(a):
    from .stages import load_all, ORDER, REGISTRY
    load_all()
    for s in ORDER:
        print(f"{s:10s} deps={','.join(REGISTRY[s]['deps']) or '-':22s} {REGISTRY[s]['desc']}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="p3cv", description=f"product 3D -> canvas video & landing v{__version__}")
    ap.add_argument("--version", action="version", version=__version__)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("dir"); p.add_argument("--example"); p.add_argument("--overwrite", action="store_true"); p.set_defaults(f=cmd_init)
    p = sp.add_parser("check"); p.add_argument("config"); p.set_defaults(f=cmd_check)
    p = sp.add_parser("run"); p.add_argument("config"); p.add_argument("stages", nargs="*")
    p.add_argument("--force", action="store_true"); p.add_argument("--wait", action="store_true")
    p.add_argument("--timeout", type=float); p.add_argument("-v", "--verbose", action="store_true"); p.set_defaults(f=cmd_run)
    p = sp.add_parser("preview"); p.add_argument("config"); p.add_argument("--times"); p.add_argument("--ar"); p.set_defaults(f=cmd_preview)
    p = sp.add_parser("status"); p.add_argument("config"); p.set_defaults(f=cmd_status)
    p = sp.add_parser("stages"); p.set_defaults(f=cmd_stages)
    p = sp.add_parser("download"); p.add_argument("urls", nargs="+"); p.add_argument("--out", default="src")
    p.set_defaults(f=lambda a: __import__("p3cv.stages.download", fromlist=["main"]).main(a.urls + ["--out", a.out]))
    a = ap.parse_args(argv)
    try:
        return a.f(a) or 0
    except P3VError as e:
        print(f"ERROR {e}", file=sys.stderr); return 2


if __name__ == "__main__":
    sys.exit(main())
