#!/usr/bin/env python3
"""External link check for a single-file landing page.

Usage:
    python3 check_links.py <landing-page.html> [--site https://smthelp.com]

Why this exists: the QA checklist said "every external URL must return 200", but
nothing executed it, so it was never run on the built artifact -- only on the
sources while sourcing images. The first time it ran on a finished page it found
a catalog PDF returning 404.

What it catches that nothing else does:
  * a URL that 200s while you are sourcing it and 404s later (file renamed upstream)
  * a URL you built by hand from a board scrape and got wrong
  * NON-BREAKING SPACES in filenames. file.autoinsertion.com stores some PDFs
    with U+00A0 in the name (%C2%A0). Normalising that to %20 -- which any
    "tidy up the URL" step will do -- silently 404s. The directory part uses
    regular spaces while the filename part uses U+00A0, in the same URL.

Self-referential URLs (canonical + hreflang) point at the page's own future
public URL. Those are expected to 404 before the page is deployed, so they are
reported separately as PENDING rather than as failures -- but they are printed
loudly, because a canonical pointing at a 404 is worse than no canonical: the
hreflang cluster only works once every alternate resolves.
"""
import argparse, html, re, subprocess, sys, urllib.parse
from collections import Counter

# Hosts we do not control or that are not meaningful to probe from a script.
SKIP_HOSTS = ("chat.smthelp.com", "youtube-nocookie.com", "schema.org",
              "i.ytimg.com", "www.youtube.com", "youtu.be")
UA = "Mozilla/5.0 (compatible; SouthernMachinery-linkcheck/1.0)"


def extract(path):
    """Return (urls_to_probe, origins_only).

    `origins_only` collects bare origins from <link rel="preconnect"> and
    <link rel="dns-prefetch">. Those are socket hints, not navigable links: the
    root path of fonts.googleapis.com legitimately 404s, and probing it produces
    a false failure. A checker that reports false failures gets ignored, which
    is how a real 404 hides behind noise.
    """
    s = open(path, encoding="utf-8").read()
    origins = set()
    for m in re.finditer(
            r'<link[^>]+rel="(?:preconnect|dns-prefetch)"[^>]*>', s, re.I):
        h = re.search(r'href="(https?://[^/"]+)', m.group(0))
        if h:
            origins.add(html.unescape(h.group(1)))
    out = set()
    for m in re.finditer(r'(?:src|href)="(https?://[^"]+)"', s):
        out.add(html.unescape(m.group(1)))
    return out - origins, origins


def probe(url, timeout=30):
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "-L", "--max-time", str(timeout), "-A", UA, url],
            capture_output=True, text=True, timeout=timeout + 10)
        return r.stdout.strip() or "000"
    except subprocess.TimeoutExpired:
        return "000"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--site", default=None,
                    help="site prefix; URLs under it are treated as self-referential")
    a = ap.parse_args()

    urls, origins = extract(a.page)
    site = a.site
    if not site:
        m = re.search(r'<link rel="canonical" href="(https?://[^/"]+)', 
                      open(a.page, encoding="utf-8").read())
        site = m.group(1) if m else None

    self_ref, external = set(), set()
    for u in urls:
        if any(h in u for h in SKIP_HOSTS):
            continue
        (self_ref if site and u.startswith(site + "/") else external).add(u)

    print(f"page: {a.page}")
    print(f"site: {site}")
    print(f"{len(external)} external + {len(self_ref)} self-referential URL(s) "
          f"(skipped: {', '.join(SKIP_HOSTS)})")
    if origins:
        print(f"skipped {len(origins)} preconnect/dns-prefetch origin(s) "
              f"(socket hints, not navigable): {', '.join(sorted(origins))}")
    print()

    fails, pending = [], []
    for u in sorted(external):
        code = probe(u)
        mark = "OK  " if code == "200" else "FAIL"
        print(f"  {mark} {code}  {u[:110]}")
        if code != "200":
            fails.append((code, u))

    if self_ref:
        print("\n  self-referential (canonical / hreflang) — 404 before deploy is expected:")
        for u in sorted(self_ref):
            code = probe(u)
            state = "LIVE" if code == "200" else "not published yet"
            print(f"    {code}  [{state}]  {u[:104]}")
            if code != "200":
                pending.append((code, u))

    print("\n=== RESULT ===")
    counts = Counter(c for c, _ in fails)
    if fails:
        print(f"{len(fails)} BROKEN external link(s): " +
              ", ".join(f"{n}x {c}" for c, n in counts.items()))
        for c, u in fails:
            print(f"  {c}  {u}")
    else:
        print("ALL EXTERNAL LINKS OK")
    if pending:
        print(f"\n{len(pending)} self-referential URL(s) not yet published.")
        print("A canonical pointing at a 404 is worse than none: the page will be dropped")
        print("and the hreflang cluster cannot form. Deploy to the canonical slug, or")
        print("point canonical/hreflang at wherever the page actually lives.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
