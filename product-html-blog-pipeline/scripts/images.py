#!/usr/bin/env python3
"""
product-html-blog-pipeline :: image discovery + validation

  images.py search --q "S7020" --q "eyelet" [--limit 40]
  images.py check  --url https://ph.smthelp.com/... [--url ...]

Rules
-----
* Source order: (1) images already embedded in the chosen document,
  (2) ph.smthelp.com search by model code / product category / component type.
* EVERY url must be confirmed HTTP 200 AND content-type image/* before use.
  A 404 or an HTML page must never become a coverImage.
* ph.smthelp.com search is fuzzy - `q=S7020` and `q=eyelet` both hit the S7020
  series, while `q=terminal` drifts to belt feeders. Try several queries.
* Prefer real product / detail / line-integration shots. No stock photos.
* LinkedIn only accepts PNG/JPEG/GIF reliably - a .webp cover is fine for the
  blog cover but pick a PNG sibling for the LinkedIn post.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
IMG_RE = re.compile(r"https://ph\.smthelp\.com/images/[^\"'<>\s)]+")


def http_head_ok(url):
    r = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, resp.headers.get("Content-Type", ""), int(
                resp.headers.get("Content-Length") or 0) or len(resp.read(4096))
    except urllib.error.HTTPError as e:
        return e.code, "", 0
    except Exception as e:
        return 0, str(e), 0


def cmd_search(args):
    found = []
    for q in args.q:
        url = f"https://ph.smthelp.com/search/images/?q={urllib.parse.quote(q)}"
        r = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(r, timeout=40) as resp:
                html = resp.read().decode("utf-8", "ignore")
        except Exception as e:
            print(f"search failed for {q}: {e}", file=sys.stderr)
            continue
        for u in IMG_RE.findall(html):
            if u not in found:
                found.append(u)
    out = found[: args.limit]
    json.dump({"queries": args.q, "count": len(out), "urls": out}, sys.stdout, ensure_ascii=False, indent=1)
    print(file=sys.stderr)


def cmd_check(args):
    res = []
    for u in args.url:
        st, ctype, size = http_head_ok(u)
        res.append({"url": u, "http": st, "contentType": ctype,
                    "bytes": size, "ok": st == 200 and ctype.startswith("image/")})
    json.dump(res, sys.stdout, ensure_ascii=False, indent=1)
    print(file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("--q", action="append", required=True)
    s.add_argument("--limit", type=int, default=40)
    s.set_defaults(func=cmd_search)
    c = sub.add_parser("check")
    c.add_argument("--url", action="append", required=True)
    c.set_defaults(func=cmd_check)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
