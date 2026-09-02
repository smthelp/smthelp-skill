# PDF Split / Merge / Search (pymupdf)

pymupdf handles these natively — use `execute_code` or inline Python.

## Split: extract pages 1-5 to a new PDF

```python
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

## Merge multiple PDFs

```python
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

## Search for text across all pages

```python
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

## Notes

- No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.
- For batch processing, wrap in a loop over a directory of PDFs.
