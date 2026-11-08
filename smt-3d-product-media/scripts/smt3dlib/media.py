"""Real footage cutting, caption overlay, voiceover (TTS), final encode and mux.
ffmpeg note: always encode to a local temp dir then copy (network/FUSE filesystems such as JuiceFS break mp4 +faststart)."""
import glob, json, os, shutil, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

FONT_MIRRORS = ["https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/SubsetOTF/SC/NotoSansSC-{W}.otf",
                "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/SubsetOTF/SC/NotoSansSC-{W}.otf"]
CACHE = os.path.expanduser("~/.cache/smt3d")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(f"M01 command failed: {' '.join(cmd[:6])} ...\n{r.stderr[-3000:]}")
    return r.stdout

def dur(f): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).strip())

def fonts(job):
    o = job["overlay"]; res = {}
    for w in ("bold", "regular"):
        f = o.get(f"font_{w}")
        if f and os.path.exists(job.path(f)): res[w] = job.path(f); continue
        W = w.title()
        cands = [f for pat in (f"{CACHE}/fonts/NotoSansSC-{W}.otf", f"/usr/share/fonts/**/NotoSans*SC*{W}*", f"/usr/share/fonts/**/NotoSans*CJK*{W}*",
                                f"{os.path.expanduser('~')}/.fonts/**/NotoSans*SC*{W}*") for f in glob.glob(pat, recursive=True) if os.path.getsize(f) > 1e6]
        if not cands:   # download Noto Sans SC (OFL) once into the user cache
            os.makedirs(f"{CACHE}/fonts", exist_ok=True); dst = f"{CACHE}/fonts/NotoSansSC-{W}.otf"
            for u in FONT_MIRRORS:
                if subprocess.run(["curl", "-fsSL", "--max-time", "300", "-o", dst, u.format(W=W)]).returncode == 0 and os.path.getsize(dst) > 1e6:
                    cands = [dst]; break
            if not cands: raise SystemExit("M02 no CJK font: set overlay.font_bold / font_regular to a Noto Sans SC (or other CJK) font file")
        res[w] = cands[0]
    return res

# ---------------- real footage ----------------
def cut_real(job):
    R = job["render"]; W, H, fps = R["width"], R["height"], R["fps"]; out = []
    for i, c in enumerate(job.get("real_clips", [])):
        d = job.wdir(f"real/r{i+1}")
        if len(glob.glob(d + "/f*.jpg")) and not c.get("force"): out.append(d); continue
        for f in glob.glob(d + "/f*.jpg"): os.remove(f)
        fit = c.get("fit", "auto")
        if fit == "auto":
            w, h = map(int, run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", job.path(c["src"])]).strip().split(",")[:2])
            fit = "blur_pad" if w / h < W / H * 0.9 else "cover"
        if fit == "blur_pad":   # vertical/portrait footage: sharp centre over a blurred full-frame copy
            vf = (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=20:2[bg];"
                  f"[b]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps={fps}")
        else:
            vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps}"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(c.get("start", 0)), "-t", str(c["dur"]), "-i", job.path(c["src"]),
               "-filter_complex" if fit == "blur_pad" else "-vf", vf, "-q:v", "3", f"{d}/f%05d.jpg"]
        run(cmd); out.append(d)
    return out

# ---------------- captions ----------------
def _seq(job, L):
    """resolve job.sequence into [(frame_file, head, sub, step, note, t_in_segment)]"""
    fps = job["render"]["fps"]; raw = sorted(glob.glob(job.wdir("frames3d") + "/f*.jpg"))
    from .motion import Timeline
    tl = Timeline(job); o = job["overlay"]; note3d = job.get("disclosure", {}).get(L, "")
    seq_spec = job.get("sequence") or [{"type": "3d", "from": 0, "to": tl.total}]
    nreal = len(job.get("real_clips", [])); seq = []
    for seg in seq_spec:
        if seg["type"] == "3d":
            a, b = int(round(seg["from"] * fps)), int(round(seg["to"] * fps))
            if len(raw) < b: raise SystemExit(f"M10 only {len(raw)} 3D frames, sequence needs {b}: run `render` first")
            for i in range(a, b):
                t = i / fps; k, sc, ts = tl.at(t)
                cap = (seg.get("caption") or sc.get("caption") or {}).get(L, {})
                seq.append((raw[i], cap.get("head", ""), cap.get("sub", ""), cap.get("step", ""), note3d, ts if not seg.get("caption") else t - seg["from"]))
        elif seg["type"] == "real":
            c = job["real_clips"][seg["clip"]]; fs = sorted(glob.glob(job.wdir(f"real/r{seg['clip']+1}") + "/f*.jpg"))
            if not fs: raise SystemExit(f"M11 real clip {seg['clip']} not cut: run `real` first")
            for j, f in enumerate(fs):
                seq.append((f, c.get("head", o["real_head"]).get(L, ""), c["caption"].get(L, ""), c.get("step", f"{seg['clip']+1}/{nreal}"),
                            o["real_note"].get(L, ""), j / fps))
    return seq

def overlay(job, L):
    """brand bar + step caption + subtitle box + disclosure footer. Layout is designed at 1280x720 and scales with height;
    text that would overflow is shrunk to fit."""
    o = job["overlay"]; R = job["render"]; W, H = R["width"], R["height"]; F = fonts(job); k = H / 720.0
    col = {kk: tuple(v) for kk, v in o["colors"].items()}
    logo = Image.open(job.path(o["logo"])).convert("RGBA"); lw = int(200 * k); logo = logo.resize((lw, int(logo.height * lw / logo.width)))
    S = lambda v: int(round(v * k))
    def ft(w, size, text=None, maxw=None):
        size = S(size)
        while True:
            f = ImageFont.truetype(F[w], max(8, size))
            if not text or not maxw or f.getlength(text) <= maxw or size <= 8: return f
            size -= 1
    d_out = job.wdir(f"cap_{L}")
    for f in glob.glob(d_out + "/f*.jpg"): os.remove(f)
    seq = _seq(job, L); bar, foot = S(70), S(36)
    for i, (f, head, sub, step, note, ts) in enumerate(seq):
        im = Image.open(f).convert("RGBA").resize((W, H))
        if o["enabled"]:
            d = ImageDraw.Draw(im)
            d.rectangle((0, 0, W, bar), fill=col["bar"] + (235,)); im.alpha_composite(logo, (S(20), max(0, (bar - logo.height) // 2))); d = ImageDraw.Draw(im)
            stepw = S(80) if step else 0; left = S(20) + lw + S(20); avail = W - left - stepw - S(30)
            d.text((left + avail // 2, bar // 2), head, font=ft("bold", 30, head, avail), fill="white", anchor="mm")
            if step: d.text((W - S(30), bar // 2), step, font=ft("bold", 26), fill=col["accent"], anchor="rm")
            if sub:
                a = min(1.0, ts * 2); box = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
                bd.rounded_rectangle((S(40), H - S(120), W - S(40), H - S(52)), radius=S(14), fill=(255, 255, 255, int(235 * a)),
                                     outline=col["box_outline"] + (int(255 * a),), width=max(1, S(3)))
                bd.text((W // 2, H - S(86)), sub, font=ft("bold", 25, sub, W - S(120)), fill=col["title"] + (int(255 * a),), anchor="mm")
                im.alpha_composite(box); d = ImageDraw.Draw(im)
            d.rectangle((0, H - foot, W, H), fill=col["bar"] + (235,))
            urlf = ft("bold", 18); urlw = int(urlf.getlength(o["footer_url"]))
            d.text((S(20), H - foot // 2), note, font=ft("regular", 18, note, W - urlw - S(60)), fill=(200, 215, 230), anchor="lm")
            d.text((W - S(20), H - foot // 2), o["footer_url"], font=urlf, fill="white", anchor="rm")
        im.convert("RGB").save(f"{d_out}/f{i:05d}.jpg", quality=92)
    return d_out, len(seq)

# ---------------- voiceover ----------------
def voice(job, L, total):
    v = job["voice"]
    if not v.get("enabled"): return None
    env = {k: x for k, x in os.environ.items() if "proxy" not in k.lower()}   # edge-tts rejects proxy URLs with ':' in the login
    d = job.wdir(f"voice_{L}"); inputs, filt, log = [], [], []
    lines = v["lines"]
    for i, ln in enumerate(lines):
        f = f"{d}/l{i:02d}.mp3"; meta = f + ".json"; key = {"voice": v["voices"][L], "text": ln[L], "rate": v.get("rate", "+0%")}
        if not (os.path.exists(f) and os.path.exists(meta) and json.load(open(meta)) == key):
            r = subprocess.run(["python3", "-m", "edge_tts", "--voice", key["voice"], f"--rate={key['rate']}", "--text", key["text"], "--write-media", f],
                               env=env, capture_output=True, text=True)
            if r.returncode: raise SystemExit(f"V01 TTS failed for line {i} ({L}): {r.stderr[-800:]}")
            json.dump(key, open(meta, "w"))
        slot = (ln.get("until", lines[i + 1]["at"] if i + 1 < len(lines) else total) - ln["at"]) - 0.1
        dd = dur(f); tempo = min(max(1.0, dd / slot), v["max_tempo"])
        if dd / tempo > slot + 0.05: log.append(f"V10 line {i} ({L}) runs {dd/tempo - slot:.2f}s past its slot: shorten the text")
        inputs += ["-i", f]; ms = int(ln["at"] * 1000)
        filt.append(f"[{i}:a]atempo={tempo:.3f},adelay={ms}|{ms}[a{i}]")
    n = len(lines)
    fc = ";".join(filt) + ";" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,apad,atrim=0:{total:.3f},loudnorm=I={v['loudness']}:TP=-1.5[out]"
    tmp = os.path.join(tempfile.gettempdir(), f"smt3d_vo_{L}.m4a")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]", "-ac", "2", "-ar", "48000", "-c:a", "aac", "-b:a", job["encode"]["audio_bitrate"], tmp])
    dst = job.work(f"voice_{L}.m4a"); shutil.copy(tmp, dst)
    return {"file": dst, "warnings": log}

# ---------------- encode ----------------
def encode(job, L, frames_dir, n_frames, audio=None, variant="Video"):
    fps = job["render"]["fps"]; E = job["encode"]; name = job.name(variant, L, ".mp4")
    tmpd = tempfile.mkdtemp(prefix="smt3d_"); v = os.path.join(tmpd, "v.mp4"); fin = os.path.join(tmpd, name)
    run(["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", f"{frames_dir}/f%05d.jpg", "-c:v", "libx264", "-preset", E["preset"],
         "-pix_fmt", "yuv420p", "-crf", str(E["crf"]), "-movflags", "+faststart", v])
    if audio: run(["ffmpeg", "-v", "error", "-y", "-i", v, "-i", audio, "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", fin])
    else: shutil.move(v, fin)
    dst = job.out("video", name); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(fin, dst); shutil.rmtree(tmpd, ignore_errors=True)
    got = dur(dst); want = n_frames / fps
    if got < want * 0.99: raise SystemExit(f"M20 encoded video is short ({got:.2f}s < {want:.2f}s)")
    return dst

def poster(job, video, t, dst):
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", "-update", "1", "-q:v", "2", dst]); return dst
