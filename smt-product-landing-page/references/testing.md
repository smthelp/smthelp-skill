# Runtime test without a browser
The sandbox usually has no headless Chrome. Use jsdom:
```bash
mkdir -p /tmp/jt && cd /tmp/jt && npm i jsdom@24 --silent
```
Test script outline: load the page with the chatwoot script removed, `runScripts:'dangerously'`, stub `matchMedia`; click `#langBtn` then `#langMenu button[data-lang="zh"]`, click `#themeBtn`; read localStorage, create a second JSDOM seeded with those values and assert lang/theme persist; switch to `ar` and assert `dir=rtl`; set calculator inputs and dispatch `input`; count `.vid`, `.post`, `.galgrid figure`.
Guard browser APIs with `typeof X === "function"` (jsdom and old browsers lack IntersectionObserver).
