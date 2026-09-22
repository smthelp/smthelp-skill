---
name: macos-pptx-native-build
description: Build, render, QA and merge native editable PPTX decks with PptxGenJS on macOS — the macOS-safe path when cyber-ppt's Windows-only scripts (pywin32 PowerPoint COM merge, python-pptx validate_pptx) don't apply. Use when the user wants a branded, editable slide deck and you are on macOS/LibreOffice, not Windows/PowerPoint.
---

# macOS Native PPTX Build (PptxGenJS + LibreOffice)

cyber-ppt mandates PptxGenJS for Phase 3 and an "import, don't regenerate" merge — but its bundled
`scripts/merge_verified_pages.py` needs `pywin32`+PowerPoint COM and `validate_pptx.py` needs
`python-pptx` (often broken in the Hermes venv). On macOS use this equivalent path.

## Build
- `npm install pptxgenjs` in the build dir. A raster asset (e.g. `build_logo.png`) MUST sit next to
  the script — `addImage` resolves relative to `__dirname`; a missing file throws
  `ERROR: Unable to read media`. Fix: copy the asset in, or `NODE_PATH=/path/to/node_modules`.
- Put shared brand/helpers in one `sm_common.js` (palette, fonts, `header/footer/kpi/bulletList/
  cover/cta` builders) and `require` it from each deck builder so a series stays DRY and identical.

## Render to PNG (review gate)
```bash
soffice --headless --convert-to pdf --outdir render DECK.pptx
pdftoppm -png -r 110 render/DECK.pdf render/slide
```
`soffice` (LibreOffice) is the macOS stand-in for "open in PowerPoint and export PNG".

## Structural QA (no python-pptx)
```python
import zipfile, re
from xml.etree import ElementTree as ET
z = zipfile.ZipFile("DECK.pptx"); W,H = 12192000, 6858000
slides = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',n)],
                key=lambda s:int(re.findall(r'\d+',s)[0]))
overflow = 0
for s in slides:
    root = ET.fromstring(z.read(s))
    for el in root.iter():
        if el.tag.split('}')[-1] in ('sp','pic','grpSp'):
            xf = el.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm')
            if xf is not None:
                x,y,cx,cy = (int(xf.get(a,'0')) for a in ('x','y','cx','cy'))
                if x+cx > W+9525 or y+cy > H+9525 or x < -9525 or y < -9525: overflow += 1
media = len([n for n in z.namelist() if n.startswith('ppt/media/')])
print(f"slides={len(slides)} overflow={overflow} media={media} -> {'PASS' if overflow==0 else 'FAIL'}")
```
Confirms no off-canvas overflow and that text is native (logo is the only expected raster).

## Merge approved single-page decks (import, not regenerate)
Byte-level OOXML import — preserves each slide's XML/theme/media, satisfies cyber-ppt's merge rule.
- Read each deck zip into a dict; seed `merged_media` from the base deck's `ppt/media/*`.
- For each appended `ppt/slides/slideN.xml` + `_rels/slideN.xml.rels`: renumber, copy verbatim;
  for each `Target="ppt/media/..."` in rels, dedupe by md5 (reuse identical bytes) or assign
  `image{k}.ext` (avoid cross-deck collisions) and rewrite the rels Target.
- Add `<Relationship>` to `ppt/_rels/presentation.xml.rels` and `<p:sldId>` to `sldIdLst`; add
  `<Override>` to `[Content_Types].xml` per new slide. Then render to confirm.
- Pitfall: Python 3.9 f-strings can't contain backslashes — precompile regexes
  (`num_re = re.compile(r'(\d+)')`) before using inside f-strings.

## Brand-lock
When the user supplies a logo + brand book, WAIVE cyber-ppt's "8 fixed style samples" gate and lock
the visual system to the supplied palette/typography. Extract via `pdftotext -layout brandbook.pdf`
+ grep for hex/`#`/font names (PIL is often broken). Then drive every deck from the shared
`sm_common.js`.
