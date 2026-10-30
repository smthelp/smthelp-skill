#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 1 helper: pull text and figures out of product source files for review.

Usage:
    python3 scripts/extract_sources.py <file-or-folder> [...] --out work/<slug>/src

For each PDF: <name>.txt (pdftotext -layout), page renders p<N>.png at 110 dpi (for reading
screenshots of Taobao/1688 listings that are images), and embedded images (pdfimages -png).
For each image: copied as-is. Writes sources_index.json listing every output.

Nothing here decides what is true. Read every render and crop yourself: supplier watermarks,
shop names, prices and other brands' logos must never reach the page (see references/input-spec.md).
"""
import argparse, json, os, shutil, subprocess, sys


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=300).returncode == 0
    except Exception:
        return False


def pdf(path, out):
    base = os.path.splitext(os.path.basename(path))[0][:60].replace(" ", "_")
    d = os.path.join(out, base)
    os.makedirs(d, exist_ok=True)
    res = {"source": path, "dir": d}
    if shutil.which("pdftotext"):
        run(["pdftotext", "-layout", path, os.path.join(d, "text.txt")])
    else:
        try:
            import fitz  # pymupdf
            doc = fitz.open(path)
            open(os.path.join(d, "text.txt"), "w").write("\n\f".join(p.get_text() for p in doc))
        except Exception as e:
            res["text_error"] = str(e)
    if shutil.which("pdftoppm"):
        run(["pdftoppm", "-r", "110", "-png", path, os.path.join(d, "p")])
    if shutil.which("pdfimages"):
        os.makedirs(os.path.join(d, "img"), exist_ok=True)
        run(["pdfimages", "-png", path, os.path.join(d, "img", "x")])
    t = os.path.join(d, "text.txt")
    res["text_chars"] = len(open(t, errors="ignore").read().strip()) if os.path.exists(t) else 0
    res["renders"] = sorted(f for f in os.listdir(d) if f.startswith("p") and f.endswith(".png"))
    res["images"] = len(os.listdir(os.path.join(d, "img"))) if os.path.isdir(os.path.join(d, "img")) else 0
    if res["text_chars"] < 200:
        res["note"] = "little or no text layer: read the page renders (listing screenshots are usually images)"
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    files = []
    for i in a.inputs:
        if os.path.isdir(i):
            files += [os.path.join(i, f) for f in sorted(os.listdir(i))]
        else:
            files.append(i)
    idx = []
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext == ".pdf":
            idx.append(pdf(f, a.out))
        elif ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            dst = os.path.join(a.out, "images", os.path.basename(f))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(f, dst)
            idx.append({"source": f, "copy": dst})
    json.dump(idx, open(os.path.join(a.out, "sources_index.json"), "w"), ensure_ascii=False, indent=1)
    for r in idx:
        print(json.dumps(r, ensure_ascii=False)[:300])


if __name__ == "__main__":
    main()
