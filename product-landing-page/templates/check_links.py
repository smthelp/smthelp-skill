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
import argparse, html, re, subprocess, sys, time, urllib.parse
from collections import Counter

# Hosts we do not control or that are not meaningful to probe from a script.
SKIP_HOSTS = ("chat.smthelp.com", "youtube-nocookie.com", "schema.org",
              "i.ytimg.com", "www.youtube.com", "youtu.be")
UA = "Mozilla/5.0 (compatible; SouthernMachinery-linkcheck/1.0)"

# Status codes that a host returns to *any* non-interactive client, so the link
# cannot be verified from a script at all -- and must not be reported as broken.
#
# LinkedIn answers 999 to every automated request, including one carrying a
# genuine desktop Chrome User-Agent (verified: bot UA, Chrome UA and the
# www.linkedin.com equivalent all return 999). Treating that as a failure made
# all eight pages in the repository report BROKEN -- the cry-wolf failure mode
# this script exists to avoid. A report that is always red gets ignored, and
# then a real 404 hides behind it.
BOT_BLOCKED = {
    "999": ("linkedin.com",),                      # LinkedIn anti-bot
    "403": ("linkedin.com", "facebook.com", "x.com"),
    "429": ("linkedin.com", "facebook.com", "x.com", "twitter.com"),
}


def classify(url, code):
    """Return 'ok' | 'blocked' | 'fail' for a probed URL."""
    if code == "200":
        return "ok"
    for c, hosts in BOT_BLOCKED.items():
        if code == c and any(h in url for h in hosts):
            return "blocked"
    return "fail"


URL_ATTRS = ("src", "href", "content", "poster", "data-full", "data-src",
             "data-original", "action")

def extract(path):
    """Return (urls_to_probe, origins_only).

    `origins_only` collects bare origins from <link rel="preconnect"> and
    <link rel="dns-prefetch">. Those are socket hints, not navigable links: the
    root path of fonts.googleapis.com legitimately 404s, and probing it produces
    a false failure. A checker that reports false failures gets ignored, which
    is how a real 404 hides behind noise.

    Note `content=` is included deliberately. An earlier version probed only
    src/href, which meant <meta property="og:image"> was never checked -- and
    og:image is the thumbnail a customer sees when the link is pasted into
    LinkedIn or WhatsApp. A dead og:image is a dead share preview, and nothing
    else in the pipeline looks at it. JSON-LD `logo` / `image` are read the same
    way, for the same reason: they have no runtime fallback.
    """
    s = open(path, encoding="utf-8").read()
    origins = set()
    for m in re.finditer(
            r'<link[^>]+rel="(?:preconnect|dns-prefetch)"[^>]*>', s, re.I):
        h = re.search(r'href="(https?://[^/"]+)', m.group(0))
        if h:
            origins.add(html.unescape(h.group(1)))

    out = set()
    for a in URL_ATTRS:
        for m in re.finditer(r'\b' + a + r'="(https?://[^"]+)"', s):
            out.add(html.unescape(m.group(1)))
    # JSON-LD string values for keys that must resolve to a real asset
    for m in re.finditer(r'"(?:logo|image|url|@id|contentUrl|thumbnailUrl)"\s*:\s*"(https?://[^"]+)"', s):
        out.add(html.unescape(m.group(1)))
    return out - origins, origins


def probe_once(url, timeout):
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "-L", "--max-time", str(timeout), "-A", UA, url],
            capture_output=True, text=True, timeout=timeout + 10)
        return r.stdout.strip() or "000"
    except subprocess.TimeoutExpired:
        return "000"


def probe(url, timeout=30, retries=2):
    """Probe with retries. Returns (code, attempts).

    A single 000 is usually a transient network or proxy hiccup, not a dead
    link -- https://smthelp.com/ was observed returning 200, 200, then 000 on
    three consecutive requests seconds apart. Reporting that as BROKEN is the
    same cry-wolf failure as probing a preconnect origin: the real 404 gets
    lost in the noise. So retry, and only fail if every attempt fails.
    """
    code = probe_once(url, timeout)
    attempts = 1
    while code != "200" and attempts <= retries:
        time.sleep(1.5)
        code = probe_once(url, timeout)
        attempts += 1
    return code, attempts


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

    fails, pending, blocked = [], [], []
    for u in sorted(external):
        code, n = probe(u)
        verdict = classify(u, code)
        mark = {"ok": "OK  ", "blocked": "BLKD", "fail": "FAIL"}[verdict]
        note = f" (passed on attempt {n})" if code == "200" and n > 1 else ""
        print(f"  {mark} {code}  {u[:104]}{note}")
        if verdict == "fail":
            fails.append((code, u))
        elif verdict == "blocked":
            blocked.append((code, u))

    if blocked:
        print("\n  bot-blocked -- returned to every client, cannot be verified by script:")
        for c, u in blocked:
            print(f"    {c}  {u}")

    if self_ref:
        print("\n  self-referential (canonical / hreflang) — 404 before deploy is expected:")
        for u in sorted(self_ref):
            code, _ = probe(u)
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
    if blocked:
        print(f"({len(blocked)} bot-blocked URL(s) not verifiable by script -- "
              f"open them in a browser to confirm)")
    if pending:
        print(f"\n{len(pending)} self-referential URL(s) not yet published.")
        print("A canonical pointing at a 404 is worse than none: the page will be dropped")
        print("and the hreflang cluster cannot form. Deploy to the canonical slug, or")
        print("point canonical/hreflang at wherever the page actually lives.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
