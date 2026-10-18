#!/usr/bin/env python3
"""Pull text and images out of every supplier file in <kit>/sources into <kit>/extracted,
then report supplier marks and Chinese text that must be rewritten.

usage: extract_sources.py <kit_dir>
 - PDF: pdftotext -layout per file, page renders at 110 dpi (pages/), embedded images (img/)
 - PPTX/DOCX/XLSX: text from the XML parts, media files copied
 - MP4/MOV: duration + contact sheet of 12 frames (look for watermarks, burned subtitles, end cards)
 - JPG/PNG: copied to extracted/img and listed in a contact sheet
Writes extracted/<file>/text.txt, extracted/report.md (supplier-term hits, CJK share, file list)."""
import json, os, re, subprocess, sys, zipfile, glob, shutil

kit = sys.argv[1]
src, ex = os.path.join(kit, "sources"), os.path.join(kit, "extracted")
os.makedirs(ex, exist_ok=True)
cfg = json.load(open(os.path.join(kit, "kit.json"), encoding="utf-8"))
terms = cfg.get("supplier_terms", [])
CJK = re.compile(r"[\u4e00-\u9fff]")
rep = ["# Extraction report", ""]


def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True)


def scan(name, text):
    hits = {t: len(re.findall((r"\b" + re.escape(t) + r"\b") if re.match(r"^[\w .-]+$", t, re.A) else re.escape(t), text, re.I)) for t in terms}
    hits = {k: v for k, v in hits.items() if v}
    cjk = len(CJK.findall(text)); tot = max(1, len(text))
    phones = sorted(set(re.findall(r"\+?\d{2,4}[ -]?\d{3,4}[ -]?\d{4}\b", text)))[:8]
    mails = sorted(set(re.findall(r"[\w.\-]+@[\w\-]+\.[\w.]+", text)))
    urls = sorted(set(re.findall(r"(?:https?://|www\.)[^\s)>\]]+", text)))[:10]
    rep.append(f"## {name}\n- characters: {len(text)}, CJK share: {cjk*100//tot}%\n- supplier terms: {hits or 'none found'}")
    if mails: rep.append(f"- emails (replace with info@smthelp.com unless Southern Machinery): {mails}")
    if phones: rep.append(f"- phone-like numbers (check, replace supplier ones): {phones}")
    if urls: rep.append(f"- urls/domains: {urls}")
    rep.append("")


for f in sorted(os.listdir(src)):
    p = os.path.join(src, f); stem = re.sub(r"[^\w.-]+", "_", os.path.splitext(f)[0])[:60]
    o = os.path.join(ex, stem); os.makedirs(o, exist_ok=True); low = f.lower()
    text = ""
    if low.endswith(".pdf"):
        sh(f'pdftotext -layout "{p}" "{o}/text.txt"'); text = open(f"{o}/text.txt", errors="ignore").read()
        os.makedirs(f"{o}/pages", exist_ok=True); os.makedirs(f"{o}/img", exist_ok=True)
        sh(f'pdftoppm -r 110 -jpeg "{p}" "{o}/pages/p"'); sh(f'pdfimages -png "{p}" "{o}/img/i"')
        for im in glob.glob(f"{o}/img/*.png"):
            if os.path.getsize(im) < 15000: os.remove(im)       # drop icons and rules
        pages = sorted(glob.glob(f"{o}/pages/*.jpg"))
        if pages: sh(f'montage {" ".join(pages[:40])} -tile 8x -geometry 220x+3+3 "{o}/pages-sheet.jpg"')
    elif low.endswith((".pptx", ".docx", ".xlsx")):
        z = zipfile.ZipFile(p); parts = []
        for n in sorted(z.namelist()):
            if n.endswith(".xml") and re.search(r"(slides/slide|word/document|sharedStrings|notesSlide)", n):
                parts.append(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf8", "ignore")))
            if "/media/" in n:
                os.makedirs(f"{o}/img", exist_ok=True); open(f"{o}/img/" + os.path.basename(n), "wb").write(z.read(n))
        text = re.sub(r"\s+", " ", " \n".join(parts)); open(f"{o}/text.txt", "w").write(text)
    elif low.endswith((".mp4", ".mov", ".m4v", ".avi", ".webm")):
        d = sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"').stdout.strip() or "0"
        n = 12; step = float(d) / (n + 1)
        os.makedirs(f"{o}/frames", exist_ok=True)
        for i in range(1, n + 1):
            sh(f'ffmpeg -v error -y -ss {i*step:.2f} -i "{p}" -frames:v 1 -vf scale=360:-2 "{o}/frames/f{i:02d}_{i*step:05.1f}s.jpg"')
        sh(f'montage {o}/frames/*.jpg -tile 6x -geometry +3+3 -title "{f} {float(d):.1f}s" "{o}/frames-sheet.jpg"')
        rep.append(f"## {f}\n- video {float(d):.1f}s - check frames-sheet.jpg for supplier watermark, burned Chinese subtitles, intro/end cards, people's faces\n")
        continue
    elif low.endswith((".jpg", ".jpeg", ".png", ".webp")):
        os.makedirs(f"{ex}/_photos", exist_ok=True); shutil.copy(p, f"{ex}/_photos/{f}")
        continue
    else:
        rep.append(f"## {f}\n- skipped (unknown type)\n"); continue
    scan(f, text)

ph = sorted(glob.glob(f"{ex}/_photos/*"))
if ph:
    sh(f'montage {" ".join(chr(34)+x+chr(34) for x in ph[:48])} -tile 8x -geometry 240x240+3+3 "{ex}/photos-sheet.jpg"')
    rep.append(f"## Photos\n- {len(ph)} files, contact sheet photos-sheet.jpg - look for supplier logos/nameplates to paint over\n")
open(os.path.join(ex, "report.md"), "w").write("\n".join(rep))
print("\n".join(rep))
