#!/usr/bin/env python3
"""Step 1.5 — Download key product/machine images from selected pages.

Scores candidates by alt/cls keywords, drops logos/banners, filters tiny
images, and verifies each download is a real JPEG with PIL. Outputs to
<base>/<out>/<hash>.jpg and writes scripts/images_log.json.

Usage:
  python3 crawl_images.py --pages pages.json --base .
  python3 crawl_images.py --pages urls.json --base . --per-page 4 --min-w 480
"""
import os, time, json, argparse, urllib.request, io, hashlib
from PIL import Image
from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# keyword hints that an <img> is a real product/machine photo (not UI chrome)
KEYW = ["machine", "insert", "smt", "tht", "pcb", "wave", "clean", "solder",
         "product", "feeder", "nozzle", "board", "placement", "radial",
         "axial", "assembly", "conveyor", "robotic", "automation"]

def fetch_bytes(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".")
    ap.add_argument("--pages", required=True,
                    help="JSON: list of URLs, or [[label,url],...]")
    ap.add_argument("--out", default="assets")
    ap.add_argument("--per-page", type=int, default=3)
    ap.add_argument("--min-w", type=int, default=360)
    ap.add_argument("--min-h", type=int, default=240)
    ap.add_argument("--min-bytes", type=int, default=12000)
    args = ap.parse_args()

    BASE = os.path.abspath(args.base)
    ASSETS = os.path.join(BASE, args.out)
    os.makedirs(ASSETS, exist_ok=True)
    raw = json.load(open(args.pages, encoding="utf-8"))
    urls = [u if isinstance(u, str) else u[1] for u in raw]

    got, seen = [], set()
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1366, "height": 768}, user_agent=UA)
        pg.set_default_timeout(20000)
        pg.set_default_navigation_timeout(20000)
        for url in urls:
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(2.5)
                imgs = pg.evaluate("""() => Array.from(document.images).map(i => ({
                    src: i.currentSrc||i.src, w: i.naturalWidth, h: i.naturalHeight,
                    alt: (i.alt||'').toLowerCase(), cls: (i.className||'').toLowerCase() }))""")
                cands = []
                for im in imgs:
                    s = im["src"]
                    if not s or "wp-content/uploads" not in s:
                        continue
                    if im["w"] < args.min_w or im["h"] < args.min_h:
                        continue
                    score = 0
                    if any(k in im["alt"] for k in KEYW):
                        score += 2
                    if "logo" in im["alt"] or "logo" in im["cls"]:
                        score -= 6
                    if "banner" in im["alt"] or "banner" in im["cls"]:
                        score -= 3
                    cands.append((score, im))
                cands.sort(key=lambda x: -x[0])
                for _, im in cands[:args.per_page]:
                    s = im["src"]
                    try:
                        data = fetch_bytes(s)
                        if len(data) < args.min_bytes:
                            continue
                        h = hashlib.md5(s.encode()).hexdigest()[:10]
                        if h in seen:
                            continue
                        seen.add(h)
                        fn = f"{hashlib.md5(url.encode()).hexdigest()[:6]}-{h}.jpg"
                        fp = os.path.join(ASSETS, fn)
                        with open(fp, "wb") as f:
                            f.write(data)
                        try:
                            Image.open(io.BytesIO(data)).verify()
                        except Exception:
                            os.remove(fp)
                            continue
                        got.append((fn, len(data), im["w"], im["h"], im["alt"][:30]))
                    except Exception as e:
                        print(f"  img fail: {repr(e)[:80]}")
                print(f"[done] {url}  candidates={len(cands)}")
            except Exception as e:
                print(f"[ERR] {url}: {repr(e)[:160]}")
        b.close()
    os.makedirs(os.path.join(BASE, "scripts"), exist_ok=True)
    with open(os.path.join(BASE, "scripts", "images_log.json"), "w") as f:
        json.dump(got, f, indent=2)
    print("\n=== downloaded ===")
    for g in got:
        print(g)

if __name__ == "__main__":
    main()
