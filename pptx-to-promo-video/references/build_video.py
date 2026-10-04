#!/usr/bin/env python3
"""Step 4 of Doc->Promo pipeline.

Build a crossfade slideshow video from:
  - slides_1080/slide-01.png ... (rendered pages)
  - audio/durations.json  (per-slide seconds + narration list)
  - audio/full/slide_NN.wav (voiceover clips)

Each non-last slide's audio is trimmed by `xfade` seconds so audio seams line
up with the video crossfades. Output: H.264 MP4 with AAC audio.

Optional: burn the English narration as on-screen subtitles with --subtitles.
Subtitles are composited onto the slide PNGs with Pillow (PIL) -- this avoids
any dependency on ffmpeg's drawtext/libass filters, which are often absent in
prebuilt ffmpeg builds. Text is auto-wrapped and centered with a semi-transparent
backing box for readability on any background.

Usage:
    python3 build_video.py --base . --out promo.mp4
    python3 build_video.py --base . --out promo.mp4 --xfade 0.5 --fps 25
    python3 build_video.py --base . --out promo_sub.mp4 --subtitles
    python3 build_video.py --base . --out promo_sub.mp4 --subtitles --subtitle-size 48
    python3 build_video.py --base . --out promo_sub.mp4 --subtitles \
        --subtitle-color 0,163,180 --accent-color 144,169,61
"""
import argparse, json, os, shutil, subprocess, sys


def which(*names, fallback=None):
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return fallback


def burn_subtitles(py, base, slides, narration, fontfile, size,
                   text_color=(255, 255, 255), accent_color=None, box_alpha=150,
                   transparent=False):
    """Render each slide PNG with its narration line baked in.

    text_color:   RGB tuple for the subtitle text (default white).
    accent_color: optional RGB tuple -> draws a brand-colored vertical bar
                  on the left edge of the subtitle box (logo color reference).
    box_alpha:    opacity of the dark backing box (0-255).
    Returns the directory containing the burned PNGs (slides_sub)."""
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

        # wrap text to ~88% width
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
        # dark backing box for readability (skipped in transparent mode)
        if not transparent:
            draw.rectangle([0, box_y0, W, box_y0 + box_h], fill=(0, 0, 0, box_alpha))
            # brand accent bar on the left edge
            if accent_color:
                bar_w = max(10, int(size * 0.22))
                draw.rectangle([28, box_y0 + 12, 28 + bar_w, box_y0 + box_h - 12],
                               fill=accent_color + (255,))
        ty = box_y0 + 22
        for ln in wrapped:
            tw = draw.textlength(ln, font=font)
            tx = (W - tw) / 2
            # transparent mode: no box, add a thin outline for legibility
            stroke = 2 if transparent else 0
            draw.text((tx, ty), ln, font=font, fill=text_color + (255,),
                      stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
            ty += lh

        img.convert("RGB").save(dst)
    return out_dir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".")
    ap.add_argument("--slides", default="slides_1080")
    ap.add_argument("--audio", default="audio")
    ap.add_argument("--out", default="promo.mp4")
    ap.add_argument("--xfade", type=float, default=0.3)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--subtitles", action="store_true",
                    help="Burn the English narration as on-screen subtitles (PIL).")
    ap.add_argument("--fontfile",
                    default="/System/Library/Fonts/Supplemental/Arial.ttf",
                    help="TTF used for burned subtitles (must support the text).")
    ap.add_argument("--subtitle-size", type=int, default=52)
    ap.add_argument("--subtitle-color", default="255,255,255",
                    help="RGB of subtitle text, e.g. '0,163,180' (logo teal).")
    ap.add_argument("--accent-color", default=None,
                    help="Optional RGB brand accent bar, e.g. '144,169,61'.")
    ap.add_argument("--transparent-bg", action="store_true",
                    help="Subtitles with NO dark box and NO accent bar "
                         "(transparent background); adds a thin outline for legibility.")
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

    # Optional subtitle burning (before video assembly)
    img_dir = args.slides
    if args.subtitles:
        if not narration:
            sys.exit("ERROR: durations.json has no narration; cannot burn subtitles.")
        try:
            tc = tuple(int(x) for x in args.subtitle_color.split(","))
            ac = tuple(int(x) for x in args.accent_color.split(",")) if args.accent_color else None
        except Exception:
            sys.exit("ERROR: color must be 'R,G,B' e.g. '0,163,180'.")
        if len(tc) != 3:
            sys.exit("ERROR: --subtitle-color must be 3 ints 'R,G,B'.")
        img_dir = burn_subtitles(sys.executable, args.base, args.slides,
                                 narration, args.fontfile, args.subtitle_size,
                                 text_color=tc, accent_color=ac,
                                 transparent=args.transparent_bg)

    # 1) Trim audio segments (drop T from tail of every non-last slide) + concat
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

    # 2) xfade filter chain for video
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

    cmd = [ffmpeg, "-y", "-loglevel", "error"]
    cmd += inputs
    cmd += ["-i", track]
    cmd += ["-filter_complex", fc]
    cmd += ["-map", "[vout]", "-map", f"{N}:a"]
    cmd += ["-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-r", str(args.fps), "-shortest",
            os.path.join(args.base, args.out)]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit("ffmpeg failed")

    total = sum(D) - (N - 1) * T
    sub_note = " (with burned subtitles)" if args.subtitles else ""
    print(f"OK -> {args.out}  ({total:.1f}s, {N} slides, xfade={T}s){sub_note}")


if __name__ == "__main__":
    main()
