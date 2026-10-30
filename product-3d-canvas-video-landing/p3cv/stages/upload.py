"""Stage 12 - upload: deliver everything in out/ (html, mp4, jpg, srt, txt) to the configured sink.
folder_name supports {product_name} {slug} {date}. Writes out/delivery.json with the location."""
import json, time
from . import stage
from ..sinks import SINKS
from ..errors import P3VError
from .. import log

EXTS = (".html", ".mp4", ".jpg", ".png", ".srt", ".txt")


@stage("upload", deps=[], desc="Upload out/ deliverables to the sink (gdrive | rclone | local)")
def run(cfg, state):
    u = cfg["upload"]; sink = SINKS.get(u["sink"])
    if not sink:
        raise P3VError("E_CONFIG", f"unknown upload.sink {u['sink']}", "gdrive | rclone | local")
    files = sorted(f for f in cfg.p("out", "x").parent.iterdir() if f.suffix in EXTS)
    if not files:
        raise P3VError("E_STAGE_ORDER", "out/ has no deliverables")
    name = u["folder_name"].format(product_name=cfg["product_name"], slug=cfg.slug, date=time.strftime("%Y-%m-%d"))
    res = sink(files, name, u, log.get("upload"))
    cfg.p("out", "delivery.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    return {"location": res["location"], "files": len(res["files"])}
