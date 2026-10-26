"""Stage 8 - render: 4K frames via Chromium CDP screenshots (1920x1080 css px x scale 2) piped to
ffmpeg. Work is split into video.chunks per format and launched as DETACHED workers
(p3cv.render_worker) writing to video.tmp_dir (default /tmp/p3cv-<slug>; writing mp4 straight to a
network workspace can fail with I/O errors). This stage returns immediately unless --wait;
`p3cv status` shows progress, `p3cv run mux` waits for completion.
Speed reference: ~1.5-3 frames/s per worker; 2 formats x 130 s x 30 fps ~ 25-60 min."""
import json, os, subprocess, sys
from . import stage
from ..config import SKILL_ROOT
from ..util import need
from .. import log


def plan(cfg):
    tl = json.loads(cfg.p("vo", "timeline.json").read_text())
    n = int(tl["total"] * cfg["video"]["fps"]); k = max(1, int(cfg["video"]["chunks"]))
    if cfg["video"].get("max_seconds"):  # smoke-test renders: only the first N seconds
        n = min(n, int(cfg["video"]["max_seconds"] * cfg["video"]["fps"]))
    step = (n + k - 1) // k
    return n, [(i, i * step, min(n, (i + 1) * step)) for i in range(k) if i * step < n]


def chunk_status(cfg):
    n, chunks = plan(cfg); tmp = cfg.tmp_dir; res = {}
    for ar in cfg["video"]["formats"]:
        for k, a, b in chunks:
            lf = tmp / f"{ar}_{k:02d}.log"; last = ""
            if lf.exists():
                lines = [l for l in lf.read_text().splitlines() if l.strip()]
                last = lines[-1] if lines else ""
            res[f"{ar}_{k:02d}"] = {"done": (tmp / f"{ar}_{k:02d}.done").exists(), "range": [a, b], "last": last}
    return res


def running_workers():
    try:
        out = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True).stdout
    except Exception:
        return []
    return [l for l in out.splitlines() if "p3cv.render_worker" in l]


@stage("render", deps=["video"], desc="Launch detached 4K render workers (resumable, chunked)")
def run(cfg, state, wait=False):
    need("ffmpeg"); lg = log.get("render")
    n, chunks = plan(cfg); tmp = cfg.tmp_dir; live = " ".join(running_workers()); launched = 0
    for ar in cfg["video"]["formats"]:
        for k, a, b in chunks:
            if (tmp / f"{ar}_{k:02d}.done").exists():
                continue
            if f"{cfg.path} {ar} {k} " in live:
                lg.info("chunk %s_%02d already running", ar, k); continue
            logf = open(tmp / f"{ar}_{k:02d}.log", "a")
            subprocess.Popen([sys.executable, "-m", "p3cv.render_worker", str(cfg.path), ar, str(k), str(a), str(b)],
                             cwd=str(SKILL_ROOT), stdout=logf, stderr=subprocess.STDOUT, start_new_session=True,
                             env=dict(os.environ))
            launched += 1
    lg.info("%d frames per format, %d chunks each; launched %d workers (tmp %s)", n, len(chunks), launched, tmp)
    if wait:
        from .mux import wait_all
        wait_all(cfg)
    return {"frames": n, "chunks": len(chunks), "launched": launched, "tmp": str(tmp)}
