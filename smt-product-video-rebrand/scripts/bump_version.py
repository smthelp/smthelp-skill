#!/usr/bin/env python3
"""bump_version.py patch|minor|major "summary" -> VERSION, SKILL.md metadata, references/changelog.md"""
import sys, re, datetime, os
SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
part, msg = sys.argv[1], sys.argv[2]
v = open(f'{SK}/VERSION').read().strip().split('.'); i = {'major': 0, 'minor': 1, 'patch': 2}[part]
v[i] = str(int(v[i]) + 1); v[i + 1:] = ['0'] * (2 - i); nv = '.'.join(v); today = datetime.date.today().isoformat()
open(f'{SK}/VERSION', 'w').write(nv + '\n')
s = open(f'{SK}/SKILL.md').read()
s = re.sub(r'version: \d+\.\d+\.\d+', f'version: {nv}', s, 1); s = re.sub(r'updated: [\d-]+', f'updated: {today}', s, 1)
open(f'{SK}/SKILL.md', 'w').write(s)
c = open(f'{SK}/references/changelog.md').read().replace('# Changelog\n', f'# Changelog\n## {nv} - {today}\n- {msg}\n', 1)
open(f'{SK}/references/changelog.md', 'w').write(c)
print(nv)
