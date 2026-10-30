"""Stage 2 — rank: play_count is 0 for non-owners, so score = sum(w_k * log1p(x_k) / log1p(max_k))."""
import math
from . import io, log

def score_all(items, weights):
    mx = {k: math.log1p(max((a.get("statistics") or {}).get(k, 0) or 0 for a in items)) or 1.0 for k in weights}
    for a in items:
        s = a.get("statistics") or {}
        a["_score"] = round(sum(w * math.log1p(s.get(k, 0) or 0) / mx[k] for k, w in weights.items()), 5)
    items.sort(key=lambda a: -a["_score"])
    for i, a in enumerate(items, 1):
        a["_rank"] = i
        a["_is_image"] = bool(a.get("images"))
    return items

def run(cfg):
    items = score_all(io.read(cfg, "awemes"), cfg["rank"]["weights"])
    io.write(cfg, "ranked", items)
    log.event("rank", "done", total=len(items), images=sum(a["_is_image"] for a in items))
    return items
