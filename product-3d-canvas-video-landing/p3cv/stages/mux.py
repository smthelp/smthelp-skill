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
            raise P3VError("E_PENDING", "still rendering (timeout reached) - run mux again later", "progress: " + prog)
        time.sleep(poll)


def upscale_chunks(cfg, ar, chunks):
    """video.upscale with video.scale 1: render at 1080p (fast) and lanczos-upscale each chunk to 4K.
    One chunk at a time, one thread, short lookahead: 4K x264 with default settings was OOM-killed
    on 8 GB sandboxes shared with other jobs. Returns the chunk file list to concat."""
    tmp = cfg.tmp_dir; W, H = (3840, 2160) if ar == "169" else (2160, 3840); files = []
    for k, _, _ in chunks:
        src, dst = tmp / f"{ar}_{k:02d}.mp4", tmp / f"{ar}_{k:02d}_up.mp4"
        if not dst.exists():
            part = dst.with_suffix(".part.mp4")
            sh(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", f"scale={W}:{H}:flags=lanczos,format=yuv420p",
                "-c:v", "libx264", "-preset", "medium", "-crf", str(cfg["video"]["crf"]), "-threads", "1",
                "-filter_threads", "1", "-x264-params", "rc-lookahead=0:bframes=2:ref=1", str(part)])
            part.rename(dst)
        files.append(dst)
    return files


@stage("mux", deps=["render", "mix"], desc="Wait for renders, concat chunks, add audio, verify")
def run(cfg, state, timeout=None):
    need("ffmpeg"); wait_all(cfg, timeout); tmp = cfg.tmp_dir; outs = {}
    _, chunks = plan(cfg)
    for ar in cfg["video"]["formats"]:
        lst = tmp / f"{ar}_list.txt"
        up = cfg["video"].get("upscale") and cfg["video"]["scale"] == 1
        files = upscale_chunks(cfg, ar, chunks) if up else [tmp / f"{ar}_{k:02d}.mp4" for k, _, _ in chunks]
        lst.write_text("".join(f"file '{f}'\n" for f in files))
        name = f"{cfg.video_basename}_{'16x9' if ar == '169' else '9x16'}_4K.mp4"
        tmpout = tmp / name
        sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(cfg.p("vo", "master.wav")),
            "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
            "-movflags", "+faststart", str(tmpout)])
        info = json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration,size",
                              "-of", "json", str(tmpout)]))
        st = [s for s in info["streams"] if s.get("width")][0]
        want = (3840, 2160) if ar == "169" else (2160, 3840)
        f = 2 if up else cfg["video"]["scale"]
        if (st["width"], st["height"]) != (want[0] * f // 2, want[1] * f // 2):
            log.get("mux").warning("%s is %sx%s", name, st["width"], st["height"])
        dest = cfg.p("out", name); shutil.copy(tmpout, dest)
        outs[ar] = {"file": str(dest.relative_to(cfg.proj)), "w": st["width"], "h": st["height"],
                    "duration": round(float(info["format"]["duration"]), 2), "bytes": int(info["format"]["size"])}
        log.get("mux").info("%s %sx%s %.1fs", name, st["width"], st["height"], float(info["format"]["duration"]))
    return outs
