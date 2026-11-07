"""Pipeline runner: resolves stage order + dependencies, runs hooks, records state and events.

Dependency graph (stage -> needs):
  download
  capture   -> download
  tts
  mix       -> tts
  subtitles -> mix
  landing   -> download, capture
  video     -> subtitles, capture
  render    -> video
  mux       -> render, mix
  thumbnail
  docs      -> mix
  upload    (uploads whatever is in out/)
"""
import os, subprocess, time, traceback
from .stages import REGISTRY, ORDER, load_all
from .errors import P3VError
from .state import State
from . import log


def run_hook(cfg, when, stage):
    cmd = cfg["hooks"].get(f"{when}_{stage}") or cfg["hooks"].get(when)
    if not cmd:
        return
    env = dict(os.environ, P3CV_PROJ=str(cfg.proj), P3CV_STAGE=stage, P3CV_WHEN=when)
    r = subprocess.run(cmd, shell=True, cwd=cfg.proj, env=env, capture_output=True, text=True)
    if r.returncode:
        raise P3VError("E_HOOK", f"{when}_{stage} hook '{cmd}' exited {r.returncode}: {r.stderr[-300:]}")


def load_plugins(cfg):
    """Import every file in product.json "plugins" so it can register stages, sinks, adapters or
    TTS providers (see docs/EXTENDING.md). Core code is never edited for an extension."""
    import importlib.util
    for rel in cfg.get("plugins", []) or []:
        path = cfg.resolve(rel)
        if not path.exists():
            raise P3VError("E_CONFIG", f"plugin {rel} not found")
        spec = importlib.util.spec_from_file_location(f"p3cv_plugin_{path.stem}", path)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        log.get("pipeline").info("plugin loaded: %s", path.name)


def run(cfg, stages=None, force=False, collect=None, **kw):
    load_all(); load_plugins(cfg); load_all(); lg = log.get("pipeline"); st = State(cfg.proj)
    todo = stages or [s for s in ORDER if s != "upload" or cfg["upload"].get("auto", False)]
    unknown = [s for s in todo if s not in REGISTRY]
    if unknown:
        raise P3VError("E_CONFIG", f"unknown stage(s): {unknown}", f"valid: {', '.join(ORDER)}")
    results = collect if collect is not None else {}
    for name in todo:
        spec = REGISTRY[name]
        missing = [d for d in spec["deps"] if not st.done(d) and d not in results]
        if missing:
            raise P3VError("E_STAGE_ORDER", f"{name} needs {missing} first", f"p3cv run {' '.join(missing + [name])}")
        if st.done(name) and not force and name not in ("render", "mux", "upload") and stages is None:
            lg.info("skip %s (done; use --force or name it explicitly)", name); continue
        lg.info("== %s: %s", name, spec["desc"]); t0 = time.time()
        st.mark(name, "running"); log.event("stage_start", stage=name)
        try:
            run_hook(cfg, "pre", name)
            extra = {k: v for k, v in kw.items() if v is not None and k in spec["fn"].__code__.co_varnames}
            out = spec["fn"](cfg, st, **extra) or {}
            run_hook(cfg, "post", name)
        except P3VError as e:
            st.mark(name, "failed", error=e.as_dict()); log.event("stage_fail", stage=name, **e.as_dict())
            lg.error("%s failed: %s", name, e); raise
        except Exception as e:
            code = {"download": "E_DOWNLOAD", "capture": "E_CAPTURE", "tts": "E_TTS", "mix": "E_AUDIO",
                    "subtitles": "E_SUBTITLE", "landing": "E_ASSEMBLE", "video": "E_VIDEO_BUILD", "render": "E_RENDER",
                    "mux": "E_FFMPEG", "thumbnail": "E_THUMB", "upload": "E_UPLOAD"}.get(name, "E_CONFIG")
            err = {"code": code,
                   "message": f"{type(e).__name__}: {e}", "hint": "see logs/p3cv.log for the traceback"}
            lg.error("%s crashed:\n%s", name, traceback.format_exc())
            st.mark(name, "failed", error=err); log.event("stage_fail", stage=name, **err); raise
        secs = round(time.time() - t0, 1)
        status = "launched" if name == "render" and out.get("launched") and not kw.get("wait") else "done"
        st.mark(name, "done", outputs=out, seconds=secs); log.event("stage_done", stage=name, seconds=secs, outputs=out)
        lg.info("   %s %s in %.1fs: %s", name, status, secs, out); results[name] = out
    return results
