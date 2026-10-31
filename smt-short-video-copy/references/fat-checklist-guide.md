# Factory acceptance checklist guide

## Files
Two independent XLSX files, rendered by `scripts/build.py`: `<MODEL>_出厂验收检查表_中文.xlsx` and `<MODEL>_Factory_Acceptance_Checklist_EN.xlsx`.
Same item numbers in both (01, 02 … continuous), A4 landscape, header row repeated, page x of y footer, freeze panes.

## Columns
编号 No. · 检查项目 Check item · 验收标准/判定依据 Criterion · 检查方法 Method · 合格 Pass ☐ · 不合格 Fail ☐ · NA ☐ (drop-down ☐/☑) ·
实测值 Measured · 结论 Conclusion (drop-down 合格/不合格/NA) · 检验员 Inspector · 日期 Date · 依据标注 Basis.
Header block: serial no., order no., test fixture/host, ambient temperature, FAT date. Footer: overall result, inspector and QA signatures, SM contact line.

## Sections A–K and the quantified criteria used for S-JVF02 (reuse, adapt per product)
| Section | Typical items | Thresholds (basis) |
|---|---|---|
| A Documents & marking | nameplate, manual, safety labels | nameplate shows model/rating/serial (P+G) |
| B Appearance & structure | finish, overall size, slot width, weight, parts complete | scratch ≤ 5 mm (G); size ±1 mm, slot width ±0.2 mm, weight ±0.2 kg tolerances (P+G); parts list complete (M) |
| C Assembly & fastening | screw torque, paint marks, drive/spring fit, rails, pins | M3 0.5–0.7 N·m, M4 1.2–1.5 N·m (G); play ≤ 0.5 mm (G) |
| D Installation & locking | handlebar travel, install steps, lock security, removal | 10 cycles no sticking (G); axial play ≤ 0.2 mm (G); manual steps (M) |
| E Material fixing | each fixing point, pick-area opening | locating deviation ≤ 0.5 mm (G) |
| F Feeding mechanism | start, dials full travel, speed vs pick cycle, part attitude, belt, noise | ≤ 70 dB(A) at 1 m, background ≤ 50 dB(A) (G); belt → NA when not in parts list (M) |
| G Indicators & sensors | lamp, switch, connector signal, photoelectric sensor | stop ≤ 1 s after switch-off (G); sensor 10/10 if fitted else NA (G) |
| H Electrical & safety | supply voltage, current, ground continuity, insulation, E-stop, wiring, safety rules | 24 V DC ±10 % (P+G); current = W ÷ V calculated; ground ≤ 0.1 Ω; insulation ≥ 1 MΩ @ 250 V DC with electronics disconnected (G, ref. IEC 60204-1 §18.2/18.3 practice) |
| I Spec check | model, voltage, frequency, channels, component range | DC supply → mains Hz NA; values from P |
| J Running test | continuous run, pick test, temperature rise, setting record | 30 min no jam (G); 100 picks/lane 0 feeder-caused failures (G); ≤ ambient + 25 K (G) |
| K Packing | cleanliness, packing, carton marking | (M/G) |

## Rules
- Every criterion quantified where a number exists; otherwise a pass/fail observable ("cannot be pulled out by hand").
- Basis tags: M manual · P product document · G assumed general practice · M+G/P+G documented item with assumed threshold · M+P.
  Every G-containing row is rendered with 【推测】 / [Assumed] and the basis column in red.
- Pressure/stroke/force values the sources do not give are written "(value not published)" — never invented as specs.
- Pneumatic products: add air pressure (e.g. 0.5–0.7 MPa supply, leak check) as P+G rows; belt products: belt tension/tracking rows.
