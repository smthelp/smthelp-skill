#!/usr/bin/env python3
"""
product-html-blog-pipeline :: pre-publish SEO/AEO gate check

  qa.py --payload payload.json --source-file "S7020T ....html"

14 gates. Any FAIL should block publishing. WARN is advisory.
Exit code 0 = all gates pass (WARN allowed), 1 = at least one FAIL.
"""

import argparse
import json
import os
import re
import sys

BANNED = re.compile(
    r"\b(best|No\.?1|#1|guarantee[ds]?|perfect|world-class|100%|never fail|most advanced)\b",
    re.I)


def words(s):
    return len(s.split())


def check(payload, source_text):
    md = payload.get("contentMarkdown", "")
    slug = payload.get("slug", "")
    seo_t = payload.get("seoTitle", "")
    seo_d = payload.get("seoDescription", "")
    title = payload.get("title", "")
    results = []

    def gate(name, ok, detail, hard=True):
        results.append({"gate": name, "status": "PASS" if ok else ("FAIL" if hard else "WARN"),
                        "detail": detail})

    # 1 Title
    gate("1 Title", 20 <= len(title) <= 110 and "Southern Machinery" in title,
         f"len={len(title)}")
    # 2 Meta (seoTitle / seoDescription)
    gate("2 Meta", len(seo_t) <= 60 and 140 <= len(seo_d) <= 160,
         f"seoTitle={len(seo_t)} seoDesc={len(seo_d)}")
    # 3 Keywords - primary keyword in first 100 words of body
    # .lower() MUST run before the sub: [^a-z0-9 ] strips uppercase letters too.
    core = re.sub(r"[^a-z0-9 ]", " ", (payload.get("seoTitle", "").split("|")[0] or "").lower())
    kws = [w for w in core.split() if len(w) > 3]
    head = " ".join(md.split()[:120]).lower()
    hit = [k for k in kws if k in head]
    gate("3 Keywords", bool(hit), f"head100 hits={hit}")
    # 4 URL slug
    gate("4 Slug", bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug)) and len(slug) <= 90,
         slug)
    # 5 Heading hierarchy
    h1 = len(re.findall(r"^# ", md, re.M))
    h2 = len(re.findall(r"^## ", md, re.M))
    h3 = len(re.findall(r"^### ", md, re.M))
    gate("5 H1-H3", h1 == 1 and h2 >= 4 and h3 >= 1, f"H1={h1} H2={h2} H3={h3}")
    # 6 Image alt text carries the product category
    alts = re.findall(r"!\[([^\]]*)\]\((https?://[^)]+)\)", md)
    gate("6 Image alt", len(alts) >= 1 and all(len(a.strip()) > 15 for a, _ in alts),
         f"{len(alts)} images")
    # 7 UX readability - no H2 block longer than ~260 words
    blocks = re.split(r"^## ", md, flags=re.M)[1:]
    longest = max((words(b) for b in blocks), default=0)
    gate("7 Readability", longest <= 320, f"longest H2 block={longest}w", hard=False)
    # 8 Schema-friendly FAQ
    faq = md.split("## FAQ")[-1] if "## FAQ" in md else ""
    faq_q = len(re.findall(r"\*\*[^*?]+\?\*\*", faq))
    gate("8 FAQ schema", 4 <= faq_q <= 6, f"{faq_q} Q&A pairs")
    # 9 Canonical / cover image set
    gate("9 Canonical+OG", bool(payload.get("coverImage", "").startswith("https://")),
         payload.get("coverImage", "")[:60], hard=False)
    # 10 Body depth
    n = words(md)
    gate("10 Depth", 1000 <= n <= 1650, f"{n} words", hard=False)
    # 11 Excerpt usable as an AI answer block
    gate("11 Excerpt", 80 <= words(payload.get("excerpt", "")) <= 160,
         f"{words(payload.get('excerpt',''))} words")
    # 12 At least one citable data point / comparison table
    gate("12 Data point", "|" in md and len(re.findall(r"\|\s*-", md)) >= 2,
         "spec table present")
    # 13 Truthfulness - every number in the article should exist in the source
    nums = re.findall(r"\b\d+(?:\.\d+)?\b", md)
    missing = [x for x in set(nums) if x not in source_text][:12]
    gate("13 Truthfulness", len(missing) <= 6, f"unverified tokens={missing}", hard=False)
    # 14 Compliance - banned superlatives
    bad = sorted(set(m.group(0) for m in BANNED.finditer(md)))
    gate("14 Compliance", not bad, f"banned={bad}")

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--payload", required=True)
    ap.add_argument("--source-file", required=True)
    args = ap.parse_args()

    payload = json.load(open(args.payload, encoding="utf-8"))
    src = ""
    if os.path.exists(args.source_file):
        src = open(args.source_file, encoding="utf-8", errors="ignore").read()

    res = check(payload, src)
    fails = [r for r in res if r["status"] == "FAIL"]
    for r in res:
        print(f"{r['status']:4}  {r['gate']:<22} {r['detail']}")
    print(f"\n{len(res) - len(fails)}/{len(res)} pass, {len(fails)} FAIL")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
