#!/usr/bin/env python3
"""Bump semver in VERSION + dyh/__init__.py and prepend a changelog stub. Usage: bump_version.py patch|minor|major "summary" """
import re, sys, datetime, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
part, summary = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "")
ma, mi, pa = map(int, (root / "VERSION").read_text().strip().split("."))
ma, mi, pa = {"major": (ma + 1, 0, 0), "minor": (ma, mi + 1, 0), "patch": (ma, mi, pa + 1)}[part]
v = f"{ma}.{mi}.{pa}"
(root / "VERSION").write_text(v + "\n")
init = root / "dyh/__init__.py"; init.write_text(re.sub(r'__version__ = "[^"]+"', f'__version__ = "{v}"', init.read_text()))
cl = root / "references/changelog.md"; t = cl.read_text()
cl.write_text(t.replace("<!-- new entries here -->", f"<!-- new entries here -->\n\n## {v} — {datetime.date.today()}\n- {summary}", 1))
print(v)
