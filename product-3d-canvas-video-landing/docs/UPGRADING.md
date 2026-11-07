# Versioning, upgrade and compatibility rules

## Versions
| Thing | Where | Rule |
|---|---|---|
| Skill version | `VERSION` (single source), mirrored in `skill.json` and `SKILL.md` front matter | SemVer; `tests/test_core.py` fails if the three differ |
| product.json format | `CONFIG_SCHEMA` in `p3cv/config.py`, `schema_version` in product.json | integer; bumps only with a MAJOR skill release |
| Invocation contract | `contract_version` in `skill.json`, docs/CONTRACT.md | integer; bumps only with a MAJOR skill release |
| Animation contract | top of `templates/anim-template.js` | additive changes only within a MAJOR |

## SemVer for this skill
- **MAJOR**: an existing product.json, anim module, CLI command, stage name, envelope key, exit code or output
  file name must change. Requires a `migrate` step (p3cv/contract.py) and a CHANGELOG "Migration" section.
- **MINOR**: new optional config keys with defaults that keep old behaviour, new stages/tools/sinks/adapters,
  new examples.
- **PATCH**: bug fixes, docs, performance with identical outputs.

## Upgrading a project
```
git -C <repo> pull
bash scripts/setup_env.sh
python3 -m p3cv migrate PROJ/product.json     # no-op when already current; keeps product.json.bak
python3 -m p3cv check   PROJ/product.json
```
A product.json newer than the installed skill fails fast with `E_CONFIG` - upgrade the skill, never edit the
number down.

## Releasing a change (any agent, any machine)
1. Change core generically; product-specific behaviour goes in product.json, the anim module or a plugin.
2. Add/adjust tests; `python3 -m unittest discover -s tests` must pass offline.
3. Smoke render: example with `"video": {"scale": 1, "max_seconds": 3}`.
4. Bump `VERSION`, `skill.json.version`, `SKILL.md` front matter `version`; add a CHANGELOG entry
   (Added / Changed / Fixed / Migration).
5. Update the repo-root `README.md` row for this skill.
6. `git commit -m "product-3d-canvas-video-landing vX.Y.Z: <what>"`, `git tag p3cv-vX.Y.Z`, push commit and tag.

## Compatibility matrix
| Skill | config_schema | contract | notes |
|---|---|---|---|
| 1.0.x | 1 (implicit) | - | first release |
| 1.1.x | 1 (implicit) | - | office/pdf text dumps, capture options |
| 1.2.x | 1 | 1 | skill.json, envelope + exit codes, manifest, migrate, replacements/forbid, upscale, privacy, relabel |
