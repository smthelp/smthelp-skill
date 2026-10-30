# learn-SMT-in-3-hours Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a standalone, evidence-bound, diagram-led SMT automation learning skill that can produce a three-hour learning package.

**Architecture:** Keep routing and non-negotiable boundaries in `SKILL.md`; load each detailed learning resource only when its topic is requested. The generated package uses Markdown diagrams and source-labelled visual briefs instead of inventing product imagery or technical settings.

**Tech Stack:** Agent Skills Markdown, YAML frontmatter, Mermaid-compatible Markdown, Python quick validator, PowerShell content assertions.

## Global Constraints

- Create only `learn-SMT-in-3-hours` and process documents; do not alter existing skill directories or YAML names.
- Use current Southern Machinery product sources for model-specific facts; otherwise label them `待确认`.
- Do not generate executable operation instructions that bypass safety or supplier documentation.

---

### Task 1: Establish an auditable skill contract

**Files:**
- Create: `learn-SMT-in-3-hours/SKILL.md`
- Test: `C:\\Users\\Admin\\.codex\\skills\\.system\\skill-creator\\scripts\\quick_validate.py`

**Interfaces:**
- Produces: routing links to four `references/*.md` files and the required learning-package contract.

- [ ] **Step 1: Verify the target is absent**

Run: `python C:\\Users\\Admin\\.codex\\skills\\.system\\skill-creator\\scripts\\quick_validate.py F:\\baidunetdiskworkspace\\My Data\\Skills\\smthelp-skills\\learn-SMT-in-3-hours`

Expected: exit code `1` with `SKILL.md not found`.

- [ ] **Step 2: Write the minimum valid entry point**

Create lowercase YAML metadata, a discriminating invocation description, an evidence hierarchy, output labels, a 180-minute package contract, safety exclusions, and relative reference links.

- [ ] **Step 3: Verify the entry point passes validation**

Run the command from Step 1 again.

Expected: exit code `0` with `Skill is valid!`.

### Task 2: Add the modular learning material

**Files:**
- Create: `learn-SMT-in-3-hours/references/curriculum.md`
- Create: `learn-SMT-in-3-hours/references/visual-language.md`
- Create: `learn-SMT-in-3-hours/references/process-and-operations.md`
- Create: `learn-SMT-in-3-hours/references/troubleshooting-and-maintenance.md`

**Interfaces:**
- Consumes: the entry point's source labels and safety constraints.
- Produces: the four reference targets promised by `SKILL.md`.

- [ ] **Step 1: Write curriculum and visual-language references**

Define a 180-minute route and reusable diagrams for process flow, equipment anatomy, parameter causality, fault trees, maintenance cards, and coordination lanes.

- [ ] **Step 2: Write process and maintenance references**

Define equipment class cards, parameter categories without unsupported values, operation checkpoints, process handoffs, diagnostic sequence, escalation boundaries, and maintenance-record structure.

- [ ] **Step 3: Read links and assertions as UTF-8**

Verify every linked reference exists, the course totals 180 minutes, and all required subject areas and safety labels occur in the content.

### Task 3: Validate integration and scope

**Files:**
- Verify: `learn-SMT-in-3-hours/SKILL.md`
- Verify: `learn-SMT-in-3-hours/references/*.md`

- [ ] **Step 1: Run structural and content validation**

Run the official validator and PowerShell assertions for required headings, reference targets, and non-empty UTF-8 content.

- [ ] **Step 2: Inspect the newly created file list**

List files only under the new directory and compare before/after `SKILL.md` counts. Confirm the delta is one.

- [ ] **Step 3: Inspect for unsupported hard claims**

Search the new files for model numbers, units, certificates, and commercial terms. Any such item must be removed or explicitly labelled as pending confirmation with a current-source requirement.
