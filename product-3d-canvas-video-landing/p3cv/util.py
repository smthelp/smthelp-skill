"""Small shared helpers: subprocess with clear errors, proxy-free env, tool checks, retries."""
import os, shutil, subprocess, time
from .errors import P3VError
from . import log

PROXY_VARS = ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]


def no_proxy_env():
    env = dict(os.environ)
    for k in PROXY_VARS:
        env.pop(k, None)
    return env


def need(tool, hint=None):
    if not shutil.which(tool):
        raise P3VError("E_DEPENDENCY", f"'{tool}' not found on PATH", hint or "run scripts/setup_env.sh")


def run(cmd, code="E_FFMPEG", **kw):
    lg = log.get("run")
    lg.debug("exec %s", " ".join(map(str, cmd)))
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise P3VError(code, f"{cmd[0]} exited {r.returncode}: {r.stderr.strip()[-600:]}")
    return r.stdout


def ffprobe_duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).strip())


def retry(fn, tries=3, delay=2.0, backoff=2.0, what="operation", exc=(Exception,)):
    lg = log.get("retry")
    for i in range(1, tries + 1):
        try:
            return fn()
        except exc as e:  # noqa
            if i == tries:
                raise
            lg.warning("%s failed (%s), retry %d/%d in %.0fs", what, e, i, tries - 1, delay)
            time.sleep(delay); delay *= backoff
