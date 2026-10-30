#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Playwright acceptance test for a page built by smt-source-to-landing-page.

Usage:
    python3 scripts/verify.py <page.html | https-url> [--config <product-dir>] [--shots <dir>] [--no-route]

Exit code 0 only when every hard check passes. Writes <shots>/verify_report.json and screenshots:
light/dark/ar x top/middle/spec/footer, mobile_en_top, mobile_ar_top and one image per section.

Hard checks: no JS page errors, no broken images, no empty src, no raw i18n keys (all languages),
no six-step brief words in headings (all languages), logo top-left (top-right in RTL), required
brand links, Chatwoot sdk script as last element before </body>, JSON-LD parses with the required
@types, canonical/OG/hreflang present, theme toggle persists both ways, all languages persist with
correct lang/dir after reload, Arabic is RTL, 390 px has no horizontal scroll (en and ar), no CDN
frameworks, reduced-motion and print CSS present, interactive parts work when present (FAB tabs,
video filter + click-to-load, lightbox, PDF preview, article expand, calculator).

Sandbox note: the sandbox browser cannot authenticate to the outbound proxy, so by default every
http(s) request is fetched by Python and handed to the browser (--no-route turns that off).
If Playwright or Chromium is missing: pip install playwright; then either
`python3 -m playwright install chromium` or `sudo apt-get install -y chromium` (arm64 sandboxes:
the Playwright CDN answers 403, apt works; the script then uses /usr/bin/chromium).
"""
import argparse, json, os, re, shutil, sys, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import BANNED, banned_hits, LANG_META, TPL  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("page")
ap.add_argument("--config", default=None, help="product folder (for languages, required links, section list)")
ap.add_argument("--shots", default="shots")
ap.add_argument("--no-route", action="store_true")
a = ap.parse_args()

from playwright.sync_api import sync_playwright  # noqa: E402

OUT = a.shots
os.makedirs(OUT, exist_ok=True)
URL = a.page if a.page.startswith("http") else "file://" + os.path.abspath(a.page)
RAW = open(a.page, encoding="utf-8").read() if not a.page.startswith("http") else urllib.request.urlopen(a.page, timeout=60).read().decode("utf-8")

brand = json.load(open(os.path.join(TPL, "brand-southern-machinery.json"), encoding="utf-8"))
cfg = {}
if a.config:
    cfg = json.load(open(os.path.join(a.config, "product.json"), encoding="utf-8"))
    if isinstance(cfg.get("brand"), dict):
        brand.update(cfg["brand"])
LANGS = cfg.get("languages", ["en", "es", "pt", "fr", "ar", "ru", "zh"])
NEED_LINKS = [s["url"] for s in brand["socials"]] + [brand["catalog_site"].rstrip("/") + "/", brand["photo_site"].rstrip("/") + "/",
                                                     "mailto:" + brand["email"], brand["whatsapp"]]
NEED_TYPES = ["Organization", "WebPage", "BreadcrumbList", "Product", "FAQPage", "ItemList", "DefinedTermSet"]

CACHE = {}


def proxy_route(route):
    url = route.request.url
    if not url.startswith("http") or "127.0.0.1" in url:
        return route.continue_()
    try:
        if url not in CACHE:
            r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux) Chrome/155 Safari/537.36", "Referer": "https://www.smthelp.com/"})
            with urllib.request.urlopen(r, timeout=25) as resp:
                CACHE[url] = (resp.status, dict(resp.headers), resp.read())
        st, hd, body = CACHE[url]
        hd = {k: v for k, v in hd.items() if k.lower() not in ("content-encoding", "transfer-encoding", "content-length", "connection")}
        route.fulfill(status=st, headers=hd, body=body)
    except urllib.error.HTTPError as e:
        route.fulfill(status=e.code, body=b"")
    except Exception:
        route.abort()


R = {"pageerrors": [], "console_errors": [], "http_errors": [], "checks": {}, "warnings": []}


def check(name, ok, detail=""):
    R["checks"][name] = {"ok": bool(ok), "detail": detail}


def warn(msg):
    R["warnings"].append(msg)


# ---------------------------------------------------------------- static checks on the HTML text
body_tail = RAW[RAW.rfind("</body>") - 1200:RAW.rfind("</body>")]
check("chatwoot_before_body_end", "/packs/js/sdk.js" in body_tail and "chatwootSDK.run" in body_tail and RAW.count("websiteToken") == 1)
check("chatwoot_https", 'BASE_URL="https://' in RAW)
ext_scripts = re.findall(r'<script[^>]+src="([^"]+)"', RAW)
ext_css = re.findall(r'<link[^>]+rel="stylesheet"[^>]*>', RAW)
check("no_cdn_frameworks", not ext_scripts and not ext_css and not re.search(r"tailwind|bootstrap(\.min)?\.(css|js)|jquery", RAW, re.I),
      {"scripts": ext_scripts, "css": ext_css})
check("reduced_motion_css", "prefers-reduced-motion" in RAW)
check("print_css", "@media print" in RAW)
check("canonical", bool(re.search(r'<link rel="canonical" href="https://[^"]+\.html">', RAW)))
check("og_tags", all(('property="og:%s"' % k) in RAW for k in ("title", "description", "url", "image", "type")))
n_hreflang = len(re.findall(r'hreflang="', RAW))
check("hreflang_all_plus_default", n_hreflang == len(LANGS) + 1 and 'hreflang="x-default"' in RAW, n_hreflang)
title = re.search(r"<title>(.*?)</title>", RAW, re.S).group(1)
desc = re.search(r'<meta name="description" content="([^"]*)"', RAW).group(1)
if len(title) > 75:
    warn("title is %d chars (aim <= 70)" % len(title))
if not 110 <= len(desc) <= 230:
    warn("meta description is %d chars (aim 140-200)" % len(desc))
if re.search(r'"uploadDate"', RAW):
    warn("VideoObject has uploadDate: confirm it came from a source, never invent it")

with sync_playwright() as p:
    exe = shutil.which("chromium") or shutil.which("chromium-browser")
    try:
        br = p.chromium.launch(args=["--no-sandbox"])
    except Exception:
        br = p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
    ctx = br.new_context(viewport={"width": 1366, "height": 860})
    if not a.no_route:
        ctx.route("**/*", proxy_route)
    pg = ctx.new_page()
    pg.set_default_navigation_timeout(90000)
    pg.on("pageerror", lambda e: R["pageerrors"].append(str(e)))
    pg.on("console", lambda m: R["console_errors"].append(m.text[:300]) if m.type == "error" else None)
    pg.on("response", lambda r: R["http_errors"].append("%d %s" % (r.status, r.url[:160])) if r.status >= 400 else None)
    pg.goto(URL, wait_until="domcontentloaded")
    pg.evaluate("localStorage.clear()")
    pg.goto(URL, wait_until="domcontentloaded")
    pg.wait_for_timeout(1500)
    pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
    h = pg.evaluate("document.body.scrollHeight")
    for y in range(0, h + 900, 700):
        pg.evaluate("window.scrollTo(0,%d)" % y)
        pg.wait_for_timeout(110)
    pg.wait_for_timeout(2500)
    has = lambda sel: pg.evaluate("!!document.querySelector(%s)" % json.dumps(sel))
    sections = pg.evaluate("[...document.querySelectorAll('main section[id]')].map(s=>s.id)")
    R["sections"] = sections

    broken = pg.evaluate("""[...document.images].filter(i=>i.getAttribute('src') && i.complete && i.naturalWidth===0).map(i=>i.src.slice(0,140))""")
    check("no_broken_images", not broken, broken)
    check("no_empty_src", pg.evaluate("""document.querySelectorAll('img[src=""],iframe[src=""]').length""") == 0)
    R["img_count"] = pg.evaluate("document.images.length")
    keys = pg.evaluate("Object.keys(I18N.en)")
    leak_js = """(keys)=>{const s=new Set(keys);return [...document.querySelectorAll('[data-i18n]')].filter(e=>s.has(e.textContent.trim())).map(e=>e.getAttribute('data-i18n'))}"""
    HEAD_JS = """[...document.querySelectorAll('h1,h2,h3,h4,.ptt,summary,title')].filter(e=>!e.closest('[hidden]')).map(e=>e.textContent)"""
    check("logo_top_left", pg.evaluate("""(()=>{const i=document.querySelector('.brand img');const r=i.getBoundingClientRect();return i.src.includes(%s)&&r.left<200&&r.top<120})()""" % json.dumps(brand["logo"].split("/")[-1])))
    hrefs = pg.evaluate("[...document.querySelectorAll('a')].map(a=>a.href)")
    miss = [n for n in NEED_LINKS if not any(hh == n or hh.startswith(n) for hh in hrefs)]
    check("required_links", not miss, miss)
    pg.wait_for_timeout(3000)
    R["chatwoot_sdk_loaded"] = pg.evaluate("!!window.chatwootSDK")
    if not R["chatwoot_sdk_loaded"]:
        warn("Chatwoot SDK did not load in the test browser (check chat.smthelp.com reachability / X-Frame-Options)")

    # interactions, only for sections that exist
    if has("#fab .ftab"):
        n = pg.evaluate("document.querySelectorAll('.ftab').length")
        last = "ft%d" % n
        pg.evaluate("document.getElementById('fab').scrollIntoView()")
        pg.click("#" + last)
        check("fab_tab", pg.evaluate("!document.getElementById('fp%d').hidden && document.getElementById('fp1').hidden" % n))
    if has("#videos .vid"):
        pg.evaluate("document.getElementById('videos').scrollIntoView()")
        f = pg.evaluate("[...document.querySelectorAll('.vchip')].map(c=>c.dataset.f).filter(x=>x!=='all').pop()")
        if f:
            want = pg.evaluate("document.querySelectorAll('.vid[data-cat=%s]').length" % json.dumps(f))
            pg.click(".vchip[data-f='%s']" % f)
            check("video_filter", pg.evaluate("[...document.querySelectorAll('.vid')].filter(v=>!v.hidden).length") == want)
            pg.click(".vchip[data-f='all']")
        pg.click(".vid .pl")
        pg.wait_for_timeout(800)
        check("video_click_to_load", pg.evaluate("document.querySelectorAll('.vid iframe').length===1 && document.querySelector('.vid iframe').src.includes('youtube-nocookie.com/embed/')"))
    if has(".galgrid figure"):
        pg.evaluate("document.getElementById('gallery').scrollIntoView()")
        pg.click(".galgrid figure >> nth=0")
        pg.wait_for_timeout(500)
        check("lightbox_open", pg.evaluate("document.getElementById('lb').classList.contains('open') && !!document.querySelector('#lb img').getAttribute('src')"))
        pg.keyboard.press("Escape")
        check("lightbox_close", pg.evaluate("!document.getElementById('lb').classList.contains('open') && !document.querySelector('#lb img').hasAttribute('src')"))
    if has("[data-pdf]"):
        pg.evaluate("document.getElementById('docs').scrollIntoView()")
        pg.click("[data-pdf] >> nth=0")
        pg.wait_for_timeout(800)
        check("pdf_preview", pg.evaluate("document.getElementById('pdfModal').classList.contains('open') && /\\.pdf/i.test(document.getElementById('pdfFrame').src)"))
        pg.keyboard.press("Escape")
    if has("#article-1"):
        n_posts = pg.evaluate("document.querySelectorAll('.post').length")
        want_posts = cfg.get("blog_count", 8)
        check("blog_count", n_posts == want_posts, "%d posts (want %d)" % (n_posts, want_posts))
        pg.evaluate("document.getElementById('article-1').open=true")
        check("blog_expand", pg.evaluate("document.querySelector('#article-1 .art:not([hidden])').offsetHeight>200"))
    if has("#matcherData"):
        # optional quick-match table (since 1.1.0): filters narrow the rows, reset restores them, search, detail + inquiry links
        pg.evaluate("document.getElementById('matcher').scrollIntoView()")
        rows = lambda: pg.evaluate("document.querySelectorAll('#mxBody tr').length")
        total = pg.evaluate("JSON.parse(document.getElementById('matcherData').textContent).rows.length")
        check("matcher_rows_rendered", rows() == total and total > 0, "%d rendered / %d in data" % (rows(), total))
        packs = pg.evaluate("[...document.querySelectorAll('#mxPack option')].map(o=>o.value).filter(Boolean)")
        counts = {}
        for pk in packs:
            pg.select_option("#mxPack", pk); counts[pk] = rows()
        pg.select_option("#mxPack", "")
        narrowed = [k for k, v in counts.items() if 0 < v < total]
        check("matcher_filter_reduces", bool(narrowed), counts)
        pg.select_option("#mxCat", index=1); n_cat = rows()
        pg.select_option("#mxPitch", index=2); n_both = rows()
        cnt = pg.evaluate("document.getElementById('mxCount').textContent")
        check("matcher_filters_combine", n_both <= n_cat < total and str(n_both) in cnt, {"cat": n_cat, "cat+pitch": n_both, "count_text": cnt})
        pg.click("#mxReset"); pg.wait_for_timeout(150)
        check("matcher_reset", rows() == total and pg.evaluate("document.getElementById('mxCat').value===''"), rows())
        first_word = pg.evaluate("(document.querySelector('#mxBody tr td b')||{}).textContent||''").split(" ")[0]
        pg.fill("#mxQ", first_word); pg.wait_for_timeout(150)
        c = rows()
        check("matcher_search", 0 < c <= total, {"q": first_word, "rows": c})
        pg.fill("#mxQ", "zzzqqqxx"); pg.wait_for_timeout(100)
        check("matcher_empty_state", rows() == 0 and pg.evaluate("!document.getElementById('mxEmpty').hidden"))
        pg.click("#mxReset")
        pg.click("#mxBody tr >> nth=0"); pg.wait_for_timeout(300)
        det = pg.evaluate("""(()=>{const m=document.getElementById('mxModal');const w=document.getElementById('mxWa');const e=document.getElementById('mxMail');
            return {open:m.classList.contains('open'),wa:w?w.href:'',mail:e?e.href:'',txt:document.getElementById('mxDetail').textContent.length}})()""")
        check("matcher_detail_inquiry", det["open"] and "wa.me" in det["wa"] and "text=" in det["wa"] and det["mail"].startswith("mailto:") and det["txt"] > 80,
              {k: (v[:90] if isinstance(v, str) else v) for k, v in det.items()})
        pg.keyboard.press("Escape")
        check("matcher_detail_close", pg.evaluate("!document.getElementById('mxModal').classList.contains('open')"))
        if has("#mxCheck"):
            pg.fill("#mxCL", "12"); pg.fill("#mxCW", "8"); pg.fill("#mxCH", "10"); pg.wait_for_timeout(150)
            check("matcher_check_part", pg.evaluate("document.getElementById('mxChkOut').textContent.trim().length>10"))
            for i in ("#mxCL", "#mxCW", "#mxCH"):
                pg.fill(i, "")
        R["matcher"] = {"rows": total, "per_packaging": counts}
    if has("#npiBox"):
        pg.evaluate("document.getElementById('npi').scrollIntoView()")
        n = pg.evaluate("document.querySelectorAll('.npi-tab').length")
        pg.click("#npiT%d" % n); pg.wait_for_timeout(150)
        ok1 = pg.evaluate("!document.getElementById('npiP%d').hidden && document.getElementById('npiP1').hidden" % n)
        pg.click("#npiT1"); before = pg.evaluate("document.getElementById('npiProg').textContent")
        pg.click("#npiP1 .npi-cb >> nth=0"); after = pg.evaluate("document.getElementById('npiProg').textContent")
        pg.click("#npiP1 .npi-next"); ok2 = pg.evaluate("!document.getElementById('npiP2').hidden")
        check("npi_stepper", ok1 and ok2 and before != after, {"last_tab": ok1, "next": ok2, "progress": [before, after]})
    if has("#calc .cres b"):
        check("calc", pg.evaluate("[...document.querySelectorAll('#calc .cres b')].every(b=>b.textContent.trim() && b.textContent.trim()!=='\u2014')"))
    ld = pg.evaluate("""(()=>{try{return JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent)['@graph'].map(x=>x['@type'])}catch(e){return null}})()""")
    check("jsonld_parses", ld is not None, ld)
    if has("#npiBox"):
        NEED_TYPES.append("HowTo")
    check("jsonld_types", ld is not None and all(t in ld for t in NEED_TYPES), [t for t in NEED_TYPES if not ld or t not in ld])
    check("geo_summary_and_faq", has("#summary .sump") and has(".sfacts") and (not "faq" in sections or has(".fqs .ans")))

    def shots(tag):
        pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
        pg.screenshot(path="%s/%s_top.png" % (OUT, tag))
        for sid, name in (("fab", "middle"), ("spec", "spec"), ("matcher", "matcher"), ("npi", "npi")):
            if has("#" + sid):
                pg.evaluate("document.getElementById('%s').scrollIntoView()" % sid); pg.wait_for_timeout(450)
                pg.screenshot(path="%s/%s_%s.png" % (OUT, tag, name))
        pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(500)
        pg.screenshot(path="%s/%s_footer.png" % (OUT, tag))

    # per-section screenshots (light, English)
    pg.goto(URL, wait_until="domcontentloaded"); pg.wait_for_timeout(1000)
    if pg.evaluate("document.documentElement.getAttribute('data-theme')") == "dark":
        pg.click("#themeBtn")
    pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
    for y in range(0, pg.evaluate("document.body.scrollHeight") + 900, 800):
        pg.evaluate("window.scrollTo(0,%d)" % y); pg.wait_for_timeout(90)
    pg.wait_for_timeout(1500)
    for sid in sections:
        if sid in ("top",):
            continue
        try:
            pg.locator("#" + sid).screenshot(path="%s/sec_%s.png" % (OUT, sid))
        except Exception as e:
            warn("section screenshot %s failed: %s" % (sid, str(e)[:80]))
    shots("light")

    # theme persistence both ways
    pg.click("#themeBtn"); pg.wait_for_timeout(200)
    pg.reload(wait_until="domcontentloaded"); pg.wait_for_timeout(1000)
    check("theme_dark_persists", pg.evaluate("document.documentElement.getAttribute('data-theme')") == "dark")
    shots("dark")
    pg.click("#themeBtn"); pg.reload(wait_until="domcontentloaded"); pg.wait_for_timeout(800)
    check("theme_light_persists", pg.evaluate("document.documentElement.getAttribute('data-theme')") == "light")

    # languages: switch, reload, check persistence, dir, translated text, raw keys, banned words
    en_h1 = pg.evaluate("document.querySelector('h1').textContent")
    langres, banned_all, leaks_all = {}, {}, {}
    order = [l for l in LANGS if l != "en"] + ["en"]
    for code in order:
        d = LANG_META[code][0]
        pg.evaluate("window.scrollTo(0,0)")
        pg.click("#langBtn"); pg.click("#langMenu button[data-lang='%s']" % code); pg.wait_for_timeout(300)
        pg.reload(wait_until="domcontentloaded"); pg.wait_for_timeout(900)
        st = pg.evaluate("""(()=>({lang:document.documentElement.lang,dir:document.documentElement.dir,h1:document.querySelector('h1').textContent,
           title:document.title, stored:localStorage.getItem(CFG.storage+'_lang')}))()""")
        leaks = pg.evaluate(leak_js, keys)
        heads = pg.evaluate(HEAD_JS)
        bad = sorted({w for x in heads for w in banned_hits(x)})
        fallback = pg.evaluate("""(()=>{const L=document.documentElement.lang; if(L==='en') return []; return Object.keys(I18N.en).filter(k=>!k.startsWith('__') && I18N[L][k]===undefined)})()""")
        if pg.evaluate("!!document.getElementById('matcherData')"):
            mxs = pg.evaluate("""(()=>({th:[...document.querySelectorAll('.mx-table thead th')].map(e=>e.textContent).join('|'),
               raw:(document.getElementById('matcher').innerText.match(/\\bmx_[a-z0-9_]+/g)||[]).slice(0,5)}))()""")
            langres.setdefault("_mx", {})[code] = mxs
            if mxs["raw"]:
                leaks = list(leaks) + mxs["raw"]
        ok = st["lang"] == code and st["dir"] == d and st["stored"] == code and (code == "en" or st["h1"] != en_h1)
        langres[code] = {"ok": ok, "state": st, "raw_key_leaks": leaks, "fallback_to_en_keys": fallback, "banned_in_headings": bad, "n_headings": len(heads)}
        if leaks:
            leaks_all[code] = leaks[:10]
        if bad:
            banned_all[code] = bad
        if code == "ar":
            check("rtl_logo_right", pg.evaluate("(()=>{const r=document.querySelector('.brand img').getBoundingClientRect();return r.left>window.innerWidth/2})()"))
            shots("ar")
    R["languages"] = langres
    mxl = langres.pop("_mx", None)
    if mxl:
        en_th = mxl.get("en", {}).get("th")
        check("matcher_labels_translated", all(v["th"] != en_th for k, v in mxl.items() if k != "en"), {k: v["th"][:60] for k, v in mxl.items()})
    check("all_languages_persist", all(v["ok"] for v in langres.values()), {k: v["state"] for k, v in langres.items() if not v["ok"]})
    check("no_raw_keys_any_language", not leaks_all, leaks_all)
    check("no_brief_words_in_headings_any_language", not banned_all, banned_all)
    if "ar" in LANGS:
        check("arabic_rtl", langres.get("ar", {}).get("state", {}).get("dir") == "rtl")

    # mobile 390 px: en and ar, top and full-page scroll width
    for code in ("en", "ar") if "ar" in LANGS else ("en",):
        mctx = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        if not a.no_route:
            mctx.route("**/*", proxy_route)
        mp = mctx.new_page()
        mp.goto(URL + ("" if code == "en" else ("&" if "?" in URL else "?") + "lang=" + code), wait_until="domcontentloaded")
        mp.wait_for_timeout(1500)
        mp.screenshot(path="%s/mobile_%s_top.png" % (OUT, code))
        sw = mp.evaluate("document.documentElement.scrollWidth")
        wide = mp.evaluate("""[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>window.innerWidth+1||r.left<-1)&&!e.closest('.tw,.ftabs,.vchips,.langmenu,#lb,.modal,.heroimgs,[hidden]')}).slice(0,8).map(e=>e.tagName+'.'+e.className)""")
        check("mobile_390_no_hscroll_" + code, sw <= 391, {"scrollWidth": sw, "overflowing": wide})
        if mp.evaluate("!!document.getElementById('matcherData')"):
            mp.evaluate("document.documentElement.style.scrollBehavior='auto';document.getElementById('matcher').scrollIntoView()"); mp.wait_for_timeout(400)
            mm = mp.evaluate("""(()=>{const s=document.getElementById('matcher');const tr=document.querySelector('#mxBody tr');
               const over=[...s.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>window.innerWidth+1||r.left<-1)&&!e.closest('[hidden],.modal')}).slice(0,6).map(e=>e.tagName+'.'+e.className);
               return {cards:tr?getComputedStyle(tr).display==='block':false, thead:getComputedStyle(document.querySelector('.mx-table thead')).display, over:over}})()""")
            mp.screenshot(path="%s/mobile_%s_matcher.png" % (OUT, code))
            check("matcher_mobile_cards_" + code, mm["cards"] and mm["thead"] == "none" and not mm["over"], mm)
        mctx.close()
    br.close()

R["pageerrors_count"] = len(R["pageerrors"])
check("no_js_page_errors", not R["pageerrors"], R["pageerrors"][:5])
failed = [k for k, v in R["checks"].items() if not v["ok"]]
R["passed"] = not failed
R["failed"] = failed
json.dump(R, open(os.path.join(OUT, "verify_report.json"), "w"), ensure_ascii=False, indent=1)
print("checks: %d passed, %d failed" % (len(R["checks"]) - len(failed), len(failed)))
for k, v in R["checks"].items():
    print(("  PASS " if v["ok"] else "  FAIL ") + k + ("" if v["ok"] else "  " + json.dumps(v["detail"], ensure_ascii=False)[:300]))
for w in R["warnings"]:
    print("  WARN " + w)
print("languages:", {k: (v["ok"], v["state"]["dir"], len(v["fallback_to_en_keys"])) for k, v in R["languages"].items()})
print("report:", os.path.join(OUT, "verify_report.json"))
sys.exit(0 if not failed else 1)
