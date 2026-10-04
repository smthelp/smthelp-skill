#!/usr/bin/env python3
"""Repository-wide external link check for a folder of landing pages.

Usage:
    python3 check_links_repo.py <dir> [--workers 8] [--timeout 30]

Why this exists on top of check_links.py (which checks one page):

  1. SPEED. Eight pages share most of their external URLs (brand logo, social
     links, the two portal hosts). Probing per page re-fetches the same URLs
     eight times. This dedups first, so the network work is a fraction of the
     sum of the parts.

  2. RELIABILITY OF THE REPORTING PATH. The first version of this sweep piped
     `check_links.py` through `grep -E '^(=== RESULT|FAIL|BROKEN|...)'`. That
     pattern anchored at line start, but the per-URL lines are indented
     (`  FAIL 404  url`) and the summary line for a failing page begins with a
     digit (`4 BROKEN external link(s)`). Both therefore failed to match, so a
     page with broken links printed *neither* "ALL EXTERNAL LINKS OK" *nor*
     any FAIL line -- it looked like it had been skipped. Do the parsing in
     Python and keep text tools out of the reporting path.

  3. It is not a per-page script pretending to be a repo sweep. Broken links
     are reported per page, with the page they appear on, and the exit code
     reflects the whole repo -- so it can gate a push.

Self-referential URLs (canonical + hreflang) are expected to 404 before deploy
and are reported as PENDING, not as failures.
"""
import argparse, sys, os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_links import extract, probe, classify, SKIP_HOSTS  # noqa: E402


def site_of(page):
    """Read the page's own canonical origin, so self-references can be told
    apart from genuine external links."""
    import re
    s = open(page, encoding="utf-8").read()
    m = re.search(r'<link rel="canonical" href="(https?://[^/"]+)', s)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--verify-attempts", type=int, default=6,
                    help="serial re-probes for any URL that failed in parallel")
    ap.add_argument("--verify-gap", type=float, default=2.0,
                    help="seconds between serial re-probes")
    a = ap.parse_args()

    pages = sorted(f for f in os.listdir(a.dir) if f.endswith(".html"))
    if not pages:
        sys.exit(f"no .html files in {a.dir}")

    per_page_ext, per_page_self = {}, {}
    all_ext, all_self = set(), set()

    for f in pages:
        p = os.path.join(a.dir, f)
        urls, _origins = extract(p)
        site = site_of(p)
        ext = {u for u in urls
               if not any(h in u for h in SKIP_HOSTS)
               and not (site and u.startswith(site + "/"))}
        slf = {u for u in urls
               if site and u.startswith(site + "/")
               and not any(h in u for h in SKIP_HOSTS)}
        per_page_ext[f], per_page_self[f] = ext, slf
        all_ext |= ext
        all_self |= slf

    print(f"{len(pages)} page(s), {len(all_ext)} unique external URL(s), "
          f"{len(all_self)} unique self-referential URL(s)")
    print(f"probing with {a.workers} workers, {a.timeout}s timeout\n")

    def run(url):
        return url, probe(url, timeout=a.timeout)[0]

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        ext_res = dict(ex.map(run, sorted(all_ext)))
        self_res = dict(ex.map(run, sorted(all_self)))

    # Re-verify every non-200 serially, on its own, with more attempts.
    #
    # Parallel probing manufactures failures: https://smthelp.com returned
    # 000 on 5 of 10 *serial* attempts in this environment, and 7 pages were
    # reported BROKEN for it purely because 12 workers were hitting the host
    # at once. Other hosts (github.com, ph.smthelp.com) were 8/8 stable
    # through the same proxy, so the host is genuinely flaky rather than the
    # proxy being broadly unreliable.
    #
    # A URL that answers 200 when given a quiet moment is NOT broken. Report
    # it as unstable, with the failure ratio, so a real 404 is not buried
    # under noise. Only a URL that fails every serial attempt is broken.
    def reverify(url):
        import time
        attempts = a.verify_attempts
        fails = 0
        for i in range(attempts):
            if i:
                time.sleep(a.verify_gap)
            code, _ = probe(url, timeout=a.timeout, retries=0)
            if code == "200":
                return ("ok" if fails == 0 else "unstable"), fails, attempts
            fails += 1
        return "broken", fails, attempts

    suspects = sorted({u for u, c in list(ext_res.items()) + list(self_res.items())
                       if classify(u, c) not in ("ok", "blocked")})
    reverified = {}
    if suspects:
        print(f"re-verifying {len(suspects)} non-200 URL(s) serially "
              f"({a.verify_attempts} attempts, {a.verify_gap}s apart)...\n")
        for u in suspects:
            verdict, fails, attempts = reverify(u)
            reverified[u] = (verdict, fails, attempts)
            if verdict != "ok":
                print(f"  {verdict.upper():<8} {u}")
                print(f"           failed {fails}/{attempts} serial attempts")
            else:
                print(f"  RECOVERED  {u}  (failed {fails}/{attempts} in parallel)")
        print()

    print("=" * 78)
    print("EXTERNAL LINKS, BY PAGE")
    print("=" * 78)
    total_fail = 0
    blocked_all = {}
    unstable_all = {}
    for f in pages:
        bad, blk = [], []
        for u in sorted(per_page_ext[f]):
            if u in reverified:
                verdict, fails, attempts = reverified[u]
                if verdict == "ok":
                    continue                      # answered 200 when probed alone
                note = f"{fails}/{attempts} serial attempts failed"
                if verdict == "unstable":
                    unstable_all[u] = note
                else:
                    bad.append((u, note))
                continue
            v = classify(u, ext_res[u])
            if v == "fail":
                bad.append((u, ext_res[u]))
            elif v == "blocked":
                blk.append((u, ext_res[u]))
                blocked_all[u] = ext_res[u]
        n = len(per_page_ext[f])
        if bad:
            total_fail += len(bad)
            print(f"\nFAIL  {f}   ({len(bad)} of {n} broken)")
            for u, c in bad:
                print(f"        {c}  {u}")
        else:
            print(f"OK    {f}   ({n} checked)")

    if unstable_all:
        print("\n" + "-" * 78)
        print("UNSTABLE -- answered 200 when probed alone, failed under load")
        print("(host-side flakiness, NOT a broken link)")
        print("-" * 78)
        for u, note in sorted(unstable_all.items()):
            print(f"  {note}  {u}")

    if blocked_all:
        print("\n" + "-" * 78)
        print("BOT-BLOCKED -- returned to every client, cannot be verified by script")
        print("(open in a browser to confirm; NOT counted as broken)")
        print("-" * 78)
        for u, c in sorted(blocked_all.items()):
            print(f"  {c}  {u}")

    print()
    print("=" * 78)
    print("SELF-REFERENTIAL (canonical / hreflang) -- 404 before deploy is expected")
    print("=" * 78)
    pending = 0
    for f in pages:
        urls = sorted(per_page_self[f])
        live = [u for u in urls if self_res[u] == "200"]
        notpub = [u for u in urls if self_res[u] != "200"]
        pending += len(notpub)
        print(f"  {f[:60]:<62} {len(live)} live / {len(notpub)} not published")
        if live:
            for u in live:
                print(f"        LIVE  {u}")

    print()
    print("=== RESULT ===")
    if total_fail:
        print(f"{total_fail} BROKEN external link(s) across the repository.")
    else:
        print("ALL EXTERNAL LINKS OK")
    if pending:
        print(f"\n{pending} self-referential URL(s) not yet published.")
        print("A canonical pointing at a 404 is worse than none: the page is dropped")
        print("and the hreflang cluster cannot form. Deploy to the canonical slug, or")
        print("point canonical/hreflang at wherever the page actually lives.")
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
