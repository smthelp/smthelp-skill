"""Stage 10 - thumbnail: 1920x1080 JPEG = headline + badges + one frozen frame of the animation.
Config thumbnail: headline_html ('NO FLAT TOP?<br><span>GRIP IT.</span>', span = highlight colour),
badges [[text, bg, fg]], subline, anim_t (cycle time to freeze), anim_focus {x,y,s}, anim_opts {}."""
import html, json
from . import stage
from .landing import anim_js
from .video import ensure_logo
from ..brand import tokens, lighten
from ..config import SKILL_ROOT
from ..errors import P3VError
from .. import log


@stage("thumbnail", deps=[], desc="Render the YouTube thumbnail")
def run(cfg, state):
    t = cfg["thumbnail"]; b = cfg["brand"]
    if not t.get("headline_html"):
        raise P3VError("E_CONFIG", "thumbnail.headline_html is empty")
    page = (SKILL_ROOT / "templates" / "thumb.html").read_text(encoding="utf-8")
    tok = tokens(b); tok["__PDARK1__"] = b.get("dark_glow") or lighten(b["dark_bg"], .12)
    for k, v in tok.items():
        page = page.replace(k, v)
    badges = "".join(f'<div style="background:{x[1] if len(x) > 1 else "#ff6600"};color:{x[2] if len(x) > 2 else "#fff"}">'
                     f'{html.escape(x[0])}</div>' for x in t.get("badges", []))
    opts = {"t": t.get("anim_t", 0), "theme": "dark", "noBox": True, "noHud": True, "noLabels": True}
    if t.get("anim_focus"):
        opts["focus"] = t["anim_focus"]
    opts.update(t.get("anim_opts", {}))
    page = (page.replace("__ANIMJS__", anim_js(cfg)).replace("__GLOBAL__", json.dumps(cfg["anim"]["global"]))
                .replace("__OPTS__", json.dumps(opts)).replace("__LOGO__", ensure_logo(cfg).resolve().as_uri())
                .replace("__LABEL__", html.escape(b["bar_label"] or cfg["product_name"].upper()))
                .replace("__HEADLINE__", t["headline_html"]).replace("__BADGES__", badges)
                .replace("__SUBLINE__", html.escape(t.get("subline", ""))))
    src = cfg.p("build", "thumb.html"); src.write_text(page, encoding="utf-8")
    out = cfg.p("out", t.get("output") or f"youtube-thumbnail-{cfg.slug}.jpg")
    from playwright.sync_api import sync_playwright
    errs = []
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = br.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1.5)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(src.as_uri()); pg.wait_for_timeout(1500)
        pg.screenshot(path=str(out), type="jpeg", quality=90); br.close()
    if errs:
        raise P3VError("E_THUMB", "; ".join(errs))
    log.get("thumbnail").info("wrote %s", out.name)
    return {"thumbnail": str(out.relative_to(cfg.proj))}
