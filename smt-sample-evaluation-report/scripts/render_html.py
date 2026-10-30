#!/usr/bin/env python3
"""Render a deck spec (deck-<lang>.json from make_spec.py) as ONE self-contained HTML report page.

usage: render_html.py <spec.json> <out.html> [--date YYYY-MM-DD]
- Same content as the PPTX (one <section> per slide; template after-sales/contact slides become the footer).
- Images embedded as base64 JPEG (max 1400 px) -> the file works offline / as an email attachment.
- SM page standard: logo top-left, dark/light toggle (localStorage), sticky contents menu, JSON-LD (Organization +
  Report), footer CTA (LinkedIn, Twitter, Facebook, YouTube, catalogue, photo library, info@smthelp.com, WhatsApp),
  Chatwoot widget bottom-right. Evidence tags: Estimate / Concept view / To be confirmed from slide notes and text.
- Speaker notes (sources) are NOT published; they stay in the PPTX."""
import base64, datetime, html, io, json, os, re, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); SKILL = os.path.dirname(HERE)
LOGO = "https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png"
E = html.escape
NUM = re.compile(r"[+\-]?[\d,. %~]+")


def b64img(path, maxw=1400):
    if not path or not os.path.exists(path): return ""
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "s"


def tags(s, H):
    n = (s.get("notes") or "") + " " + json.dumps(s, ensure_ascii=False)
    t = ""
    if "Estimate" in n or "±5" in n: t += f' <span class="tag t">{E(H["estimate"])}</span>'
    if "Concept view" in n: t += f' <span class="tag c">{E(H["concept"])}</span>'
    return t


def table(rows, num=True):
    h = "<div class='tbl'><table><thead><tr>" + "".join(f"<th>{E(str(c))}</th>" for c in rows[0]) + "</tr></thead><tbody>"
    for r in rows[1:]:
        h += "<tr>" + "".join(("<td class=n>" if num and NUM.fullmatch(str(c).strip()) else "<td>") + E(str(c)) + "</td>" for c in r) + "</tr>"
    return h + "</tbody></table></div>"


def fig(src, cap="", cls=""):
    u = b64img(src)
    return f"<figure class='{cls}'><img src='{u}' alt='{E(cap)}' loading='lazy'>" + (f"<figcaption>{E(cap)}</figcaption>" if cap else "") + "</figure>" if u else ""


def main():
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    spec = json.load(open(a[0], encoding="utf-8")); out = a[1]
    date = a[a.index("--date") + 1] if "--date" in a else datetime.date.today().isoformat()
    lang = spec.get("lang", "en")
    T = json.load(open(os.path.join(SKILL, "assets", "i18n", "en.json"), encoding="utf-8"))
    if lang != "en" and os.path.exists(os.path.join(SKILL, "assets", "i18n", lang + ".json")):
        T.update(json.load(open(os.path.join(SKILL, "assets", "i18n", lang + ".json"), encoding="utf-8")))
    H = T["html"]
    secs, nav, desc = [], [], ""
    for i, s in enumerate(spec["slides"]):
        t = s["type"]; sid = slug(s.get("kicker") or s.get("title", t)) + f"-{i}"
        if t == "cover":
            desc = s["subtitle"]
            ms = "".join(f"<div class='metric'><b>{E(m['v'])}</b><span>{E(m['l'])}</span></div>" for m in s["metrics"])
            secs.append(f"""<div class="hero" id="top"><div class="wrap grid"><div>
<div class="kicker">{E(s['kicker'])}</div><h1>{E(s['title'])}</h1><p class="lead">{E(s['subtitle'])}</p>
<div class="metrics">{ms}</div>
<div class="btns"><a class="btn p" href="#{slug(spec['slides'][-1].get('kicker','next'))}-{len(spec['slides'])-1}">{E(H['contact'])}</a><a class="btn s" href="https://wa.me/8613602562576">{E(H['whatsapp'])}</a></div>
</div><div>{fig(s.get('image'), '', 'heroimg')}</div></div></div>""")
            continue
        nav.append((sid, s["kicker"].split(" · ")[0] if t == "board" else (s.get("kicker") or s["title"])))
        head = f"<div class='k'>{E(s.get('kicker',''))}</div><h2>{E(s['title'])}{tags(s, H)}</h2>"
        if s.get("lead"): head += f"<p class='intro'>{E(s['lead'])}</p>"
        body = ""
        if t in ("steps", "cards"):
            items = s.get("steps") or s.get("cards")
            cs = "".join(f"<div class='card'><div class='ic'>{k+1}</div><h3>{E(c['h'])}</h3><p>{E(c['b'])}</p></div>" for k, c in enumerate(items))
            im = fig(s.get("image"), s.get("caption", ""), "side")
            body = f"<div class='two'><div class='stack'>{cs}</div>{im}</div>" if im else f"<div class='cards'>{cs}</div>"
        elif t == "table":
            body = table(s["rows"]) + (f"<p class='note'>{E(s['note'])}</p>" if s.get("note") else "")
        elif t == "metrics":
            ks = "".join(f"<div class='kpi'><b>{E(m['v'])}</b><span>{E(m['l'])}</span></div>" for m in s["metrics"])
            body = f"<div class='kpis'>{ks}</div>" + (f"<p class='note'>{E(s['text'])}</p>" if s.get("text") else "") + fig(s.get("image"), s.get("caption", ""), "wide")
        elif t == "board":
            ks = "".join(f"<div class='kpi'><b>{E(m['v'])}</b><span>{E(m['l'])}</span></div>" for m in s["metrics"])
            body = fig(s["image"], "", "board") + f"<div class='kpis six'>{ks}</div>" + (f"<p class='note'>{E(s['text'])}</p>" if s.get("text") else "")
        elif t == "bullets":
            li = "".join(f"<li>{E(b)}</li>" for b in s["bullets"])
            im = fig(s.get("image"), s.get("caption", ""), "side")
            body = f"<div class='two'><ul class='as'>{li}</ul>{im}</div>" if im else f"<ul class='as'>{li}</ul>"
        elif t == "gallery":
            body = "<div class='photos'>" + "".join(fig(g["src"], g.get("cap", "")) for g in s["images"]) + "</div>"
        elif t == "cta":
            cs = "".join(f"<div class='card'><div class='ic'>{k+1}</div><h3>{E(c['h'])}</h3><p>{E(c['b'])}</p></div>" for k, c in enumerate(s["facts"]))
            body = f"<div class='cards'>{cs}</div><div class='ctabar'><span>{E(s['text'])}</span><a class='btn p' href='mailto:info@smthelp.com?subject={E(spec['title'])}'>{E(H['email'])}</a><a class='btn p2' href='https://wa.me/8613602562576'>{E(H['whatsapp'])}</a></div>"
        secs.append(f"<section id='{sid}'><div class='wrap'>{head}{body}</div></section>")
    navh = "".join(f"<a href='#{i}'>{E(k)}</a>" for i, k in nav)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "name": "Southern Machinery", "url": "https://www.smthelp.com", "logo": LOGO, "email": "info@smthelp.com",
         "sameAs": ["https://www.linkedin.com/company/smtmachine", "https://twitter.com/smtspecialist", "https://www.facebook.com/autoinsertion", "https://www.youtube.com/c/Smthelping"]},
        {"@type": "Report", "name": spec["title"], "description": desc, "inLanguage": lang, "datePublished": date,
         "author": {"@type": "Organization", "name": "Southern Machinery"}}]}
    css = open(os.path.join(SKILL, "assets", "html", "report.css"), encoding="utf-8").read()
    gen = H["generated"].format(date=date, ver=spec.get("skill_version", "?"))
    page = f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(spec['title'])} | Southern Machinery</title><meta name="description" content="{E(desc)}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{css}</style></head><body>
<header class="top"><div class="wrap"><a href="#top"><img class="logo" src="{LOGO}" alt="Southern Machinery"></a>
<nav class="menu">{navh}</nav><div class="ctrl"><button id="th" title="{E(H['theme'])}">◐</button><button onclick="print()" title="PDF">⎙</button></div></div></header>
{''.join(secs)}
<footer><div class="wrap"><div class="grid">
<div><img src="{LOGO}" alt="Southern Machinery"><p>{E(H['f_about'])}</p>
<div class="soc"><a href="https://www.linkedin.com/company/smtmachine">LinkedIn</a><a href="https://cn.linkedin.com/in/smtsupplier">LinkedIn Profile</a><a href="https://twitter.com/smtspecialist">Twitter</a><a href="https://www.facebook.com/autoinsertion">Facebook</a><a href="https://www.youtube.com/c/Smthelping">YouTube</a></div></div>
<div><p><a href="https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html">{E(H['f_cat'])}</a></p><p><a href="https://ph.smthelp.com">{E(H['f_ph'])}</a></p></div>
<div><p><a href="mailto:info@smthelp.com">info@smthelp.com</a></p><p><a href="https://wa.me/8613602562576">WhatsApp +86 136 0256 2576</a></p></div>
</div><p class="disc">{E(T.get('a_disclaimer',''))}<br>{E(gen)}</p></div></footer>
<script>(function(){{var r=document.documentElement,k='sm-theme',v=localStorage.getItem(k);if(v)r.dataset.theme=v;
document.getElementById('th').onclick=function(){{r.dataset.theme=r.dataset.theme==='dark'?'light':'dark';localStorage.setItem(k,r.dataset.theme)}};}})();</script>
<script>window.chatwootSettings={{"position":"right","type":"standard","launcherTitle":"Southern Machinery Global Support"}};
(function(d,t){{var BASE_URL=(location.protocol==="https:"?"https://":"http://")+"chat.smthelp.com";var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
g.src=BASE_URL+"/packs/js/sdk.js";g.async=true;s.parentNode.insertBefore(g,s);g.onload=function(){{window.chatwootSDK.run({{websiteToken:'saMcpgSupcmd1VQwytgPLfbK',baseUrl:BASE_URL}})}}}})(document,"script");</script>
</body></html>"""
    open(out, "w", encoding="utf-8").write(page)
    print(f"html {len(page)//1024} KB, {len(secs)} sections -> {out}")


if __name__ == "__main__":
    main()
