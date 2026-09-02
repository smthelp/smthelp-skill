---
name: pdf-tools
description: "PDF operations: extract text via OCR (pymupdf, marker-pdf), edit text via natural-language prompts (nano-pdf), split/merge/search via pymupdf, and the always-first `web_extract` path for remote URLs. Class-level umbrella for everything PDF-related. Use when the user says 'read this PDF', 'extract text from this scan', 'fix a typo in this PDF', 'merge these PDFs', or 'search across this PDF'."
metadata:
  source: hermes
  origin: "productivity/pdf-tools"
---
# PDF Tools (Class-Level Umbrella)

Class-level umbrella for PDF operations. Three concerns covered:

1. **Read / extract** — `references/extraction.md` (pymupdf, marker-pdf, `web_extract`)
2. **Edit** — `references/editing.md` (nano-pdf NL-prompt editing)
3. **Split / merge / search** — `references/manipulation.md` (pymupdf)

For the full reference content of each section, load the corresponding `references/<topic>.md`.

## When to Use

- "Read this PDF" / "extract text from this PDF" → Section 1 (extraction)
- "Edit this PDF" / "fix a typo in this PDF" / "change a title" → Section 2 (editing)
- "Split this PDF" / "merge these PDFs" / "search across this PDF" → Section 3 (manipulation)

## Decision Flow (the most-asked PDF question)

**"Read this PDF for me"** — pick the right path:

```
Is the document available as a URL?
├── YES → use web_extract (handles PDF→markdown via Firecrawl, no local deps)
└── NO / local file
    ├── Is it text-based (selectable text when opened in Preview)?
    │   ├── YES → pymupdf (instant, ~25MB install)
    │   └── NO (scanned / image-based) → marker-pdf (~3-5GB, supports OCR)
    └── Need equations / LaTeX / forms / complex layout?
        ├── YES → marker-pdf
        └── NO → pymupdf is fine
```

**"Edit this PDF"** — nano-pdf is the only NL-driven option; otherwise fall back to:
- For text edits in small regions: pymupdf inline
- For complex layout edits: open in Preview/Acrobat manually

**"Split / merge / search"** — pymupdf covers all three natively.

## Common Prerequisites

```bash
# For extraction (lightweight)
pip install pymupdf pymupdf4llm

# For OCR / scanned docs / equations (heavy, ~3-5GB)
pip install marker-pdf

# For NL editing
uv pip install nano-pdf
```

## Common Pitfalls

- **Always try `web_extract` first for URLs** — it handles PDF-to-markdown with no local deps. Only fall back to local extraction if `web_extract` fails.
- **marker-pdf needs ~5GB free disk** — check first with `python scripts/extract_marker.py --check` and warn the user if disk is low.
- **nano-pdf requires an LLM API key** — check `nano-pdf --help` for the config option.
- **Page numbers may be 0-based or 1-based** — if the edit hits the wrong page, retry with ±1.

## References

| File | Covers |
|---|---|
| `references/extraction.md` | pymupdf (text-based PDF, instant) vs marker-pdf (scanned/OCR, 3-5GB). Decision flow + helper scripts + arxiv shortcut. |
| `references/editing.md` | nano-pdf NL-prompt editing. Page numbering, API key config, output verification. |
| `references/manipulation.md` | pymupdf for split/merge/search inline Python recipes. |
| `references/extraction-fallback.md` | **When `vision_analyze` is unavailable** (`No LLM provider configured for task=vision`): probe text-vs-image PDF with `pdftotext -layout`, then `pdftoppm` + `tesseract --psm 6` OCR chain; xlsx read via terminal `python3` heredoc when `execute_code` is blocked; multi-product-library consolidation strategy. |

> Note: if the vision LLM is not configured, do NOT retry `vision_analyze` — go straight to the `pdftoppm`+`tesseract` chain in `extraction-fallback.md`.
