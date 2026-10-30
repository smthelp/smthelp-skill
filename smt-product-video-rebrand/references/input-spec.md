# Input specification

## A. What Jason provides
| Input | Required | Form | Notes |
|---|---|---|---|
| Product source clips | yes | Drive folder / file links | any orientation; 720p+ preferred; originals are never modified |
| Official facts source | yes | landing page URL, brochure PDF, spec sheet | the only basis for claims |
| Themes | yes | list of N topics (one video each), optional English title per topic | title is a suggestion; may be shortened to 40-70 chars or hedged |
| Output folder | no | Drive folder id | default: the source folder |
| Brand preferences | no | free text | mapped to project.json / brand_overrides (below) |
| Extra footage per theme | no | clips | asked for when a theme has no footage |

## B. project.json (one per product) - schema: config/project.schema.json
| Key | Example | Use |
|---|---|---|
| product.model | X3100 | Southern Machinery model, never the supplier's |
| product.name | X-ray SMD component counter | generic search term |
| product.chip | SMART EMS X3100 | blank-slide label, thumbnail chip (<= 24 chars) |
| product.tag | SMART EMS X3100 · X-RAY SMD COMPONENT COUNTER | top-right tag, intro kicker |
| product.footer_cta / outro_headline | Free trial count with your own reels | bottom-left CTA / outro card headline |
| product.outro_line | Smart EMS X3100 ... · Shenzhen Southern Machinery, since 2011 | small line on outro card |
| product.outro_chapter | Free trial count & contact | last chapter label |
| file_prefix | x3100-x-ray-smd-counter | SEO file names |
| default_intro_shot | ["F14", 4.0] | intro still when a video has none |
| landing_page / landing_label / utm_prefix | URL / "X3100 specifications, FAQ and quotation request" / x3100 | description link `?utm_source=youtube&utm_medium=video&utm_campaign=<utm_prefix>-<topic>` |
| desc_cta / desc_disclaimer | "Enquiries and free trial count with your own reels" | description line 2 / footer note |
| outro_text | spoken outro, may use {whatsapp_display} {web} | |
| primary_keyword | x-ray smd counter | lint warns if missing from tags |
| pronunciations | [["X3100","X thirty-one hundred"]] | regex -> spoken text, before brand.json list |
| forbidden_claims | regex list | lint error if found in narration, callouts or SEO |
| example_only_patterns | ["99\\.99 ?%"] | lint warns unless the same text says example/brochure |
| drive_folder_id, doc_title | | delivery |
| logo, brand_overrides | | optional brand changes (deep-merged over brand.json) |

## C. content/<batch>.py
```python
OUTRO_TEXT = "Want to see it ...? WhatsApp +86 136 0256 2576, or visit smthelp.com."
SLIDES = {'howitworks': dict(type='flow', kicker='HOW IT WORKS', heading='Three steps',
                             steps=[('Load','up to 4 reels'),('Count','one X-ray shot'),('Label','and upload')], hl=1)}
VIDEOS = [dict(
  slug='mes-erp-integration', topic='mes-erp-integration', kicker='SMART EMS X3100 · MES / ERP',
  title='MES and ERP integration for smart SMT inventory',      # right-panel title (<= 60 chars)
  intro_title='X-ray counting +\nMES / ERP integration',          # 2 lines, <= 22 chars each
  intro_shot=('F22', 0.8), music=1, mirror=False,                 # optional
  # optional overrides: page, outro, outro_head, footer_cta, desc_cta, outro_ch
  scenes=[dict(ch='Why counts must reach your MES', vis=['F16h','F2z','slide:howitworks'],
               co=dict(k='SMART INVENTORY', h='A count only helps once your system knows it', b=['...','...'], stat=None),
               text="Two or three spoken sentences. This is also the subtitle text.")])]
SEO = {'mes-erp-integration': dict(title=..., kw=..., summary=..., tags=[...13-15], hashtags=[...2-5],
                                   thumb='MES / ERP\nINTEGRATION', thumb_hi='MES', thumb_shot=('F22', 0.8))}
NOTES = ['production note shown in the copy doc', ...]
SOURCES = [('name', 'url', 'what it supports'), ...]
```
`vis` items: shot ids from shots.py or `slide:<id>` (`blank`, a key of SLIDES, or an id handled by content/slides.py).
Durations are automatic: each scene lasts as long as its narration (+0.45 s), footage gets ~0.75x speed, slides fill the rest (min 3 s each, min 1.6 s per shot).

## D. Slide types (SLIDES entries)
| type | keys |
|---|---|
| rows | rows=[str], numbered |
| stat | stat (<= 10 chars), sub, foot |
| formula | lines=[(label, value)], hl_last, foot |
| flow | steps=[(title, sub)], hl (index), foot |
| split | left=(HEAD,[items]), right=(HEAD,[items]), foot |
| table | header=[..], rows=[(..)], widths, foot |
| grid | cards=[(big, label)], icons=[reel/tube/tray/bag/loose/tape/chip/cable/bolt/plastic/honey or None], foot |
| bars | bars=[(label, 0-1, note)], foot |
All take kicker (CAPS) and heading (<= 40 chars). Progressive builds (rows, flow, table, bars) reveal one item per step.
