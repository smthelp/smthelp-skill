"""Command line:  python -m p3cv <command> ...

  init  DIR [--example juki-gripper-nozzle]   create a project folder with product.json (+ example anim)
  check PRODUCT_JSON                          validate config, tools and Python packages
  run   PRODUCT_JSON [stage ...] [--force] [--wait] [--timeout S]
  preview PRODUCT_JSON [--times 5,30,60] [--ar 169]
  status PRODUCT_JSON                         stage table + render chunk progress
  stages                                      list stages and dependencies
  download URL [URL ...] --out DIR            stand-alone downloader (no product.json needed)
  manifest PRODUCT_JSON                       write out/manifest.json (deliverables + sha256 + versions)
  migrate PRODUCT_JSON                        upgrade product.json to the current schema_version (.bak kept)
  relabel IMAGE --bbox x0,y0,x1,y1 --text T   replace the model name on a machine label in a photo
  info                                        print skill.json (name, version, contract, dependencies)

Contract (docs/CONTRACT.md): `run ... --json-out FILE` writes a result envelope; exit 0 ok, 2 error,
3 pending (render still running - call the same command again), 1 environment/usage problem.
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
        if (ex / "img").is_dir():  # example assets (photos referenced by product.json)
            shutil.copytree(ex / "img", d / "img", dirs_exist_ok=True)
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
    raw = json.dumps({k: v for k, v in json.loads(cfg.path.read_text(encoding="utf-8")).items() if k != "privacy"}, ensure_ascii=False)
    for c in cfg.get("privacy.confidential", []) or []:
        if Path(c).name and Path(c).name in raw:
            print("WARN confidential source referenced in product.json:", c)
    print(f"config OK: {cfg['product_name']} | {len(cfg['segments'])} segments | {len(cfg['video']['scenes'])} scenes")
    print("environment OK" if ok else "fix the items above (scripts/setup_env.sh)")
    return 0 if ok else 1


def cmd_run(a):
    from . import pipeline
    from .contract import envelope
    cfg = Config(a.config); log.setup(cfg.proj, "DEBUG" if a.verbose else "INFO"); done = {}
    try:
        done = pipeline.run(cfg, a.stages or None, force=a.force, wait=a.wait or None, timeout=a.timeout, collect=done)
        env = envelope(a.config, "ok", done)
    except P3VError as e:
        env = envelope(a.config, "pending" if e.code == "E_PENDING" else "error", done, e.as_dict())
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(env, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(json.dumps(env, indent=1, ensure_ascii=False, default=str))
    return env["exit_code"]


def cmd_manifest(a):
    from .contract import manifest
    m = manifest(Config(a.config)); print(json.dumps(m, indent=1, ensure_ascii=False))
    return 0 if not m["missing"] else 3


def cmd_migrate(a):
    from .contract import migrate
    print(json.dumps(migrate(a.config), ensure_ascii=False))


def cmd_info(a):
    from .contract import info
    print(json.dumps(info(), indent=1, ensure_ascii=False))


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
    p.add_argument("--timeout", type=float); p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--json-out", help="write the result envelope (docs/CONTRACT.md) to this file"); p.set_defaults(f=cmd_run)
    p = sp.add_parser("manifest"); p.add_argument("config"); p.set_defaults(f=cmd_manifest)
    p = sp.add_parser("migrate"); p.add_argument("config"); p.set_defaults(f=cmd_migrate)
    p = sp.add_parser("info"); p.set_defaults(f=cmd_info)
    p = sp.add_parser("relabel", add_help=False); p.add_argument("rest", nargs=argparse.REMAINDER)
    p.set_defaults(f=lambda a: __import__("p3cv.tools.relabel", fromlist=["main"]).main(a.rest))
    p = sp.add_parser("preview"); p.add_argument("config"); p.add_argument("--times"); p.add_argument("--ar"); p.set_defaults(f=cmd_preview)
    p = sp.add_parser("status"); p.add_argument("config"); p.set_defaults(f=cmd_status)
    p = sp.add_parser("stages"); p.set_defaults(f=cmd_stages)
    p = sp.add_parser("download"); p.add_argument("urls", nargs="+"); p.add_argument("--out", default="src")
    p.set_defaults(f=lambda a: __import__("p3cv.stages.download", fromlist=["main"]).main(a.urls + ["--out", a.out]))
    a = ap.parse_args(argv)
    try:
        return a.f(a) or 0
    except P3VError as e:
        print(f"ERROR {e}", file=sys.stderr); return 3 if e.code == "E_PENDING" else 2


if __name__ == "__main__":
    sys.exit(main())
