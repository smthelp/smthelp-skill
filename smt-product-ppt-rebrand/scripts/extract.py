#!/usr/bin/env python3
"""Step 1 - extract text, tables and images from source PDF / PPTX / PPT files.

usage: extract.py <out_dir> <file> [<file> ...]
For each file writes <out_dir>/<stem>/text.md (slide/page text + tables), images/*.jpg
(>= 200x150 px, alpha flattened on white), contact.jpg (numbered thumbnails), and
<out_dir>/index.md listing every file with page count, characters and image count.
.ppt needs conversion first: LibreOffice if installed, else Google Drive (gws) conversion
(scripts/convert_ppt.sh). Image-only PDFs (few characters) are flagged NEEDS_VISUAL_READ."""
import glob, os, re, shutil, subprocess, sys
from PIL import Image, ImageDraw

MIN_W, MIN_H = 200, 150

def save_img(src, dst):
    im = Image.open(src)
    if im.size[0] < MIN_W or im.size[1] < MIN_H: return False
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); im = bg
    else: im = im.convert("RGB")
    im.thumbnail((1600, 1600)); im.save(dst, quality=88); return True

def contact(imgdir, out):
    ims = sorted(glob.glob(os.path.join(imgdir, "*.jpg")))
    if not ims: return
    W, cols = 200, 8; rows = (len(ims) + cols - 1) // cols
    c = Image.new("RGB", (W * cols, (W + 16) * rows), "white"); d = ImageDraw.Draw(c)
    for j, p in enumerate(ims):
        t = Image.open(p); sz = t.size; t.thumbnail((190, 190)); x, y = (j % cols) * W, (j // cols) * (W + 16)
        c.paste(t, (x, y)); d.text((x, y + 196), f"{os.path.basename(p)} {sz[0]}x{sz[1]}", fill="red")
    c.save(out, quality=80)

def do_pdf(f, od):
    pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1))
    txt = subprocess.run(["pdftotext", "-layout", f, "-"], capture_output=True, text=True).stdout
    txt = "\n".join(re.sub(r" {2,}", "  ", l).rstrip() for l in txt.splitlines() if l.strip())
    tmp = os.path.join(od, "_raw"); os.makedirs(tmp, exist_ok=True)
    subprocess.run(["pdfimages", "-png", "-p", f, os.path.join(tmp, "p")])
    n = 0
    for p in sorted(glob.glob(os.path.join(tmp, "*.png"))):
        try: n += save_img(p, os.path.join(od, "images", os.path.basename(p)[:-4] + ".jpg"))
        except Exception: pass
    shutil.rmtree(tmp)
    return pages, txt, n

def do_pptx(f, od):
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    prs = Presentation(f); out = []; n = 0
    def shapes(coll):
        for sh in coll:
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP: yield from shapes(sh.shapes)
            else: yield sh
    for i, s in enumerate(prs.slides, 1):
        out.append(f"## Slide {i}")
        for sh in shapes(s.shapes):
            if sh.has_text_frame and sh.text_frame.text.strip(): out.append(sh.text_frame.text.replace("\v", " ").strip())
            if getattr(sh, "has_table", False) and sh.has_table:
                for r in sh.table.rows: out.append("| " + " | ".join(c.text.strip() for c in r.cells) + " |")
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
                try:
                    blob = sh.image.blob; ext = sh.image.ext; p = os.path.join(od, f"_s{i:02d}.{ext}")
                    open(p, "wb").write(blob)
                    if ext.lower() in ("png", "jpg", "jpeg", "gif", "bmp", "tiff") and save_img(p, os.path.join(od, "images", f"s{i:02d}_{n+1}.jpg")): n += 1
                    os.remove(p)
                except Exception: pass
        if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
            out.append("Notes: " + s.notes_slide.notes_text_frame.text.strip())
    return len(prs.slides), "\n".join(out), n

def main(od, files):
    os.makedirs(od, exist_ok=True); idx = ["| File | Pages | Chars | Images | Flag |", "|---|---|---|---|---|"]
    for f in files:
        stem = re.sub(r"[^A-Za-z0-9._-]+", "_", os.path.splitext(os.path.basename(f))[0])[:60]
        d = os.path.join(od, stem); os.makedirs(os.path.join(d, "images"), exist_ok=True)
        ext = f.lower().rsplit(".", 1)[-1]
        try:
            if ext == "pdf": pages, txt, n = do_pdf(f, d)
            elif ext == "pptx": pages, txt, n = do_pptx(f, d)
            else: print(f"SKIP {f}: convert .{ext} to .pptx first (convert_ppt.sh)"); idx.append(f"| {os.path.basename(f)} | - | - | - | X01 unsupported |"); continue
        except Exception as e:
            print(f"FAIL {f}: {e}"); idx.append(f"| {os.path.basename(f)} | - | - | - | X02 unreadable: {e} |"); continue
        open(os.path.join(d, "text.md"), "w", encoding="utf-8").write(f"# {os.path.basename(f)}\n\n{txt}\n")
        contact(os.path.join(d, "images"), os.path.join(d, "contact.jpg"))
        flag = "NEEDS_VISUAL_READ" if len(txt) < 150 * max(pages, 1) else ""
        idx.append(f"| {os.path.basename(f)} | {pages} | {len(txt)} | {n} | {flag} |")
        print(f"ok {stem}: {pages} pages, {len(txt)} chars, {n} images {flag}")
    open(os.path.join(od, "index.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
