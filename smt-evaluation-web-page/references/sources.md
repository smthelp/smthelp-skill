# Matching sources
- Videos: https://file.autoinsertion.com/public/Southern-Machinery-YouTube-Video-Board.html — parse `data-title` + `data-url`, filter by machine model and process keywords, pick 8 (machine demo, process detail, feeder/gripper, case study).
- Catalogues: https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html — parse `data-original` + `data-url` (decode `&amp;` → `%26` in URLs), pick 6 PDFs/HTML; iframes are allowed.
- Photos: crop from the customer document (render pages at 200 dpi), or ph.smthelp.com (`https://ph.smthelp.com/search/images/?q=TERM`, drop `.md` for full size). Blur customer names/logos and supplier marks (I.C.T, ETON …); view every crop before captioning.
- Scanned PDFs: `pdftoppm -r 200 -png in.pdf p` then `tesseract p-01.png p-01 -l eng`; confirm numbers on the page images.
