"""Stage 1 - download: fetch every source (3D viewer pages, landing pages, docs) into PROJ/src.

Independent module. Also usable stand-alone, without a product.json:
    python -m p3cv.stages.download URL [URL ...] --out DIR

For each file it records size, sha256, detected kind (edrawings | threejs | landing | pdf | other),
<title>, meta description, a plain-text dump (DIR/<id>.txt) and extracts embedded base64 images
(DIR/../img/<id>_b64_N.ext) with their alt text. Results go to src/manifest.json.
"""
import argparse, base64, hashlib, html, json, re, sys, urllib.request
from pathlib import Path
from . import stage
from ..errors import P3VError
from ..util import retry
from .. import log

B64_RE = re.compile(r"data:image/(jpeg|jpg|png|webp|gif);base64,([A-Za-z0-9+/=]{200,})")


def classify(text, url=""):
    low = text[:400000].lower()
    if url.lower().endswith(".pdf") or text.startswith("%PDF"):
        return "pdf"
    if url.lower().endswith((".pptx", ".docx")) or text.startswith("PK"):
        return "office"
    if "edrawings" in low or "modelcontents" in low or "hoops" in low:
        return "edrawings"
    if "three.webglrenderer" in low or "three.mathutils" in low or "three.object3d" in low:
        return "threejs"
    if "<section" in low or "<nav" in low:
        return "landing"
    return "other"


def text_dump(s):
    s = B64_RE.sub("", s)
    s = re.sub(r"<style.*?</style>|<script.*?</script>", "", s, flags=re.S | re.I)
    s = html.unescape(re.sub(r"<[^>]+>", "\n", s))
    return "\n".join(l.strip() for l in s.splitlines() if l.strip())


def meta(s):
    t = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
    d = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', s, re.I)
    return (html.unescape(t.group(1).strip()) if t else ""), (html.unescape(d.group(1)) if d else "")


def fetch(url, dest, timeout=120, retries=3, max_mb=80, ua="Mozilla/5.0"):
    lg = log.get("download")

    def once():
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read(max_mb * 1024 * 1024 + 1)
        if len(data) > max_mb * 1024 * 1024:
            raise P3VError("E_DOWNLOAD", f"{url} larger than {max_mb} MB", "raise download.max_mb")
        if len(data) < 200:
            raise P3VError("E_DOWNLOAD", f"{url} returned only {len(data)} bytes")
        return data
    try:
        data = retry(once, tries=retries, what=f"GET {url}")
    except P3VError:
        raise
    except Exception as e:
        raise P3VError("E_DOWNLOAD", f"{url}: {e}", "check the URL (spaces must be %20) and network/proxy")
    dest.write_bytes(data)
    lg.info("saved %s (%.1f MB)", dest.name, len(data) / 1e6)
    return data


def ext_for(url):
    u = url.lower().split("?")[0]
    for e in (".pdf", ".pptx", ".docx"):
        if u.endswith(e):
            return e
    return ".html"


def doc_text(path, kind):
    """Plain text of a PDF (pdftotext -layout) or an Office file (slide/paragraph XML), or ''."""
    import subprocess, zipfile
    try:
        if kind == "pdf":
            return subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True,
                                  text=True, timeout=120).stdout
        if str(path).lower().endswith(".pptx"):
            try:  # python-pptx keeps presentation order (slideN.xml numbering may not)
                from pptx import Presentation
                out = []
                for i, sl in enumerate(Presentation(str(path)).slides, 1):
                    out.append(f"--- slide {i}\n" + "\n".join(sh.text_frame.text.strip() for sh in sl.shapes
                                                             if sh.has_text_frame and sh.text_frame.text.strip()))
                return "\n".join(out)
            except ImportError:
                pass
        with zipfile.ZipFile(path) as z:
            names = sorted((n for n in z.namelist() if re.match(r"(ppt/slides/slide\d+|word/document)\.xml$", n)),
                           key=lambda n: int(re.sub(r"\D", "", n) or 0))
            out = []
            for i, n in enumerate(names, 1):
                x = z.read(n).decode("utf-8", "ignore")
                paras = [html.unescape(re.sub(r"<[^>]+>", "", p)) for p in re.findall(r"<a:p>.*?</a:p>|<w:p[ >].*?</w:p>", x, re.S)]
                out.append(f"--- {n.split('/')[-1]}\n" + "\n".join(p for p in paras if p.strip()))
            return "\n".join(out)
    except Exception:
        return ""


def analyse(item_id, path, url, img_dir, extract_b64=True):
    raw = path.read_bytes()
    s = raw.decode("utf-8", "ignore")
    kind = classify(s, url)
    rec = {"id": item_id, "url": url, "file": path.name, "bytes": len(raw),
           "sha256": hashlib.sha256(raw).hexdigest(), "kind": kind}
    if kind in ("pdf", "office"):
        t = doc_text(path, kind)
        if t:
            (path.parent / f"{item_id}.txt").write_text(t, encoding="utf-8")
    else:
        rec["title"], rec["description"] = meta(s)
        (path.parent / f"{item_id}.txt").write_text(text_dump(s), encoding="utf-8")
        rec["remote_images"] = sorted(set(re.findall(r'https://ph\.smthelp\.com/[^"\')\s]+\.(?:png|jpe?g|gif|webp)', s)))
        imgs = []
        if extract_b64 and kind == "landing":
            img_dir.mkdir(parents=True, exist_ok=True)
            seen = set()
            for n, m in enumerate(B64_RE.finditer(s)):
                h = hashlib.md5(m.group(2)[:5000].encode()).hexdigest()
                if h in seen:
                    continue
                seen.add(h)
                ext = "jpg" if m.group(1) in ("jpeg", "jpg") else m.group(1)
                f = img_dir / f"{item_id}_b64_{len(imgs)}.{ext}"
                f.write_bytes(base64.b64decode(m.group(2)))
                alt = re.findall(r'alt="([^"]*)"', s[m.end():m.end() + 500])
                imgs.append({"file": str(f.name), "alt": alt[0] if alt else ""})
        rec["embedded_images"] = imgs
    return rec


@stage("download", desc="Fetch 3D viewers, landing pages and docs into src/, write manifest.json")
def run(cfg, state):
    lg = log.get("download")
    d = cfg["download"]; src = cfg.p("src", "x").parent; img = cfg.p("img", "x").parent
    items = []
    for group in ("drawings", "landing", "docs"):
        for it in cfg["sources"].get(group, []):
            items.append((group, it))
    if not items:
        raise P3VError("E_CONFIG", "sources is empty", "add sources.drawings / sources.landing URLs")
    manifest = []
    for group, it in items:
        url = it["url"]; iid = it["id"]
        ext = ext_for(url)
        dest = src / f"{iid}{ext}"
        if dest.exists() and dest.stat().st_size > 200 and not it.get("refresh"):
            lg.info("skip %s (already downloaded)", dest.name)
        else:
            fetch(url, dest, d["timeout"], d["retries"], d["max_mb"], d["user_agent"])
        rec = analyse(iid, dest, url, img, d["extract_base64_images"])
        rec["group"] = group
        if it.get("viewer") and it["viewer"] != rec["kind"]:
            lg.warning("%s: config says viewer=%s but page looks like %s", iid, it["viewer"], rec["kind"])
        manifest.append(rec)
        log.event("artifact", stage="download", id=iid, kind=rec["kind"], bytes=rec["bytes"])
    (src / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    return {"manifest": "src/manifest.json", "count": len(manifest)}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Download product sources and analyse them")
    ap.add_argument("urls", nargs="+"); ap.add_argument("--out", default="src")
    a = ap.parse_args(argv)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    import logging; logging.basicConfig(level="INFO")
    res = []
    for n, u in enumerate(a.urls):
        iid = f"s{n}"; ext = ext_for(u)
        fetch(u, out / f"{iid}{ext}")
        res.append(analyse(iid, out / f"{iid}{ext}", u, out.parent / "img"))
    (out / "manifest.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    print(json.dumps([{k: r.get(k) for k in ("id", "kind", "title", "bytes")} for r in res], indent=1))


if __name__ == "__main__":
    sys.exit(main())
