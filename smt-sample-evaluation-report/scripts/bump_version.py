#!/usr/bin/env python3
"""Bump the skill version and log the change.

usage: bump_version.py patch|minor|major "<what changed>"
Updates SKILL.md metadata (version, updated) and prepends a line to references/changelog.md.
patch = wording/bug fix, minor = new parameter/slide/language/machine, major = formula or input format change."""
import datetime, os, re, sys

SKILL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
if len(sys.argv) < 3 or sys.argv[1] not in ("patch", "minor", "major"): sys.exit(__doc__)
part, msg = sys.argv[1], " ".join(sys.argv[2:])
p = os.path.join(SKILL, "SKILL.md"); t = open(p, encoding="utf-8").read()
cur = re.search(r"^(\s*version:\s*)(\d+)\.(\d+)\.(\d+)", t, re.M)
ma, mi, pa = int(cur.group(2)), int(cur.group(3)), int(cur.group(4))
ma, mi, pa = (ma + 1, 0, 0) if part == "major" else (ma, mi + 1, 0) if part == "minor" else (ma, mi, pa + 1)
new = f"{ma}.{mi}.{pa}"; today = datetime.date.today().isoformat()
t = t[:cur.start()] + cur.group(1) + new + t[cur.end():]
t = re.sub(r"^(\s*updated:\s*).*$", lambda m: m.group(1) + today, t, count=1, flags=re.M)
open(p, "w", encoding="utf-8").write(t)
c = os.path.join(SKILL, "references", "changelog.md")
body = open(c, encoding="utf-8").read() if os.path.exists(c) else "# Changelog\n\n"
head, rest = body.split("\n\n", 1) if "\n\n" in body else (body, "")
open(c, "w", encoding="utf-8").write(f"{head}\n\n## {new} - {today}\n- {msg}\n\n{rest}")
print("version", new)
