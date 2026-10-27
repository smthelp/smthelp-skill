---
name: smt-sample-evaluation-report
description: Turn a customer's boards into a customer-specific evaluation report deck on the SM 16:9 PPT template (EN/PT/...). Two report types - sample_test (one board measured on one machine; capacity, ramp-up, ROI manual vs automation, payback, benefits, BOM fit) and line_evaluation (several boards estimated from PCBA photos or BOMs on a multi-machine line such as radial + odd-form; marked board photos, cycle per machine, line output, bottleneck and balance option, feeder plan per station, component readiness). Use when Jason says 打样结果/样板测试/试产/PCBA 评估/照片评估 + 评估报告/方案/ROI/产能分析/线体配置 for a customer board, or asks for a sample-test report, PCBA evaluation, solution deck or ROI deck for a named customer, or to refresh an old evaluation PPT.
metadata:
  version: 2.1.0
  updated: 2026-10-27
  cases: Zebu ZK50 / S3000 (sample_test); Acuity Brands 4 boards / S-3010 + 3x S-70DL (line_evaluation, reissue of 2020 PCBA Evaluation)
  depends_on: smt-brand-kit (smdeck.py primitives, A4 make_deck.py), learn-SMT-in-3-hours (evidence labels)
---

# SMT Sample Evaluation Report

Customer boards -> one `case.json` -> one calculation -> one slide spec per language -> PPTX (and/or single-file HTML report) -> QA gate.

- `--html` writes `<slug>-<lang>.html` from the same spec (render_html.py): one self-contained page, images embedded, SM logo, dark/light, contents menu, JSON-LD, footer CTA, Chatwoot; speaker notes (sources) are not published. Use `--no-pptx` for HTML only.
- `--customer-alias "LED Driver Manufacturer"` anonymises the report (all text, notes, file names; paths untouched); QA E8 fails if the real name survives. `--slug` sets the file stem (SEO: `<topic>-<alias>-smart-ems-pcb-assembly` style).

| case.json `type` | When | Slides |
|---|---|---|
| `sample_test` (default) | one board was run on one machine; cycle measured | cover, why automate, test evidence, BOM fit, capacity, ramp-up, ROI, payback, why machine, benefits, gallery, specs, assumptions, next steps |
| `line_evaluation` | several boards, estimated from PCBA photos/BOM, multi-machine line (radial + odd-form / axial) | cover, method, proposed line, results table, one marked-photo slide per board, feeder plan, line balance, component readiness, specs, gallery, accuracy & open points, next steps |
Figures are computed once in `calc.py`; every slide number is formatted from that result, never typed by hand.

```
case_dir/case.json + photos/ ─┐
assets/config/defaults.json ──┼─> calc.py -> out/calc.json
assets/machines/<id>.json ────┘        └─> make_spec.py (+ assets/i18n/<lang>.json) -> out/deck-<lang>.json
                                                └─> render16.py (16:9 SM template 202309) | smt-brand-kit make_deck.py (A4)
                                                        └─> out/<slug>-<lang>.pptx + prev-<lang>/ -> qa.py -> out/qa.json, summary.md
```

## Read first
- `references/input-spec.md` - case.json fields, units, where each comes from (test video, program file, BOM, wage law)
- `references/method.md` - every formula, rounding rule and evidence label; the 16-slide report structure
- `references/output-spec.md` - files produced, slide types, delivery checklist
- `references/feedback-log.md` - rules learned from Jason; apply all `done` rules, ask about `open` ones
- Worked examples: `assets/examples/zebu-zk50-s3000/` (sample_test) and `assets/examples/acuity-pcba-line/` (line_evaluation) -> `python3 scripts/run.py <example>`

## Workflow
0. **Refreshing an old evaluation PPT**: read every slide (python-pptx: text, tables, pictures); take board photos with their crop, and read engineer markers (ellipse = radial, rectangle = odd-form/axial) as fractions of the picture into `boards[].markers`; carry the old counts/rates into case.json and list every inconsistency found as a board `note` (never silently fix).
1. **Case folder**: copy the example matching the report type to a new folder (e.g. `output/solutions/<customer>-<board>/case.json`); put chosen photos in `photos/`.
2. **Facts in** (input-spec.md):
   - from the test video/program: cycle seconds per panel, boards per panel, program points per board;
   - from the customer BOM: every part of this process with refs, qty, value, span, polarity; mark parts outside the machine limits `"fit": false`; put other processes (axial, odd-form, SMT) in `out_of_scope`;
   - labour: currency, monthly wage + official source; optional `wage_card` text per language;
   - `params` only where the customer or Jason gave a real value (efficiency, shifts, manual rate, employer factor, running cost). Everything else stays default and is labelled a planning assumption.
   - Never put price, lead time or warranty in case.json.
3. **Ask Jason** only what the files cannot answer - typically: is the cycle per panel or per board; does the test program cover the full BOM; which machine options are offered. Record the answer in case.json (`test`, `open_points`).
4. **Machine**: use `assets/machines/<id>.json`; for a new machine copy `s3000.json` and fill specs/selling points from the latest catalogue only (source field required).
5. **Run**: `python3 scripts/run.py <case_dir> [--langs en,pt] [--layout 16x9|a4]`. Exit 1 = QA or overflow error: fix case/i18n wording (shorten copy), never shrink fonts or hand-edit numbers.
6. **Check**: open every `out/prev-<lang>/*.png`; read `out/summary.md` and `out/qa.json` warnings.
7. **Deliver** the PPTX files with a 2-3 line summary (figures from summary.md); mention open points (e.g. full-BOM cycle to be re-confirmed).
8. **Feedback**: each remark from Jason -> `python3 scripts/feedback.py add <area> "<remark>" --case <slug> --rule "<rule>"`; fold the rule into references/scripts, then `python3 scripts/bump_version.py patch|minor|major "<what changed>"` and push.

## Configurable parameters (assets/config/defaults.json, override in case.json `params`)
| Key | Default | Meaning |
|---|---|---|
| efficiency | 0.85 | line efficiency applied to the measured cycle |
| hours_per_shift / working_days_month / days_per_week | 8 / 22 / 5 | calendar |
| shifts_compare | [1,2,3] | rows in the payback table |
| manual_parts_per_operator_hour | 900 | hand insertion rate |
| employer_factor | 1.8 | wage -> employer cost |
| machine_operators_per_shift | 1 | operators on the machine |
| machine_running_cost_month | 550 | consumables, wear parts, power (case currency) |
| manual_ppm | 2000 | manual insertion defect rate (assumption) |
| ramp | [0.6,0.8,0.95,1.0] | weekly ramp-up rates |
| payback_months | [12,24] | break-even columns |
| layout | 16x9 | 16x9 = SM template 202309; a4 = smt-brand-kit A4 portrait |
| forbidden_patterns | price/lead time/warranty regexes | QA E3 |

## Folder layout
```
SKILL.md                      this guide (metadata.version = current version)
scripts/  run.py calc.py make_spec.py render16.py mark_board.py qa.py bump_version.py feedback.py
references/ input-spec.md method.md output-spec.md feedback-log.md changelog.md
assets/config/defaults.json   parameters      assets/i18n/<lang>.json   wording (en, pt)
assets/machines/<id>.json     machine facts (s3000, s3010, s70dl)   assets/template/          SM PPT template 202309 + template.json
assets/examples/zebu-zk50-s3000/ (sample_test) · assets/examples/acuity-pcba-line/ (line_evaluation)
```

## Version record
`metadata.version` in this file + `references/changelog.md` (newest first) + `references/feedback-log.md` (Jason's remarks -> rules). Every run stamps the version into calc.json, deck specs and summary.md, so any delivered deck can be traced to the skill version that made it.

## Line evaluation inputs (summary - full list in input-spec.md)
- `line`: machine groups `[{"machine": "s3010", "qty": 1}, {"machine": "s70dl", "qty": 3, "stations": ["FS#1","FS#2","FS#3"]}]`; rate = machine file `eval_cph` (or `cph` override).
- `boards[]`: id, pcb, model, boards_per_panel, parts per process per board, photo, markers, feeders per station, optional `qty` override per machine, `note`.
- `evidence: "photo"` requires `accuracy_note` (QA E7). `scripts/mark_board.py` draws the markers (red circle radial, blue box odd-form, amber box axial).

## Rules
- Measured figures come only from the test (video, program, report). Catalogue figures carry the catalogue as source. Everything else is a planning assumption and is listed on the assumptions slide.
- If the test program covered fewer points than the BOM, the report computes on the BOM and states the cycle must be re-confirmed with the full program (QA E4). Never present it as a contractual performance.
- No machine price anywhere; payback is "customer quote ÷ monthly saving".
- Numbers are formatted per language (EN 1,029 / 0.32; PT 1.029 / 0,32). Add a language = add `assets/i18n/<lang>.json` with identical keys (translate with one subagent per language) plus that language in every `{en,pt}` text of case/machine files.
- Every report ends with the disclaimer: the equipment PO specification prevails and SM may adjust after acceptance (from the 2020 evaluation format).
- Missing translations fall back to English and QA warns (W3); translate before sending a non-English deck.
- Template slides kept at the end (after-sales, contact) are translated through `template_text` in the language file.

## Upgrading the skill
- Formula change: edit `calc.py` and `references/method.md` together; re-run the Zebu example and compare `out/summary.md` with the previous version (CHANGELOG lists the reference figures).
- New slide/section: add strings to every `assets/i18n/*.json`, build it in `make_spec.py`, support its type in `render16.py`.
- New template: add a `template.json` (file, layout, drop, keep, safe area, colours) and pass `--template`.
- Always: `scripts/bump_version.py`, one line in references/changelog.md, push to github smthelp/smthelp-skill (and sync the Drive smthelp-Skill folder when connected).
