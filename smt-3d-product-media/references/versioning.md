# Versioning, compatibility and sync

Two version numbers:
- **Skill version** (semver, `VERSION`, SKILL.md `metadata.version`, `skill.json`):
  - patch: bug fix, wording, default tweak that does not change existing outputs' meaning
  - minor: new optional job key, new command, new action/kinematics, new palette, new language
  - major: breaking change to job.json, commands or output layout
- **Job schema** (`smt-3d-product-media/job@<major>`): changes only with a skill major. Every 1.x release accepts job@1 files unchanged; new keys are optional with defaults in `config/defaults.json`.

Compatibility rules
1. Never rename or remove a job key or command within a major; deprecate (WARN) for one minor first.
2. New behaviour defaults to the old behaviour.
3. Output names/layout (`out/video`, `out/deck`, `manifest.json`) are part of the contract.
4. A major release ships `scripts/migrate_job.py <old> <new>` and a migration note in the changelog.
5. `manifest.json` records skill version + schema + CAD sha1 so any video/deck can be traced and rebuilt.

Release
```bash
tests/smoke.sh                                         # must print PASS
python3 scripts/bump_version.py minor "add orbit-only scene"
# run the printed git commands: commit, tag smt-3d-product-media-vX.Y.Z, push
tools/publish_to_repo.sh                               # sync to github.com/smthelp/smthelp-skill + README row + tag
```
Rollback: `git checkout smt-3d-product-media-v1.0.0 -- smt-3d-product-media`.

Sync to an agent: `git pull` in the repo, then point the agent at `smt-3d-product-media/SKILL.md` (copy or symlink the folder into its skills directory). Pin a version with the tag when a job must be rebuilt exactly.
