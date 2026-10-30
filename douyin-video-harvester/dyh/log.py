"""Logging: human lines to stderr + JSON lines to <run_dir>/run.log.jsonl (one event per line)."""
import json, logging, sys, os
from datetime import datetime

_run_file = None

def setup(run_dir=None, level="INFO"):
    global _run_file
    logging.basicConfig(stream=sys.stderr, level=getattr(logging, level.upper(), logging.INFO),
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    if run_dir:
        os.makedirs(run_dir, exist_ok=True)
        _run_file = os.path.join(run_dir, "run.log.jsonl")

def get(name):
    return logging.getLogger(f"dyh.{name}")

def event(stage, kind, **data):
    """Structured event for auditing/resume; also echoed at INFO."""
    rec = {"t": datetime.now().astimezone().isoformat(timespec="seconds"), "stage": stage, "event": kind, **data}
    get(stage).info("%s %s", kind, json.dumps(data, ensure_ascii=False)[:300])
    if _run_file:
        with open(_run_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
