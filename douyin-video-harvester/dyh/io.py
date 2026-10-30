"""Run-dir layout: every stage reads/writes fixed files so stages are independent and resumable."""
import json, os
from .errors import DyhError

FILES = {
    "awemes": "01_awemes.json",        # scrape output: raw aweme objects
    "ranked": "02_ranked.json",        # rank output: + _score, _rank
    "candidates": "03_candidates.json",# filter output: subset to review
    "videos": "04_videos",             # download output dir: {rank:03d}_{aweme_id}.mp4
    "sheets": "05_sheets",             # contact sheets for visual review
    "dupes": "06_dupes.json",          # near-duplicate pairs
    "selection": "07_selection.json",  # HUMAN/AGENT GATE: [{"aweme_id","filename"}]
    "final": "08_final",               # renamed files
    "verify": "09_verify.json",
    "upload": "10_upload.json",
    "manifest": "manifest.csv",
}

def p(cfg, key):
    return os.path.join(cfg["run_dir"], FILES[key])

def read(cfg, key):
    path = p(cfg, key)
    if not os.path.exists(path):
        raise DyhError("E_STAGE_INPUT", path)
    return json.load(open(path, encoding="utf-8"))

def write(cfg, key, data):
    os.makedirs(cfg["run_dir"], exist_ok=True)
    tmp = p(cfg, key) + ".tmp"
    json.dump(data, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, p(cfg, key))
    return p(cfg, key)

def by_id(items):
    return {a["aweme_id"]: a for a in items}
