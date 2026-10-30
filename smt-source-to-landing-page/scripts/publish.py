#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish a built landing page.

1) GitHub copy into the landing-page repo (default smthelping/smt-product-landing-html):
    python3 scripts/publish.py github <page.html> --line materials-consumables --title "AI Radial Splicing Tape ..." \
        [--repo-dir ./smt-product-landing-html] [--push] [--dry-run]
   - clones the repo if --repo-dir does not exist (git over https; credentials come from the environment)
   - copies the page into <line>/, adds or updates its row in README.md's table for that line,
     recounts "**N pages in M product lines.**", commits; pushes only with --push.

2) WebDAV upload to file.autoinsertion.com (optional, only when the user asks):
    python3 scripts/publish.py webdav <page.html> [--dir "Product%20landing%20Page"]
   - the password is read from SMFILE_PASS or asked with getpass every time; it is never written anywhere.
   - checks the public URL answers 200 with the same byte count.
"""
import argparse, getpass, json, os, re, shutil, subprocess, sys, urllib.request

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = json.load(open(os.path.join(SKILL, "templates", "brand-southern-machinery.json"), encoding="utf-8"))


def sh(cmd, cwd=None, check=True):
    print("$", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def human(n):
    return "%.2f MB" % (n / 1048576) if n >= 1048576 else "%d KB" % round(n / 1024)


def update_readme(readme, line, rel, title, size, langs):
    s = open(readme, encoding="utf-8").read()
    row = "| %s | `%s` | %s | %s |" % (title, rel, size, langs)
    if "`%s`" % rel in s:
        s = re.sub(r"^\|[^\n]*`%s`[^\n]*$" % re.escape(rel), row, s, flags=re.M)
    else:
        m = re.search(r"^###[^\n]*`%s/`[^\n]*$" % re.escape(line), s, flags=re.M)
        if m:
            # last table row after this heading
            seg_start = m.end()
            nxt = re.search(r"^#{2,3} ", s[seg_start:], flags=re.M)
            seg_end = seg_start + (nxt.start() if nxt else len(s) - seg_start)
            seg = s[seg_start:seg_end]
            rows = list(re.finditer(r"^\|[^\n]*\|$", seg, flags=re.M))
            if rows:
                at = seg_start + rows[-1].end()
                s = s[:at] + "\n" + row + s[at:]
            else:
                s = s[:seg_end] + "\n| Page | File | Size | Languages |\n|---|---|---|---|\n" + row + "\n" + s[seg_end:]
        else:
            s = s.rstrip() + "\n\n### %s - `%s/`\n\n| Page | File | Size | Languages |\n|---|---|---|---|\n%s\n" % (
                line.replace("-", " ").title(), line, row)
    root = os.path.dirname(readme)
    pages, lines = 0, set()
    for dp, dn, fn in os.walk(root):
        if ".git" in dp:
            continue
        h = [f for f in fn if f.endswith(".html")]
        if h:
            pages += len(h)
            lines.add(os.path.relpath(dp, root))
    s = re.sub(r"\*\*\d+ pages in \d+ product lines\.\*\*", "**%d pages in %d product lines.**" % (pages, len(lines)), s)
    open(readme, "w", encoding="utf-8").write(s)
    return pages, len(lines)


def do_github(a):
    repo = a.repo or BRAND["github_landing_repo"]
    rd = a.repo_dir or os.path.join(os.getcwd(), repo.split("/")[-1])
    if not os.path.isdir(os.path.join(rd, ".git")):
        sh(["git", "clone", "https://github.com/%s.git" % repo, rd])
    else:
        sh(["git", "pull", "--ff-only"], cwd=rd, check=False)
    fname = os.path.basename(a.page)
    rel = "%s/%s" % (a.line, fname)
    os.makedirs(os.path.join(rd, a.line), exist_ok=True)
    shutil.copyfile(a.page, os.path.join(rd, rel))
    size = human(os.path.getsize(a.page))
    pages, lines = update_readme(os.path.join(rd, "README.md"), a.line, rel, a.title, size, a.langs)
    print("README: %d pages in %d product lines; row for %s (%s)" % (pages, lines, rel, size))
    if a.dry_run:
        print(sh(["git", "status", "--short"], cwd=rd).stdout)
        print("dry run: nothing committed")
        return
    sh(["git", "add", rel, "README.md"], cwd=rd)
    msg = a.message or "Add %s landing page (%s/)" % (a.title, a.line)
    r = sh(["git", "commit", "-m", msg], cwd=rd, check=False)
    print(r.stdout or r.stderr)
    if a.push:
        r = sh(["git", "push", "origin", "HEAD"], cwd=rd, check=False)
        print(r.stdout, r.stderr)
        sha = sh(["git", "rev-parse", "HEAD"], cwd=rd).stdout.strip()
        print("commit: https://github.com/%s/commit/%s" % (repo, sha))
        print("file:   https://github.com/%s/blob/main/%s" % (repo, rel))


def do_webdav(a):
    w = BRAND["webdav"]
    pw = os.environ.get("SMFILE_PASS") or getpass.getpass("WebDAV password for %s (not stored): " % w["user"])
    remote = "%s/%s" % (a.dir.strip("/"), os.path.basename(a.page).replace(" ", "%20"))
    base = w["base"].rstrip("/")
    subprocess.run(["curl", "-s", "-o", "/dev/null", "-u", "%s:%s" % (w["user"], pw), "-X", "MKCOL", "%s/%s/" % (base, a.dir.strip("/")),
                    "-w", "MKCOL -> %{http_code}\n"])
    subprocess.run(["curl", "-s", "-u", "%s:%s" % (w["user"], pw), "-T", a.page, "%s/%s" % (base, remote), "-w", "PUT -> %{http_code}, %{size_upload} bytes\n"])
    pub = "%s/%s" % (w["public_base"].rstrip("/"), remote)
    try:
        with urllib.request.urlopen(pub, timeout=60) as r:
            body = r.read()
        print("public:", pub, r.status, len(body), "bytes (local %d)" % os.path.getsize(a.page))
    except Exception as e:
        print("public check failed:", pub, e)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    g = sp.add_parser("github")
    g.add_argument("page"); g.add_argument("--line", required=True, help="product-line folder, e.g. materials-consumables")
    g.add_argument("--title", required=True); g.add_argument("--langs", default="7 + x-default")
    g.add_argument("--repo", default=None); g.add_argument("--repo-dir", default=None)
    g.add_argument("--message", default=None); g.add_argument("--push", action="store_true"); g.add_argument("--dry-run", action="store_true")
    w = sp.add_parser("webdav")
    w.add_argument("page"); w.add_argument("--dir", default=BRAND["webdav"]["default_dir"])
    a = ap.parse_args()
    do_github(a) if a.cmd == "github" else do_webdav(a)


if __name__ == "__main__":
    main()
