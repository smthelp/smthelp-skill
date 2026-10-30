"""Stage 9 — upload + manifest: upload final files via the configured sink, check remote size == local size,
write 10_upload.json and manifest.csv (aweme_id, filename, stats, desc, url)."""
import csv, os
from . import io, log, sinks
from .errors import DyhError

def run(cfg, manifest_copy=None):
    sink = sinks.make(cfg); sel = io.read(cfg, "selection")
    existing = sink.existing_names()
    fdir = io.p(cfg, "final"); results = {}
    for r in sel:
        path = os.path.join(fdir, r["filename"])
        if r["filename"] in existing:
            log.event("upload", "skip_exists", name=r["filename"]); continue
        results[r["filename"]] = sink.upload(path); log.event("upload", "uploaded", name=r["filename"])
    total = None
    if hasattr(sink, "resolve"):
        results, total = sink.resolve([r["filename"] for r in sel])
    bad = [n for n, x in results.items() if int(x.get("size", -1)) != os.path.getsize(os.path.join(fdir, n))]
    missing = [r["filename"] for r in sel if r["filename"] not in results]
    io.write(cfg, "upload", {"files": results, "destination_total": total, "size_mismatch": bad, "missing": missing})
    cands = io.by_id(io.read(cfg, "candidates"))
    rows = []
    for i, r in enumerate(sel, 1):
        a = cands[r["aweme_id"]]; s = a.get("statistics") or {}
        rows.append([i, a["_rank"], r["aweme_id"], r["filename"], s.get("digg_count"), s.get("comment_count"),
                     s.get("share_count"), s.get("collect_count"), (a.get("desc") or "")[:80].replace("\n", " "),
                     results.get(r["filename"], {}).get("url", "")])
    for dst in filter(None, [io.p(cfg, "manifest"), manifest_copy]):
        with open(dst, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["order", "orig_rank", "aweme_id", "filename", "likes", "comments", "shares", "favorites", "desc", "url"])
            w.writerows(rows)
    log.event("upload", "done", uploaded=len(results), destination_total=total, size_mismatch=bad, missing=missing)
    if bad or missing: raise DyhError("E_UPLOAD", f"mismatch={bad} missing={missing}")
    return rows
