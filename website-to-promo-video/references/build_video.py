#!/usr/bin/env python3
"""Build a crossfade slideshow promo video from slides + TTS voiceover.

Enhanced variant of the pptx-to-promo-video build step, with:
  - burned English subtitles (PIL) -- no libfreetype/libass needed
  - --bold  : use Arial Bold TTF (thicker, more legible on small screens)
  - --subtitle-color R,G,B  : e.g. '10,165,165' == #0AA5A5
  - --accent-color R,G,B    : optional brand bar on the left of the sub box
  - --bgm PATH  : mix a royalty-free BGM track under the voiceover
                  (looped, low volume, video stream copied -- fast)

Pipeline:
  slides_sel/slide-01.png ...        (1920x1080 rendered pages)
  audio/durations.json                (per-slide seconds + narration list)
  audio/full/slide_NN.wav            (voiceover clips)
  [optional] audio/bgm.mp3           (royalty-free background music)

Each non-last slide's audio is trimmed by `xfade` seconds so audio seams
line up with the video crossfades. With --bgm, the BGM is mixed in last.

Usage:
  python3 build_video.py --base . --out promo.mp4
  python3 build_video.py --base . --out promo_sub.mp4 --subtitles --bold \
        --subtitle-color 10,165,165 --accent-color 144,169,61
  python3 build_video.py --base . --out promo_bgm.mp4 --subtitles --bold \
        --subtitle-color 10,165,165 --bgm audio/bgm.mp3
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

def which(*names, fallback=None):
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return fallback

def burn_subtitles(base, slides, narration, fontfile, size,
                   text_color=(255, 255, 255), accent_color=None, box_alpha=150,
                   transparent_bg=False):
    """Render each slide PNG with its narration line baked in. Returns dir."""
    from PIL import Image, ImageDraw, ImageFont
    out_dir = os.path.join(base, "slides_sub")
    os.makedirs(out_dir, exist_ok=True)
    try:
        font = ImageFont.truetype(fontfile, size)
    except Exception:
        font = ImageFont.load_default()
    for i, line in enumerate(narration, 1):
        src = os.path.join(base, slides, f"slide-{i:02d}.png")
        dst = os.path.join(out_dir, f"slide-{i:02d}.png")
        img = Image.open(src).convert("RGBA")
        W, H = img.size
        draw = ImageDraw.Draw(img, "RGBA")
        maxw = int(W * 0.88)
        words = line.split()
        wrapped, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=font) <= maxw:
                cur = test
            else:
                if cur:
                    wrapped.append(cur)
                cur = w
        if cur:
            wrapped.append(cur)
        if not wrapped:
            wrapped = [line]
        lh = int(size * 1.3)
        th = lh * len(wrapped)
        box_h = th + 44
        box_y0 = H - box_h - 70
        if not transparent_bg:
            draw.rectangle([0, box_y0, W, box_y0 + box_h], fill=(0, 0, 0, box_alpha))
            if accent_color:
                bar_w = max(10, int(size * 0.22))
                draw.rectangle([28, box_y0 + 12, 28 + bar_w, box_y0 + box_h - 12],
                               fill=accent_color + (255,))
        ty = box_y0 + 22
        for ln in wrapped:
            tw = draw.textlength(ln, font=font)
            tx = (W - tw) / 2
            draw.text((tx, ty), ln, font=font, fill=text_color + (255,))
            ty += lh
        img.convert("RGB").save(dst)
    return out_dir

def parse_rgb(s, name):
    try:
        t = tuple(int(x) for x in s.split(","))
    except Exception:
        sys.exit(f"ERROR: --{name} must be 'R,G,B' e.g. '10,165,165'.")
    if len(t) != 3:
        sys.exit(f"ERROR: --{name} must be 3 ints 'R,G,B'.")
    return t

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".")
    ap.add_argument("--slides", default="slides_sel")
    ap.add_argument("--audio", default="audio")
    ap.add_argument("--out", default="promo.mp4")
    ap.add_argument("--xfade", type=float, default=0.4)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--subtitles", action="store_true",
                    help="Burn English narration as on-screen subtitles (PIL).")
    ap.add_argument("--bold", action="store_true",
                    help="Use Arial Bold TTF for subtitles (thicker/legible).")
    ap.add_argument("--fontfile", default=None,
                    help="TTF for burned subtitles (default Arial / Arial Bold).")
    ap.add_argument("--subtitle-size", type=int, default=52)
    ap.add_argument("--subtitle-color", default="255,255,255",
                    help="RGB of subtitle text, e.g. '10,165,165' == #0AA5A5.")
    ap.add_argument("--accent-color", default=None,
                    help="Optional RGB brand accent bar, e.g. '144,169,61'.")
    ap.add_argument("--transparent-bg", action="store_true",
                    help="Render subtitles with no background box or accent bar.")
    ap.add_argument("--bgm", default=None,
                    help="Royalty-free BGM mp3 to mix under the voiceover.")
    ap.add_argument("--bgm-volume", type=float, default=0.18,
                    help="BGM relative volume vs voiceover (default 0.18).")
    args = ap.parse_args()

    ffmpeg = which("ffmpeg", fallback="/opt/homebrew/bin/ffmpeg")
    if not ffmpeg:
        sys.exit("ERROR: ffmpeg required.")

    with open(os.path.join(args.base, args.audio, "durations.json"), encoding="utf-8") as f:
        meta = json.load(f)
    D = meta["durations"]
    narration = meta.get("narration", [])
    N = len(D)
    T = args.xfade

    # --- subtitle burning (before video assembly) ---
    img_dir = args.slides
    if args.subtitles:
        if not narration:
            sys.exit("ERROR: durations.json has no narration; cannot burn subtitles.")
        tc = parse_rgb(args.subtitle_color, "subtitle-color")
        ac = parse_rgb(args.accent_color, "accent-color") if args.accent_color else None
        fontfile = args.fontfile
        if fontfile is None:
            fontfile = ("/System/Library/Fonts/Supplemental/Arial Bold.ttf"
                        if args.bold else
                        "/System/Library/Fonts/Supplemental/Arial.ttf")
        img_dir = burn_subtitles(args.base, args.slides, narration, fontfile,
                                 args.subtitle_size, text_color=tc, accent_color=ac,
                                 transparent_bg=args.transparent_bg)

    # --- 1) trim audio segs + concat voiceover ---
    seg_dir = os.path.join(args.base, "work", "segs")
    os.makedirs(seg_dir, exist_ok=True)
    seg_files = []
    for i in range(N):
        src = os.path.join(args.base, args.audio, "full", f"slide_{i+1:02d}.wav")
        dst = os.path.join(seg_dir, f"seg_{i+1:02d}.wav")
        if i < N - 1:
            dur = max(0.1, D[i] - T)
            subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", src,
                            "-t", f"{dur:.3f}", "-c", "copy", dst], check=True)
        else:
            subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", src,
                            "-c", "copy", dst], check=True)
        seg_files.append(dst)
    list_path = os.path.join(seg_dir, "list.txt")
    with open(list_path, "w") as f:
        for s in seg_files:
            f.write(f"file '{os.path.abspath(s)}'\n")
    track = os.path.join(args.base, "work", "voiceover.wav")
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", list_path, "-c", "copy", track], check=True)

    # --- 2) xfade video filter chain ---
    inputs = []
    for i in range(N):
        img = os.path.join(args.base, img_dir, f"slide-{i+1:02d}.png")
        inputs += ["-loop", "1", "-t", f"{D[i]:.3f}", "-i", img]
    xfades = []
    prev = "0:v"
    for t in range(1, N):
        prefix = sum(D[:t])
        offset = prefix - t * T
        out = f"v{t}"
        xfades.append(
            f"[{prev}][{t}:v]xfade=transition=fade:duration={T}:offset={offset:.3f}[{out}]")
        prev = out
    fc = ";".join(xfades) + f";[{prev}]format=yuv420p[vout]"

    # write the (no-BGM) video to a temp file first if BGM will be mixed
    clean_path = args.out
    bgm_tmp = None
    if args.bgm:
        bgm_tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False,
                                              dir=os.path.join(args.base, "work"))
        clean_path = bgm_tmp.name

    cmd = [ffmpeg, "-y", "-loglevel", "error"]
    cmd += inputs
    cmd += ["-i", track]
    cmd += ["-filter_complex", fc]
    cmd += ["-map", "[vout]", "-map", f"{N}:a"]
    cmd += ["-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-r", str(args.fps), "-shortest",
            os.path.join(args.base, clean_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit("ffmpeg failed")

    total = sum(D) - (N - 1) * T

    # --- 3) optional BGM mix (video stream copied, fast) ---
    if args.bgm:
        if not os.path.exists(args.bgm):
            sys.exit(f"ERROR: BGM file not found: {args.bgm}")
        bgm_out = os.path.join(args.base, args.out)
        mix = (f"[1:a]volume={args.bgm_volume:.3f}[bg];"
                f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=0[a]")
        cmd2 = [ffmpeg, "-y", "-loglevel", "error",
                 "-i", clean_path, "-stream_loop", "-1", "-i", args.bgm,
                 "-filter_complex", mix,
                 "-map", "0:v", "-map", "[a]",
                 "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                 bgm_out]
        r2 = subprocess.run(cmd2, capture_output=True, text=True)
        if r2.returncode != 0:
            print(r2.stderr[-3000:])
            sys.exit("ffmpeg BGM mix failed")
        try:
            os.remove(clean_path)
        except OSError:
            pass
        sub_note = " (subtitles + BGM)" if args.subtitles else " (BGM)"
        print(f"OK -> {args.out}  ({total:.1f}s, {N} slides, xfade={T}s){sub_note}")
    else:
        sub_note = " (with burned subtitles)" if args.subtitles else ""
        print(f"OK -> {args.out}  ({total:.1f}s, {N} slides, xfade={T}s){sub_note}")

if __name__ == "__main__":
    main()
