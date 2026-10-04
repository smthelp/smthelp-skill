# PDF Generation Pipeline — Exact Recipe

## Why this exists

Single-page A4 ROI PDFs for SMT/THT B2B sales need:
- Pixel-precise canvas control (7 boxed sections on one A4 page)
- No external font assets (offline-friendly, no FOUT)
- Fast iteration (re-render + visual QA in < 10s)
- Bypass Homebrew Python's PEP 668 protection

**reportlab** is the only library that ticks all four. `pdflatex` / `wkhtmltopdf` / `weasyprint` all have CJK font / boxed-layout issues that make the 7-section design impractical.

## The exact commands (copy-paste, run in order)

```bash
# Step 1: Create isolated venv (NEVER use system pip — Homebrew Python blocks it)
python3 -m venv /tmp/pdfenv

# Step 2: Install the two libraries you need
/tmp/pdfenv/bin/pip install reportlab pypdfium2 --quiet

# Step 3: Generate the PDF
/tmp/pdfenv/bin/python3 build_roi_pdf.py
# → produces /Users/jasonwu/Downloads/S-70LD_ROI_WhiteGoods_Controller.pdf

# Step 4: Render preview PNG for visual QA
/tmp/pdfenv/bin/python3 -c "
import pypdfium2 as pdfium
pdf = pdfium.PdfDocument('/Users/jasonwu/Downloads/S-70LD_ROI_WhiteGoods_Controller.pdf')
pdf[0].render(scale=2.0).to_pil().save('/tmp/preview.png')
print('Pages:', len(pdf))
"

# Step 5: Visual QA — load the PNG into vision_analyze
# Then iterate on the reportlab script and re-run from Step 3.
```

Total time: **< 10 seconds** per iteration. Budget 3 iterations per PDF.

## Known failure modes (and fixes)

### Failure 1: `pip install reportlab` fails with "pass the --user flag"

**Cause:** Homebrew Python 3.12+ enforces PEP 668 — no system pip installs.

**Fix:** Use the venv recipe above. If you must use system pip, pass `--break-system-packages`, but this will break Homebrew's Python. **Do not do this.**

### Failure 2: `from reportlab.platypus import Table, TableStyle` fails

**Cause:** Missing import in the script. The reportlab package exposes the low-level `canvas` API at `reportlab.pdfgen.canvas` and the high-level flowables at `reportlab.platypus`. You need **both** for this design.

**Fix:** Add to script header:
```python
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import simpleSplit
```

### Failure 3: PDF renders but the layout is broken (text overlaps, off-page, wrong size)

**Cause:** Skipped visual QA. Reportlab will silently produce a malformed PDF.

**Fix:** Always run Step 4 + Step 5. Common issues:
- Two text blocks drawn at the same y coordinate → use the y-tracking pattern (decrement y after each line)
- Table column widths sum > 168mm (A4 - 2×12mm margins) → measure with `colWidths=[...]` and verify sum
- Card body text longer than card height → use `simpleSplit()` to wrap, then count wrapped lines × line-height, and set card height to fit

### Failure 4: PDF is > 1 page

**Cause:** Total content height > 297mm (A4 height). Often the Why-Us cards or the table overflow.

**Fix:** Use `c.showPage()` exactly once at the end. If the table is too tall, reduce font from 8.5pt to 8pt, or split into 2 stacked tables. Verify with:
```python
from pypdf import PdfReader
print(len(PdfReader("out.pdf").pages))  # must be 1
```

### Failure 5: CJK characters render as squares/empty

**Cause:** Helvetica is a Latin-only font.

**Fix:** Register a TTF before drawing:
```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('NotoCJK', '/Library/Fonts/NotoSansCJK-Regular.ttc'))
c.setFont('NotoCJK', 10)
```

For pure-English one-pagers (which is the standard for the white-goods / automotive / EU verticals), Helvetica + Helvetica-Bold is correct and avoids the CJK complication.

### Failure 6: vision_analyze can't see the image

**Cause:** PNG file path not accessible to the vision tool.

**Fix:** Save the preview to `/tmp/preview.png` (or `/Users/jasonwu/Downloads/..._preview.png`), then call `vision_analyze(image_url='/tmp/preview.png', question='...')`. The vision tool accepts both absolute paths and URLs.

## The visual QA loop (in 4 lines)

```python
# 1. Build
subprocess.run(['/tmp/pdfenv/bin/python3', 'build_pdf.py'], check=True)

# 2. Render preview
subprocess.run(['/tmp/pdfenv/bin/python3', '-c', '''
import pypdfium2 as pdfium
pdf = pdfium.PdfDocument("out.pdf")[0].render(scale=2.0).to_pil()
pdf.save("/tmp/preview.png")
'''], check=True)

# 3. Visually inspect (in the agent loop, this is vision_analyze)

# 4. Fix, then go to step 1
```

A typical one-pager takes **3 iterations** to nail: first pass has 2-3 layout problems, second pass has 0-1, third pass is clean.

## When NOT to use this pipeline

- **Multi-page brochures or datasheets** → use Word/InDesign + PDF export, or `fpdf2` for a simpler multi-page route
- **Charts and data viz** → use `matplotlib` + `PdfPages` for chart-heavy reports
- **Form-fillable PDFs** → use `pdfkit` + an HTML form template
- **CJK-heavy content** → register a TTF first, or use a different design

This pipeline is purpose-built for the single-page A4 ROI / leave-behind use case. Don't generalize it.
