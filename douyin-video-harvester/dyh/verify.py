"""Stage 8 — verify: ffprobe duration vs API duration (± tolerance) and optional full decode."""
import os
from . import io, log, media
from .errors import DyhError

def run(cfg):
    v = cfg["verify"]; cands = io.by_id(io.read(cfg, "candidates")); rep, bad = [], []
    for r in io.read(cfg, "selection"):
        f = os.path.join(io.p(cfg, "final"), r["filename"])
        api = (cands[r["aweme_id"]].get("video") or {}).get("duration", 0) / 1000
        dur = media.duration(cfg, f)
        err = media.decode_errors(cfg, f) if v["full_decode"] else ""
        ok = abs(dur - api) <= v["duration_tolerance_s"] and not err
        rep.append({"filename": r["filename"], "bytes": os.path.getsize(f), "duration": round(dur, 2),
                    "api_duration": api, "decode_error": err[:200], "ok": ok})
        if not ok: bad.append(r["filename"])
    io.write(cfg, "verify", rep)
    log.event("verify", "done", ok=len(rep) - len(bad), bad=bad)
    if bad: raise DyhError("E_VERIFY", ", ".join(bad) + " — re-download those ids")
    return rep
