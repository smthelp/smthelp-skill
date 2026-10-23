# Error handling

| Code | Where | Meaning | Action |
|---|---|---|---|
| X01 | extract | unsupported type (.ppt not converted, .doc, video) | run convert_ppt.sh; skip non-deck files and list them in the delivery |
| X02 | extract | file unreadable / corrupt / encrypted | try Drive export to PDF; else skip and report |
| NEEDS_VISUAL_READ | extract | image-only PDF | open contact sheet / page images and read tables visually; never guess numbers |
| E10 | validate | missing key / empty field | fill from sources, or drop the slide |
| E11 | validate | required slide type missing / unknown type / summary not last | fix structure |
| E12 | validate | too many / too few items | split slide (e.g. Model Selection 1/2) or trim |
| E13 | validate | FAB row not 3 cells / table row width mismatch | fix data |
| E14 | validate | placeholder text (TBD, XXX, 待定) | replace with source facts or remove |
| E15 | validate | third-party brand name | rewrite neutrally |
| E16 | validate | Chinese text | translate |
| E17 | validate | image file missing | fix path / re-extract |
| W20/W21 | validate | long title/lead/metric value | shorten (wrap risk) |
| B01 | build | python-pptx exception | read traceback; usually a malformed field |
| Q01-Q03 | qa | slide count, closing slides, empty placeholder | rebuild; check template indices in brand.json |
| Q04 | qa | shape outside slide | adjust spec / layout |
| Q05 | qa | run not in brand font | bug in a new slide function - use `_font()` |
| Q06 | qa | core properties empty | fill spec.meta |
| Q07/Q08 | qa | name not SEO / file too big | seo_name.py / shrink images |
| R01 | render | no LibreOffice and no Drive access | deliver with QA pass, say visual check pending |
| Drive 4xx/5xx | upload/render | transient API error | retry once, then report |

Source conflicts are not errors: resolve (most specific source wins), note in slide notes, report to Jason.
Loop guard: if the same fix fails twice, stop and ask Jason one concrete question.
