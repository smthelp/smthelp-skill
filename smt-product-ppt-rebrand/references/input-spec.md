# Input specification

## Inputs to the skill
| Input | Required | Notes |
|---|---|---|
| Drive folder id or local files | yes | PDF, PPTX, PPT. Other types ignored. |
| Scope | no | "all products" or a list of models; default = one deck per product line found |
| Audience / language | no | default overseas EMS engineers, English (`config/deck-rules.json`) |
| Template | no | default `assets/template/southern-machinery-template-202309.pptx` |
| Date label | no | default current month, e.g. "October 2026" |

## spec.json (one per deck)
```json
{
 "meta":  {"title": "SEO title", "subject": "one line", "keywords": "comma, separated, search, terms"},
 "title": {"eyebrow": "ESD STORAGE", "name": "Product Name — Model", "subtitle": "...", "tagline": "A · B · C",
           "date": "October 2026", "image": "hero.jpg", "notes": "..."},
 "contents": [["Product Overview", "What it is and where it is used"], ["...", "..."]],
 "slides": [ {"type": "overview", "...": "..."}, {"type": "summary", "...": "..."} ]
}
```
- `contents`: 4-6 pairs [heading, one-line description].
- `slides`: 5-14 body slides, last one `summary`; field details in `slide-types.md`.
- Image fields are file names inside the assets directory passed to `run.py`.
- `notes` on any slide = speaker notes (sources, conflicts). Never shown on the slide.

## facts.md (working file, not validated)
Per product line: models, parameter table, features, applications, claims, images chosen, conflicts and how resolved.
