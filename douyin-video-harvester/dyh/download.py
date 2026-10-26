"""Stage 4 — download: try each CDN url (highest bitrate first) via yt-dlp generic extractor with referer+cookies.
Idempotent: existing files >= min_bytes are skipped."""
import concurrent.futures as cf, os, subprocess, tempfile
from . import io, log
from .cookies import load_douyin, write_netscape
from .errors import DyhError

def urls_of(a, limit):
    v = a.get("video") or {}
    urls = []
    for br in sorted(v.get("bit_rate") or [], key=lambda b: -(b.get("bit_rate") or 0)):
        urls += (br.get("play_addr") or {}).get("url_list", [])
    urls += (v.get("play_addr") or {}).get("url_list", [])
    seen, out = set(), []
    for u in urls:
        if u not in seen: seen.add(u); out.append(u)
    return out[:limit]

def fname(a):
    return f"{a['_rank']:03d}_{a['aweme_id']}.mp4"

def one(cfg, a, ckfile, outdir):
    d = cfg["download"]; dst = os.path.join(outdir, fname(a))
    if os.path.exists(dst) and os.path.getsize(dst) >= d["min_bytes"]:
        return a["aweme_id"], "cached"
    for i, u in enumerate(urls_of(a, d["max_urls"])):
        cmd = [cfg["yt_dlp"], "-q", "--no-warnings", "--cookies", ckfile, "--referer", d["referer"],
               "-o", dst, "--force-overwrites", u]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=d["timeout_s"])
        except subprocess.TimeoutExpired:
            log.event("download", "timeout", id=a["aweme_id"], url_idx=i); continue
        except FileNotFoundError:
            raise DyhError("E_DEP", cfg["yt_dlp"])
        if r.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) >= d["min_bytes"]:
            return a["aweme_id"], "ok"
        log.event("download", "url_failed", id=a["aweme_id"], url_idx=i, err=r.stderr.strip()[-160:])
    return a["aweme_id"], "failed"

def run(cfg, ids=None):
    cands = io.read(cfg, "candidates")
    if ids: cands = [a for a in cands if a["aweme_id"] in ids or str(a["_rank"]) in ids]
    outdir = io.p(cfg, "videos"); os.makedirs(outdir, exist_ok=True)
    fd, ckfile = tempfile.mkstemp(suffix=".cookies.txt"); os.close(fd)
    write_netscape(load_douyin(cfg["cookies"]), ckfile)
    try:
        with cf.ThreadPoolExecutor(cfg["download"]["workers"]) as ex:
            res = list(ex.map(lambda a: one(cfg, a, ckfile, outdir), cands))
    finally:
        os.remove(ckfile)
    failed = [i for i, s in res if s == "failed"]
    log.event("download", "done", ok=sum(s != "failed" for _, s in res), failed=failed)
    if failed:
        log.get("download").error("E_DOWNLOAD for %s — rerun `download` (cached files skipped); "
                                   "if persistent, rescrape (CDN urls expire after hours)", failed)
    return res
