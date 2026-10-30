#!/usr/bin/env python3
"""Find candidate assets for a product page on Southern Machinery's own sources.

usage: harvest_assets.py "<keyword regex>" [image search terms ...]
  e.g. harvest_assets.py "calibrat|fuji nxt|jig" calibration "calibration jig"

Prints three lists (review them; nothing is chosen automatically):
  IMAGES   ph.smthelp.com search hits (.md. = medium; drop ".md" for full size)
  VIDEOS   YouTube video board rows whose title matches the regex (seconds, url, title)
  CATALOGS product catalogue board rows whose file name matches the regex (url | name)
Open every image before captioning it; reject photos of other machines.
"""
import re, sys, html, urllib.parse, urllib.request
VIDEO_BOARD = "https://file.autoinsertion.com/public/Southern-Machinery-YouTube-Video-Board.html"
CATALOG_BOARD = "https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html"
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "ignore")
if len(sys.argv) < 2: sys.exit(__doc__)
rx = re.compile(sys.argv[1], re.I)
terms = sys.argv[2:] or [sys.argv[1].split("|")[0]]
print("== IMAGES")
seen = set()
for q in terms:
    for u in re.findall(r'https://ph\.smthelp\.com/images/[^"\'\s<>]+', get("https://ph.smthelp.com/search/images/?q=" + urllib.parse.quote(q))):
        if u not in seen: seen.add(u); print(u)
print("== VIDEOS")
for m in re.finditer(r'data-title="([^"]*)"[^>]*?data-duration="(\d+)" data-url="([^"]*)"', get(VIDEO_BOARD)):
    t = html.unescape(m.group(1))
    if rx.search(t): print(m.group(2), m.group(3), t)
print("== CATALOGS")
for m in re.finditer(r'data-original="([^"]*)" data-path="[^"]*" data-url="([^"]*)"', get(CATALOG_BOARD)):
    n = html.unescape(m.group(1))
    if rx.search(n): print(html.unescape(m.group(2)), "|", n)
