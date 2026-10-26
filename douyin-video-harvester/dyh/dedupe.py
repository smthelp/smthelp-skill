"""Stage 6 — dedupe: 16x16 gray frames at fixed seconds; mean abs diff < threshold => same video
(catches 往年今日 reposts and the same clip posted by sister accounts — add their dirs to compare_dirs)."""
import glob, itertools, os
from . import io, log, media

def run(cfg):
    dd = cfg["dedupe"]
    files = sorted(glob.glob(os.path.join(io.p(cfg, "videos"), "*.mp4")))
    for d in dd["compare_dirs"]:
        files += sorted(glob.glob(os.path.join(d, "*.mp4")))
    sig = {f: b"".join(media.gray16(cfg, f, t) for t in dd["times_s"]) for f in files}
    pairs = []
    for a, b in itertools.combinations(files, 2):
        diff = sum(abs(x - y) for x, y in zip(sig[a], sig[b])) / len(sig[a])
        if diff < dd["threshold"]:
            pairs.append({"a": a, "b": b, "diff": round(diff, 1)})
    io.write(cfg, "dupes", pairs)
    log.event("dedupe", "done", files=len(files), dup_pairs=len(pairs))
    return pairs
