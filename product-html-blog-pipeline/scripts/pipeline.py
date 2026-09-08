#!/usr/bin/env python3
"""
product-html-blog-pipeline :: source selection + state bookkeeping

Subcommands
-----------
  select     Scan the Product Html folder, diff against the blog state file, and
             print a ranked candidate list (JSON to stdout).
  publish    POST a payload JSON to the blog API, verify, and append to the state file.
  linkedin   (in linkedin.py) upload an image + post to the company page.

Design rules (learned the hard way - do not "simplify" these away)
------------------------------------------------------------------
* fileHash is the FULL sha256 hex digest. Earlier runs compared only the first 16
  chars and concluded that all 140 files were unpublished.
* State files live in <root>/.automation-state/, NOT in the workspace root.
* Never store tokens in the state files, in the repo, or in stdout.
* macOS AppleDouble files ("._*") are not real documents - always skip them.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

STATE_DIR = ".automation-state"
BLOG_STATE = "product-html-blog-publisher-state.json"
LI_STATE = "product-html-linkedin-publisher-state.json"

SCAN_EXT = ("html", "md", "txt", "svg")

# Files that are rules / config / templates, never source material.
SKIP_EXACT = {
    "AGENTS.md", "CLAUDE.md", "README.md", "VScode.code-workspace",
    ".cursor", ".superdesign", ".automation-state", ".git", ".workbuddy",
}
SKIP_RE = re.compile(
    r"(^|/)(AGENTS|CLAUDE|README)|\.code-workspace$|(^|/)\._|"
    r"form[- ]trigger|form[- ]trigger-template|trigger-template",
    re.I,
)

# Social cards / infographics: scannable but weak source material -> ranked last.
WEAK_RE = re.compile(r"linkedin|svg card|post v\d+\.svg$|infographic", re.I)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_state(root):
    p = os.path.join(root, STATE_DIR, BLOG_STATE)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def save_state(root, records):
    p = os.path.join(root, STATE_DIR, BLOG_STATE)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p):
        shutil.copy(p, p + ".bak")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=1)


def text_of(path):
    """Crude HTML/MD/SVG -> text, enough for richness scoring."""
    raw = open(path, encoding="utf-8", errors="ignore").read()
    if path.lower().endswith((".html", ".svg")):
        raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
        raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S | re.I)
        raw = re.sub(r"<[^>]+>", " ", raw)
    raw = re.sub(r"&[a-z#0-9]+;", " ", raw)
    return re.sub(r"\s+", " ", raw).strip()


def tokens(name):
    """Topic tokens from a filename or slug: keep digits attached to letters."""
    base = os.path.splitext(os.path.basename(name))[0].lower()
    base = base.replace("–", "-").replace("—", "-")
    toks = [t for t in re.split(r"[^a-z0-9]+", base) if t]
    return set(t for t in toks if len(t) > 2 or re.search(r"\d", t))


# --------------------------------------------------------------------------- #
# select
# --------------------------------------------------------------------------- #
def cmd_select(args):
    root = args.root
    state = load_state(root)

    published = {}          # basename -> [(status, slug, fileHash), ...]
    pub_tokens = []         # topic token sets of already-published slugs
    pub_slugs = set()
    for r in state:
        b = os.path.basename(r.get("filePath") or "")
        published.setdefault(b, []).append(
            (r.get("status"), r.get("slug"), r.get("fileHash"))
        )
        if r.get("slug"):
            pub_slugs.add(r["slug"])
            pub_tokens.append(tokens(r["slug"]))

    cands = []
    for ext in SCAN_EXT:
        for p in glob.glob(os.path.join(root, "*." + ext)):
            b = os.path.basename(p)
            if b.startswith("._") or SKIP_RE.search(b) or b in SKIP_EXACT:
                continue
            h = sha256(p)
            recs = published.get(b)
            if recs is None:
                kind = "new"
            elif any(x[2] == h for x in recs):
                continue                       # already published, unchanged
            else:
                kind = "updated"

            body = text_of(p)
            words = len(body.split())
            if words < 120:
                continue                       # not enough to write from

            imgs = len(set(re.findall(r"https://ph\.smthelp\.com/\S+?\.(?:png|jpe?g|webp|gif)",
                                      open(p, encoding="utf-8", errors="ignore").read())))
            specs = len(re.findall(r"\b\d+(?:\.\d+)?\s?(?:mm|kg|kW|KVA|V|VAC|A|MPa|dB|CPH|PCS/H|pcs/h|%)\b", body))

            tk = tokens(b)
            overlap = 0.0
            for pt in pub_tokens:
                if not pt:
                    continue
                j = len(tk & pt) / max(1, len(tk | pt))
                overlap = max(overlap, j)

            mtime = os.path.getmtime(p)
            score = (
                2.0 * (1.0 - overlap)                 # freshness of topic  (0..2)
                + min(words / 1200.0, 2.0)            # richness            (0..2)
                + min(imgs / 4.0, 1.0)                # images in source    (0..1)
                + min(specs / 12.0, 1.5)              # hard spec density   (0..1.5)
                + (0.4 if kind == "updated" else 0.0) # updated docs slightly ahead
                - (2.0 if WEAK_RE.search(b) else 0.0) # social cards last
            )

            cands.append({
                "file": p,
                "basename": b,
                "kind": kind,
                "score": round(score, 3),
                "topicOverlap": round(overlap, 3),
                "words": words,
                "inlineImages": imgs,
                "specHits": specs,
                "mtime": int(mtime),
                "mtimeIso": datetime.fromtimestamp(mtime, timezone.utc).strftime("%Y-%m-%d"),
            })

    cands.sort(key=lambda c: (-c["score"], -c["mtime"]))
    out = {
        "root": root,
        "scanned": len(cands) + len([1 for r in state]),
        "publishedRecords": len(state),
        "publishedSlugs": sorted(pub_slugs),
        "candidates": cands[: args.limit],
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print(file=sys.stderr)


# --------------------------------------------------------------------------- #
# publish
# --------------------------------------------------------------------------- #
def cmd_publish(args):
    import urllib.error
    import urllib.request

    token = os.environ.get("SMTHELP_BLOG_TOKEN")
    if not token:
        tok_file = os.path.expanduser("~/.config/smthelp/blog_token")
        if os.path.exists(tok_file):
            token = open(tok_file).read().strip()
    if not token:
        sys.exit("ERROR: set SMTHELP_BLOG_TOKEN (or ~/.config/smthelp/blog_token)")

    root = args.root
    payload = json.load(open(args.payload, encoding="utf-8"))
    base = args.base.rstrip("/")

    slug = payload["slug"]
    state = load_state(root)
    if not args.force and any(r.get("slug") == slug for r in state):
        sys.exit(f"ERROR: slug '{slug}' already in state file. Use --force or pick a new slug.")

    def call(method, url, body=None):
        data = json.dumps(body).encode() if body is not None else None
        h = {"Authorization": "Bearer " + token,
             "Origin": base,
             "Content-Type": "application/json",
             "User-Agent": "Mozilla/5.0"}
        r = urllib.request.Request(url, data=data, headers=h, method=method)
        try:
            with urllib.request.urlopen(r, timeout=90) as resp:
                return resp.status, resp.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "ignore")

    st, body = call("POST", base + "/api/posts", payload)
    if st >= 300:
        # Slug collision -> server appends "-2". Retry once with a suffixed slug.
        if st == 500 or "slug" in body.lower():
            payload["slug"] = slug + "-2"
            slug = payload["slug"]
            st, body = call("POST", base + "/api/posts", payload)
        if st >= 300:
            rec = {"filePath": args.file, "fileHash": sha256(args.file) if args.file and os.path.exists(args.file) else "",
                   "sourceMtime": int(os.path.getmtime(args.file)) if args.file and os.path.exists(args.file) else 0,
                   "title": payload.get("title", ""), "slug": slug, "postId": "",
                   "postUrl": "", "publishedAt": "", "status": "failed",
                   "error": f"HTTP {st}: {body[:300]}", "imageUrls": []}
            state.append(rec)
            save_state(root, state)
            sys.exit(f"ERROR: publish failed HTTP {st}: {body[:400]}")

    data = json.loads(body).get("data", {})
    final_slug = data.get("slug", slug)
    post_url = f"{base}/blog/{final_slug}"

    # Verify on the PUBLIC route. GET /api/posts/<slug> can 403 even with a valid token.
    vr = urllib.request.Request(post_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(vr, timeout=60) as resp:
            http_ok = resp.status
    except urllib.error.HTTPError as e:
        http_ok = e.code
    if http_ok != 200:
        sys.exit(f"ERROR: published but public page returns {http_ok}: {post_url}")

    rec = {
        "filePath": args.file,
        "fileHash": sha256(args.file) if args.file and os.path.exists(args.file) else "",
        "sourceMtime": int(os.path.getmtime(args.file)) if args.file and os.path.exists(args.file) else 0,
        "title": payload.get("title", ""),
        "slug": final_slug,
        "postId": data.get("id", ""),
        "postUrl": post_url,
        "publishedAt": data.get("publishedAt") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "status": "published",
        "error": "",
        "imageUrls": [payload.get("coverImage", "")] if payload.get("coverImage") else [],
    }
    state.append(rec)
    save_state(root, state)
    print(json.dumps(rec, ensure_ascii=False, indent=1))


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.environ.get(
        "PRODUCT_HTML_ROOT",
        "/Volumes/MOVESPEED/baidunetdiskworkspace/Product Presentation/Product Html"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("select")
    s.add_argument("--limit", type=int, default=12)
    s.set_defaults(func=cmd_select)

    p = sub.add_parser("publish")
    p.add_argument("--payload", required=True, help="path to payload JSON")
    p.add_argument("--file", required=True, help="source document that the article was written from")
    p.add_argument("--base", default="https://jasonwu.smthelp.eu")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_publish)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
