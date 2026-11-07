"""Stage 6 - landing: insert the interactive "How it works" section (canvas animation + steps +
3D turntable + photo + value cards + CTA) into the existing landing page -> ONE self-contained HTML.

Inputs : src/<landing.base>.html, anim module JS, img/tt/v*.png, landing.section.photo_panel.image
Output : out/<landing.output or slug-landing-page-animated.html>
Config : landing.insert_before (exact HTML snippet to insert before; must exist once),
         landing.nav_after_href (e.g. "#models": a How-It-Works link is added after every nav link to it),
         landing.nav_after_text (optional: only links whose visible text contains this string)
         landing.replacements ([find, replace] or {find, replace, count}): rewrite the base page's own copy
           (title, meta, hero, specs, FAQ, JSON-LD) for a new model/variant; each must match exactly `count`
           times (default 1) or the stage fails, so a changed base page never ships half-rewritten.
         landing.forbid (strings that must not remain, e.g. the old model name): reported as `leftovers`.
"""
import base64, html, io, json, re, urllib.parse
from . import stage
from ..brand import tokens
from ..config import SKILL_ROOT
from ..errors import P3VError
from .. import log


def data_uri(path, width, q):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "WEBP", quality=q, method=6)
    return "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()


def anim_js(cfg):
    p = cfg.resolve(cfg["anim"]["module"])
    if not p or not p.exists():
        raise P3VError("E_ANIM", f"anim.module {cfg['anim']['module']} not found",
                       "start from templates/anim-template.js")
    return p.read_text(encoding="utf-8")


def fill_section(cfg, frames, photo_uri):
    s = cfg["landing"]["section"]; b = cfg["brand"]; e = html.escape
    tpl = (SKILL_ROOT / "templates" / "section.html").read_text(encoding="utf-8")
    tpl = tpl.split("-->", 1)[1]
    steps = s.get("steps") or []
    if not steps:
        raise P3VError("E_CONFIG", "landing.section.steps is empty (list of [name, description])")
    steps_html = "\n".join(f'     <li><div><b>{e(n)}</b><span>{e(d)}</span></div></li>' for n, d in steps)
    cards_html = "\n".join(f'   <div class="sr-card"><div class="k">{e(k)}</div><h4>{e(h)}</h4><p>{e(p)}</p></div>'
                           for k, h, p in s.get("cards", []))
    tt, ph, cta = s.get("tt_panel", {}), s.get("photo_panel", {}), s.get("cta", {})
    vals = {
        "eyebrow": s.get("eyebrow", "How it works"), "title": s.get("title", ""), "intro": s.get("intro", ""),
        "canvas_label": s.get("canvas_label", "Animated mechanism"), "step_count": str(len(steps)),
        "first_step": steps[0][0], "steps_html": steps_html, "cards_html": cards_html,
        "tt_title": tt.get("title", "3D model"), "tt_text": tt.get("text", ""), "tt_alt": tt.get("alt", "3D model"),
        "photo_title": ph.get("title", ""), "photo_text": ph.get("text", ""), "photo_alt": ph.get("alt", ""),
        "photo_fit": ph.get("fit", "cover"),
        "whatsapp": b["whatsapp"], "email": b["email"],
        "whatsapp_text": urllib.parse.quote(cta.get("whatsapp_text", "Hi, I am interested in " + cfg["product_name"])),
        "email_subject": urllib.parse.quote(cta.get("email_subject", cfg["product_name"] + " RFQ")),
        "whatsapp_label": cta.get("whatsapp_label", "Chat on WhatsApp"),
        "email_label": cta.get("email_label", "Email " + b["email"]),
    }
    for k, v in vals.items():
        raw = k.endswith("_html") or k in ("whatsapp_text", "email_subject", "step_count", "whatsapp")
        tpl = tpl.replace("{{" + k + "}}", v if raw else e(v))
    left = re.findall(r"\{\{(\w+)\}\}", tpl)
    if left:
        raise P3VError("E_ASSEMBLE", f"unfilled template tokens: {left}")
    for k, v in tokens(b).items():
        tpl = tpl.replace(k, v)
    tpl = (tpl.replace("__ANIMJS__", anim_js(cfg)).replace("__ANIMGLOBAL__", cfg["anim"]["global"])
              .replace("__FRAMES__", json.dumps(frames)).replace("__F0__", frames[0])
              .replace("__NF__", str(len(frames) - 1)).replace("__PHOTO__", photo_uri))
    return tpl


def apply_replacements(page, reps):
    for i, r in enumerate(reps):
        find, rep, cnt = (r[0], r[1], 1) if isinstance(r, (list, tuple)) else (r["find"], r["replace"], r.get("count", 1))
        n = page.count(find)
        if n != cnt:
            raise P3VError("E_ASSEMBLE", f"landing.replacements[{i}] matched {n}x (expected {cnt}): {find[:70]!r}",
                           "the base page changed or the snippet is not exact; copy it from src/<base>.html")
        page = page.replace(find, rep)
    return page


def leftovers(page, forbid):
    out = []
    for w in forbid or []:
        for m in re.finditer(re.escape(w), page):
            out.append(page[max(0, m.start() - 40):m.end() + 40].replace("\n", " "))
    return out


@stage("landing", deps=["download", "capture"], desc="Insert the animation section into the landing page")
def run(cfg, state):
    lg = log.get("landing"); L = cfg["landing"]
    base = cfg.p("src", f"{L['base']}.html")
    if not base.exists():
        raise P3VError("E_CONFIG", f"landing.base '{L['base']}' -> {base.name} not in src/", "run download first")
    page = base.read_text(encoding="utf-8").replace("\r\n", "\n")
    page = apply_replacements(page, L.get("replacements") or [])
    frames = [data_uri(f, 760, 60) for f in sorted(cfg.p("img", "tt", "x").parent.glob("v*.png"))]
    if len(frames) < 2:
        raise P3VError("E_STAGE_ORDER", "no turntable frames in img/tt/", "run capture")
    img = L["section"].get("photo_panel", {}).get("image")
    photo = data_uri(cfg.resolve(img), 900, 80) if img else frames[0]
    sec = fill_section(cfg, frames, photo)
    marker = L["insert_before"]
    if not marker or page.count(marker) != 1:
        raise P3VError("E_ASSEMBLE", f"insert_before marker found {page.count(marker or '#') if marker else 0}x (need exactly 1)",
                       "pick a unique snippet such as the next section's opening comment")
    page = page.replace(marker, sec + "\n" + marker, 1)
    n = 0
    if L.get("nav_after_href"):
        href = L["nav_after_href"]
        links = set(re.findall(r'<a [^>]*href="' + re.escape(href) + r'"[^>]*>.*?</a>', page, re.S))
        if L.get("nav_after_text"):  # only nav links whose label matches (skip hero buttons etc.)
            links = {m for m in links if L["nav_after_text"] in html.unescape(re.sub(r"<[^>]+>", "", m))}
        for m in links:
            new = re.sub(r'href="' + re.escape(href) + '"', 'href="#how-it-works"', m)
            new = re.sub(r'\sdata-i18n="[^"]*"', "", new)
            new = re.sub(r">(.*?)</a>$", ">" + L["nav_label"] + "</a>", new, flags=re.S)
            page = page.replace(m, m + "\n          " + new); n += 1
        if not n:
            lg.warning("no nav link with href=%s found; nav not updated", href)
    out = cfg.p("out", L.get("output") or f"{cfg.slug}-landing-page-animated.html")
    out.write_text(page, encoding="utf-8")
    left = leftovers(page, L.get("forbid"))
    for x in left[:10]:
        lg.warning("forbidden text left: ...%s...", x)
    lg.info("wrote %s (%d KB, nav links added: %d, leftovers: %d)", out.name, len(page) // 1024, n, len(left))
    return {"html": str(out.relative_to(cfg.proj)), "kb": len(page) // 1024, "nav_links": n, "leftovers": left}
