# Pre-delivery checklist

Automated — `scripts/check_page.py <html> --case <case>` must print all PASS:
- [ ] single file, no external stylesheet / script src
- [ ] only whitelisted hosts referenced
- [ ] report images and logo inlined
- [ ] viewport meta, semantic tags (header, nav, main, section, footer)
- [ ] every language present, 100 % key coverage
- [ ] numbers identical across languages
- [ ] no forbidden words in headings
- [ ] no redact terms, no prices
- [ ] Chatwoot token, hreflang per language, JSON-LD parses, size < 3 MB

Smoke test — `node scripts/smoke_test.js <html>`: all languages switch, ar → rtl, theme toggles, blog modal opens, counts of sections/videos/docs/blogs/bars as expected.

Manual:
- [ ] every derived number recomputed; conflicts listed under "Accuracy & open points" and tagged To be confirmed
- [ ] customer alias, board/part aliases consistent in all slides and blogs
- [ ] photos checked visually: no customer name/logo, no supplier marks, captions match
- [ ] no contacts, terms, delivery country, competitor brand
- [ ] open points sent to Jason as questions with the delivery
