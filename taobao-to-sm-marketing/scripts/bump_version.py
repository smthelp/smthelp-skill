#!/usr/bin/env python3
"""Bump the skill version and add a CHANGELOG entry.
usage: bump_version.py patch|minor|major "what changed" [--kit "product that triggered it"]"""
import os, sys, re, datetime, argparse
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument("part", choices=["patch", "minor", "major"]); ap.add_argument("note"); ap.add_argument("--kit", default="")
a = ap.parse_args()
vf = os.path.join(root, "VERSION"); M, m, p = map(int, open(vf).read().strip().split("."))
M, m, p = (M + 1, 0, 0) if a.part == "major" else (M, m + 1, 0) if a.part == "minor" else (M, m, p + 1)
v = f"{M}.{m}.{p}"; open(vf, "w").write(v + "\n")
sk = os.path.join(root, "SKILL.md"); t = open(sk, encoding="utf-8").read()
t = re.sub(r"(\n  version: )[\d.]+", rf"\g<1>{v}", t, 1); t = re.sub(r"(\n  updated: )[\d-]+", rf"\g<1>{datetime.date.today()}", t, 1)
open(sk, "w", encoding="utf-8").write(t)
cl = os.path.join(root, "CHANGELOG.md"); c = open(cl, encoding="utf-8").read()
entry = f"## {v} - {datetime.date.today()}\n- {a.note}" + (f" (kit: {a.kit})" if a.kit else "") + "\n\n"
c = c.replace("<!-- new entries -->\n", "<!-- new entries -->\n" + entry, 1); open(cl, "w", encoding="utf-8").write(c)
print("version", v)
