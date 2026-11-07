"""Uniform invocation contract (docs/CONTRACT.md): result envelope, delivery manifest, migration.

Every agent calls the skill the same way - `python -m p3cv run PRODUCT_JSON [stages] --json-out FILE` -
and reads the same envelope back:
  {"skill", "version", "config_schema", "status": ok|pending|error, "exit_code", "project",
   "stages": {name: outputs}, "error": {code, message, hint} | null}
Exit codes: 0 ok, 2 error, 3 pending (still rendering: call again), 1 usage/environment problem.
"""
import hashlib, json, time
from pathlib import Path
from . import __version__
from .config import CONFIG_SCHEMA, SKILL_ROOT

SKILL_NAME = "product-3d-canvas-video-landing"
EXIT = {"ok": 0, "error": 2, "pending": 3}


def envelope(cfg_path, status, stages=None, error=None):
    return {"skill": SKILL_NAME, "version": __version__, "config_schema": CONFIG_SCHEMA, "status": status,
            "exit_code": EXIT[status], "project": str(Path(cfg_path).resolve().parent),
            "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "stages": stages or {}, "error": error}


def sha256(p, bs=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(bs), b""):
            h.update(b)
    return h.hexdigest()


KINDS = [("landing_html", "-landing-page-animated.html"), ("video_16x9", "_16x9_4K.mp4"), ("video_9x16", "_9x16_4K.mp4"),
         ("thumbnail", "youtube-thumbnail-"), ("seo", "youtube-seo-title-description-"), ("srt", "-subtitles-en.srt"),
         ("vo_script", "-voiceover-script-en.txt"), ("delivery", "delivery.json")]


def kind_of(name):
    for k, pat in KINDS:
        if pat in name:
            return k
    return "other"


def manifest(cfg):
    """Write PROJ/out/manifest.json: every deliverable with kind, bytes and sha256, plus versions."""
    out = cfg.proj / "out"; files = []
    for f in sorted(out.glob("*")):
        if f.is_file() and f.name != "manifest.json":
            files.append({"file": f"out/{f.name}", "kind": kind_of(f.name), "bytes": f.stat().st_size, "sha256": sha256(f)})
    st = {}
    sp = cfg.proj / "state.json"
    if sp.exists():
        st = {k: v.get("status") for k, v in json.loads(sp.read_text()).items()}
    m = {"skill": SKILL_NAME, "version": __version__, "config_schema": CONFIG_SCHEMA, "slug": cfg.slug,
         "product_name": cfg["product_name"], "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
         "stages": st, "files": files,
         "missing": [k for k, _ in KINDS[:7] if not any(x["kind"] == k for x in files)]}
    (out / "manifest.json").write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
    return m


def migrate(path):
    """Upgrade a product.json to CONFIG_SCHEMA in place (keeps a .bak). Schema 1 = v1.x files; files
    without schema_version are v1.0/1.1 and only gain the key. Add one step per future schema bump."""
    p = Path(path); raw = json.loads(p.read_text(encoding="utf-8")); v = raw.get("schema_version", 1); steps = []
    # future: if v == 1: <transform>; v = 2; steps.append("1->2 ...")
    if raw.get("schema_version") != CONFIG_SCHEMA:
        raw = {"schema_version": CONFIG_SCHEMA, **{k: x for k, x in raw.items() if k != "schema_version"}}
        steps.append(f"set schema_version {CONFIG_SCHEMA}")
    if steps:
        p.with_suffix(".json.bak").write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        p.write_text(json.dumps(raw, indent=1, ensure_ascii=False), encoding="utf-8")
    return {"file": str(p), "from": v, "to": CONFIG_SCHEMA, "steps": steps}


def info():
    return json.loads((SKILL_ROOT / "skill.json").read_text(encoding="utf-8"))
