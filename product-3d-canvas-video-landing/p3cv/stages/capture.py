"""Stage 2 - capture: turn a 3D viewer page into turntable frames img/tt/v00.png.. (white background,
4:3). Uses the adapter for the drawing's viewer kind. Drawings with "capture": true in sources are
captured; the first one becomes the turntable used by the landing page and video.
Fallback: put your own frames (photos, renders) in img/tt/ as v00.png... and set capture.enabled=false.
"""
import json
from . import stage
from ..adapters import ADAPTERS
from ..errors import P3VError
from .. import log

GL_ARGS = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]


def clean(raw, out, c):
    from PIL import Image
    x0, y0, x1, y1 = c["crop"]; mb = c["whiten"]["min_bright"]; mc = c["whiten"]["max_chroma"]
    im = Image.open(raw).convert("RGB")
    im = im.crop((x0, y0, min(x1, im.width), min(y1, im.height)))
    px = im.load(); W, H = im.size
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]; mx = max(r, g, b)
            if mx > mb and mx - min(r, g, b) < mc:
                px[x, y] = (255, 255, 255)
    aw, ah = (int(v) for v in c["aspect"].split(":"))
    nw = max(W, int(H * aw / ah)); canvas = Image.new("RGB", (nw, H), (255, 255, 255))
    canvas.paste(im, ((nw - W) // 2, 0)); canvas.save(out)


@stage("capture", deps=["download"], desc="Capture a 360 turntable from the 3D viewer into img/tt/")
def run(cfg, state):
    lg = log.get("capture"); c = cfg["capture"]
    tt = cfg.p("img", "tt", "x").parent
    if not c["enabled"]:
        n = len(list(tt.glob("v*.png")))
        if n < 2:
            raise P3VError("E_CAPTURE", "capture disabled but img/tt/ has no v*.png frames",
                           "add frames or enable capture")
        return {"frames": n, "source": "manual"}
    man = json.loads(cfg.p("src", "manifest.json").read_text())
    targets = [m for m in man if m["group"] == "drawings" and
               any(d.get("capture") and d["id"] == m["id"] for d in cfg["sources"]["drawings"])]
    if not targets:
        raise P3VError("E_CONFIG", "no drawing has \"capture\": true")
    from playwright.sync_api import sync_playwright
    errors = []
    with sync_playwright() as p:
        br = p.chromium.launch(args=GL_ARGS)
        for m in targets:
            fn = ADAPTERS.get(m["kind"])
            if not fn:
                errors.append(f"{m['id']}: no adapter for kind {m['kind']}"); continue
            raw_dir = cfg.p("r", "capture", m["id"], "x").parent
            pg = br.new_page(viewport={"width": c["viewport"][0], "height": c["viewport"][1]})
            try:
                pg.goto("file://" + str(cfg.p("src", m["file"])), timeout=180000)
                frames = fn(pg, c, raw_dir, lg)
            except Exception as e:
                errors.append(f"{m['id']}: {e}"); lg.warning("capture %s failed: %s", m["id"], e)
                continue
            finally:
                pg.close()
            for old in tt.glob("v*.png"):
                old.unlink()
            for i, f in enumerate(frames):
                clean(f, tt / f"v{i:02d}.png", c)
            br.close()
            return {"frames": len(frames), "source": m["id"], "skipped": errors}
        br.close()
    raise P3VError("E_CAPTURE", "; ".join(errors), "try another drawing, or supply frames manually")
