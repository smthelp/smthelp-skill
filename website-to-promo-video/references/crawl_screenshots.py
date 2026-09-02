#!/usr/bin/env python3
"""Step 1 — Crawl a website and screenshot its main pages (1920x1080) with Playwright.

Robust by design:
  - wait_until="commit" + hard per-page timeout (no page can hang the run)
  - skip files that already exist (safe to re-run / resume)
  - removes common chat/cookie/fixed overlays for clean shots
  - drives the SYSTEM Chrome (channel="chrome") — no Chromium install needed

Usage:
  python3 crawl_screenshots.py --pages pages.json --base .
  python3 crawl_screenshots.py --pages pages.json --base . --w 1080 --h 1920   # 竖屏 9:16
  python3 crawl_screenshots.py --pages pages.json --base . --out slides --timeout 30000

pages.json format:  [["home","https://example.com/"], ["about","https://example.com/about"], ...]
Screenshots land in <base>/<out>/slide-<label>.png
"""
import os, sys, time, json, argparse
from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

OVERLAY_JS = """() => {
  const sel=['.cky-consent-container','#cookie-notice','.chat-widget',
    '.intercom-lightweight-app','.fb-customerchat','.elfsight-app',
    '#tawkto-container','.tidio-chat','.whatshelp-widget'];
  sel.forEach(s=>document.querySelectorAll(s).forEach(e=>e.remove()));
  document.querySelectorAll('*').forEach(e=>{
    if(getComputedStyle(e).position==='fixed'){e.style.display='none';}
  });
}"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".")
    ap.add_argument("--pages", required=True, help="JSON: [[label,url],...]")
    ap.add_argument("--out", default="slides")
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--chrome", action="store_true",
                    help="Use system Chrome channel (recommended; avoids Chromium install).")
    ap.add_argument("--timeout", type=int, default=25000)
    args = ap.parse_args()

    BASE = os.path.abspath(args.base)
    OUT = os.path.join(BASE, args.out)
    os.makedirs(OUT, exist_ok=True)
    pages = json.load(open(args.pages, encoding="utf-8"))

    launch = {"headless": True,
              "args": ["--hide-scrollbars", "--disable-gpu", "--no-sandbox",
                       "--disable-dev-shm-usage"]}
    if args.chrome:
        launch["channel"] = "chrome"

    with sync_playwright() as p:
        b = p.chromium.launch(**launch)
        ctx = b.new_context(viewport={"width": args.w, "height": args.h},
                             device_scale_factor=1, user_agent=UA, locale="en-US")
        page = ctx.new_page()
        page.set_default_timeout(args.timeout)
        for label, url in pages:
            out = os.path.join(OUT, f"slide-{label}.png")
            if os.path.exists(out):
                print(f"[skip] {label} ({out} exists)")
                continue
            try:
                print(f"[shot] {label} -> {url}")
                page.goto(url, wait_until="commit", timeout=args.timeout)
                try:
                    page.wait_for_load_state("networkidle", timeout=6000)
                except Exception:
                    pass
                time.sleep(2.5)
                page.evaluate(OVERLAY_JS)
                time.sleep(0.3)
                page.evaluate("window.scrollTo(0,0)")
                time.sleep(0.4)
                page.screenshot(path=out, clip={"x": 0, "y": 0,
                                               "width": args.w, "height": args.h})
                print(f"       saved {out}")
            except Exception as e:
                print(f"[ERR] {label}: {e}")
        b.close()
    print("done.")

if __name__ == "__main__":
    main()
