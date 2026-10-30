"""Stage 7 - video: build build/video_built.html from templates/video.html + product.json scenes,
then render preview PNGs (r/preview/<ar>_<t>.png) at the start + middle of every scene so the layout
can be checked BEFORE the slow 4K render. Image paths become absolute file:// URLs."""
import json, urllib.request
from pathlib import Path
from . import stage
from .landing import anim_js
from ..brand import tokens, rgba, lighten
from ..config import SKILL_ROOT
from ..errors import P3VError
from .. import log


def ensure_logo(cfg):
    logo = cfg.p("img", "logo.png")
    if not logo.exists():
        try:
            req = urllib.request.Request(cfg["brand"]["logo_url"], headers={"User-Agent": "Mozilla/5.0"})
            logo.write_bytes(urllib.request.urlopen(req, timeout=60).read())
        except Exception as e:
            log.get("video").warning("logo download failed (%s); brand bar shows text only", e)
    return logo


def build(cfg):
    b = cfg["brand"]
    tl = json.loads(cfg.p("vo", "timeline.json").read_text())
    cues = json.loads(cfg.p("vo", "cues.json").read_text())
    tt = [Path(f).resolve().as_uri() for f in sorted(cfg.p("img", "tt", "x").parent.glob("v*.png"))]
    scenes = []
    for sc in cfg["video"]["scenes"]:
        sc = dict(sc)
        if sc.get("photo"):
            sc["photo"] = cfg.resolve(sc["photo"]).resolve().as_uri()
        scenes.append(sc)
    if not scenes:
        raise P3VError("E_CONFIG", "video.scenes is empty")
    page = (SKILL_ROOT / "templates" / "video.html").read_text(encoding="utf-8")
    tok = tokens(b); tok.update({"__PD45__": rgba(b["primary_dark"], .45), "__P18__": rgba(b["primary"], .18),
                                 "__PDARK1__": b.get("dark_glow") or lighten(b["dark_bg"], .12)})
    for k, v in tok.items():
        page = page.replace(k, v)
    data = {"scenes": scenes, "anim_global": cfg["anim"]["global"]}
    page = (page.replace("__ANIMJS__", anim_js(cfg)).replace("__CFG__", json.dumps(data))
                .replace("__CUES__", json.dumps(cues)).replace("__TL__", json.dumps(tl))
                .replace("__TT__", json.dumps(tt)).replace("__LOGO__", ensure_logo(cfg).resolve().as_uri())
                .replace("__BARLABEL__", b["bar_label"] or cfg["product_name"].upper()))
    out = cfg.p("build", "video_built.html"); out.write_text(page, encoding="utf-8")
    return out, tl


def preview(cfg, html, tl, times=None, formats=None):
    from playwright.sync_api import sync_playwright
    lg = log.get("video"); errs = []
    if times is None:
        times = []
        sc = cfg["video"]["scenes"]
        for i, s in enumerate(sc):
            a = 0 if i == 0 else tl["segments"][s["from_segment"]]["start"]
            e = tl["segments"][sc[i + 1]["from_segment"]]["start"] if i + 1 < len(sc) else tl["total"]
            times += [round(a + 1.5, 1), round((a + e) / 2, 1)]
    outdir = cfg.p("r", "preview", "x").parent; shots = []
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--allow-file-access-from-files"])
        for ar in formats or cfg["video"]["formats"]:
            W, H = (1920, 1080) if ar == "169" else (1080, 1920)
            pg = br.new_page(viewport={"width": W, "height": H})
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(html.as_uri() + "?ar=" + ar); pg.wait_for_timeout(1500)
            for t in times:
                pg.evaluate(f"renderAt({t})"); pg.wait_for_timeout(150)
                f = outdir / f"{ar}_{t:06.1f}.png"; pg.screenshot(path=str(f)); shots.append(f)
            pg.close()
        br.close()
    if errs:
        raise P3VError("E_VIDEO_BUILD", "JS errors in video page: " + " | ".join(sorted(set(errs))[:3]))
    try:  # contact sheet for quick review
        from PIL import Image
        for ar in formats or cfg["video"]["formats"]:
            fs = sorted(outdir.glob(f"{ar}_*.png")); w, h = (480, 270) if ar == "169" else (180, 320)
            cols = 4 if ar == "169" else 8; rows = (len(fs) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * w, rows * h), "white")
            for i, f in enumerate(fs):
                sheet.paste(Image.open(f).convert("RGB").resize((w, h)), ((i % cols) * w, (i // cols) * h))
            sheet.save(outdir / f"sheet_{ar}.jpg", quality=85)
    except Exception as e:
        lg.warning("contact sheet failed: %s", e)
    lg.info("%d preview frames in r/preview (see sheet_169.jpg / sheet_916.jpg)", len(shots))
    return shots


@stage("video", deps=["subtitles", "capture"], desc="Build the video page and render preview frames")
def run(cfg, state):
    html, tl = build(cfg)
    shots = preview(cfg, html, tl)
    return {"page": str(html.relative_to(cfg.proj)), "previews": len(shots), "total_s": tl["total"]}
