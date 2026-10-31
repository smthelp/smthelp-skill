#!/usr/bin/env python3
"""Download every source link into <kit>/sources/ and extract readable text.

usage: python3 fetch_sources.py <kit_dir> <url> [<url> ...]
- PDF  -> kept as .pdf (read it with a PDF reader / read_file pages mode; render image-only pages)
- HTML -> .html + .html.txt (scripts, styles and data: URIs stripped). A text < 300 chars usually
          means a JS-only page (e.g. an eDrawings 3D viewer): use it as a visual source, not a spec source.
- WAV/MP3/MP4 -> kept; transcribe with transcribe_audio.py
Writes <kit>/sources/access_report.md: URL, HTTP status, bytes, type, text length -> paste into META["sources"].
"""
import os, re, sys, html, subprocess, urllib.parse
kit, urls = sys.argv[1], sys.argv[2:]
src = os.path.join(kit, "sources"); os.makedirs(src, exist_ok=True)
rows = []
for u in urls:
    name = urllib.parse.unquote(u.rstrip("/").split("/")[-1]) or "index.html"
    name = re.sub(r"[^\w.\-]+", "_", name)
    fn = os.path.join(src, name)
    r = subprocess.run(["curl", "-sSL", "-o", fn, "-w", "%{http_code} %{size_download}", u], capture_output=True, text=True)
    code, size = (r.stdout.split() + ["?", "0"])[:2]
    kind = subprocess.run(["file", "-b", fn], capture_output=True, text=True).stdout.split(",")[0] if os.path.exists(fn) else "missing"
    tlen = ""
    if name.lower().endswith((".html", ".htm")) and os.path.exists(fn):
        s = open(fn, encoding="utf-8", errors="ignore").read()
        s = re.sub(r"<script[^>]*>.*?</script>|<style[^>]*>.*?</style>", "", s, flags=re.S)
        s = re.sub(r"data:[^\"')]+", "", s)
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
        open(fn + ".txt", "w").write(t); tlen = str(len(t))
    rows.append((u, code, size, kind, tlen))
    print(code, size, kind, tlen, name)
with open(os.path.join(src, "access_report.md"), "w") as f:
    f.write("| URL | HTTP | bytes | type | text chars |\n|---|---|---|---|---|\n")
    for r in rows: f.write("| " + " | ".join(r) + " |\n")
