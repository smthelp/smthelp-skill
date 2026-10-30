#!/usr/bin/env python3
"""Bump SKILL.md version and log it.  usage: bump_version.py major|minor|patch "note" """
import os, re, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
part, note = sys.argv[1], " ".join(sys.argv[2:]) or "update"
p = os.path.join(ROOT, "SKILL.md"); s = open(p, encoding="utf-8").read()
v = list(map(int, re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)", s, re.M).groups()))
i = {"major": 0, "minor": 1, "patch": 2}[part]; v[i] += 1; v[i + 1:] = [0] * (2 - i)
nv = ".".join(map(str, v)); open(p, "w", encoding="utf-8").write(re.sub(r"^version:\s*[\d.]+", f"version: {nv}", s, count=1, flags=re.M))
cl = os.path.join(ROOT, "references", "changelog.md")
open(cl, "a", encoding="utf-8").write(f"\n- {nv} ({datetime.date.today()}): {note}\n")
print(nv)
