"""Stage 3 — filter: text pre-screen (keywords) + drop image posts + drop ids already delivered (exclude_id_files).
Text is only a pre-screen: final relevance is judged visually from contact sheets (stage 5)."""
import csv, json, os
from . import io, log

def load_excluded(paths):
    ids = set()
    for p in paths:
        if not os.path.exists(p):
            log.get("filter").warning("exclude file missing: %s", p); continue
        if p.endswith(".csv"):
            for row in csv.DictReader(open(p, encoding="utf-8")):
                if row.get("aweme_id"): ids.add(row["aweme_id"].strip())
        else:
            for x in json.load(open(p, encoding="utf-8")):
                ids.add(str(x.get("aweme_id") if isinstance(x, dict) else x))
    return ids

def classify(desc, inc, exc):
    d = desc or ""
    if any(k in d for k in exc): return "excluded_keyword"
    if inc and any(k in d for k in inc): return "keyword_hit"
    return "no_keyword"

def run(cfg):
    f = cfg["filter"]
    ranked = io.read(cfg, "ranked")
    skip = load_excluded(f["exclude_id_files"])
    out, stats = [], {}
    for a in ranked:
        if cfg["rank"]["skip_image_posts"] and a.get("_is_image"): why = "image_post"
        elif a["aweme_id"] in skip: why = "already_delivered"
        else: why = classify(a.get("desc"), f["include_keywords"], f["exclude_keywords"])
        stats[why] = stats.get(why, 0) + 1
        a["_filter"] = why
        if why == "keyword_hit" or (why == "no_keyword" and not f["require_include"]):
            out.append(a)
    out = out[: f["candidate_limit"]]
    io.write(cfg, "candidates", out)
    log.event("filter", "done", candidates=len(out), **stats)
    return out

def print_table(cfg, n=80):
    for a in io.read(cfg, "candidates")[:n]:
        s = a.get("statistics") or {}
        print(a["_rank"], a["aweme_id"], s.get("digg_count"), s.get("comment_count"), s.get("share_count"),
              round((a.get("video") or {}).get("duration", 0) / 1000), (a.get("desc") or "")[:60].replace("\n", " "))
