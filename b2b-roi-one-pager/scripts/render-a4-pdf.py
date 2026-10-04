#!/usr/bin/env python3
"""
render-a4-pdf.py — Render an HTML one-pager to a single-page A4 PDF
using Playwright + the local Chromium headless shell.

Usage:
    python3 scripts/render-a4-pdf.py path/to/one-pager.html
    python3 scripts/render-a4-pdf.py path/to/one-pager.html --output /custom/out.pdf
    python3 scripts/render-a4-pager.py path/to/one-pager.html --preview  # also write a PNG preview

Why this script exists (vs Chrome's --print-to-pdf):
- Auto-discovers the latest chrome-headless-shell version in the Playwright cache
  (so you don't have to update the version number when Playwright bumps)
- Validates the HTML is exactly 1 A4 page tall (1123px @ 96dpi) before rendering
- Warns if the PDF silently spills to 2 pages
- Verifies the final page count via regex on the PDF binary (no pymupdf needed)
- Writes a PNG preview alongside for vision verification

The 2026-06-05 validated headless shell path was:
/Users/jasonwu/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell

This script globs for `chromium_headless_shell-*` and picks the latest, so version
drift is handled automatically.
"""

import argparse
import glob
import os
import re
import sys

# A4 dimensions in pixels @ 96 DPI
A4_WIDTH_PX = 794
A4_HEIGHT_PX = 1123

HEADLESS_GLOB = (
    "/Users/jasonwu/Library/Caches/ms-playwright/"
    "chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"
)


def find_headless_shell():
    matches = sorted(glob.glob(HEADLESS_GLOB))
    if not matches:
        print(f"ERROR: No chromium headless shell found at {HEADLESS_GLOB}", file=sys.stderr)
        print("Run: playwright install chromium", file=sys.stderr)
        sys.exit(1)
    return matches[-1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", help="Path to input HTML file")
    ap.add_argument("--output", "-o", help="Output PDF path (default: <html_basename>.pdf next to HTML)")
    ap.add_argument("--preview", "-p", action="store_true", help="Also write a PNG preview of page 1")
    args = ap.parse_args()

    html_path = os.path.abspath(args.html)
    if not os.path.exists(html_path):
        print(f"ERROR: HTML not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        pdf_path = os.path.abspath(args.output)
    else:
        base = os.path.splitext(html_path)[0]
        pdf_path = base + ".pdf"

    preview_path = os.path.splitext(pdf_path)[0] + "_preview.png"

    headless = find_headless_shell()
    print(f"Using headless shell: {headless}")
    print(f"Input HTML: {html_path}")
    print(f"Output PDF: {pdf_path}")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed. Run: pip install playwright", file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=headless)
        try:
            page = browser.new_page(viewport={"width": A4_WIDTH_PX, "height": A4_HEIGHT_PX})
            page.goto(f"file://{html_path}", wait_until="networkidle")

            # A4 height sanity check
            h = page.evaluate("() => document.documentElement.scrollHeight")
            w = page.evaluate("() => document.documentElement.scrollWidth")
            print(f"HTML render size: {w} x {h} px  (A4 target: {A4_WIDTH_PX} x {A4_HEIGHT_PX})")

            if h > A4_HEIGHT_PX:
                print(f"⚠️  WARN: HTML is {h}px tall but A4 is {A4_HEIGHT_PX}px — content WILL overflow to page 2")
                print(f"     Either tighten padding/font sizes or rely on .page {{ overflow: hidden }} as a safety net.")
            elif h < A4_HEIGHT_PX - 50:
                print(f"ℹ️  NOTE: HTML is {h}px tall, A4 is {A4_HEIGHT_PX}px — {A4_HEIGHT_PX - h}px of bottom whitespace (you could add more content).")
            else:
                print(f"✓  Height check OK ({h}px fits within {A4_HEIGHT_PX}px A4)")

            # Render PNG preview (always, for sanity)
            page.screenshot(
                path=preview_path,
                full_page=False,
                clip={"x": 0, "y": 0, "width": A4_WIDTH_PX, "height": A4_HEIGHT_PX},
            )
            print(f"PNG preview: {preview_path}  ({os.path.getsize(preview_path):,} bytes)")

            # Render the PDF
            page.pdf(
                path=pdf_path,
                format="A4",
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                prefer_css_page_size=True,
            )
        finally:
            browser.close()

    # Verify the resulting PDF page count
    with open(pdf_path, "rb") as f:
        data = f.read()
    page_count = len(re.findall(rb"/Type\s*/Page[^s]", data))
    print(f"PDF size: {len(data):,} bytes")
    print(f"PDF pages: {page_count}  {'✓' if page_count == 1 else '⚠️  Expected exactly 1 page'}")

    if args.preview:
        pass  # already saved above

    if page_count != 1:
        sys.exit(2)

    print(f"\nDone. PDF: {pdf_path}")


if __name__ == "__main__":
    main()
