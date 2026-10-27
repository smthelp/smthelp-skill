#!/usr/bin/env python3
"""Multilingual single-file HTML evaluation report page (EN default + ES, PT, FR, AR rtl, RU, ZH).

usage:
  render_web.py export <deck-en.json> <web_dir>            -> <web_dir>/strings_en.json (all texts to translate)
  render_web.py build  <deck-en.json> <web_dir> <out_dir>  -> <out_dir>/<page.json file>
web_dir holds: page.json (file name, videos, catalogues, extra gallery, blog/faq counts),
               web_en.json (SEO, quick answer, videos, catalogues, 8 blogs, FAQ, UI texts),
               i18n/<lang>.json (same keys as strings_en.json; missing keys fall back to English).
Page: SM logo, sticky menu, theme (dark/light) + language switch saved in localStorage (?lang= overrides),
Arabic rtl, report sections from the deck spec (numbers identical in every language), YouTube video
cards (modal player), catalogue viewer (iframe), 8 blogs (modal reader), FAQ, contact, footer socials,
Chatwoot bottom-right, JSON-LD (Organization, Report, FAQPage, VideoObject, BlogPosting, Breadcrumb).
Forbidden in every heading/title: hook, diagnosis, framework, vehicle, loop, CTA (checked at build)."""
import json, os, re, sys, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from render_html import b64img
LOGO = "https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png"
E = H.escape
LN = {"en": "English", "es": "Español", "pt": "Português", "fr": "Français", "ar": "العربية", "ru": "Русский", "zh": "中文"}
BAD = re.compile(r"\b(hook|diagnosis|framework|vehicle|loop|cta)\b|钩子|诊断|框架|载体|循环|行动号召", re.I)


def walk(spec):
    """Yield (key, text) for every visible text in the spec, in a fixed order."""
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
                if re.search(r"[A-Za-z]{3,}", str(cell)) and not re.fullmatch(r"(Board \d+|FS#\d|S-\d+\w*)", str(cell)): yield f"{p}_r{r}c{k}", str(cell)


def main():
    a = sys.argv[1:]
    if len(a) < 3: sys.exit(__doc__)
    mode, spec, wd = a[0], json.load(open(a[1], encoding="utf-8")), a[2]
    web = json.load(open(os.path.join(wd, "web_en.json"), encoding="utf-8"))
    EN = dict(walk(spec)); EN.update(web)
    if mode == "export":
        json.dump(EN, open(os.path.join(wd, "strings_en.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(len(EN), "strings ->", os.path.join(wd, "strings_en.json")); return
    out = a[3]; pg = json.load(open(os.path.join(wd, "page.json"), encoding="utf-8"))
    I18N = {"en": EN}
    for l in pg["langs"][1:]:
        fp = os.path.join(wd, "i18n", l + ".json")
        if os.path.exists(fp):
            d = json.load(open(fp, encoding="utf-8")); I18N[l] = {k: d[k] for k in EN if k in d and d[k]}
    errs = []
    for l, d in I18N.items():
        for k, v in d.items():
            if (k.endswith(("_title", "_kicker", "t")) or k.startswith(("bl", "ans_h2", "seo_title")) and k.endswith(("t", "h2", "title"))) and BAD.search(v) and not re.search(r"p\d+$", k):
                errs.append(f"forbidden word in {l}:{k}: {v[:60]}")
        miss = [k for k in EN if k not in d]
        if miss: print(f"warn {l}: {len(miss)} keys fall back to English")
    T = lambda k, tag="span", cls="": f"<{tag} data-k=\"{k}\"{' class=' + chr(34) + cls + chr(34) if cls else ''}>{E(EN[k])}</{tag}>"
    num = re.compile(r"[+\-]?[\d,. %~–]+")
    secs, nav = [], []
    sl = spec["slides"]
    # hero
    s0 = sl[0]
    ms = "".join(f"<div class='metric'><b>{E(m['v'])}</b>{T(f's0_m{j}')}</div>" for j, m in enumerate(s0["metrics"]))
    hero = f"""<div class="hero" id="top"><div class="wrap grid"><div>{T('s0_kicker','div','kicker')}{T('s0_title','h1')}{T('s0_subtitle','p','lead')}
<div class="metrics">{ms}</div><div class="btns"><a class="btn p" href="#contact">{T('ui_contact')}</a><a class="btn s" href="https://wa.me/8613602562576">{T('ui_whatsapp')}</a></div></div>
<figure class="heroimg"><img src="{b64img(s0.get('image'))}" alt="THT auto insertion line"></figure></div></div>"""
    # quick answer (GEO)
    qf = "".join(f"<tr><th>{T(f'qf{n}k')}</th><td>{T(f'qf{n}v')}</td></tr>" for n in range(1, 10) if f"qf{n}k" in EN)
    secs.append(f"<section id='answer' class='alt'><div class='wrap'>{T('ans_kick','div','k')}{T('ans_h2','h2')}<p class='geo'>{T('ans_p')}</p><div class='tbl facts'><table>{qf}</table></div></div></section>")
    nav.append(("answer", "nav_answer"))
    tagh = lambda s: (f" <span class='tag t' data-k='tag_est'>{E(EN['tag_est'])}</span>" if "±5" in json.dumps(s, ensure_ascii=False) or "Estimate" in (s.get("notes") or "") else "") + (f" <span class='tag c' data-k='tag_concept'>{E(EN['tag_concept'])}</span>" if "Concept view" in (s.get("notes") or "") else "")
    def cell(i, r, k, v):
        key = f"s{i}_r{r}c{k}"
        return f"<span data-k='{key}'>{E(v)}</span>" if key in EN else E(v)
    def fig(src, capk=None, cls="side"):
        u = b64img(src)
        return f"<figure class='{cls}'><img src='{u}' alt='' loading='lazy'>" + (f"<figcaption>{T(capk)}</figcaption>" if capk and capk in EN else "") + "</figure>" if u else ""
    for i, s in enumerate(sl[1:], 1):
        t = s["type"]; sid = f"r{i}"; p = f"s{i}"
        nav.append((sid, f"{p}_kicker"))
        head = T(f"{p}_kicker", "div", "k") + f"<h2>{T(f'{p}_title')}{tagh(s)}</h2>" + (T(f"{p}_lead", "p", "intro") if s.get("lead") else "")
        body = ""
        if t in ("steps", "cards", "cta"):
            f = "steps" if t == "steps" else ("cards" if t == "cards" else "facts")
            cs = "".join(f"<div class='card'><div class='ic'>{j+1}</div>{T(f'{p}_{f}{j}h','h3')}{T(f'{p}_{f}{j}b','p')}</div>" for j in range(len(s[f])))
            im = fig(s.get("image"), f"{p}_caption")
            body = f"<div class='two'><div class='stack'>{cs}</div>{im}</div>" if im else f"<div class='cards'>{cs}</div>"
            if t == "cta": body += f"<div class='ctabar'>{T(f'{p}_text')}<a class='btn p' href='mailto:info@smthelp.com'>{T('ui_email')}</a><a class='btn p2' href='https://wa.me/8613602562576'>{T('ui_whatsapp')}</a></div>"
        elif t == "table":
            rows = s["rows"]
            h_ = "<div class='tbl'><table><thead><tr>" + "".join(f"<th>{cell(i,0,k,c)}</th>" for k, c in enumerate(rows[0])) + "</tr></thead><tbody>"
            for r, row in enumerate(rows[1:], 1):
                h_ += "<tr>" + "".join(("<td class=n>" if num.fullmatch(str(c).strip()) else "<td>") + cell(i, r, k, str(c)) + "</td>" for k, c in enumerate(row)) + "</tr>"
            body = h_ + "</tbody></table></div>" + (f"<p class='note'>{T(f'{p}_note')}</p>" if s.get("note") else "")
        elif t in ("board", "metrics"):
            ks = "".join(f"<div class='kpi'><b>{E(m['v'])}</b>{T(f'{p}_m{j}')}</div>" for j, m in enumerate(s["metrics"]))
            body = fig(s.get("image"), None, "board") + f"<div class='kpis six'>{ks}</div>" + (f"<p class='note'>{T(f'{p}_text')}</p>" if s.get("text") else "")
        elif t == "bullets":
            li = "".join(f"<li>{T(f'{p}_b{j}')}</li>" for j in range(len(s["bullets"])))
            im = fig(s.get("image"), f"{p}_caption")
            body = f"<div class='two'><ul class='as'>{li}</ul>{im}</div>" if im else f"<ul class='as'>{li}</ul>"
        elif t == "gallery":
            gs = [(g["src"], f"{p}_g{j}", None) for j, g in enumerate(s["images"])]
            body = "<div class='photos'>" + "".join(f"<figure><img src='{b64img(src)}' alt='' loading='lazy'><figcaption>{T(k)}</figcaption></figure>" for src, k, _ in gs)
            body += "".join(f"<figure><a href='{g['full']}' target='_blank' rel='noopener'><img src='{g['url']}' alt='{E(EN[g['cap']])}' loading='lazy'></a><figcaption>{T(g['cap'])}</figcaption></figure>" for g in pg.get("extra_gallery", [])) + "</div>"
        secs.append(f"<section id='{sid}'{' class=alt' if i % 2 == 0 else ''}><div class='wrap'>{head}{body}</div></section>")
    # move CTA (last slide) after the extra sections
    cta = secs.pop(); ctanav = nav.pop()
    vids = "".join(f"<button class='vcard' data-yt='{v['id']}'><img src='https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg' alt='' loading='lazy'><span class='dur'>{v['dur']}</span><b data-k='{v['t']}'>{E(EN[v['t']])}</b><small data-k='{v['d']}'>{E(EN[v['d']])}</small></button>" for v in pg["videos"])
    secs.append(f"<section id='videos'><div class='wrap'>{T('vid_kick','div','k')}{T('vid_h2','h2')}{T('vid_lead','p','intro')}<div class='vgrid'>{vids}</div><p><a href='https://www.youtube.com/c/Smthelping' target='_blank' rel='noopener'>{T('vid_more')}</a></p></div></section>")
    cats = "".join(f"<div class='card doc'><span class='dt'>{c['type']}</span><h3 data-k='{c['t']}'>{E(EN[c['t']])}</h3><p data-k='{c['d']}'>{E(EN[c['d']])}</p><div class='dbtn'><button class='btn p2 sm' data-doc='{c['url']}'>{T('cat_view')}</button><a class='btn o sm' href='{c['url']}' target='_blank' rel='noopener'>{T('cat_open')}</a></div></div>" for c in pg["catalogs"])
    secs.append(f"<section id='docs' class='alt'><div class='wrap'>{T('cat_kick','div','k')}{T('cat_h2','h2')}{T('cat_lead','p','intro')}<div class='cards'>{cats}</div><div id='docview' hidden><div class='dvbar'><button class='btn o sm' id='docclose'>{T('cat_close')}</button></div><iframe id='docframe' title='catalogue' loading='lazy'></iframe></div></div></section>")
    bl = "".join(f"<button class='card blog' data-blog='{n}'><div class='ic'>{n}</div><h3 data-k='bl{n}t'>{E(EN[f'bl{n}t'])}</h3><p data-k='bl{n}s'>{E(EN[f'bl{n}s'])}</p><span class='more'>{T('blog_read')} →</span></button>" for n in range(1, pg["blogs"] + 1))
    arts = "".join(f"<article id='blog{n}' hidden><h2 data-k='bl{n}t'>{E(EN[f'bl{n}t'])}</h2>" + "".join(f"<p data-k='bl{n}p{j}'>{E(EN[f'bl{n}p{j}'])}</p>" for j in range(1, 7) if f"bl{n}p{j}" in EN) + "</article>" for n in range(1, pg["blogs"] + 1))
    secs.append(f"<section id='blog'><div class='wrap'>{T('blog_kick','div','k')}{T('blog_h2','h2')}{T('blog_lead','p','intro')}<div class='cards'>{bl}</div></div></section>")
    fq = "".join(f"<details><summary data-k='q{n}'>{E(EN[f'q{n}'])}</summary><p data-k='a{n}'>{E(EN[f'a{n}'])}</p></details>" for n in range(1, pg["faq"] + 1))
    secs.append(f"<section id='faq' class='alt'><div class='wrap'>{T('faq_kick','div','k')}{T('faq_h2','h2')}<div class='faq'>{fq}</div></div></section>")
    secs.append(cta.replace("<section id='r", "<section data-r='", 1).replace("data-r='", "id='contact' data-r='", 1))
    nav += [("videos", "nav_videos"), ("docs", "nav_docs"), ("blog", "nav_blog"), ("faq", "nav_faq"), ("contact", "nav_contact")]
    short = {"s1_kicker", "s2_kicker", "s3_kicker", f"s{len(sl)-4}_kicker"}
    navh = "".join(f"<a href='#{i}' data-k='{k}'>{E(EN[k])}</a>" for i, k in nav if k.startswith("nav_") or k in ("s1_kicker", "s3_kicker") or ("Feeder" in EN.get(k, "") or "balance" in EN.get(k, "")))
    url = pg["canonical_base"] + pg["file"]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": "https://www.smthelp.com/#org", "name": "Southern Machinery", "url": "https://www.smthelp.com", "logo": LOGO, "email": "info@smthelp.com", "telephone": "+86 136 0256 2576",
         "sameAs": ["https://www.linkedin.com/company/smtmachine", "https://twitter.com/smtspecialist", "https://www.facebook.com/autoinsertion", "https://www.youtube.com/c/Smthelping"]},
        {"@type": "Report", "name": EN["seo_title"], "description": EN["seo_desc"], "url": url, "inLanguage": pg["langs"], "datePublished": pg["date_published"],
         "author": {"@id": "https://www.smthelp.com/#org"}, "about": ["THT auto insertion line", "LED driver PCB assembly", "S-3010 radial insertion machine", "S-70DL odd-form insertion machine"], "abstract": EN["ans_p"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": EN[f"q{n}"], "acceptedAnswer": {"@type": "Answer", "text": EN[f"a{n}"]}} for n in range(1, pg["faq"] + 1)]},
        {"@type": "Blog", "name": EN["blog_h2"], "blogPost": [{"@type": "BlogPosting", "headline": EN[f"bl{n}t"], "description": EN[f"bl{n}s"], "datePublished": pg["date_published"], "author": {"@id": "https://www.smthelp.com/#org"}} for n in range(1, pg["blogs"] + 1)]},
        {"@type": "ItemList", "name": EN["vid_h2"], "itemListElement": [{"@type": "VideoObject", "position": k + 1, "name": EN[v["t"]], "description": EN[v["d"]], "thumbnailUrl": f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg", "embedUrl": f"https://www.youtube.com/embed/{v['id']}", "contentUrl": f"https://www.youtube.com/watch?v={v['id']}", "uploadDate": pg["date_published"]} for k, v in enumerate(pg["videos"])]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Southern Machinery", "item": "https://www.smthelp.com"}, {"@type": "ListItem", "position": 2, "name": "THT auto insertion solutions", "item": pg["canonical_base"]}, {"@type": "ListItem", "position": 3, "name": EN["s0_title"], "item": url}]}]}
    css = open(os.path.join(HERE, "..", "assets", "html", "report.css"), encoding="utf-8").read() + open(os.path.join(HERE, "..", "assets", "html", "web.css"), encoding="utf-8").read()
    js = open(os.path.join(HERE, "..", "assets", "html", "web.js"), encoding="utf-8").read()
    langs = "".join(f"<button data-lang='{l}'>{LN[l]}</button>" for l in pg["langs"])
    hreflang = "".join(f"<link rel='alternate' hreflang='{l}' href='{url}?lang={l}'>" for l in pg["langs"]) + f"<link rel='alternate' hreflang='x-default' href='{url}'>"
    page = f"""<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title data-k="seo_title">{E(EN['seo_title'])}</title>
<meta name="description" content="{E(EN['seo_desc'])}"><meta name="keywords" content="{E(EN['seo_keys'])}"><meta name="robots" content="index,follow">
<link rel="canonical" href="{url}">{hreflang}
<meta property="og:type" content="article"><meta property="og:title" content="{E(EN['seo_title'])}"><meta property="og:description" content="{E(EN['seo_desc'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{pg['extra_gallery'][0]['full'] if pg.get('extra_gallery') else LOGO}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#003142">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{css}</style></head><body>
<header class="top"><div class="wrap"><a href="#top"><img class="logo" src="{LOGO}" alt="Southern Machinery"></a>
<nav class="menu">{navh}</nav>
<div class="ctrl"><div class="lang"><button id="langBtn" aria-haspopup="true" title="{E(EN['ui_lang'])}">🌐 <span id="langCur">EN</span></button><div id="langMenu" hidden>{langs}</div></div>
<button id="th" data-kt="ui_theme" title="{E(EN['ui_theme'])}"><span id="themeIcon">☀</span></button><button onclick="print()" title="{E(EN['ui_print'])}">⎙</button></div></div></header>
{hero}
{''.join(secs)}
<div id="modal" hidden><div class="mbox"><button id="mclose" aria-label="close">×</button><div id="mbody"></div></div></div>
<div id="arts" hidden>{arts}</div>
<footer><div class="wrap"><div class="grid">
<div><img src="{LOGO}" alt="Southern Machinery"><p data-k="foot_about">{E(EN['foot_about'])}</p>
<div class="soc"><a href="https://www.linkedin.com/company/smtmachine" target="_blank" rel="noopener">LinkedIn</a><a href="https://cn.linkedin.com/in/smtsupplier" target="_blank" rel="noopener">LinkedIn Profile</a><a href="https://twitter.com/smtspecialist" target="_blank" rel="noopener">X / Twitter</a><a href="https://www.facebook.com/autoinsertion" target="_blank" rel="noopener">Facebook</a><a href="https://www.youtube.com/c/Smthelping" target="_blank" rel="noopener">YouTube</a></div></div>
<div><p><a href="https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html" target="_blank" rel="noopener" data-k="foot_cat">{E(EN['foot_cat'])}</a></p><p><a href="https://ph.smthelp.com" target="_blank" rel="noopener" data-k="foot_ph">{E(EN['foot_ph'])}</a></p></div>
<div><p><a href="mailto:info@smthelp.com">info@smthelp.com</a></p><p><a href="https://wa.me/8613602562576">WhatsApp +86 136 0256 2576</a></p></div>
</div><p class="disc">© 2026 <span data-k="foot_rights">{E(EN['foot_rights'])}</span></p></div></footer>
<script>var I18N={json.dumps(I18N, ensure_ascii=False)};var CFG={{prefix:"{pg['storage_prefix']}",langs:{json.dumps(pg['langs'])}}};</script>
<script>{js}</script>
<script>window.chatwootSettings={{"position":"right","type":"standard","launcherTitle":"Southern Machinery Global Support"}};
(function(d,t){{var BASE_URL=(location.protocol==="https:"?"https://":"http://")+"chat.smthelp.com";var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
g.src=BASE_URL+"/packs/js/sdk.js";g.async=true;s.parentNode.insertBefore(g,s);g.onload=function(){{window.chatwootSDK.run({{websiteToken:'saMcpgSupcmd1VQwytgPLfbK',baseUrl:BASE_URL}})}}}})(document,"script");</script>
</body></html>"""
    for e in errs: print("ERROR", e)
    os.makedirs(out, exist_ok=True); fp = os.path.join(out, pg["file"]); open(fp, "w", encoding="utf-8").write(page)
    print(f"web {len(page)//1024} KB, langs {list(I18N)} -> {fp}")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
