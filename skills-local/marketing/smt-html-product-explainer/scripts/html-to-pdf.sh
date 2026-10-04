#!/usr/bin/env bash
# html-to-pdf.sh — Export a self-contained SMT/THT explainer HTML to a print-ready PDF.
#
# Usage:
#   ./html-to-pdf.sh /path/to/explainer.html                # writes <name>.pdf next to it
#   ./html-to-pdf.sh /path/to/explainer.html /path/out.pdf  # explicit output
#
# Requires:
#   - macOS with Google Chrome.app at the default install path
#   - python3 + pymupdf (fitz) for the page-count sanity check
#     (install once with: pip3 install pymupdf)
#
# Behavior:
#   1. Runs Chrome headless with the print-to-pdf flag and a 10s virtual time budget
#      (lets Google Fonts and CSS animations settle before the snapshot)
#   2. Prints page count + per-page size so you can spot pagination issues at a glance
#   3. Exits non-zero if Chrome failed to write the PDF
#
# IMPORTANT: the input HTML MUST contain the @media print hardening block from
# the smt-html-product-explainer skill, otherwise the H1 gradient text will
# render as a solid colored rectangle in the PDF.

set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <input.html> [output.pdf]" >&2
  exit 2
fi

INPUT="$1"
if [[ ! -f "$INPUT" ]]; then
  echo "Error: input file not found: $INPUT" >&2
  exit 2
fi

if [[ $# -eq 2 ]]; then
  OUTPUT="$2"
else
  DIR=$(dirname "$INPUT")
  BASE=$(basename "$INPUT" .html)
  OUTPUT="$DIR/$BASE.pdf"
fi

if [[ ! -x "$CHROME" ]]; then
  echo "Error: Google Chrome not found at $CHROME" >&2
  echo "Install Chrome from https://www.google.com/chrome/ or edit this script's CHROME path." >&2
  exit 3
fi

echo "→ Exporting: $INPUT"
echo "  Output:    $OUTPUT"

"$CHROME" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --hide-scrollbars \
  --print-to-pdf="$OUTPUT" \
  --print-to-pdf-no-header \
  --no-pdf-header-footer \
  --virtual-time-budget=10000 \
  "file://$INPUT" 2>&1 | grep -v "allocator\|task_policy" || true

if [[ ! -f "$OUTPUT" ]]; then
  echo "Error: PDF was not created." >&2
  exit 4
fi

SIZE_BYTES=$(stat -f %z "$OUTPUT" 2>/dev/null || stat -c %s "$OUTPUT")
SIZE_KB=$((SIZE_BYTES / 1024))
echo "✓ PDF created: ${SIZE_KB} KB"

# Page count sanity check via pymupdf
if command -v python3 >/dev/null 2>&1; then
  python3 - <<PYEOF
try:
    import fitz
    doc = fitz.open("$OUTPUT")
    print(f"  pages: {doc.page_count}")
    for i, p in enumerate(doc):
        print(f"    p{i+1}: {p.rect.width:.0f}x{p.rect.height:.0f}pt")
    if doc.page_count == 0:
        print("  WARNING: zero pages — PDF may be empty", flush=True)
        raise SystemExit(5)
    # Check first page is A4
    p0 = doc[0]
    if abs(p0.rect.width - 595) > 5 or abs(p0.rect.height - 842) > 5:
        print(f"  NOTE: page 1 is {p0.rect.width:.0f}x{p0.rect.height:.0f}pt, expected A4 (595x842pt)")
except ImportError:
    print("  (skipped page check: pip3 install pymupdf to enable)")
PYEOF
fi

echo "→ Done. Open with: open '$OUTPUT'"
