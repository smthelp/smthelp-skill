#!/usr/bin/env python3
"""Build a single-file Southern Machinery product landing page.

usage: build_page.py <product_dir> [--out DIR]

<product_dir> holds:
  product.json   page config (file name, images, videos, catalogues, evidence labels, JSON-LD extras)
  blogs.json     8 English articles, each a list of 6 paragraphs
  i18n/<lang>.json  UI strings for en es pt fr ar ru zh (identical key sets; en is the source)
Section row counts (spec rows, open points, FAQ, study blocks ...) are read from the en keys,
so adding s18p/s18v/s18s or q9/a9 to every language file adds a row without touching this script.
"""
import json, re, sys, os, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "assets", "base")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args: sys.exit(__doc__)
PD = args[0]
OUTDIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else PD
P = json.load(open(os.path.join(PD, "product.json"), encoding="utf-8"))
BLOGS = json.load(open(os.path.join(PD, "blogs.json"), encoding="utf-8"))
LANGS = ["en", "es", "pt", "fr", "ar", "ru", "zh"]
I18N = {l: json.load(open(os.path.join(PD, "i18n", f"{l}.json"), encoding="utf-8")) for l in LANGS}
EN = I18N["en"]
FILE = P["file"]
URL = P.get("canonical_base", "https://www.smthelp.com/") + FILE
LOGO = P.get("logo", "https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png")
STORE = P.get("storage_prefix", re.sub(r"[^a-z0-9]", "", FILE.split("-smart")[0])[:20] + "_")
def count(pat): return len([k for k in EN if re.fullmatch(pat, k)])
N_SPEC, N_DISC, N_FAQ = count(r"s\d+p"), count(r"d\d+p"), count(r"q\d+")
N_STUDY, N_FC, N_MC = count(r"l\d+t"), count(r"fc\d+"), count(r"mc\d+")
N_TR, N_QF, N_M, N_SV = count(r"tr\d+"), count(r"qf\d+k"), count(r"m\d+v"), count(r"sv\d+t")

def t(k): return H.escape(EN[k])
def el(tag, k, attrs=""):
    return f'<{tag}{(" "+attrs) if attrs else ""} data-i18n="{k}">{t(k)}</{tag}>'

css = open(os.path.join(BASE, "base.css"), encoding="utf-8").read()
# drop the chatwoot holder block from the template css; we add our own below
css = css.replace(".woot-widget-holder", ".x-woot-old")
css += r"""
/* ===== page additions ===== */
.answer{background:var(--card);border:1px solid var(--line);border-inline-start:4px solid var(--brand);border-radius:var(--radius);padding:26px 28px;box-shadow:var(--shadow);display:grid;grid-template-columns:1.5fr 1fr;gap:30px}
.answer p{font-size:15.5px;color:var(--fg2);margin:0}
.answer dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:7px 14px;font-size:13.5px}
.answer dt{color:var(--fg3);font-weight:600}
.answer dd{margin:0;color:var(--fg)}
.answer h3{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--gold2);margin-bottom:12px}
.quote{margin-top:26px;font-size:clamp(18px,2.2vw,24px);font-weight:700;color:var(--brand);border-inline-start:4px solid var(--gold);padding-inline-start:16px}
.flow{display:flex;flex-wrap:wrap;align-items:stretch;gap:10px;margin-top:8px}
.flow .nd{flex:1 1 150px;background:var(--card);border:1px solid var(--line2);border-radius:12px;padding:14px;font-size:13.5px;font-weight:600;text-align:center;display:grid;place-items:center;position:relative}
.flow .nd.q{background:color-mix(in srgb,var(--gold) 16%,var(--card));border-color:var(--gold)}
.flow .ar{display:grid;place-items:center;color:var(--gold2);font-weight:800;font-size:18px}
html[dir=rtl] .flow .ar{transform:scaleX(-1)}
.flow .br{font-size:11.5px;color:var(--fg3);font-weight:500;display:block;margin-top:6px}
.diag{background:var(--bg2);border:1px dashed var(--line2);border-radius:var(--radius);padding:20px;margin-top:26px}
.diag h3{font-size:15px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.study{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:28px}
.study .b{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--brand);border-radius:12px;padding:16px}
.study h4{font-size:14px;margin-bottom:8px;color:var(--brand)}
.study p{font-size:13px;color:var(--fg2);margin:0 0 10px}
.study .ck{font-size:12px;color:var(--fg3);border-top:1px dashed var(--line2);padding-top:8px;margin:0}
.ol{counter-reset:s;list-style:none;padding:0;margin:0}
.ol li{counter-increment:s;position:relative;padding:8px 0 8px 40px;font-size:14px;color:var(--fg2);border-bottom:1px solid var(--line)}
html[dir=rtl] .ol li{padding:8px 40px 8px 0}
.ol li:before{content:counter(s);position:absolute;inset-inline-start:0;top:7px;width:26px;height:26px;border-radius:50%;background:var(--brand);color:#fff;font-size:12.5px;font-weight:700;display:grid;place-items:center}
.ul2{margin:0;padding-inline-start:18px;font-size:14px;color:var(--fg2)}
.ul2 li{margin-bottom:7px}
.catgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:20px}
.catc{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;box-shadow:var(--shadow);display:flex;flex-direction:column}
.catc h3{font-size:15px;margin-bottom:6px}
.catc p{font-size:13px;color:var(--fg2);flex:1}
.catc .acts{display:flex;gap:8px;flex-wrap:wrap}
.catc button,.catc a.o{font:inherit;font-size:12.5px;font-weight:600;padding:7px 12px;border-radius:8px;border:1px solid var(--line2);background:var(--bg2);color:var(--brand);cursor:pointer}
.catc button.on{background:var(--brand);color:#fff;border-color:var(--brand)}
.viewer{border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--bg3);box-shadow:var(--shadow2)}
.viewer iframe{display:block;width:100%;height:640px;border:0;background:#fff}
@media(max-width:760px){.viewer iframe{height:460px}.study{grid-template-columns:1fr}.catgrid{grid-template-columns:1fr}.answer{grid-template-columns:1fr}}
@media(max-width:1040px) and (min-width:761px){.study{grid-template-columns:repeat(2,1fr)}.catgrid{grid-template-columns:repeat(2,1fr)}}
.fcta{background:linear-gradient(135deg,var(--gold),#f2c26a);color:#3a2606;border-radius:var(--radius);padding:28px 30px;margin-bottom:38px;display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.fcta h2{color:#3a2606;font-size:clamp(19px,2.3vw,25px);margin-bottom:6px}
.fcta p{color:#4d3510;margin:0;font-size:14.5px;max-width:62ch}
.fcta .acts{display:flex;gap:9px;flex-wrap:wrap}
.fcta a{display:inline-block;margin:0;background:#3a2606;color:#fff;padding:11px 16px;border-radius:10px;font-weight:600;font-size:13.5px}
.fcta a.l{background:rgba(255,255,255,.55);color:#3a2606}
.fcta a:hover{text-decoration:none;opacity:.9;color:#fff}
.fcta a.l:hover{color:#3a2606}
.woot-widget-holder,.woot--bubble-holder{position:fixed!important;bottom:20px!important;right:20px!important;left:auto!important;z-index:2147483000!important}
"""

def ev(kind):
    cls = {"v": "ev-v", "c": "ev-c", "t": "ev-t"}[kind]
    return f'<span class="ev {cls}" data-i18n="ev_{kind}">{t("ev_"+kind)}</span>'

# ---------------- gallery (product.json "gallery": [{"md":url,"full":url,"key":i18n key}]) ----------------
GAL = P["gallery"]
# A gallery entry may give "file" (path inside the product dir) instead of URLs: the photo is
# embedded once as a WebP data URI (max 900 px). Use it only for photos not yet on ph.smthelp.com.
def embed(path, px=900, q=62):
    import base64, io
    from PIL import Image
    im = Image.open(os.path.join(PD, path)).convert("RGB"); im.thumbnail((px, px))
    b = io.BytesIO(); im.save(b, "WEBP", quality=q)
    return "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
for g in GAL:
    if g.get("file"): g["md"], g["full"] = embed(g["file"], P.get("embed_px", 720), P.get("embed_q", 55)), ""
WEB = [g["full"] for g in GAL if g["full"].startswith("http")] or [LOGO]  # public URLs for SEO tags
gal = "".join(f'<figure data-full="{g["full"]}"><img src="{g["md"]}" alt="{t(g["key"])}" data-i18n-alt="{g["key"]}" loading="lazy" decoding="async" width="500" height="320"><figcaption data-i18n="{g["key"]}">{t(g["key"])}</figcaption></figure>' for g in GAL)
hero_imgs = [GAL[i] for i in P.get("hero", [0, 1, 2, 3, 4])]
hero = "".join(f'<img src="{g["md"]}" alt="{t(g["key"])}" data-i18n-alt="{g["key"]}"' + (' fetchpriority="high"' if i == 0 else ' loading="lazy" decoding="async"') + '>' for i, g in enumerate(hero_imgs))

# ---------------- videos ----------------
# A video is a YouTube id ("id") or, since 1.2.0, a self-hosted MP4 ("src": URL or path relative to
# the published HTML, e.g. "videos/x.mp4") with a "poster" photo inside the product dir (embedded).
def _vthumb(v):
    if v.get("src"): return embed(v["poster"], 480, 60) if v.get("poster") else LOGO
    return f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"
VIDEOS = [(v.get("id", ""), v["t"], v["d"], v["dur"], v.get("src", ""), _vthumb(v)) for v in P["videos"]]
# static fallback cards (runtime re-renders them per language)
vid_static = "".join(f'<article class="vid" data-vid="{i}" data-src="{sr}" tabindex="0" role="button"><div class="th"><img loading="lazy" decoding="async" src="{th}" alt="{t(a)}"><div class="pl"><i></i></div></div><div class="bd"><span class="dur">{d}</span><h3>{t(a)}</h3><p>{t(b)}</p></div></article>' for i, a, b, d, sr, th in VIDEOS)

# ---------------- catalogues ----------------
CATS = [(c["t"], c["d"], c["url"], c.get("type", "PDF")) for c in P["catalogs"]]
cats = "".join(f'<div class="catc"><span class="dur" style="font-family:JetBrains Mono,monospace;font-size:11px;color:var(--gold2)">{ty}</span><h3 data-i18n="{a}">{t(a)}</h3><p data-i18n="{b}">{t(b)}</p><div class="acts"><button type="button" class="pv{" on" if i==0 else ""}" data-src="{H.escape(u)}" data-i18n="cat_preview">{t("cat_preview")}</button><a class="o" href="{H.escape(u)}" target="_blank" rel="noopener" data-i18n="cat_open">{t("cat_open")}</a></div></div>' for i, (a, b, u, ty) in enumerate(CATS))

# ---------------- blog ----------------
posts = ""
for i, paras in enumerate(BLOGS, 1):
    body = "".join(f'<p class="step">{H.escape(p)}</p>' for p in paras)
    posts += (f'<details class="post" id="article-{i}"{" open" if i==1 else ""}><summary><span class="pt"><small>ARTICLE {i:02d}</small>'
              f'<span data-i18n="bl{i}t">{t(f"bl{i}t")}</span></span></summary><div class="pbody">'
              f'<p class="psum" data-i18n="bl{i}s">{t(f"bl{i}s")}</p><p class="enonly" data-i18n="blog_note">{t("blog_note")}</p>{body}</div></details>')

# ---------------- tables ----------------
SPEC_EV = {int(k): v for k, v in P["spec_evidence"].items()}  # "v" verified, "c" to be confirmed, "t" concept
spec_rows = "".join(f'<tr><th data-i18n="s{i}p">{t(f"s{i}p")}</th><td data-i18n="s{i}v">{t(f"s{i}v")}</td><td data-i18n="s{i}s">{t(f"s{i}s")}</td><td>{ev(SPEC_EV[i])}</td></tr>' for i in range(1, N_SPEC + 1))
# optional "disc_status" key: the table lists product versions rather than conflicts
DISC_ST = f'<span class="ev ev-v" data-i18n="disc_status">{t("disc_status")}</span>' if "disc_status" in EN else ev("c")
disc_rows = "".join(f'<tr><th data-i18n="d{i}p">{t(f"d{i}p")}</th><td data-i18n="d{i}a">{t(f"d{i}a")}</td><td data-i18n="d{i}b">{t(f"d{i}b")}</td><td data-i18n="d{i}c">{t(f"d{i}c")}</td><td>{DISC_ST}</td></tr>' for i in range(1, N_DISC + 1))
qf = "".join(f'<dt data-i18n="qf{i}k">{t(f"qf{i}k")}</dt><dd data-i18n="qf{i}v">{t(f"qf{i}v")}</dd>' for i in range(1, N_QF + 1))
faq = "".join(f'<details{" open" if i==1 else ""}><summary data-i18n="q{i}">{t(f"q{i}")}</summary><div class="ans" data-i18n="a{i}">{t(f"a{i}")}</div></details>' for i in range(1, N_FAQ + 1))
study = "".join(f'<div class="b"><h4 data-i18n="l{i}t">{t(f"l{i}t")}</h4><p data-i18n="l{i}d">{t(f"l{i}d")}</p><p class="ck" data-i18n="l{i}c">{t(f"l{i}c")}</p></div>' for i in range(1, N_STUDY + 1))
fc = "".join(f'<li data-i18n="fc{i}">{t(f"fc{i}")}</li>' for i in range(1, N_FC + 1))
mc = "".join(f'<li data-i18n="mc{i}">{t(f"mc{i}")}</li>' for i in range(2, N_MC + 1))

def card(n, t1, d1):
    return f'<div class="card"><div class="num">{n}</div><h3 data-i18n="{t1}">{t(t1)}</h3><p data-i18n="{d1}">{t(d1)}</p></div>'

def fitcard(i, img):
    if isinstance(img, int): img = GAL[img]["md"]  # 1.2.0: a gallery index reuses that photo
    lis = "".join(f'<li data-i18n="f{i}l{j}">{t(f"f{i}l{j}")}</li>' for j in range(1, 4))
    return (f'<div class="mach"><img src="{img}" alt="{t(f"f{i}t")}" data-i18n-alt="f{i}t" loading="lazy" decoding="async"><div class="mb"><span class="tag" data-i18n="f{i}tag">{t(f"f{i}tag")}</span>'
            f'<h3 data-i18n="f{i}t">{t(f"f{i}t")}</h3><p data-i18n="f{i}d">{t(f"f{i}d")}</p><ul>{lis}</ul><div class="role" data-i18n="f{i}r">{t(f"f{i}r")}</div></div></div>')

# calculator defaults: product.json "calc_defaults" = [count, share %, minutes, rate, upkeep minutes, upkeep rate, price]
CD = [str(x) for x in P.get("calc_defaults", ["120", "5", "30", "", "10", "", ""])]
def fld(id_, k, val="", hint=None):
    h = f'<div class="hint" data-i18n="{hint}">{t(hint)}</div>' if hint else ""
    return f'<div class="fld"><label for="{id_}" data-i18n="{k}">{t(k)}</label><input id="{id_}" type="number" min="0" step="any" inputmode="decimal" value="{val}">{h}</div>'

def rrow(k, id_):
    return f'<div class="r"><span data-i18n="{k}">{t(k)}</span><b id="{id_}">—</b></div>'

# ---------------- JSON-LD ----------------
ORG = {"@type": "Organization", "@id": "https://www.smthelp.com/#organization", "name": "Shenzhen Southern Machinery Sales and Service Co., Ltd.",
       "alternateName": "Southern Machinery", "url": "https://www.smthelp.com", "logo": LOGO, "email": "info@smthelp.com",
       "telephone": "+86-13602562576", "foundingDate": "2011",
       "address": {"@type": "PostalAddress", "addressLocality": "Shenzhen", "addressRegion": "Guangdong", "addressCountry": "CN"},
       "sameAs": ["https://www.linkedin.com/company/smtmachine", "https://cn.linkedin.com/in/smtsupplier", "https://twitter.com/smtspecialist",
                  "https://www.facebook.com/autoinsertion", "https://www.youtube.com/c/Smthelping"]}
props = [(EN[f"s{i}p"], EN[f"s{i}v"]) for i in P.get("ld_spec_rows", range(1, N_SPEC + 1))]
LD = {"@context": "https://schema.org", "@graph": [
    ORG,
    {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": EN["seo_title"], "description": EN["seo_desc"], "inLanguage": "en",
     "isPartOf": {"@type": "WebSite", "name": "Southern Machinery", "url": "https://www.smthelp.com"},
     "primaryImageOfPage": WEB[0],
     "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#answer .answer p", "h1"]}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Southern Machinery", "item": "https://www.smthelp.com"},
        {"@type": "ListItem", "position": 2, "name": P.get("breadcrumb_category", "SMT equipment"), "item": "https://www.smthelp.com"},
        {"@type": "ListItem", "position": 3, "name": P["product_name"], "item": URL}]},
    {"@type": "Product", "name": P["product_name"], "alternateName": P.get("alternate_names", []),
     "description": EN["ans_p"], "category": P.get("category", "SMT equipment"),
     "image": WEB[:6], "brand": {"@id": ORG["@id"]}, "manufacturer": {"@id": ORG["@id"]}, "url": URL,
     "additionalProperty": [{"@type": "PropertyValue", "name": a, "value": b} for a, b in props],
     "disambiguatingDescription": P.get("disambiguation", "")},
    {"@type": "HowTo", "name": P.get("howto_name", EN["learn_h2"]), "totalTime": P.get("howto_time", "PT30M"),
     "tool": [{"@type": "HowToTool", "name": n} for n in P.get("howto_tools", [P["product_name"]])],
     "step": [{"@type": "HowToStep", "position": i, "name": EN[f"l{i}t"].split(": ", 1)[-1], "text": EN[f"l{i}d"]} for i in range(1, N_STUDY + 1)]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": EN[f"q{i}"], "acceptedAnswer": {"@type": "Answer", "text": EN[f"a{i}"]}} for i in range(1, N_FAQ + 1)]},
    {"@type": "ItemList", "name": P["product_name"] + " videos", "itemListElement": [
        {"@type": "VideoObject", "position": n, "name": EN[a], "description": EN[b],
         "thumbnailUrl": (f"https://i.ytimg.com/vi/{i}/hqdefault.jpg" if i else (th if th.startswith("http") else LOGO)),
         "contentUrl": (f"https://www.youtube.com/watch?v={i}" if i else (sr if sr.startswith("http") else P["canonical_base"] + sr)),
         **({"embedUrl": f"https://www.youtube-nocookie.com/embed/{i}"} if i else {}), "uploadDate": P.get("video_upload_date", "2023-05-13")}
        for n, (i, a, b, d, sr, th) in enumerate(VIDEOS, 1)]},
    {"@type": "Blog", "name": EN["blog_h2"], "blogPost": [
        {"@type": "BlogPosting", "headline": EN[f"bl{i}t"], "description": EN[f"bl{i}s"], "url": f"{URL}#article-{i}",
         "author": {"@id": ORG["@id"]}, "publisher": {"@id": ORG["@id"]}, "datePublished": P.get("date_published", "2026-01-01"), "inLanguage": "en",
         "image": WEB[i % len(WEB)]} for i in range(1, len(BLOGS) + 1)]}
]}
for v in LD["@graph"][6]["itemListElement"]: v.pop("uploadDate")  # upload dates unknown

hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="{URL}{"" if l=="en" else "?lang="+l}">\n' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{URL}">'

RUNTIME = open(os.path.join(BASE, "runtime.js"), encoding="utf-8").read().replace("__STORE__", STORE)
RUNTIME = RUNTIME.replace("__I18N__", json.dumps(I18N, ensure_ascii=False)).replace("__VIDEOS__", json.dumps([{"id": i, "t": a, "d": b, "dur": d, "src": sr, "th": th} for i, a, b, d, sr, th in VIDEOS]))

CHAT = """window.chatwootSettings = {"position":"right","type":"standard","launcherTitle":"Southern Machinery Global Support"};
(function(d,t) {
  /* Protocol-adaptive: an http:// script on an https:// page is blocked as mixed content. */
  var BASE_URL=(location.protocol==="https:"?"https://":"http://")+"chat.smthelp.com";
  var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
  g.src=BASE_URL+"/packs/js/sdk.js";
  g.async = true;
  s.parentNode.insertBefore(g,s);
  g.onload=function(){
    window.chatwootSDK.run({
      websiteToken: 'saMcpgSupcmd1VQwytgPLfbK',
      baseUrl: BASE_URL
    })
  }
})(document,"script");"""

page = f"""<!DOCTYPE html>
<html lang="en" data-theme="light" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t("seo_title")}</title>
<script>(function(){{try{{var m=localStorage.getItem("{STORE}theme");if(!m&&window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches)m="dark";if(m==="dark")document.documentElement.setAttribute("data-theme","dark");}}catch(e){{}}}})();</script>
<meta name="description" content="{t("seo_desc")}">
<meta name="keywords" content="{t("seo_keys")}">
<meta name="author" content="Shenzhen Southern Machinery Sales and Service Co., Ltd.">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="theme-color" content="#0c665c">
<link rel="preconnect" href="https://i.ytimg.com">
<link rel="preconnect" href="https://ph.smthelp.com">
<link rel="canonical" href="{URL}">
{hreflang}
<meta property="og:type" content="product">
<meta property="og:site_name" content="Southern Machinery">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{t("og_title")}">
<meta property="og:description" content="{t("og_desc")}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{WEB[0]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@smtspecialist">
<meta name="twitter:title" content="{t("og_title")}">
<meta name="twitter:description" content="{t("og_desc")}">
<meta name="twitter:image" content="{WEB[0]}">
<script type="application/ld+json">{json.dumps(LD, ensure_ascii=False)}</script>
<style>{css}</style>
</head>
<body>
<div class="topbar"><div class="wrap"><span class="dot"></span>{el("span","topbar")}</div></div>
<header id="hdr">
  <div class="wrap hd">
    <a class="brand" href="#top">
      <img src="{LOGO}" alt="Southern Machinery" width="116" height="32">
      <span class="bs"><b>Southern Machinery</b>{el("span","brand_sub")}</span>
    </a>
    <nav class="mn" id="nav">
      <a href="#why" data-i18n="nav_why">{t("nav_why")}</a>
      <a href="#how" data-i18n="nav_how">{t("nav_how")}</a>
      <a href="#fit" data-i18n="nav_fit">{t("nav_fit")}</a>
      <a href="#spec" data-i18n="nav_spec">{t("nav_spec")}</a>
      <a href="#disclosure" data-i18n="nav_disc">{t("nav_disc")}</a>
      <a href="#learn" data-i18n="nav_learn">{t("nav_learn")}</a>
      <a href="#videos" data-i18n="nav_videos">{t("nav_videos")}</a>
      <a href="#blog" data-i18n="nav_blog">{t("nav_blog")}</a>
      <a href="#faq" data-i18n="nav_faq">{t("nav_faq")}</a>
      <a href="#contact" class="cta" data-i18n="nav_contact">{t("nav_contact")}</a>
    </nav>
    <div class="hctl">
      <button class="ibtn" id="themeBtn" type="button" aria-label="{t("aria_theme")}" data-i18n-aria="aria_theme" title="{t("aria_theme")}" data-i18n-title="aria_theme"><span id="themeIcon">☀</span></button>
      <div class="lw" id="langWrap">
        <button class="ibtn" id="langBtn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="{t("aria_lang")}" data-i18n-aria="aria_lang" title="{t("aria_lang")}" data-i18n-title="aria_lang"><span id="langIcon">EN</span></button>
        <div class="langmenu" id="langMenu" role="menu"></div>
      </div>
      <button class="ibtn burger" id="burger" type="button" aria-label="{t("aria_menu")}" data-i18n-aria="aria_menu"><span>☰</span></button>
    </div>
  </div>
</header>
<main>
<section class="hero" id="top">
  <div class="wrap">
    <div>
      {el("span","hero_badge",'class="badge"')}
      <h1><span data-i18n="hero_h1a">{t("hero_h1a")}</span><br><em data-i18n="hero_h1b">{t("hero_h1b")}</em></h1>
      {el("p","hero_sub",'class="sub"')}
      <div class="acts">
        <a class="btn btn-p" href="#contact" data-i18n="hero_cta1">{t("hero_cta1")}</a>
        <a class="btn btn-s" href="#spec" data-i18n="hero_cta2">{t("hero_cta2")}</a>
      </div>
    </div>
    <div class="heroimgs playing" id="heroImgs">{hero}</div>
  </div>
</section>
<div class="metrics"><div class="wrap">
  {"".join(f'<div class="m"><div class="v" dir="ltr">{t(f"m{i}v")}</div><div class="l" data-i18n="m{i}l">{t(f"m{i}l")}</div></div>' for i in range(1,N_M+1))}
</div></div>
<div class="trust"><div class="wrap">{"".join(el("span", f"tr{i}") for i in range(1,N_TR+1))}</div></div>

<section id="answer"><div class="wrap">
  {el("span","ans_kick",'class="kick"')}
  {el("h2","ans_h2",'class="sec"')}
  <div class="answer"><p data-i18n="ans_p">{t("ans_p")}</p><div>{el("h3","qf_h")}<dl>{qf}</dl></div></div>
</div></section>

<section id="why" class="alt"><div class="wrap">
  {el("span","why_kick",'class="kick"')}
  {el("h2","why_h2",'class="sec"')}
  {el("p","why_lead",'class="lead"')}
  <div class="grid g3">{card("01","w1t","w1d")}{card("02","w2t","w2d")}{card("03","w3t","w3d")}</div>
  {el("p","why_quote",'class="quote"')}
</div></section>

<section id="how"><div class="wrap">
  {el("span","how_kick",'class="kick"')}
  {el("h2","how_h2",'class="sec"')}
  {el("p","how_lead",'class="lead"')}
  <div class="evline">{ev("v")}</div>
  <div class="grid g4">{"".join(card(lbl, f"h{i}t", f"h{i}d") for i, lbl in enumerate(P.get("how_labels", ["01","02","03","04"]), 1))}</div>
  <div class="diag">
    <h3><span data-i18n="dg_title">{t("dg_title")}</span>{ev("t")}</h3>
    <div class="flow">
      <div class="nd" data-i18n="dg1">{t("dg1")}</div><div class="ar">→</div>
      <div class="nd" data-i18n="dg2">{t("dg2")}</div><div class="ar">→</div>
      <div class="nd" data-i18n="dg3">{t("dg3")}</div><div class="ar">→</div>
      <div class="nd q"><span><span data-i18n="dg4">{t("dg4")}</span><span class="br"><b data-i18n="dg_no">{t("dg_no")}</b> → <span data-i18n="dg5">{t("dg5")}</span></span></span></div><div class="ar">→</div>
      <div class="nd"><span><b data-i18n="dg_yes">{t("dg_yes")}</b> · <span data-i18n="dg6">{t("dg6")}</span></span></div>
    </div>
  </div>
</div></section>

<section id="fit" class="alt"><div class="wrap">
  {el("span","fit_kick",'class="kick"')}
  {el("h2","fit_h2",'class="sec"')}
  {el("p","fit_lead",'class="lead"')}
  <div class="grid g3">{"".join(fitcard(i, u) for i, u in enumerate(P["fit_images"], 1))}</div>
</div></section>

<section id="spec"><div class="wrap">
  {el("span","spec_kick",'class="kick"')}
  {el("h2","spec_h2",'class="sec"')}
  {el("p","spec_lead",'class="lead"')}
  <div class="tw"><table><thead><tr><th data-i18n="sh_p">{t("sh_p")}</th><th data-i18n="sh_v">{t("sh_v")}</th><th data-i18n="sh_s">{t("sh_s")}</th><th data-i18n="sh_e">{t("sh_e")}</th></tr></thead><tbody>{spec_rows}</tbody></table></div>
</div></section>

<section id="disclosure" class="alt"><div class="wrap">
  {el("span","disc_kick",'class="kick"')}
  {el("h2","disc_h2",'class="sec"')}
  {el("p","disc_lead",'class="lead"')}
  <div class="evline"><span class="ev {'ev-v' if 'disc_status' in EN else 'ev-c'}" data-i18n="disc_ev">{t("disc_ev")}</span></div>
  <div class="tw"><table class="t-wide"><thead><tr><th data-i18n="dh_p">{t("dh_p")}</th><th data-i18n="dh_a">{t("dh_a")}</th><th data-i18n="dh_b">{t("dh_b")}</th><th data-i18n="dh_c">{t("dh_c")}</th><th data-i18n="dh_s">{t("dh_s")}</th></tr></thead><tbody>{disc_rows}</tbody></table></div>
</div></section>

<section id="learn"><div class="wrap">
  {el("span","learn_kick",'class="kick"')}
  {el("h2","learn_h2",'class="sec"')}
  {el("p","learn_lead",'class="lead"')}
  <div class="study">{study}</div>
  <div class="grid g2">
    <div class="card"><h3 data-i18n="fc_h">{t("fc_h")}</h3><p data-i18n="fc_lead" style="margin-bottom:10px">{t("fc_lead")}</p><ol class="ol">{fc}</ol></div>
    <div class="card"><h3 data-i18n="mc_h">{t("mc_h")}</h3><div class="evline" style="margin:6px 0 12px">{ev("v")}</div><ul class="ul2">{mc}</ul></div>
  </div>
</div></section>

<section id="roi" class="alt"><div class="wrap">
  {el("span","roi_kick",'class="kick"')}
  {el("h2","roi_h2",'class="sec"')}
  {el("p","roi_lead",'class="lead"')}
  <div class="calc">
    <div class="ch"><h3 data-i18n="calc_h">{t("calc_h")}</h3><p data-i18n="calc_sub">{t("calc_sub")}</p></div>
    <div class="cb">
      <div>{fld("cFeeders","c_feeders",CD[0])}{fld("cShare","c_share",CD[1])}{fld("cMin","c_min",CD[2])}{fld("cRate","c_rate",CD[3])}{fld("cTech","c_tech",CD[4])}{fld("cTechRate","c_techrate",CD[5])}{fld("cPrice","c_price",CD[6],'c_hint_price')}</div>
      <div class="cres">{rrow("r_hours","rHours")}{rrow("r_value","rValue")}{rrow("r_cost","rCost")}{rrow("r_net","rNet")}
        <div class="big"><div class="k" data-i18n="r_pb">{t("r_pb")}</div><div class="v" id="rPayback">—</div><div class="u" id="rPaybackU"></div></div></div>
    </div>
    <div class="cf" data-i18n="calc_foot">{t("calc_foot")}</div>
  </div>
</div></section>

<section id="gallery"><div class="wrap">
  {el("span","gal_kick",'class="kick"')}
  {el("h2","gal_h2",'class="sec"')}
  {el("p","gal_lead",'class="lead"')}
  <div class="galgrid">{gal}</div>
</div></section>

<section id="videos" class="alt"><div class="wrap">
  {el("span","vid_kick",'class="kick"')}
  {el("h2","vid_h2",'class="sec"')}
  {el("p","vid_lead",'class="lead"')}
  <div class="vids" id="vidGrid">{vid_static}</div>
  <p style="margin-top:20px"><a href="https://file.autoinsertion.com/public/Southern-Machinery-YouTube-Video-Board.html" target="_blank" rel="noopener" data-i18n="vid_more">{t("vid_more")}</a></p>
</div></section>

<section id="catalog"><div class="wrap">
  {el("span","cat_kick",'class="kick"')}
  {el("h2","cat_h2",'class="sec"')}
  {el("p","cat_lead",'class="lead"')}
  <div class="catgrid" id="catGrid">{cats}</div>
  <div class="viewer"><iframe id="catFrame" title="{t("cat_frame")}" data-i18n-title="cat_frame" loading="lazy" data-src="{H.escape(CATS[0][2])}"></iframe></div>
  <p style="margin-top:16px"><a href="https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html" target="_blank" rel="noopener" data-i18n="cat_more">{t("cat_more")}</a></p>
</div></section>

<section id="blog" class="alt"><div class="wrap">
  {el("span","blog_kick",'class="kick"')}
  {el("h2","blog_h2",'class="sec"')}
  {el("p","blog_lead",'class="lead"')}
  <div class="posts">{posts}</div>
</div></section>

<section id="service"><div class="wrap">
  {el("span","svc_kick",'class="kick"')}
  {el("h2","svc_h2",'class="sec"')}
  <div class="svc">{"".join(f'<div class="s"><div class="ic">{ic}</div><h4 data-i18n="sv{i}t">{t(f"sv{i}t")}</h4><p data-i18n="sv{i}d">{t(f"sv{i}d")}</p></div>' for i, ic in zip(range(1,N_SV+1), P.get("service_icons", ["🎥","🧑‍🔧","⚙️","🏭"])))}</div>
</div></section>

<section id="faq" class="alt"><div class="wrap">
  {el("span","faq_kick",'class="kick"')}
  {el("h2","faq_h2",'class="sec"')}
  <div class="fqs">{faq}</div>
</div></section>

<section id="contact"><div class="wrap">
  {el("span","ct_kick",'class="kick"')}
  {el("h2","ct_h2",'class="sec"')}
  {el("p","ct_lead",'class="lead"')}
  <form id="qform" class="calc">
    <div class="ch"><h3 data-i18n="form_subject">{t("form_subject")}</h3><p data-i18n="form_note">{t("form_note")}</p></div>
    <div class="cb" style="grid-template-columns:1fr">
      <div class="grid g2" style="gap:14px">
        <div class="fld"><label for="fN" data-i18n="form_name">{t("form_name")}</label><input id="fN" type="text" autocomplete="name"></div>
        <div class="fld"><label for="fC" data-i18n="form_company">{t("form_company")}</label><input id="fC" type="text" autocomplete="organization"></div>
        <div class="fld"><label for="fE" data-i18n="form_email">{t("form_email")}</label><input id="fE" type="email" autocomplete="email" required></div>
        <div class="fld"><label for="fS" data-i18n="form_scope">{t("form_scope")}</label><input id="fS" type="text"></div>
      </div>
      <div class="fld"><label for="fT" data-i18n="form_msg">{t("form_msg")}</label><textarea id="fT" rows="5" style="width:100%;padding:11px 13px;border:1px solid var(--line2);border-radius:9px;background:var(--bg);color:var(--fg);font-size:14.5px"></textarea></div>
      <div class="acts" style="display:flex;gap:11px;flex-wrap:wrap">
        <button class="btn btn-p" type="submit" data-i18n="form_submit">{t("form_submit")}</button>
        <a class="btn btn-p" style="background:#25d366;color:#fff" href="https://wa.me/8613602562576" target="_blank" rel="noopener" data-i18n="wa_btn">{t("wa_btn")}</a>
        <a class="btn" style="border-color:var(--line2);color:var(--brand)" href="mailto:info@smthelp.com" data-i18n="mail_btn">{t("mail_btn")}</a>
      </div>
    </div>
  </form>
</div></section>
</main>

<footer>
  <div class="wrap">
    <div class="fcta">
      <div><h2 data-i18n="fcta_h">{t("fcta_h")}</h2><p data-i18n="fcta_p">{t("fcta_p")}</p></div>
      <div class="acts">
        <a href="mailto:info@smthelp.com?subject={H.escape(EN["form_subject"]).replace(" ","%20")}" data-i18n="fcta_b1">{t("fcta_b1")}</a>
        <a href="https://wa.me/8613602562576" target="_blank" rel="noopener" data-i18n="fcta_b2">{t("fcta_b2")}</a>
        <a class="l" href="https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html" target="_blank" rel="noopener" data-i18n="fcta_b3">{t("fcta_b3")}</a>
        <a class="l" href="https://ph.smthelp.com" target="_blank" rel="noopener" data-i18n="fcta_b4">{t("fcta_b4")}</a>
      </div>
    </div>
    <div class="fg">
      <div>
        <img class="fl" src="{LOGO}" alt="Southern Machinery" loading="lazy" decoding="async">
        <p data-i18n="foot_about">{t("foot_about")}</p>
        <h4 data-i18n="foot_follow" style="margin-top:16px">{t("foot_follow")}</h4>
        <div class="soc">
          <a href="https://www.linkedin.com/company/smtmachine" target="_blank" rel="noopener" data-i18n-title="soc_li_c" title="{t("soc_li_c")}" aria-label="{t("soc_li_c")}">in</a>
          <a href="https://cn.linkedin.com/in/smtsupplier" target="_blank" rel="noopener" data-i18n-title="soc_li_p" title="{t("soc_li_p")}" aria-label="{t("soc_li_p")}">Li</a>
          <a href="https://twitter.com/smtspecialist" target="_blank" rel="noopener" data-i18n-title="soc_tw" title="{t("soc_tw")}" aria-label="{t("soc_tw")}">X</a>
          <a href="https://www.facebook.com/autoinsertion" target="_blank" rel="noopener" data-i18n-title="soc_fb" title="{t("soc_fb")}" aria-label="{t("soc_fb")}">f</a>
          <a href="https://www.youtube.com/c/Smthelping" target="_blank" rel="noopener" data-i18n-title="soc_yt" title="{t("soc_yt")}" aria-label="{t("soc_yt")}">▶</a>
        </div>
      </div>
      <div>
        <h4 data-i18n="foot_h1">{t("foot_h1")}</h4>
        <a href="{CATS[0][2]}" target="_blank" rel="noopener" data-i18n="foot_l1">{t("foot_l1")}</a>
        <a href="{CATS[1][2]}" target="_blank" rel="noopener" data-i18n="foot_l2">{t("foot_l2")}</a>
        <a href="{CATS[4][2]}" target="_blank" rel="noopener" data-i18n="foot_l3">{t("foot_l3")}</a>
        <a href="{H.escape(CATS[3][2])}" target="_blank" rel="noopener" data-i18n="foot_l4">{t("foot_l4")}</a>
      </div>
      <div>
        <h4 data-i18n="foot_h2">{t("foot_h2")}</h4>
        <a href="https://file.autoinsertion.com" target="_blank" rel="noopener" data-i18n="foot_l5">{t("foot_l5")}</a>
        <a href="https://ph.smthelp.com" target="_blank" rel="noopener" data-i18n="foot_l6">{t("foot_l6")}</a>
        <a href="https://file.autoinsertion.com/public/Southern-Machinery-YouTube-Video-Board.html" target="_blank" rel="noopener" data-i18n="foot_l7">{t("foot_l7")}</a>
        <a href="https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html" target="_blank" rel="noopener" data-i18n="foot_l8">{t("foot_l8")}</a>
      </div>
      <div>
        <h4 data-i18n="foot_h3">{t("foot_h3")}</h4>
        <a href="mailto:info@smthelp.com" dir="ltr">info@smthelp.com</a>
        <a href="https://wa.me/8613602562576" target="_blank" rel="noopener" data-i18n="foot_wa">{t("foot_wa")}</a>
        <a href="tel:+8613602562576" dir="ltr">+86 13602562576</a>
        <a href="https://www.smthelp.com" target="_blank" rel="noopener" dir="ltr">www.smthelp.com</a>
        <a href="#contact" data-i18n="ct_addr">{t("ct_addr")}</a>
      </div>
    </div>
    <div class="bot"><p class="disc" data-i18n="foot_disc">{t("foot_disc")}</p><p class="disc mono" data-i18n="foot_rights" dir="ltr">{t("foot_rights")}</p></div>
  </div>
</footer>

<div class="modal" id="vModal" role="dialog" aria-modal="true" aria-label="{t("aria_video")}" data-i18n-aria="aria_video">
  <div class="inner">
    <button class="cl" id="vClose" type="button">✕</button>
    <iframe id="vFrame" title="YouTube video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    <video id="vPlayer" controls playsinline preload="none" style="display:none;width:100%;max-height:82vh;background:#000"></video>
  </div>
</div>
<div id="lb" role="dialog" aria-modal="true" aria-label="{t("aria_viewer")}" data-i18n-aria="aria_viewer"><button type="button" aria-label="{t("aria_close")}" data-i18n-aria="aria_close">✕</button><img alt="" data-i18n-alt="lb_alt"></div>

<a class="wafab" href="https://wa.me/8613602562576" target="_blank" rel="noopener" aria-label="{t("aria_wa")}" data-i18n-aria="aria_wa">
  <svg viewBox="0 0 32 32" width="26" height="26" fill="currentColor"><path d="M16 3C9.4 3 4 8.3 4 14.9c0 2.6.8 5 2.3 7L4 29l7.3-2.3c1.4.7 3 1.1 4.7 1.1 6.6 0 12-5.3 12-11.9C28 8.3 22.6 3 16 3zm0 21.8c-1.5 0-3-.4-4.3-1.1l-.3-.2-4.3 1.4 1.4-4.2-.2-.3a9.6 9.6 0 0 1-1.7-5.4c0-5.3 4.3-9.6 9.4-9.6s9.4 4.3 9.4 9.6-4.3 9.6-9.4 9.6zm5.2-7c-.3-.1-1.7-.9-2-1s-.5-.1-.7.1c-.2.3-.8 1-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5s0-.4 0-.5c-.1-.2-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.3 5.2 4.6.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3z"/></svg>
</a>

<script>{RUNTIME}</script>
<script>{CHAT}</script>
</body>
</html>
"""
os.makedirs(OUTDIR, exist_ok=True)
open(os.path.join(OUTDIR, FILE), "w", encoding="utf-8").write(page)
print(os.path.join(OUTDIR, FILE), len(page))
