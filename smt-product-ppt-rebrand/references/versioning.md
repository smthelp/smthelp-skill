# Versioning and sync

- Semver in `VERSION` and `SKILL.md` metadata; history in `references/changelog.md`.
  - patch: wording, bug fix, layout tweak, new feedback rule
  - minor: new slide type, new config key, new script option, new language
  - major: spec.json format change or new brand template that breaks old specs
- Brand standard has its own id (`brand_version` in brand.json, e.g. SM-PPT-202309); every build-log records both versions so any deck can be traced.
- Release:
  ```bash
  python3 scripts/run.py --example                   # must PASS
  python3 scripts/bump_version.py minor "add timeline slide type"
  git add smt-product-ppt-rebrand && git commit -m "smt-product-ppt-rebrand v1.1.0: add timeline slide type"
  git tag -a smt-product-ppt-rebrand-v1.1.0 -m "add timeline slide type" && git push origin HEAD --tags
  ```
- Sync to an agent: `git pull` in the repo, then copy/symlink `smt-product-ppt-rebrand/` into the agent's skills dir (see repo README). Roll back with `git checkout smt-product-ppt-rebrand-v1.0.0 -- smt-product-ppt-rebrand`.
