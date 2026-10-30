"""Logging: human log to console + PROJ/logs/p3cv.log, machine events to PROJ/logs/events.jsonl."""
import json, logging, sys, time
from pathlib import Path

_events = None


def setup(proj: Path, level="INFO"):
    global _events
    logs = proj / "logs"; logs.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger("p3cv"); root.setLevel(level); root.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)-5s %(name)s: %(message)s", "%H:%M:%S")
    for h in (logging.StreamHandler(sys.stdout), logging.FileHandler(logs / "p3cv.log", encoding="utf-8")):
        h.setFormatter(fmt); root.addHandler(h)
    _events = logs / "events.jsonl"
    return root


def get(name):
    return logging.getLogger("p3cv." + name)


def event(event_name, **kw):
    """Append one structured event (stage_start, stage_done, stage_fail, warn, artifact ...)."""
    if _events is None:
        return
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "event": event_name, **kw}
    with open(_events, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
