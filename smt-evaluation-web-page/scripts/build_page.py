#!/usr/bin/env python3
"""smt-evaluation-web-page: evaluation / solution result -> ONE multilingual, self-contained HTML file.

usage:
  build_page.py export <case_dir>            write <case_dir>/web/strings_en.json (every text to translate)
  build_page.py build  <case_dir> [out_dir]  write <out_dir or case_dir/out>/<page.json "file">

<case_dir> layout (see references/input-contract.md):
  report.json        report spec: slides[] (cover, steps, cards, table, metrics, bullets, gallery, cta)
  photos/            images referenced by report.json (relative paths), inlined as base64 at build
  web/page.json      page settings: file, langs, sections, nav_slides, palette/brand overrides, videos, catalogs, redact
  web/web_en.json    SEO, quick answer, video/catalogue texts, 8 blogs, FAQ (UI texts come from templates/ui)
  web/i18n/<l>.json  translations of strings_en.json (missing keys fall back to templates/ui/<l>.json, then English)
Exit code 1 when a heading/title contains a forbidden word or a redact term appears in the page."""
import base64, io, json, os, re, sys, urllib.request, html as H
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
E = H.escape


def meta_version():
    m = re.search(r"^version:\s*([\w.\-]+)", open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read(), re.M)
    return m.group(1) if m else "0"


def jload(p, default=None):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


def merge(a, b):
    out = dict(a)
    for k, v in (b or {}).items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def b64img(path, maxw=1400):
    if not path or not os.path.exists(path): return ""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def inline_logo(url):
    cache = os.path.join(ROOT, "assets", "logo-" + os.path.basename(url.split("?")[0]))
    try:
        if not os.path.exists(cache):
            urllib.request.urlretrieve(url, cache)
        ext = "png" if url.lower().endswith(".png") else "jpeg"
        return f"data:image/{ext};base64," + base64.b64encode(open(cache, "rb").read()).decode()
    except Exception:
        return url


KEEP = re.compile(r"(Board \d+|Module [A-Z]|FS#\d|S-?\d+\w*|SM-[A-Z0-9-]+|[A-Z0-9]{2,}-?\d+[A-Z0-9-]*)")


def walk(spec):
    """(key, text) for every visible text of the report spec, in a fixed order."""
    for i, s in enumerate(spec["slides"]):
        p = f"s{i}"
        for f in ("kicker", "title", "subtitle", "lead", "text", "note", "caption"):
            if s.get(f): yield f"{p}_{f}", s[f]
        for j, m in enumerate(s.get("metrics", [])): yield f"{p}_m{j}", m["l"]
        for f in ("steps", "cards", "facts"):
            for j, c in enumerate(s.get(f, [])): yield f"{p}_{f}{j}h", c["h"]; yield f"{p}_{f}{j}b", c["b"]
        for j, b in enumerate(s.get("bullets", [])): yield f"{p}_b{j}", b
        for j, g in enumerate(s.get("images", [])):
            if g.get("cap"): yield f"{p}_g{j}", g["cap"]
        for r, row in enumerate(s.get("rows", [])):
            for k, cell in enumerate(row):
                c = str(cell)
                if re.search(r"[A-Za-z]{3,}", c) and not KEEP.fullmatch(c): yield f"{p}_r{r}c{k}", c


def load_case(case):
    spec = jload(os.path.join(case, "report.json")) or jload(os.path.join(case, "deck-en.json"))
    if not spec: sys.exit("missing report.json in " + case)
    wd = os.path.join(case, "web")
    web = jload(os.path.join(wd, "web_en.json"), {})
    ui_en = jload(os.path.join(ROOT, "templates", "ui", "en.json"), {})
    EN = dict(walk(spec)); EN.update(web)
    return spec, wd, web, ui_en, EN


def tonum(v):
    m = re.search(r"-?\d[\d,]*\.?\d*", str(v))
    return float(m.group(0).replace(",", "")) if m else None


def main():
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in ("export", "build"): sys.exit(__doc__)
    case = os.path.abspath(a[1]); spec, wd, web, ui_en, EN = load_case(case)
    if a[0] == "export":
        json.dump(EN, open(os.path.join(wd, "strings_en.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(len(EN), "strings ->", os.path.join(wd, "strings_en.json")); return
    out = a[2] if len(a) > 2 else os.path.join(case, "out")
    pg = jload(os.path.join(wd, "page.json"))
    brand = merge(jload(os.path.join(ROOT, "config", "brand.json")), pg.get("brand"))
    pal = merge(brand["palette"], pg.get("palette"))
    langs = pg.get("langs", list(brand["langs"]))
    EN = {**ui_en, **EN}
    I18N = {"en": EN}
    for l in langs[1:]:
        ui = jload(os.path.join(ROOT, "templates", "ui", l + ".json"), {})
        d = {**ui, **jload(os.path.join(wd, "i18n", l + ".json"), {})}
        I18N[l] = {k: d[k] for k in EN if d.get(k)}
        miss = [k for k in EN if k not in I18N[l]]
        if miss: print(f"warn {l}: {len(miss)} keys fall back to English")
    bad = re.compile(r"\b(" + "|".join(w for w in brand["forbidden_title_words"] if w.isascii()) + r")\b|" + "|".join(w for w in brand["forbidden_title_words"] if not w.isascii()), re.I)
    errs = []
    for l, d in I18N.items():
        for k, v in d.items():
            heading = re.search(r"(_title|_kicker|_h2|^bl\d+t|^seo_title|^v\d+t|^cat\d+t|^s\d+_steps\d+h|^s\d+_cards\d+h)$", k)
            if heading and bad.search(v): errs.append(f"forbidden word in {l}:{k}: {v[:60]}")
    T = lambda k, tag="span", cls="": f"<{tag} data-k=\"{k}\"{' class=' + chr(34) + cls + chr(34) if cls else ''}>{E(EN.get(k, k))}</{tag}>"
    img = lambda p: b64img(os.path.join(case, p) if p and not os.path.isabs(p) else p)
    num = re.compile(r"[+\-]?[\d,. %~–]+")
    sl = spec["slides"]
    # hero
    s0 = sl[0]
    ms = "".join(f"<div class='metric'><b>{E(m['v'])}</b>{T(f's0_m{j}')}</div>" for j, m in enumerate(s0.get("metrics", [])))
    hero = f"""<div class="hero" id="top"><div class="wrap grid"><div>{T('s0_kicker','div','kicker')}{T('s0_title','h1')}{T('s0_subtitle','p','lead')}
<div class="metrics">{ms}</div><div class="btns"><a class="btn p" href="#contact">{T('ui_contact')}</a><a class="btn s" href="{brand['whatsapp']}">{T('ui_whatsapp')}</a></div></div>
<figure class="heroimg"><img src="{img(s0.get('image'))}" alt="{E(pg.get('hero_alt', EN['s0_title']))}"></figure></div></div>"""
    tagh = lambda s: (f" <span class='tag t' data-k='tag_est'>{E(EN['tag_est'])}</span>" if "Estimate" in (s.get("notes") or "") else "") + \
                     (f" <span class='tag c' data-k='tag_concept'>{E(EN['tag_concept'])}</span>" if "Concept view" in (s.get("notes") or "") else "") + \
                     (f" <span class='tag t' data-k='tag_tbc'>{E(EN['tag_tbc'])}</span>" if "To be confirmed" in (s.get("notes") or "") and "tag_tbc" in EN else "")

    def cell(i, r, k, v):
        key = f"s{i}_r{r}c{k}"
        return f"<span data-k='{key}'>{E(v)}</span>" if key in EN else E(v)

    def fig(src, capk=None, cls="side"):
        u = img(src)
        return f"<figure class='{cls}'><img src='{u}' alt='' loading='lazy'>" + (f"<figcaption>{T(capk)}</figcaption>" if capk and capk in EN else "") + "</figure>" if u else ""

    def bars(i, s):
        ch = s["chart"]; rows = s["rows"]; lc = ch.get("label_col", 0); cols = ch["cols"]
        vals = [[tonum(r[c]) for c in cols] for r in rows[1:]]
        mx = max((v for vs in vals for v in vs if v), default=1)
        h_ = "<div class='bars' role='img'>"
        for r, row in enumerate(rows[1:], 1):
            for n, c in enumerate(cols):
                v = vals[r - 1][n]
                if v is None: continue
                h_ += f"<div class='bar b{n+1}'><span>{cell(i, r, lc, str(row[lc]))}{' · ' + cell(i, 0, c, str(rows[0][c])) if len(cols) > 1 else ''}</span><div class='track'><div class='fill' style='width:{max(4, v / mx * 100):.1f}%'></div><span class='val'>{E(str(row[c]))}</span></div></div>"
        return h_ + "</div>"

    blocks = {}
    blocks["answer"] = ("nav_answer", f"<section id='answer' class='alt'><div class='wrap'>{T('ans_kick','div','k')}{T('ans_h2','h2')}<p class='geo'>{T('ans_p')}</p><div class='tbl facts'><table>" +
                        "".join(f"<tr><th>{T(f'qf{n}k')}</th><td>{T(f'qf{n}v')}</td></tr>" for n in range(1, 13) if f"qf{n}k" in EN) + "</table></div></div></section>")
    report, rnav = [], []
    last_cta = sl[-1]["type"] == "cta"
    for i, s in enumerate(sl[1:], 1):
        t = s["type"]; sid = f"r{i}"; p = f"s{i}"
        if t == "cta" and i == len(sl) - 1: sid = "contact"
        head = T(f"{p}_kicker", "div", "k") + f"<h2>{T(f'{p}_title')}{tagh(s)}</h2>" + (T(f"{p}_lead", "p", "intro") if s.get("lead") else "")
        body = ""
        if t in ("steps", "cards", "cta"):
            f = {"steps": "steps", "cards": "cards", "cta": "facts"}[t]
            cs = "".join(f"<div class='card'><div class='ic'>{j+1}</div>{T(f'{p}_{f}{j}h','h3')}{T(f'{p}_{f}{j}b','p')}</div>" for j in range(len(s.get(f, []))))
            im = fig(s.get("image"), f"{p}_caption")
            body = f"<div class='two'><div class='stack'>{cs}</div>{im}</div>" if im else f"<div class='cards'>{cs}</div>"
            if t == "cta": body += f"<div class='ctabar'>{T(f'{p}_text') if s.get('text') else ''}<a class='btn p' href='mailto:{brand['email']}'>{T('ui_email')}</a><a class='btn p2' href='{brand['whatsapp']}'>{T('ui_whatsapp')}</a></div>"
        elif t == "table":
            rows = s["rows"]; mode = (s.get("chart") or {}).get("mode", "table+bars") if s.get("chart") else "table"
            tb = "<div class='tbl'><table><thead><tr>" + "".join(f"<th scope='col'>{cell(i,0,k,c)}</th>" for k, c in enumerate(rows[0])) + "</tr></thead><tbody>"
            for r, row in enumerate(rows[1:], 1):
                tb += "<tr>" + "".join(("<td class=n>" if num.fullmatch(str(c).strip()) else "<td>") + cell(i, r, k, str(c)) + "</td>" for k, c in enumerate(row)) + "</tr>"
            tb += "</tbody></table></div>"
            body = (bars(i, s) if "bars" in mode else "") + (tb if "table" in mode else "") + (f"<p class='note'>{T(f'{p}_note')}</p>" if s.get("note") else "")
        elif t in ("board", "metrics"):
            ks = "".join(f"<div class='kpi'><b>{E(m['v'])}</b>{T(f'{p}_m{j}')}</div>" for j, m in enumerate(s["metrics"]))
            body = fig(s.get("image"), None, "board") + f"<div class='kpis six'>{ks}</div>" + (f"<p class='note'>{T(f'{p}_text')}</p>" if s.get("text") else "")
        elif t == "bullets":
            li = "".join(f"<li>{T(f'{p}_b{j}')}</li>" for j in range(len(s["bullets"])))
            im = fig(s.get("image"), f"{p}_caption")
            body = f"<div class='two'><ul class='as'>{li}</ul>{im}</div>" if im else f"<ul class='as'>{li}</ul>"
        elif t == "gallery":
            body = "<div class='photos'>" + "".join(f"<figure><img src='{img(g['src'])}' alt='{E(EN.get(f'{p}_g{j}', ''))}' loading='lazy'><figcaption>{T(f'{p}_g{j}')}</figcaption></figure>" for j, g in enumerate(s["images"]))
            body += "".join(f"<figure><a href='{g['full']}' target='_blank' rel='noopener'><img src='{g['url']}' alt='{E(EN[g['cap']])}' loading='lazy'></a><figcaption>{T(g['cap'])}</figcaption></figure>" for g in pg.get("extra_gallery", [])) + "</div>"
        html_ = f"<section id='{sid}'{' class=alt' if i % 2 == 0 else ''}><div class='wrap'>{head}{body}</div></section>"
        if sid == "contact": blocks["contact"] = ("nav_contact", html_)
        else: report.append(html_); rnav.append((sid, f"{p}_kicker"))
    if "contact" not in blocks and "ct_h2" in EN:
        blocks["contact"] = ("nav_contact", f"<section id='contact'><div class='wrap'>{T('ct_h2','h2')}<p class='intro' data-k='ct_p'>{E(EN.get('ct_p',''))}</p><div class='ctabar'><a class='btn p' href='mailto:{brand['email']}'>{T('ui_email')}</a><a class='btn p2' href='{brand['whatsapp']}'>{T('ui_whatsapp')}</a></div></div></section>")
    blocks["report"] = (None, "".join(report))
    vids = "".join(f"<button class='vcard' data-yt='{v['id']}'><img src='https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg' alt='' loading='lazy'>" + (f"<span class='dur'>{v['dur']}</span>" if v.get("dur") else "") + f"<b data-k='{v['t']}'>{E(EN[v['t']])}</b><small data-k='{v['d']}'>{E(EN[v['d']])}</small></button>" for v in pg.get("videos", []))
    blocks["videos"] = ("nav_videos", f"<section id='videos'><div class='wrap'>{T('vid_kick','div','k')}{T('vid_h2','h2')}{T('vid_lead','p','intro')}<div class='vgrid'>{vids}</div><p><a href='{brand['youtube_channel']}' target='_blank' rel='noopener'>{T('vid_more')}</a></p></div></section>") if vids else None
    cats = "".join(f"<div class='card doc'><span class='dt'>{c['type']}</span><h3 data-k='{c['t']}'>{E(EN[c['t']])}</h3><p data-k='{c['d']}'>{E(EN[c['d']])}</p><div class='dbtn'><button class='btn p2 sm' data-doc='{c['url']}'>{T('cat_view')}</button><a class='btn o sm' href='{c['url']}' target='_blank' rel='noopener'>{T('cat_open')}</a></div></div>" for c in pg.get("catalogs", []))
    blocks["docs"] = ("nav_docs", f"<section id='docs' class='alt'><div class='wrap'>{T('cat_kick','div','k')}{T('cat_h2','h2')}{T('cat_lead','p','intro')}<div class='cards'>{cats}</div><div id='docview' hidden><div class='dvbar'><button class='btn o sm' id='docclose'>{T('cat_close')}</button></div><iframe id='docframe' title='catalogue' loading='lazy'></iframe></div></div></section>") if cats else None
    nb = pg.get("blogs", 0)
    bl = "".join(f"<button class='card blog' data-blog='{n}'><div class='ic'>{n}</div><h3 data-k='bl{n}t'>{E(EN[f'bl{n}t'])}</h3><p data-k='bl{n}s'>{E(EN[f'bl{n}s'])}</p><span class='more'>{T('blog_read')} →</span></button>" for n in range(1, nb + 1))
    arts = "".join(f"<article id='blog{n}' hidden><h2 data-k='bl{n}t'>{E(EN[f'bl{n}t'])}</h2>" + "".join(f"<p data-k='bl{n}p{j}'>{E(EN[f'bl{n}p{j}'])}</p>" for j in range(1, 9) if f"bl{n}p{j}" in EN) + "</article>" for n in range(1, nb + 1))
    blocks["blog"] = ("nav_blog", f"<section id='blog'><div class='wrap'>{T('blog_kick','div','k')}{T('blog_h2','h2')}{T('blog_lead','p','intro')}<div class='cards'>{bl}</div></div></section>") if nb else None
    nf = pg.get("faq", 0)
    fq = "".join(f"<details><summary data-k='q{n}'>{E(EN[f'q{n}'])}</summary><p data-k='a{n}'>{E(EN[f'a{n}'])}</p></details>" for n in range(1, nf + 1))
    blocks["faq"] = ("nav_faq", f"<section id='faq' class='alt'><div class='wrap'>{T('faq_kick','div','k')}{T('faq_h2','h2')}<div class='faq'>{fq}</div></div></section>") if nf else None
    order = pg.get("sections", ["answer", "report", "videos", "docs", "blog", "faq", "contact"])
    secs, nav = [], []
    nav_slides = set(pg.get("nav_slides", [1, 2]))
    for b in order:
        blk = blocks.get(b)
        if not blk: continue
        if b == "report":
            nav += [(sid, k) for sid, k in rnav if int(sid[1:]) in nav_slides]
        elif blk[0]: nav.append((b if b != "contact" else "contact", blk[0]))
        secs.append(blk[1])
    navh = "".join(f"<a href='#{i}' data-k='{k}'>{E(EN[k])}</a>" for i, k in nav if k in EN)
    url = pg["canonical_base"] + pg["file"]
    org = brand["url"].rstrip("/") + "/#org"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": org, "name": brand["name"], "url": brand["url"], "logo": brand["logo_url"], "email": brand["email"], "telephone": brand["phone"], "sameAs": [u for _, u in brand["socials"]]},
        {"@type": "Report", "name": EN["seo_title"], "description": EN["seo_desc"], "url": url, "inLanguage": langs, "datePublished": pg.get("date_published", str(date.today())),
         "author": {"@id": org}, "about": pg.get("about", [EN["s0_title"]]), "abstract": EN.get("ans_p", "")}]}
    if nf: ld["@graph"].append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": EN[f"q{n}"], "acceptedAnswer": {"@type": "Answer", "text": EN[f"a{n}"]}} for n in range(1, nf + 1)]})
    if nb: ld["@graph"].append({"@type": "Blog", "name": EN["blog_h2"], "blogPost": [{"@type": "BlogPosting", "headline": EN[f"bl{n}t"], "description": EN[f"bl{n}s"], "author": {"@id": org}} for n in range(1, nb + 1)]})
    if pg.get("videos"): ld["@graph"].append({"@type": "ItemList", "name": EN["vid_h2"], "itemListElement": [{"@type": "VideoObject", "position": k + 1, "name": EN[v["t"]], "description": EN[v["d"]], "thumbnailUrl": f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg", "embedUrl": f"https://www.youtube.com/embed/{v['id']}", "contentUrl": f"https://www.youtube.com/watch?v={v['id']}", "uploadDate": pg.get("date_published", str(date.today()))} for k, v in enumerate(pg["videos"])]})
    ld["@graph"].append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": brand["name"], "item": brand["url"]}, {"@type": "ListItem", "position": 2, "name": pg.get("breadcrumb", "Solutions"), "item": pg["canonical_base"]}, {"@type": "ListItem", "position": 3, "name": EN["s0_title"], "item": url}]})
    palette = ":root{" + "".join(f"--{k}:{v};" for k, v in pal["light"].items()) + "}[data-theme=dark]{" + "".join(f"--{k}:{v};" for k, v in pal["dark"].items()) + "}"
    logo = inline_logo(brand["logo_url"]) if brand.get("logo_inline") else brand["logo_url"]
    cw = brand.get("chatwoot", {})
    chat = "" if not cw.get("enabled") else f"""<script>window.chatwootSettings={{"position":"right","type":"standard","launcherTitle":{json.dumps(cw['title'])}}};
(function(d,t){{if(location.protocol==="file:")return;var BASE_URL=(location.protocol==="https:"?"https://":"http://")+"{cw['host']}";var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
g.src=BASE_URL+"/packs/js/sdk.js";g.async=true;g.onerror=function(){{}};s.parentNode.insertBefore(g,s);g.onload=function(){{window.chatwootSDK.run({{websiteToken:'{cw['token']}',baseUrl:BASE_URL}})}}}})(document,"script");</script>"""
    tok = {
        "SEO_TITLE": E(EN["seo_title"]), "SEO_DESC": E(EN["seo_desc"]), "SEO_KEYS": E(EN.get("seo_keys", "")), "SKILL_VERSION": meta_version(), "URL": url,
        "HREFLANG": "".join(f"<link rel='alternate' hreflang='{l}' href='{url}?lang={l}'>" for l in langs) + f"<link rel='alternate' hreflang='x-default' href='{url}'>",
        "OG_IMAGE": pg.get("og_image", brand["logo_url"]), "THEME_COLOR": brand["theme_color"], "JSONLD": json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"),
        "PALETTE": palette, "CSS": open(os.path.join(ROOT, "templates", "page.css"), encoding="utf-8").read(),
        "LOGO": logo, "BRAND": E(brand["name"]), "NAV": navh, "UI_LANG": E(EN["ui_lang"]), "UI_THEME": E(EN["ui_theme"]), "UI_PRINT": E(EN["ui_print"]),
        "LANG_BUTTONS": "".join(f"<button data-lang='{l}'>{brand['langs'][l]}</button>" for l in langs),
        "HERO": hero, "SECTIONS": "\n".join(secs), "ARTICLES": arts,
        "FOOT_ABOUT": E(EN["foot_about"]), "FOOT_CAT": E(EN["foot_cat"]), "FOOT_PH": E(EN["foot_ph"]), "FOOT_RIGHTS": E(EN["foot_rights"]),
        "SOCIALS": "".join(f"<a href='{u}' target='_blank' rel='noopener'>{E(n)}</a>" for n, u in brand["socials"]),
        "CATALOG_BOARD": brand["catalog_board"], "PHOTO_SITE": brand["photo_site"], "EMAIL": brand["email"], "WHATSAPP": brand["whatsapp"], "PHONE": E(brand["phone"]),
        "YEAR": str(date.today().year), "I18N": json.dumps(I18N, ensure_ascii=False).replace("</", "<\\/"),
        "CFG": json.dumps({"prefix": pg.get("storage_prefix", "smtpage_"), "langs": langs, "rtl": brand.get("rtl", ["ar"])}),
        "JS": open(os.path.join(ROOT, "templates", "page.js"), encoding="utf-8").read(), "CHATWOOT": chat}
    tpl = open(os.path.join(ROOT, "templates", "page.html"), encoding="utf-8").read()
    page = re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: tok[m.group(1)], tpl)
    for term in pg.get("redact", []):
        if re.search(re.escape(term), re.sub(r"data:[^\"')]+", "", page), re.I): errs.append(f"redact term in page: {term}")
    for e in errs: print("ERROR", e)
    os.makedirs(out, exist_ok=True); fp = os.path.join(out, pg["file"]); open(fp, "w", encoding="utf-8").write(page)
    print(f"page {len(page)//1024} KB, langs {list(I18N)} -> {fp}")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
