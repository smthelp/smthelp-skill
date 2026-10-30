"""Render worker: frames [a, b) of one aspect ratio -> TMP/<ar>_<k>.mp4 (+ .done marker).
Launched detached by stages/render.py, one process per chunk, so renders survive the 20-minute
limit of a single shell call and resume chunk-by-chunk after a crash.
Usage: python -m p3cv.render_worker PRODUCT_JSON AR CHUNK_INDEX START END"""
import base64, subprocess, sys, time
from pathlib import Path


def main():
    cfgp, ar, k, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from p3cv.config import Config
    cfg = Config(cfgp); v = cfg["video"]; fps = v["fps"]; sc = v["scale"]
    W, H = (1920, 1080) if ar == "169" else (1080, 1920)
    tmp = cfg.tmp_dir; out = tmp / f"{ar}_{k:02d}.mp4"; done = tmp / f"{ar}_{k:02d}.done"
    if done.exists():
        print("already done", out, flush=True); return
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg",
                           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(v["crf"]),
                           "-pix_fmt", "yuv420p", "-threads", "1", str(out)], stdin=subprocess.PIPE)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        cdp = pg.context.new_cdp_session(pg)
        pg.goto(cfg.p("build", "video_built.html").as_uri() + "?ar=" + ar); pg.wait_for_timeout(2500)
        t0 = time.time()
        for i in range(a, b):
            pg.evaluate(f"renderAt({i / fps})")
            r = cdp.send("Page.captureScreenshot", {"format": "jpeg", "quality": v["jpeg_quality"],
                                                     "clip": {"x": 0, "y": 0, "width": W, "height": H, "scale": sc}})
            ff.stdin.write(base64.b64decode(r["data"]))
            if (i - a) % 150 == 0:
                print(f"progress ar={ar} chunk={k} frame={i} of {a}-{b} elapsed={time.time()-t0:.0f}s", flush=True)
        br.close()
    ff.stdin.close()
    if ff.wait() != 0:
        print("ffmpeg failed", flush=True); sys.exit(2)
    done.write_text(str(b - a)); print("done", ar, k, flush=True)


if __name__ == "__main__":
    main()
