#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
geo_scan.py — Phase 2 技术抓取（客观事实，不做主观判断）

用法:
  python3 geo_scan.py --url https://www.smthelp.com --profile smt --out /tmp/scan.json
  python3 geo_scan.py --url https://example.com --pages /,/about,/faq --probe-mirrors --out scan.json

输出: JSON 事实集，供 geo_score.py 消费。
设计原则: 只报事实，不打分。所有判定留给 rubric 与 Agent。
"""
import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from collections import Counter
from datetime import datetime, timezone
from html import unescape

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0 Safari/537.36")


# ----------------------------- fetch -----------------------------
def fetch(url, timeout=30):
    """Return (ok, status, headers_dict, text). Never raises."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            body = raw.decode("utf-8", errors="ignore")
            return True, r.status, dict(r.headers), body
    except urllib.error.HTTPError as e:
        return False, e.code, dict(e.headers or {}), ""
    except Exception as e:
        return False, 0, {"error": str(e)}, ""


def head(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, r.status, dict(r.headers), ""
    except urllib.error.HTTPError as e:
        return False, e.code, dict(e.headers or {}), ""
    except Exception as e:
        return False, 0, {"error": str(e)}, ""


# ----------------------------- parse helpers -----------------------------
def strip_tags(html):
    t = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).strip()


def count_words(html):
    return len(strip_tags(html).split())


def page_facts(url, html, status, headers):
    """Extract per-page objective facts."""
    low = html.lower()
    ld_blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S | re.I)
    ld_types = []
    for b in ld_blocks:
        ld_types += re.findall(r'"@type"\s*:\s*"([^"]+)"', b)

    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S | re.I)
    h3 = re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.S | re.I)
    txt = strip_tags(html)
    nums = re.findall(
        r"\b\d+(?:\.\d+)?\s*(?:kg|mm|cm|kW|W|V|Hz|°C|CPH|ppm|pcs|m/min|rpm|%)\b", txt, re.I)
    imgs = re.findall(r"<img[^>]*>", html, re.I)
    desc = re.findall(
        r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']*)', html, re.I)
    words = count_words(html)

    return {
        "url": url,
        "status": status,
        "title": (re.findall(r"<title[^>]*>(.*?)</title>", html, re.S | re.I) or [""])[0].strip(),
        "meta_description": desc[0].strip() if desc else None,
        "meta_keywords": bool(re.search(
            r'<meta[^>]+name=["\']keywords["\']', html, re.I)),
        "canonical": bool(re.search(r'rel=["\']canonical', html, re.I)),
        "og_count": len(re.findall(r'property=["\']og:', html, re.I)),
        "jsonld_count": len(ld_blocks),
        "jsonld_types": sorted(set(ld_types)),
        "h1_count": len(h1),
        "h1_text": [re.sub(r"<[^>]+>", "", x).strip()[:120] for x in h1],
        "h2_count": len(h2),
        "h3_count": len(h3),
        "question_headings": len([x for x in h2 + h3
                                 if re.search(r"\?|how|what|why|which|who", strip_tags(x), re.I)]),
        "words": words,
        "quantified_params": len(nums),
        "data_density_per_100w": round(len(nums) / words * 100, 2) if words else 0.0,
        "table_count": len(re.findall(r"<table", html, re.I)),
        "img_total": len(imgs),
        "img_missing_alt": len([i for i in imgs if "alt=" not in i.lower()]),
        "viewport": bool(re.search(r'name=["\']viewport', html, re.I)),
        "is_soft404": (status == 200 and bool(re.search(
            r"<title[^>]*>\s*(404|page not found|not found)", html, re.I))),
        "script_src_count": len(re.findall(r"<script[^>]+src=", html, re.I)),
        "css_link_count": len(re.findall(r"<link[^>]+rel=[\"']stylesheet", html, re.I)),
    }


def extract_nap(html):
    """Best-effort NAP extraction: addresses / phones / emails."""
    txt = strip_tags(html)
    phones = sorted(set(re.findall(r"\+?\d[\d\s\-()]{7,}\d", txt)))
    phones = [p.strip() for p in phones if len(re.sub(r"\D", "", p)) >= 8][:20]
    emails = sorted(set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]{2,}", txt)))[:20]
    # v1.1: stricter address matcher — require BOTH a street/unit token AND a
    # city/region token, plus a house/room number. Loose matching produced 18
    # false positives on smthelp.com (menu labels, product names).
    street = r"(?:Road|Rd\.|Street|St\.|Avenue|Ave\.|Block|Building|Floor|Rm\.?|Room|Industrial Area)"
    city = r"(?:Shenzhen|Shanghai|Beijing|Guangzhou|Dongguan|Guangdong|China|Vietnam|Mexico|Brazil)"
    unit = r"(?:No\.?\s*\d+|\d+\s*(?:F|Floor)|Rm\.?\s*\d+|\d{1,4}\s*[A-Z]?)"
    addrs = sorted(set(
        a.strip(" ,.;") for a in re.findall(
            r"[^.;\n]{8,140}?" + unit + r"[^.;\n]{0,60}?" + street +
            r"[^.;\n]{0,90}?" + city + r"[^.;\n]{0,40}", txt, re.I)
        if 14 <= len(a.strip()) <= 160))[:8]
    return {"phones": phones, "emails": emails, "addresses": addrs}


def discover_sitemaps(base, robots_txt):
    cands = []
    for m in re.findall(r"(?im)^\s*sitemap\s*:\s*(\S+)", robots_txt or ""):
        cands.append(m.strip())
    cands += [base.rstrip("/") + p for p in
              ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml", "/sitemap.txt")]
    seen, out = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


# ----------------------------- main -----------------------------
def main():
    ap = argparse.ArgumentParser(description="GEO audit — Phase 2 technical scan")
    ap.add_argument("--url", required=True, help="site root, include scheme")
    ap.add_argument("--pages", default="/", help="comma separated extra paths")
    ap.add_argument("--profile", default="industrial", help="industry profile key")
    ap.add_argument("--probe-mirrors", action="store_true", help="probe sibling TLDs")
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()

    base = args.url.rstrip("/")
    host = re.sub(r"^https?://", "", base).split("/")[0]
    root_domain = ".".join(host.split(".")[-2:]) if host.count(".") >= 1 else host
    T = args.timeout
    print(f"[scan] target {base}", file=sys.stderr)

    # --- transport ---
    ok, st, hdrs, home_html = fetch(base + "/", T)
    if not ok:
        print(f"[scan] FATAL cannot fetch {base}: status={st} {hdrs}", file=sys.stderr)
        sys.exit(1)

    server = hdrs.get("Server") or hdrs.get("server")
    ok_h, st_h, hdrs_h, _ = head(base + "/", 20)
    h2 = str(hdrs_h.get("HTTP/2", "")) == "" and st_h == 0  # HEAD unsupported
    scan = {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "url": base,
        "host": host,
        "root_domain": root_domain,
        "profile": args.profile,
        "https": base.startswith("https://"),
        "http_status": st,
        "server": server,
        "cdn_hint": hdrs.get("Via") or hdrs.get("X-Cache") or hdrs.get("x-cache"),
        "http2_or_cdn": bool(hdrs.get("Via") or hdrs.get("X-Cache") or hdrs.get("x-cache")),
        "last_modified_header": hdrs.get("Last-Modified"),
    }

    # --- robots + sitemaps ---
    _, rs, _, robots_txt = fetch(base + "/robots.txt", T)
    scan["robots_txt"] = robots_txt if rs == 200 else None
    scan["robots_status"] = rs
    scan["no_robots_block"] = not re.search(r"(?im)^\s*Disallow\s*:\s*/", robots_txt or "")

    sitemap_info = []
    for sm in discover_sitemaps(base, robots_txt):
        ok_s, st_s, _, body = fetch(sm, T)
        if not ok_s:
            sitemap_info.append({"url": sm, "status": st_s, "valid": False,
                                 "soft404": False, "urls": 0})
            continue
        locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", body, re.S)
        mods = re.findall(r"<lastmod>\s*(.*?)\s*</lastmod>", body, re.S)
        soft404 = bool(re.search(r"<title[^>]*>\s*(404|page not found)", body, re.I))
        sitemap_info.append({
            "url": sm, "status": st_s, "valid": bool(locs) and not soft404,
            "soft404": soft404, "urls": len(locs),
            "lastmod_coverage": round(len(mods) / len(locs), 3) if locs else 0.0,
            "lastmod_top": Counter(m.split("T")[0] for m in mods).most_common(5),
            "sample_urls": locs[:10],
        })
    valid_maps = [s for s in sitemap_info if s["valid"]]
    scan["sitemaps"] = sitemap_info
    scan["sitemap_valid"] = bool(valid_maps)
    scan["sitemap_urls"] = max((s["urls"] for s in valid_maps), default=0)
    scan["sitemap_lastmod_coverage"] = max(
        (s["lastmod_coverage"] for s in valid_maps), default=0.0)
    scan["sitemap_soft404"] = [s["url"] for s in sitemap_info if s["soft404"]]

    # --- pages ---
    paths = [p.strip() for p in args.pages.split(",") if p.strip()]
    pages = []
    home_done = False
    for p in ["/"] + [x for x in paths if x != "/"]:
        u = base + ("" if p == "/" else (p if p.startswith("/") else "/" + p))
        if u == base + "/" and home_done and p == "/":
            continue
        if p == "/":
            html_, st_ = home_html, st
            home_done = True
        else:
            o, st_, _, html_ = fetch(u, T)
        if not html_:
            pages.append({"url": u, "status": st_, "error": True})
            print(f"  [page] {st_} {u}  (empty)", file=sys.stderr)
            continue
        f = page_facts(u, html_, st_, hdrs)
        pages.append(f)
        print(f"  [page] {st_} {u}  words={f['words']} h1={f['h1_count']} "
              f"ld={f['jsonld_count']} og={f['og_count']}", file=sys.stderr)
    scan["pages"] = pages
    good = [p for p in pages if not p.get("error")]

    # --- aggregate ---
    scan["jsonld_total"] = sum(p.get("jsonld_count", 0) for p in good)
    scan["jsonld_types_all"] = sorted({t for p in good for t in p.get("jsonld_types", [])})
    scan["og_total"] = sum(p.get("og_count", 0) for p in good)
    scan["canonical_coverage"] = round(
        sum(1 for p in good if p.get("canonical")) / len(good), 3) if good else 0.0
    scan["meta_desc_coverage"] = round(
        sum(1 for p in good if p.get("meta_description")) / len(good), 3) if good else 0.0
    scan["h1_coverage"] = round(
        sum(1 for p in good if p.get("h1_count", 0) > 0) / len(good), 3) if good else 0.0
    scan["title_unique"] = len({p.get("title") for p in good}) == len(good) if good else False
    scan["meta_keywords_present"] = any(p.get("meta_keywords") for p in good)
    scan["homepage_h1"] = next(
        (p.get("h1_count", 0) for p in good if p.get("url", "").rstrip("/") == base), 0)
    scan["avg_words"] = round(sum(p.get("words", 0) for p in good) / len(good), 1) if good else 0
    scan["avg_data_density"] = round(
        sum(p.get("data_density_per_100w", 0) for p in good) / len(good), 2) if good else 0.0
    scan["total_question_headings"] = sum(p.get("question_headings", 0) for p in good)
    scan["has_spec_table"] = any(p.get("table_count", 0) > 0 for p in good)
    scan["viewport"] = any(p.get("viewport") for p in good)
    # v1.1: soft-404 = HTTP 200 that renders a 404 page; dead nav links = pages
    # linked from the site that return a 404 template. Both waste crawl budget.
    scan["soft404_pages"] = [p["url"] for p in good if p.get("is_soft404")]
    scan["no_soft404"] = not scan["soft404_pages"] and not scan["sitemap_soft404"]
    scan["render_block_ok"] = sum(p.get("script_src_count", 0) for p in good[:1]) <= 3
    scan["script_src_count_home"] = (good[0].get("script_src_count", 0) if good else 0)

    home_txt_lower = strip_tags(home_html).lower()
    scan["has_faq_content"] = bool(
        re.search(r"\?\s", strip_tags(home_html)) or
        any("faq" in (p.get("url") or "").lower() for p in good))
    scan["faq_page_present"] = any(
        re.search(r"/faq|/questions", (p.get("url") or ""), re.I) for p in good)

    # --- hreflang (含协议缺失检测) ---
    hreflangs = re.findall(r'<link[^>]+hreflang=["\']([^"\']+)["\'][^>]*>', home_html, re.I)
    hreflang_hrefs = re.findall(r'<link[^>]+hreflang=["\']([^"\']+)["\'][^>]*href=["\']([^"\']*)["\']',
                                home_html, re.I)
    broken = [h for _, h in hreflang_hrefs if not h.startswith(("http://", "https://"))]
    scan["hreflang_count"] = len(hreflangs)
    scan["hreflang_langs"] = sorted(set(hreflangs))
    scan["hreflang_broken_hrefs"] = broken
    scan["hreflang_valid"] = bool(hreflangs) and not broken

    # --- NAP ---
    nap = extract_nap(home_html)
    # v1.1: scan ALL contact/about pages (not just the first) so competing
    # addresses on different pages are actually surfaced as conflicts.
    for p in good:
        if re.search(r"contact|about|company", p.get("url", ""), re.I):
            _, _, _, ch = fetch(p["url"], T)
            if ch:
                n2 = extract_nap(ch)
                for k in ("phones", "emails", "addresses"):
                    nap[k] = sorted(set(nap[k]) | set(n2[k]))
    # v1.1: de-duplicate addresses that share the same street token — they are
    # the same location written twice, not a real NAP conflict.
    def _street_key(a):
        m = re.search(r"(?:Road|Rd\.|Street|St\.|Avenue|Ave\.|Industrial Area)", a, re.I)
        return re.sub(r"\s+", "", a.lower())[:22] if not m else \
            re.sub(r"\s+", "", a[:m.start()].lower())[-16:]
    uniq_addrs, seen_keys = [], set()
    for a in nap["addresses"]:
        k = _street_key(a)
        if k not in seen_keys:
            seen_keys.add(k)
            uniq_addrs.append(a)
    nap["addresses"] = uniq_addrs
    scan["nap"] = nap
    scan["nap_conflicts"] = max(1, len(nap["addresses"]))

    # --- company name variants (from footer / title / headings / about page) ---
    # v1.1: harvest from home + about/contact pages, and normalise whitespace so
    # "Co.,Ltd" vs "Co., Ltd." don't inflate the count artificially.
    names = set()
    m = re.search(r"<title[^>]*>(.*?)</title>", home_html, re.S | re.I)
    if m:
        names.add(unescape(m.group(1)).split("–")[0].split("|")[0].strip())
    name_html = home_html
    for p in good:
        if re.search(r"about|contact|company", p.get("url", ""), re.I):
            _, _, _, nh = fetch(p["url"], T)
            if nh:
                name_html += nh
    for pat in (r"([A-Z][\w\s&.'-]{3,55}?\s+Co\.,?\s*Ltd\.?)",
                r"([A-Z][\w\s&.'-]{3,55}?\s+Co\.,?\s*Limited)",
                r"([A-Z][\w\s&.'-]{3,55}?\s+Machinery\s+Co\.[^,]{0,24})",
                r"([A-Z][\w\s&.'-]{3,40}?\s+(?:Machinery|Technology|Industrial)\b)"):
        for x in re.findall(pat, name_html)[:6]:
            names.add(re.sub(r"\s+", " ", unescape(x)).strip(" .,"))
    # merge near-duplicates: ignore punctuation / spacing / Ltd-vs-Limited
    def _nkey(n):
        s = re.sub(r"[^a-z0-9]", "", n.lower())
        return re.sub(r"(co(ltd)?(limited)?)$", "", s)
    uniq, nk = [], set()
    for n in sorted(names, key=len, reverse=True):
        k = _nkey(n)
        if len(k) > 3 and k not in nk:
            nk.add(k)
            uniq.append(n)
    scan["company_name_variants"] = uniq[:8]
    scan["name_variants"] = max(1, len(uniq))

    # --- mirrors ---
    mirrors = []
    if args.probe_mirrors:
        for tld in ("com", "net", "org", "cn", "eu"):
            d = f"{root_domain.split('.')[0]}.{tld}"
            # v1.1: treat both "host" and its bare (no-www) form as self
            if d == host or d == host.replace("www.", ""):
                mirrors.append({"domain": d, "status": "self", "same_title": True})
                continue
            o, s, hh, hb = fetch(f"https://{d}", 15)
            same = False
            if hb:
                t1 = (re.findall(r"<title[^>]*>(.*?)</title>", hb, re.S | re.I) or [""])[0]
                t0 = (re.findall(r"<title[^>]*>(.*?)</title>", home_html, re.S | re.I) or [""])[0]
                same = bool(t1) and t1.strip() == t0.strip()
            mirrors.append({"domain": d, "status": s, "same_title": same})
            print(f"  [mirror] {d} -> {s} same_title={same}", file=sys.stderr)
    # v1.1: distinguish TRUE mirrors (same <title>, i.e. duplicate content that
    # splits entity weight) from sibling sites (same brand, different content).
    # Only true mirrors should trigger the CAP-E1 entity-consistency cap.
    scan["mirror_domains"] = [m["domain"] for m in mirrors
                              if m.get("same_title") and m.get("status") != "self"]
    scan["sibling_domains"] = [m["domain"] for m in mirrors
                               if m.get("status") == 200 and not m.get("same_title")]
    # v1.1: mirror_domain_count INCLUDES the canonical host itself — the entity
    # risk is "N domains serving the same content", not "N-1 duplicates".
    # Without this, a 2-domain mirror reports count=1 and never trips CAP-E1.
    scan["mirror_domain_count"] = max(1, len([
        m for m in mirrors if m.get("same_title")]))
    scan["mirror_probe"] = mirrors

    # --- freshness (v1.1) ---
    # sitemap lastmod is unreliable: bulk-regenerated sitemaps stamp thousands
    # of URLs with one date. Prefer REAL publish dates found on blog/news pages.
    blog_dates = []
    for p in good:
        if not re.search(r"blog|news|article|insight|journal", p.get("url", ""), re.I):
            continue
        _, _, _, bh = fetch(p["url"], T)
        if not bh:
            continue
        for d in re.findall(r"(20\d{2})[-/年](\d{1,2})[-/月](\d{1,2})", bh):
            try:
                blog_dates.append(datetime(int(d[0]), int(d[1]), int(d[2])))
            except Exception:
                pass
        mt = re.findall(r'datetime=["\'](20\d{2}-\d{2}-\d{2})', bh)
        for d in mt:
            try:
                blog_dates.append(datetime.fromisoformat(d))
            except Exception:
                pass
    if blog_dates:
        newest = max(blog_dates)
        scan["content_freshness_days"] = (datetime.now() - newest).days
        scan["content_lastmod_newest"] = newest.date().isoformat()
        scan["freshness_source"] = "blog_publish_dates"
        scan["blog_date_samples"] = sorted({d.date().isoformat() for d in blog_dates})[-5:]
    else:
        mods = []
        for s in valid_maps:
            mods += [d for d, _ in s.get("lastmod_top", [])]
        if mods:
            try:
                newest = max(datetime.fromisoformat(d) for d in mods)
                scan["content_freshness_days"] = (datetime.now() - newest).days
                scan["content_lastmod_newest"] = newest.date().isoformat()
                scan["freshness_source"] = "sitemap_lastmod_unreliable"
            except Exception:
                scan["content_freshness_days"] = None
        else:
            scan["content_freshness_days"] = None

    # --- schema presence flags ---
    t = {x.lower() for x in scan["jsonld_types_all"]}
    scan["has_organization"] = "organization" in t
    scan["has_product_schema"] = bool(t & {"product", "itemlist"})
    scan["has_faqpage"] = "faqpage" in t
    scan["has_breadcrumb"] = "breadcrumblist" in t
    scan["has_person"] = "person" in t
    scan["has_article_schema"] = bool(t & {"article", "blogposting", "newsarticle"})
    scan["has_video_object"] = "videoobject" in t
    scan["has_og"] = scan["og_total"] > 0
    scan["has_jsonld"] = scan["jsonld_total"] > 0
    scan["has_altname"] = "alternatename" in home_txt_lower or "alternateName" in home_html
    scan["sameas_declared"] = "sameas" in home_txt_lower or "sameAs" in home_html
    scan["has_faq_schema"] = scan["has_faqpage"]
    scan["social_matrix"] = bool(re.search(
        r"linkedin\.com|facebook\.com|youtube\.com|twitter\.com|x\.com", home_html, re.I))
    scan["multimodal_assets"] = bool(re.search(
        r"youtube\.com|youtu\.be|<video", home_html, re.I))

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(scan, f, ensure_ascii=False, indent=2)

    print("\n[scan] summary", file=sys.stderr)
    for k in ("https", "sitemap_valid", "sitemap_urls", "jsonld_total", "og_total",
              "canonical_coverage", "h1_coverage", "homepage_h1", "hreflang_valid",
              "nap_conflicts", "name_variants", "avg_words", "avg_data_density",
              "content_freshness_days"):
        print(f"  {k}: {scan.get(k)}", file=sys.stderr)
    print(f"[scan] written -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
