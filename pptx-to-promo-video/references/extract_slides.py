#!/usr/bin/env python3
"""Step 1 of Doc->Promo pipeline.

Render a PPTX (or PDF) into uniformly-sized 1920x1080 PNGs, one per page,
zero-padded as slide-01.png ... slide-NN.png.

Usage:
    python3 extract_slides.py path/to/doc.pptx --out slides_1080
    python3 extract_slides.py doc.pdf --out slides_1080 --w 1080 --h 1920
"""
import argparse, os, re, shutil, subprocess, sys


def which(*names, fallback=None):
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return fallback


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help=".pptx or .pdf file")
    ap.add_argument("--out", default="slides_1080", help="output dir for PNGs")
    ap.add_argument("--work", default="work", help="temp dir for pdf/png")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    args = ap.parse_args()

    soffice = which("soffice", "libreoffice", fallback="/opt/homebrew/bin/soffice")
    ffmpeg = which("ffmpeg", fallback="/opt/homebrew/bin/ffmpeg")
    pdftoppm = which("pdftoppm", fallback="/opt/homebrew/bin/pdftoppm")

    if not ffmpeg or not pdftoppm:
        sys.exit("ERROR: ffmpeg and pdftoppm are required.")

    base = os.path.dirname(os.path.abspath(args.input))
    work = os.path.join(base, args.work)
    os.makedirs(work, exist_ok=True)
    os.makedirs(args.out, exist_ok=True)

    src = os.path.abspath(args.input)

    # 1) PPTX -> PDF (skip if already PDF)
    if src.lower().endswith(".pdf"):
        pdf = src
    else:
        if not soffice:
            sys.exit("ERROR: soffice/libreoffice required to convert PPTX.")
        print("Converting PPTX -> PDF ...")
        subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                        "--outdir", work, src,
                        "-env:UserInstallation=file:///tmp/lo_profile"], check=True)
        pdf = os.path.join(work, os.path.splitext(os.path.basename(src))[0] + ".pdf")

    # 2) PDF -> per-page PNG
    print("Rendering PDF -> PNG ...")
    subprocess.run([pdftoppm, "-png", "-r", str(args.dpi), pdf,
                   os.path.join(work, "slide")], check=True)

    # 3) scale+crop to target, zero-pad rename (FIX: numeric sort, not lexicographic)
    pngs = [f for f in os.listdir(work) if f.startswith("slide") and f.endswith(".png")]
    pngs.sort(key=lambda f: int(re.search(r"(\d+)", f).group(1)))
    print(f"Found {len(pngs)} pages")
    for i, f in enumerate(pngs, 1):
        out = os.path.join(args.out, f"slide-{i:02d}.png")
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", os.path.join(work, f),
                        "-vf", f"scale={args.w}:{args.h}:force_original_aspect_ratio=increase,crop={args.w}:{args.h}",
                        out], check=True)
    print(f"Slides ready: {args.out}/slide-01.png ... slide-{len(pngs):02d}.png")


if __name__ == "__main__":
    main()
