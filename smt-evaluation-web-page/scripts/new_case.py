#!/usr/bin/env python3
"""Scaffold a new case from examples/_template.  usage: new_case.py <case_dir>"""
import os, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) < 2: sys.exit(__doc__)
dst = sys.argv[1]
if os.path.exists(dst): sys.exit(f"{dst} exists")
shutil.copytree(os.path.join(ROOT, "examples", "_template"), dst)
os.makedirs(os.path.join(dst, "photos"), exist_ok=True); os.makedirs(os.path.join(dst, "web", "i18n"), exist_ok=True)
print("case ready:", dst, "-> fill report.json, web/page.json, web/web_en.json, photos/")
