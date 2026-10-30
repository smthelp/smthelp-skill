# Feedback log

One entry per piece of feedback. Status open -> done once the rule is in the skill.

### FB-004 [workflow] done - 2026-10-26
- Case: Acuity-Brands
- Feedback: 参考 2020 S-70DL PCBA Evaluation（Acuity）和 202309 模板，把 skill 优化更新为全新版本
- Rule: Support line_evaluation (multi-board, multi-machine, photo markers, feeder plan, balance) and reissue old evaluation PPTs on the 202309 template
- Applied: line_evaluation type: calc.compute_line, make_spec.build_line, render16 board slide, mark_board.py, qa E7/W3/W4, machines s3010/s70dl, Acuity example; v2.0.0 (2026-10-26)

### FB-003 [template] done - 2026-10-20
- Case: Zebu-ZK50-S3000
- Feedback: 把 PPT 修改为附件模板（Southern Machinery PPT template 202309）
- Rule: default layout 16x9 on assets/template/sm-template-202309.pptx; keep its after-sales + contact slides at the end, translated per language.
- Done: render16.py + template.json, v1.0.0

### FB-002 [facts] done - 2026-10-19
- Case: Zebu-ZK50-S3000
- Feedback: 按真实 BOM 计算：11 radial/board，22/panel；7 s 按 2 板拼板计
- Rule: compute on the BOM; cycle is per panel; if the test program had fewer points, flag "to be confirmed" (QA E4).
- Done: calc.py / qa.py, v1.0.0

### FB-001 [facts] done - 2026-10-19
- Case: Zebu-ZK50-S3000
- Feedback: 不显示机器价格，回本 = 客户报价 ÷ 月节省
- Rule: never publish price; payback table shows savings recovered in 12/24 months.
- Done: make_spec.py payback slide + QA E3, v1.0.0

