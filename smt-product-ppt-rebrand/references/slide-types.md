# Slide types (smbuild.py)

All slides use the template content layout; title is drawn in the header band. Limits come from `config/deck-rules.json`.

| type | required fields | optional | limits |
|---|---|---|---|
| overview | title, lead, apps [[head, text] x3], image | caption, notes | lead <= 230 chars |
| metrics | title, items [[value, label, sub] x3-4] | lead, footer | value <= 11 chars (bigger values wrap) |
| pains | title, lead, items [[head, text] x3-8] | footer | |
| fab | title, rows [[[F head, F text], [A head, A text], [B head, B text]] x2-3] | notes | exactly 3 cells per row |
| process | title, steps [[head, text] x3-8] | lead, images [[file, caption] x<=3], per_row, footer | |
| gallery | title, items [{image, head, body:[2 bullets], fit?}] x2-4 | lead, imgh (in, default 2.9) | fit:true = contain on white |
| beforeafter | title, lead, before, after, caption | side [file, caption] | |
| specs | title, rows [[name, value]] | footer | <= 14 rows |
| brands | title, lead, image, items [[brand, parts]] | | |
| table | title, columns [..], rows [[..]] | widths [..], lead, footer | <= 14 rows; row width = columns |
| video | title, items [{video .mp4, poster .jpg, head, body:[2 bullets]}] x1-2 | lead, vh (in), notes | embedded, plays in PowerPoint |
| summary | title, lead, items [[head, text] x3-4], cta | | always the last body slide |

Snippets:
```json
{"type":"metrics","title":"Key Figures","items":[["50","PCB slots","10 mm pitch"],["35–460 mm","Adjustable width","Full range"]],"footer":"..."}
{"type":"fab","title":"FAB 1 · Protection","rows":[[["Permanent anti-static","10⁶–10⁹ Ω"],["Safe discharge","Controlled"],["Higher yield","Fewer ESD failures"]]]}
{"type":"table","title":"Model Selection Guide","columns":["Model","Size","PCBs"],"widths":[2,3,1],"rows":[["G6601","355 x 320 x 563","50"]]}
```
Adding a slide type = new `s_<type>` function + entry in `TYPES` (+ `NEEDS_A` if it uses images) + rules in deck-rules.json + this table -> minor version bump.
