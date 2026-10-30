"""Stage 9 - mux: wait until every render chunk is done, concat chunks, add master.wav (AAC 192k),
write out/<basename>_16x9_4K.mp4 and _9x16_4K.mp4, verify size/duration with ffprobe.
If a worker died, mux relaunches it (resume) instead of failing, up to video.max_relaunch times.
Note: in shells with a hard time limit, call `p3cv run mux --timeout 1100` repeatedly."""
import json, shutil, time
from . import stage
from .render import chunk_status, plan, running_workers
from ..errors import P3VError
from ..util import run as sh, need
from .. import log


def wait_all(cfg, timeout=None, poll=20):
    lg = log.get("mux"); t0 = time.time(); relaunch = 0; last = None
    while True:
        st = chunk_status(cfg)
        if all(v["done"] for v in st.values()):
            return True
        if not running_workers():
            relaunch += 1
            if relaunch > cfg["video"].get("max_relaunch", 3):
                raise P3VError("E_RENDER", "render workers keep dying: " +
                               "; ".join(f"{k}: {v['last']}" for k, v in st.items() if not v["done"]),
                               f"see logs in {cfg.tmp_dir}")
            lg.warning("no live render worker; relaunching missing chunks (%d)", relaunch)
            from .render import run as render_run
            render_run(cfg, None)
        prog = "; ".join(f"{k}:{'done' if v['done'] else v['last'][-40:]}" for k, v in st.items())
        if prog != last:
            lg.info("waiting: %s", prog); last = prog
        if timeout and time.time() - t0 > timeout:
            raise P3VError("E_RENDER", "still rendering (timeout reached) - run mux again later", "progress: " + prog)
        time.sleep(poll)


@stage("mux", deps=["render", "mix"], desc="Wait for renders, concat chunks, add audio, verify")
def run(cfg, state, timeout=None):
    need("ffmpeg"); wait_all(cfg, timeout); tmp = cfg.tmp_dir; outs = {}
    _, chunks = plan(cfg)
    for ar in cfg["video"]["formats"]:
        lst = tmp / f"{ar}_list.txt"
        lst.write_text("".join(f"file '{tmp / f'{ar}_{k:02d}.mp4'}'\n" for k, _, _ in chunks))
        name = f"{cfg.video_basename}_{'16x9' if ar == '169' else '9x16'}_4K.mp4"
        tmpout = tmp / name
        sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(cfg.p("vo", "master.wav")),
            "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
            "-movflags", "+faststart", str(tmpout)])
        info = json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration,size",
                              "-of", "json", str(tmpout)]))
        st = [s for s in info["streams"] if s.get("width")][0]
        want = (3840, 2160) if ar == "169" else (2160, 3840)
        if (st["width"], st["height"]) != (want[0] * cfg["video"]["scale"] // 2, want[1] * cfg["video"]["scale"] // 2):
            log.get("mux").warning("%s is %sx%s", name, st["width"], st["height"])
        dest = cfg.p("out", name); shutil.copy(tmpout, dest)
        outs[ar] = {"file": str(dest.relative_to(cfg.proj)), "w": st["width"], "h": st["height"],
                    "duration": round(float(info["format"]["duration"]), 2), "bytes": int(info["format"]["size"])}
        log.get("mux").info("%s %sx%s %.1fs", name, st["width"], st["height"], float(info["format"]["duration"]))
    return outs
