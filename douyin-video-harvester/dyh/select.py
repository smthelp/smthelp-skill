"""Stage 7 — select (gate): reviewer writes 07_selection.json = [{"aweme_id": "...", "filename": "...mp4"}, ...]
in final order. This stage validates it and copies files to 08_final/<filename>."""
import os, shutil
from . import io, log
from .naming import check
from .errors import DyhError
from .download import fname

def template(cfg):
    """Write a starter selection from top candidates with downloaded files (filenames left to fill)."""
    cands = io.read(cfg, "candidates"); vdir = io.p(cfg, "videos")
    rows = [{"aweme_id": a["aweme_id"], "rank": a["_rank"], "desc": (a.get("desc") or "")[:60], "filename": ""}
            for a in cands if os.path.exists(os.path.join(vdir, fname(a)))][: cfg["select"]["count"]]
    return io.write(cfg, "selection", rows)

def run(cfg, existing_names=()):
    sel = io.read(cfg, "selection"); cands = io.by_id(io.read(cfg, "candidates"))
    errs, seen = [], set(existing_names)
    if len(sel) != cfg["select"]["count"]:
        errs.append(f"expected {cfg['select']['count']} rows, got {len(sel)}")
    for r in sel:
        n = r.get("filename", "")
        if r.get("aweme_id") not in cands: errs.append(f"{r.get('aweme_id')}: not a candidate")
        errs += [f"{n}: {e}" for e in check(n)]
        if n in seen: errs.append(f"{n}: duplicate (in this batch or already at destination)")
        seen.add(n)
    if errs: raise DyhError("E_SELECTION", "; ".join(errs))
    fdir = io.p(cfg, "final"); os.makedirs(fdir, exist_ok=True)
    for r in sel:
        shutil.copy2(os.path.join(io.p(cfg, "videos"), fname(cands[r["aweme_id"]])), os.path.join(fdir, r["filename"]))
    log.event("select", "done", files=len(sel))
    return sel
