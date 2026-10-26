"""Config loading: defaults <- config file (JSON) <- CLI overrides. See config/config.schema.json."""
import json, copy, os
from .errors import DyhError

DEFAULTS = {
    "run_dir": "runs/{run_name}",
    "cookies": "secrets/douyin.cookies.txt",
    "chromium": "/usr/bin/chromium",
    "yt_dlp": "yt-dlp",
    "ffmpeg": "ffmpeg",
    "ffprobe": "ffprobe",
    "proxy_from_env": True,
    "scrape": {"max_scrolls": 400, "stall_limit": 20, "scroll_wait_ms": 1500, "first_wait_ms": 8000},
    "rank": {"weights": {"digg_count": 0.45, "comment_count": 0.35, "share_count": 0.12, "collect_count": 0.08},
             "skip_image_posts": True},
    "filter": {"include_keywords": [], "exclude_keywords": [], "require_include": False,
               "exclude_id_files": [], "candidate_limit": 40},
    "download": {"workers": 6, "timeout_s": 110, "max_urls": 8, "min_bytes": 30000,
                 "referer": "https://www.douyin.com/"},
    "frames": {"positions": [0.25, 0.5, 0.8], "tile": "9x6", "thumb": 180},
    "dedupe": {"times_s": [1, 3, 6], "threshold": 12, "compare_dirs": []},
    "select": {"count": 20},
    "verify": {"duration_tolerance_s": 1.0, "full_decode": True},
    "sink": {"type": "local", "options": {}},
    "log_level": "INFO",
}

def _merge(a, b):
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            _merge(a[k], v)
        else:
            a[k] = v
    return a

def load(path=None, overrides=None):
    cfg = copy.deepcopy(DEFAULTS)
    if path:
        if not os.path.exists(path):
            raise DyhError("E_CONFIG", f"{path} not found")
        try:
            _merge(cfg, json.load(open(path, encoding="utf-8")))
        except json.JSONDecodeError as e:
            raise DyhError("E_CONFIG", f"{path}: {e}")
    _merge(cfg, overrides or {})
    if not cfg.get("run_name"):
        raise DyhError("E_CONFIG", "run_name is required (config or --run-name)")
    cfg["run_dir"] = cfg["run_dir"].format(run_name=cfg["run_name"])
    return cfg
