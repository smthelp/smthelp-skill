"""Stage 5 — frames: N frames per video (labelled with rank) tiled into contact sheets for visual relevance review.
Captions lie (hashtag spam, talking heads), so the reviewer — agent or human — must look at these."""
import glob, os, shutil, subprocess
from . import io, log, media
from .errors import DyhError

def run(cfg):
    fr = cfg["frames"]; vdir = io.p(cfg, "videos"); sdir = io.p(cfg, "sheets")
    tmp = os.path.join(sdir, "_frames"); os.makedirs(tmp, exist_ok=True)
    files = sorted(glob.glob(os.path.join(vdir, "*.mp4")))
    if not files: raise DyhError("E_STAGE_INPUT", vdir)
    if not shutil.which("montage"): raise DyhError("E_DEP", "imagemagick montage")
    n = fr["thumb"]
    for f in files:
        rank = os.path.basename(f).split("_")[0]; d = media.duration(cfg, f)
        for pos in fr["positions"]:
            out = os.path.join(tmp, f"{rank}_{pos:.2f}.jpg")
            if os.path.exists(out): continue
            vf = (f"scale={n}:{n}:force_original_aspect_ratio=decrease,pad={n}:{n}:(ow-iw)/2:(oh-ih)/2,"
                  f"drawtext=text='{rank}':x=4:y=4:fontsize=26:fontcolor=yellow:box=1:boxcolor=black")
            subprocess.run([cfg["ffmpeg"], "-v", "error", "-ss", f"{d*pos:.2f}", "-i", f, "-frames:v", "1",
                            "-vf", vf, "-y", out])
    frames = sorted(glob.glob(os.path.join(tmp, "*.jpg")))
    cols, rows = map(int, fr["tile"].split("x")); per = cols * rows
    per -= per % len(fr["positions"])
    sheets = []
    for i in range(0, len(frames), per):
        out = os.path.join(sdir, f"sheet_{i//per+1:02d}.jpg")
        subprocess.run(["montage", *frames[i:i+per], "-tile", fr["tile"], "-geometry", "+2+2", out], check=True)
        sheets.append(out)
    log.event("frames", "done", videos=len(files), sheets=sheets)
    return sheets
