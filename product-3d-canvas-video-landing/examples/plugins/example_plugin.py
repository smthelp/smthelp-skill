"""Example plugin: adds a 'manifest' stage and a 'webhook' sink WITHOUT touching core code.
Enable in product.json:   "plugins": ["examples/plugins/example_plugin.py"]
Then:  python -m p3cv run product.json manifest      or   "upload": {"sink": "webhook", "url": "..."}"""
import hashlib, json, urllib.request
from p3cv.stages import stage
from p3cv.sinks import SINKS
from p3cv import log


@stage("manifest", deps=[], desc="Write out/manifest.json (name, size, sha256 of every deliverable)")
def manifest(cfg, state):
    rows = []
    for f in sorted(cfg.p("out", "x").parent.iterdir()):
        if f.is_file() and f.name != "manifest.json":
            rows.append({"name": f.name, "bytes": f.stat().st_size, "sha256": hashlib.sha256(f.read_bytes()).hexdigest()})
    cfg.p("out", "manifest.json").write_text(json.dumps(rows, indent=1))
    log.get("manifest").info("%d files", len(rows))
    return {"files": len(rows)}


def webhook(files, folder_name, u, lg):
    body = json.dumps({"folder": folder_name, "files": [f.name for f in files]}).encode()
    urllib.request.urlopen(urllib.request.Request(u["url"], body, {"Content-Type": "application/json"}), timeout=30)
    return {"location": u["url"], "files": [{"name": f.name, "bytes": f.stat().st_size} for f in files]}


SINKS["webhook"] = webhook
