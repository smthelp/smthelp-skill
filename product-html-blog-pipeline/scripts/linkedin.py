#!/usr/bin/env python3
"""
product-html-blog-pipeline :: LinkedIn company-page image post

Usage
-----
  linkedin.py --blog-slug <slug> --commentary-file commentary.txt [--image-url URL]
  linkedin.py --repair            # retry every published blog whose LI status is
                                  # failed / needs_token / missing (never reposts
                                  # a slug that already has a linkedInPostUrn)

Hard-won rules
--------------
1. `visibility` must be **PUBLIC**. "PUBLISHED" is not a valid enum symbol -> 422.
2. A 201 response frequently carries NO `x-restli-id`. Fall back to
   GET /rest/posts?q=author&author=<org>&count=5 and read elements[0].id.
3. Polling GET /rest/images/{id} returns 400 - the URL form is wrong, not the
   upload. Skip polling; the URN is usable immediately after the PUT.
4. Only JPG/PNG upload reliably. Prefer a PNG asset over a .webp cover.
5. Never print, log or persist the access token.
"""

import argparse
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pipeline import (BLOG_STATE, LI_STATE, STATE_DIR, load_state, save_state)  # noqa: E402

ORG = "urn:li:organization:3039402"          # Southern Machinery company page
API_VERSION = "202601"
PUBLIC_URL = "https://www.linkedin.com/feed/update/"


def get_token():
    t = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    if not t:
        f = os.path.expanduser("~/.config/smthelp/linkedin_token")
        if os.path.exists(f):
            t = open(f).read().strip()
    return t


def api(method, url, token, body=None, ctype="application/json", raw=None, timeout=90):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    h = {"Authorization": "Bearer " + token, "Linkedin-Version": API_VERSION}
    if data is not None:
        h["Content-Type"] = ctype
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "ignore"), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore"), dict(e.headers)


def fetch_image(url):
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        ctype = resp.headers.get("Content-Type", "")
        if not ctype.startswith("image/"):
            raise ValueError(f"not an image: {ctype}")
        return resp.read(), ctype


def upload_image(token, img_bytes):
    st, body, _ = api("POST", "https://api.linkedin.com/rest/images?action=initializeUpload",
                      token, {"initializeUploadRequest": {"owner": ORG}})
    if st >= 300:
        raise RuntimeError(f"initializeUpload failed {st}: {body[:200]}")
    val = json.loads(body).get("value", {})
    up = val.get("uploadUrl")
    urn = val.get("image")
    if not up or not urn:
        raise RuntimeError("initializeUpload returned no uploadUrl/image")
    st2, b2, _ = api("PUT", up, token, raw=img_bytes, ctype="application/octet-stream", timeout=180)
    if st2 >= 300:
        raise RuntimeError(f"image PUT failed {st2}: {b2[:200]}")
    return urn


def resolve_urn(token, commentary_hint):
    """201 often omits x-restli-id - find the freshest share by commentary prefix."""
    st, body, _ = api("GET",
                      f"https://api.linkedin.com/rest/posts?q=author&author={ORG}&count=5",
                      token)
    if st >= 300:
        return None, None
    els = json.loads(body).get("elements", [])
    if not els:
        return None, None
    hint = (commentary_hint or "")[:60]
    for e in els:
        if hint and hint in (e.get("commentary") or ""):
            return e.get("id"), e.get("publishedAt")
    return els[0].get("id"), els[0].get("publishedAt")


def post(args):
    token = get_token()
    root = args.root
    blog = load_state(root)
    row = next((r for r in blog if r.get("slug") == args.blog_slug), None)

    li_path = os.path.join(root, STATE_DIR, LI_STATE)
    li = []
    if os.path.exists(li_path):
        li = json.load(open(li_path, encoding="utf-8"))
    if any(r.get("blogSlug") == args.blog_slug and r.get("status") == "published" for r in li):
        print("already published to LinkedIn; refusing to duplicate")
        return 0

    if not token:
        rec = {"blogSlug": args.blog_slug, "blogPostUrl": (row or {}).get("postUrl", ""),
               "blogPublishedAt": (row or {}).get("publishedAt", ""),
               "linkedInPostUrn": "", "linkedInPostUrl": "", "linkedInPublishedAt": "",
               "status": "needs_token", "error": "LINKEDIN_ACCESS_TOKEN not configured",
               "imageUrl": "", "imageUrn": ""}
        li.append(rec)
        json.dump(li, open(li_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("status: needs_token (set LINKEDIN_ACCESS_TOKEN)")
        return 1

    commentary = open(args.commentary_file, encoding="utf-8").read().strip()
    blog_url = (row or {}).get("postUrl") or args.blog_url
    if not blog_url:
        sys.exit("ERROR: blog postUrl unknown - pass --blog-url")

    image_url = args.image_url or (row or {}).get("coverImage") or ""
    image_urn = ""
    if image_url:
        try:
            img, ctype = fetch_image(image_url)
            if ctype not in ("image/png", "image/jpeg", "image/jpg", "image/gif"):
                raise ValueError(f"unsupported LinkedIn format: {ctype}")
            image_urn = upload_image(token, img)
        except Exception as exc:                       # text-only fallback
            print("image skipped:", exc, file=sys.stderr)
            image_url, image_urn = "", ""

    body = {
        "author": ORG,
        "commentary": commentary,
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED",
                         "targetEntities": [],
                         "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
    }
    if image_urn:
        body["content"] = {"media": {"id": image_urn, "altText": args.alt_text}}

    st, resp, hdrs = api("POST", "https://api.linkedin.com/rest/posts", token, body)
    urn = hdrs.get("x-restli-id") or hdrs.get("X-RestLi-Id")
    published_ms = None
    if st in (200, 201) and not urn:
        urn, published_ms = resolve_urn(token, commentary)
    if st >= 300 or not urn:
        rec = {"blogSlug": args.blog_slug, "blogPostUrl": blog_url,
               "blogPublishedAt": (row or {}).get("publishedAt", ""),
               "linkedInPostUrn": "", "linkedInPostUrl": "", "linkedInPublishedAt": "",
               "status": "failed", "error": f"HTTP {st}: {resp[:200]}",
               "imageUrl": image_url, "imageUrn": image_urn}
        li.append(rec)
        json.dump(li, open(li_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(json.dumps(rec, ensure_ascii=False, indent=1))
        return 1

    ts = (datetime.fromtimestamp(published_ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
          if published_ms else datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"))
    rec = {"blogSlug": args.blog_slug, "blogPostUrl": blog_url,
           "blogPublishedAt": (row or {}).get("publishedAt", ""),
           "linkedInPostUrn": urn, "linkedInPostUrl": PUBLIC_URL + urn,
           "linkedInPublishedAt": ts, "status": "published", "error": "",
           "imageUrl": image_url, "imageUrn": image_urn}
    if os.path.exists(li_path):
        shutil.copy(li_path, li_path + ".bak")
    li.append(rec)
    json.dump(li, open(li_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rec, ensure_ascii=False, indent=1))
    return 0


def repair(args):
    """List published blogs that have no successful LinkedIn post, newest first.

    Deliberately capped: the historical backlog can be dozens of posts and dumping
    them all onto the company page in one hour would spam the feed. Process a few
    per run and re-run later.
    """
    root = args.root
    blog = load_state(root)
    li_path = os.path.join(root, STATE_DIR, LI_STATE)
    li = json.load(open(li_path, encoding="utf-8")) if os.path.exists(li_path) else []
    done = {r.get("blogSlug") for r in li if r.get("status") == "published"}
    pending = [r for r in blog if r.get("status") == "published" and r.get("slug") not in done]
    pending.sort(key=lambda r: r.get("publishedAt") or "", reverse=True)
    out = [{"slug": r.get("slug"), "postUrl": r.get("postUrl"),
            "publishedAt": r.get("publishedAt"),
            "coverImage": (r.get("imageUrls") or [""])[0]} for r in pending[: args.limit]]
    print(json.dumps({"pending": len(pending), "showing": out}, ensure_ascii=False, indent=1))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.environ.get(
        "PRODUCT_HTML_ROOT",
        "/Volumes/MOVESPEED/baidunetdiskworkspace/Product Presentation/Product Html"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("post")
    p.add_argument("--blog-slug", required=True)
    p.add_argument("--commentary-file", required=True)
    p.add_argument("--image-url", default="")
    p.add_argument("--blog-url", default="")
    p.add_argument("--alt-text", default="Southern Machinery SMT/THT PCB assembly automation equipment")
    p.set_defaults(func=post)

    r = sub.add_parser("repair")
    r.add_argument("--limit", type=int, default=5)
    r.set_defaults(func=repair)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
