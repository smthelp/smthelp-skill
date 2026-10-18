#!/usr/bin/env python3
"""Brand + evidence quality gate for every deliverable in a kit.

usage: qa_kit.py <kit_dir> [files...]      (default: everything in <kit>/out)
Checks per file type
  all text   supplier terms from kit.json, supplier emails/phones, never-publish words
             (price, lead time, warranty, payment terms, certified, saving %), banned heading words
  .pptx      no Chinese characters, SM contact (info@smthelp.com) present, zip integrity
  .srt       no Chinese, no supplier terms
  .html      runs smt-product-landing-page check_page.py when the landing dir exists; Chinese allowed (zh i18n)
  .mp4       duration, resolution, audio stream present
  .png/.pdf  size by format
Exit 1 on any ERROR; WARN lines need a human look (e.g. a percentage that is a spec, not a saving)."""
import json, os, re, subprocess, sys, zipfile, glob

kit = sys.argv[1]
cfg = json.load(open(os.path.join(kit, "kit.json"), encoding="utf-8"))
files = sys.argv[2:] or sorted(glob.glob(os.path.join(kit, "out", "**", "*.*"), recursive=True))
terms = [t for t in cfg.get("supplier_terms", []) if t]
CJK = re.compile(r"[\u4e00-\u9fff]")
NEVER = [r"\$\s?\d", r"\bUSD\b", r"\bRMB\b", r"\bEUR\b", r"lead[ -]time\s*(?:is|of|:)?\s*\d", r"\bin stock\b",
         r"\bwarranty\s*(?:is|of|:)?\s*\d", r"payment terms?\s*:", r"\b(?:CE|ISO\s?\d{4,5}|FDA|UL)[- ]?(?:certified|certificate)",
         r"\bsav(?:e|es|ing|ings)\s+(?:up to\s+)?\d+\s?%", r"\bROI of \d", r"\byield (?:of |up to )?\d+\s?%"]
BANNED_HEAD = re.compile(r"\b(hook|diagnosis|framework|vehicle|loop|CTA)\b|钩子|诊断|框架|载体|循环|行动号召", re.I)
SM_OK = re.compile(r"smthelp|autoinsertion|southern", re.I)
err, warn = [], []


def text_of(p):
    low = p.lower()
    if low.endswith(".pptx"):
        z = zipfile.ZipFile(p)
        if z.testzip() is not None: err.append(f"{p}: corrupt zip")
        slides = sorted([n for n in z.namelist() if re.match(r"ppt/(slides/slide|notesSlides/notesSlide)\d+\.xml", n)])
        return "\n".join(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf8", "ignore")) for n in slides), \
               [re.sub(r"<[^>]+>", " ", z.read(n).decode("utf8", "ignore")) for n in slides if "slides/slide" in n]
    if low.endswith((".srt", ".txt", ".md", ".json", ".html")):
        return open(p, encoding="utf-8", errors="ignore").read(), []
    return "", []


def probe(p):
    r = subprocess.run(f'ffprobe -v error -show_entries stream=codec_type,width,height:format=duration -of json "{p}"', shell=True, capture_output=True, text=True)
    return json.loads(r.stdout or "{}")


for p in files:
    low = p.lower(); name = os.path.relpath(p, kit)
    if low.endswith(".mp4"):
        j = probe(p); st = j.get("streams", []); d = float(j.get("format", {}).get("duration", 0))
        v = [s for s in st if s.get("codec_type") == "video"]; a = [s for s in st if s.get("codec_type") == "audio"]
        if not v: err.append(f"{name}: no video stream")
        if not a: warn.append(f"{name}: no audio stream")
        print(f"OK   {name}: {d:.1f}s {v[0].get('width')}x{v[0].get('height')}" if v else f"?? {name}")
        continue
    if low.endswith((".png", ".jpg", ".pdf")):
        print(f"OK   {name}: {os.path.getsize(p)//1024} KB (check visually)"); continue
    txt, slides = text_of(p)
    if not txt: continue
    for t in terms:
        pat = (r"\b" + re.escape(t) + r"\b") if re.match(r"^[\w .-]+$", t, re.A) else re.escape(t)
        n = len(re.findall(pat, txt, re.I))
        if n: err.append(f"{name}: supplier term '{t}' x{n}")
    for m in set(re.findall(r"[\w.\-]+@[\w\-]+\.[\w.]+", txt)):
        if not SM_OK.search(m) and not m.endswith((".png", ".jpg", ".webp")): err.append(f"{name}: foreign email {m}")
    for pat in NEVER:
        for m in re.findall(pat, txt, re.I)[:3]: warn.append(f"{name}: never-publish pattern '{m}'")
    if low.endswith((".pptx", ".srt")) and CJK.search(txt):
        err.append(f"{name}: Chinese characters ({len(CJK.findall(txt))}) in an English deliverable")
    if low.endswith(".pptx"):
        if "info@smthelp.com" not in txt: err.append(f"{name}: SM contact info@smthelp.com missing")
        for i, s in enumerate(slides, 1):
            head = s[:300]
            if BANNED_HEAD.search(head): err.append(f"{name}: slide {i} heading uses a banned word")
        print(f"OK   {name}: {len(slides)} slides checked")
    elif low.endswith(".html"):
        lp = os.path.join(kit, "landing")
        chk = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "smt-product-landing-page", "scripts", "check_page.py"))
        if os.path.exists(os.path.join(lp, "product.json")) and os.path.exists(chk):
            r = subprocess.run(f'python3 "{chk}" "{lp}" "{p}"', shell=True, capture_output=True, text=True)
            (print if r.returncode == 0 else err.append)(f"{name}: check_page -> {r.stdout.strip()[-300:]}")
    else:
        print(f"OK   {name}")

for w in warn: print("WARN ", w)
for e in err: print("ERROR", e)
print(f"\n{len(err)} errors, {len(warn)} warnings")
sys.exit(1 if err else 0)
