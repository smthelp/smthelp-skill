# smthelp-webapp-builder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Southern Machinery web-app builder skill to the repository so the brand system, the two delivery variants, and the five-class verification suite are reusable from any workspace.

**Architecture:** A single self-contained `SKILL.md`. Routing rules, brand tokens, asset endpoints, the SPA and single-file variants, and the verification suite live in one file, so an invocation starts work without a second read. The build pipeline for the single-file variant keeps sources and artefact separate and rebuilds idempotently.

**Tech Stack:** Agent Skills Markdown, YAML frontmatter, Python build/validate/falsify/checklinks scripts, Chrome DevTools Protocol over Node 22 native WebSocket, zero third-party dependencies.

## Global Constraints

- Add only `smthelp-webapp-builder/` and process documents; do not alter existing skill directories.
- All technical values in generated pages must trace to a source; unknowns are labelled `待确认` and never guessed.
- Customer internal material converted to a public page must be anonymised, and the page must state its own provenance and uncertainty.
- Do not hand-edit a built artefact; it is regenerated from `template.html`.

---

### Task 1: Establish the entry point

**Files:**
- Create: `smthelp-webapp-builder/SKILL.md`
- Verify: `C:\Users\Admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py`

**Interfaces:**
- Produces: the routing table, brand tokens, asset endpoints, and the two delivery variants.

- [ ] **Step 1: Confirm the target is absent**

Run: `ls F:\baidunetdiskworkspace\My Data\Skills\smthelp-skills\smthelp-webapp-builder`

Expected: no such directory.

- [ ] **Step 2: Copy the authored skill into the repository**

Copy `C:\Users\Admin\.workbuddy-ai\skills\smthelp-webapp-builder\SKILL.md` to
`F:\baidunetdiskworkspace\My Data\Skills\smthelp-skills\smthelp-webapp-builder\SKILL.md`.

- [ ] **Step 3: Confirm the copy is byte-identical**

Compare sizes and MD5 of source and destination.

Expected: identical.

- [ ] **Step 4: Record the validator outcome**

Run `quick_validate.py` against the new directory using the managed virtual environment
(`C:\Users\Admin\.workbuddy-ai\binaries\python\envs\default`, which provides `yaml`).

Expected: the legacy frontmatter keys are reported as unexpected. This is accepted and documented in the design spec; the sibling `smthelp-*` skills carry the same keys, and the frontmatter is not rewritten for a validator alone.

### Task 2: Add the process documents

**Files:**
- Create: `docs/superpowers/specs/2026-09-18-smthelp-webapp-builder-design.md`
- Create: `docs/superpowers/plans/2026-09-18-smthelp-webapp-builder.md`

**Interfaces:**
- Consumes: the section map and constraints of the entry point.
- Produces: the auditable design record and this plan.

- [ ] **Step 1: Write the design record**

State the purpose, the eleven-section architecture, the requirements that must hold for any generated page, the validation gates, and the accepted frontmatter deviation with its reason.

- [ ] **Step 2: Write this plan**

- [ ] **Step 3: Read both documents back as UTF-8**

Confirm headings, the section map, and the deviation note are intact and no content is truncated.

### Task 3: Commit and publish

**Files:**
- Stage: `smthelp-webapp-builder/SKILL.md`
- Stage: `docs/superpowers/specs/2026-09-18-smthelp-webapp-builder-design.md`
- Stage: `docs/superpowers/plans/2026-09-18-smthelp-webapp-builder.md`

- [ ] **Step 1: Stage only the new paths**

Do not stage unrelated working-tree state that predates this change.

- [ ] **Step 2: Confirm the staged set**

Expected: exactly three added files, no deletions, no modifications to other skills.

- [ ] **Step 3: Commit and push**

Push to `origin main` of `smthelp/smthelp-skill`, then confirm the remote ref advanced to the local commit.
