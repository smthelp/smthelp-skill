#!/usr/bin/env python3
"""Create or update one file in a GitHub repo through the Hark `apicall github` connector.
Runs apicall in-process because a base64 page is larger than the shell argument limit.

usage: push_github.py <owner/repo> <local file> [repo path] [commit message]
Run from a shell call that passes credentials [{"provider":"github"}].
Default target for landing pages: smthelping/smt-product-landing-html (repo root).
"""
import sys, base64, json, io, runpy, contextlib
repo, local = sys.argv[1], sys.argv[2]
path = sys.argv[3] if len(sys.argv) > 3 else local.rsplit("/", 1)[-1]
msg = sys.argv[4] if len(sys.argv) > 4 else "Add/update " + path
owner, name = repo.split("/")
def call(*args):
    sys.argv = ["apicall", "github", *args]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try: runpy.run_path("/usr/local/bin/apicall", run_name="__main__")
        except SystemExit: pass
    try: return json.loads(buf.getvalue())
    except Exception: return {"raw": buf.getvalue()[:500]}
cur = call("contents_get", f"owner={owner}", f"repo={name}", f"path={path}")
sha = cur.get("sha") if isinstance(cur, dict) else None
params = ["contents_put", f"owner={owner}", f"repo={name}", f"path={path}", f"message={msg}",
          "content=" + base64.b64encode(open(local, "rb").read()).decode()]
if sha: params.append(f"sha={sha}")
r = call(*params)
if "content" in r: print("OK", r["content"]["html_url"])
else: print("FAILED", json.dumps(r.get("error", r))[:400]); sys.exit(1)
