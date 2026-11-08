#!/usr/bin/env python3
"""Bump the skill version, log the change and print the git commands to release it.

usage: bump_version.py patch|minor|major "<what changed>"
patch = bug fix, wording, default tweak;  minor = new optional job key, command, action, palette;
major = breaking job.json / command / output change (bump schema job@N, ship migrate_job.py).
Updates VERSION, SKILL.md metadata, skill.json (version, updated) and references/changelog.md."""
import json
import datetime, os, re, sys
SKILL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NAME = os.path.basename(SKILL)
if len(sys.argv) < 3 or sys.argv[1] not in ("patch", "minor", "major"): sys.exit(__doc__)
part, msg = sys.argv[1], " ".join(sys.argv[2:])
ma, mi, pa = map(int, open(os.path.join(SKILL, "VERSION")).read().strip().split("."))
ma, mi, pa = (ma + 1, 0, 0) if part == "major" else (ma, mi + 1, 0) if part == "minor" else (ma, mi, pa + 1)
new = f"{ma}.{mi}.{pa}"; today = datetime.date.today().isoformat()
open(os.path.join(SKILL, "VERSION"), "w").write(new + "\n")
p = os.path.join(SKILL, "SKILL.md"); t = open(p, encoding="utf-8").read()
t = re.sub(r"^(\s*version:\s*).*$", lambda m: m.group(1) + new, t, count=1, flags=re.M)
t = re.sub(r"^(\s*updated:\s*).*$", lambda m: m.group(1) + today, t, count=1, flags=re.M)
open(p, "w", encoding="utf-8").write(t)
sj = os.path.join(SKILL, "skill.json"); m = json.load(open(sj, encoding="utf-8")); m["version"] = new; m["updated"] = today
json.dump(m, open(sj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
c = os.path.join(SKILL, "references", "changelog.md"); body = open(c, encoding="utf-8").read()
head, rest = body.split("\n\n", 1)
open(c, "w", encoding="utf-8").write(f"{head}\n\n## {new} - {today}\n- {msg}\n\n{rest}")
print("version", new)
print(f'git add {NAME} && git commit -m "{NAME} v{new}: {msg}" && git tag -a {NAME}-v{new} -m "{msg}" && git push origin HEAD --tags')
