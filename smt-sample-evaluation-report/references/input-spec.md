# Input specification - case.json

One case folder per customer board + machine: `case.json`, `photos/`, and `out/` (generated).
Text that the customer reads is given per language: `{"en": "...", "pt": "..."}` (missing language falls back to en).

| Field | Type / unit | Required | Source | Notes |
|---|---|---|---|---|
| slug | string | yes | - | output file name stem, e.g. `Zebu-ZK50-S3000-Radial-Insertion-Solution` |
| customer, country | string | yes | inquiry | customer name as it may appear to the customer |
| board, board_variant | string | yes | BOM / drawing | e.g. `ZK50`, `ZK50 AUTO` |
| machine | id | yes | - | file in `assets/machines/` (e.g. `s3000`) |
| languages | list | yes | - | e.g. `["en","pt"]`; each needs `assets/i18n/<lang>.json` |
| test.cycle_s_per_panel | s | yes | test video / report | **per panel**; confirm with Jason if per board |
| test.boards_per_panel | int | yes | panel drawing / video | |
| test.program_points_per_board | int | recommended | program file (xls) | if < BOM points the report flags it (QA E4) |
| test.source | string | yes | - | where/when the test was made |
| bom_source | string | yes | BOM file name + revision | |
| bom[] | list | yes | customer BOM | only parts of this process |
| bom[].refs / pn / value / qty | | yes | BOM | qty per board |
| bom[].desc | {lang} | yes | BOM | short component type |
| bom[].span_mm | mm | yes | BOM / datasheet | must be in machine `spans_mm` (QA E5) |
| bom[].lead_mm | mm | optional | datasheet | or give case-level `lead_range_mm: [min,max]` |
| bom[].polarised | bool | optional | BOM polarity column | drives the polarity card |
| bom[].fit | bool | default true | engineer | false = cannot be inserted -> excluded from ppb, shown with — |
| lead_range_mm | [min,max] mm | optional | BOM / datasheets | used when per-part lead_mm is absent |
| out_of_scope | {lang} | recommended | BOM | other processes (axial, odd-form, SMT) |
| labour.currency | string | yes | - | `R$`, `US$`, `€`, `₹` ... |
| labour.monthly_wage | number | yes | official source | statutory minimum or customer's real wage |
| labour.wage_source | string | yes | law / customer | cited in notes |
| labour.wage_card | {lang} | optional | news / law | replaces the generic labour-cost card |
| params | object | optional | customer / Jason | overrides assets/config/defaults.json (see SKILL.md table) |
| photos.cover/why/test/capacity/benefits/assumptions | {src, cap{lang}, focus[x,y]} | recommended | test video frames, customer photos, ph.smthelp.com | check every image visually; caption what it really shows |
| photos.gallery[] | up to 6 {src, cap} | optional | | |
| open_points[] | {lang} | optional | engineer | extra "To be confirmed" lines |

Never include: price, discount, lead time, warranty, customer contact data. QA E3 blocks a `price` field and price/lead-time/warranty text.

## Where the facts come from (typical sample-test pack)
- Test video: cycle time (from panel clamp to release), boards per panel, finished-board shots (frames -> photos/).
- Program file: number of insertion points per board actually programmed.
- Customer BOM: positions, qty, values, spans, polarity; other processes for out_of_scope.
- Wage: official decree / statistics of the customer's country for the current year.
- Machine: latest catalogue -> assets/machines/<id>.json.

# line_evaluation case (type = "line_evaluation")

| Field | Type / unit | Required | Notes |
|---|---|---|---|
| type | "line_evaluation" | yes | |
| slug, customer, country, languages | | yes | `board` = short description of the board family |
| evidence | "photo" / "bom" / "sample" | yes | photo -> accuracy_note required (QA E7) |
| accuracy_note | {lang} | photo: yes | e.g. "Estimated from PCBA photos: about ±5 %..." |
| source | string | yes | photos/BOM received, original evaluation and engineer |
| line[] | {machine, qty, stations[], cph?} | yes | one group per process; `cph` overrides machine `eval_cph` |
| boards[].id / pcb / model | string | yes | PCB number and assembly model as on the board |
| boards[].boards_per_panel | int | yes | |
| boards[].parts | {radial: n, oddform: n, axial: n} | yes | per board |
| boards[].photo | path | yes | panel photo |
| boards[].markers | [{type, x, y, w, h}] fractions | recommended | one board's parts marked; QA W4 compares with parts |
| boards[].feeders | {station: "Tube ×2, tape ×1"} | recommended | odd-form feeder plan |
| boards[].qty | {machine: n} | optional | fewer/more machines for this board |
| boards[].note | {lang} | optional | corrections or doubts vs the source - shown on the board slide and assumptions |
| labour | null or as sample_test | optional | ROI slides need labour (planned for line mode) |
| photos.cover / method / line / readiness / gallery | | recommended | |
| open_points[] | {lang} | optional | |

Reading markers from an old PPT: for each ellipse/rectangle without text on the board-photo slide,
x = (shape.left - picture.left) / picture.width, y likewise with top/height, w = shape.width / picture.width,
h = shape.height / picture.height (picture crop must be applied to the saved photo first).
