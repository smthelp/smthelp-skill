# Output specification

`<case_dir>/out/` after `scripts/run.py`:

| File | Content | Use |
|---|---|---|
| calc.json | every raw figure + params + skill_version | audit, reuse in HTML page / email |
| deck-<lang>.json | slide spec (types: cover, cards, steps, table, metrics, gallery, bullets, cta) | edit wording, re-render |
| <slug>-<lang>.pptx | evaluation report deck | deliver to Jason |
| prev-<lang>/NN-type.png | layout preview (approximate fonts) | check before delivery |
| render-<lang>.log | renderer result ("slides N errors 0") | QA E6 |
| qa.json | errors / warnings | must be 0 errors |
| summary.md | key figures + QA | chat reply / email draft |

Re-render one language after hand-editing a spec:
`python3 scripts/render16.py out/deck-pt.json out/<slug>-pt.pptx --preview out/prev-pt`

## Delivery checklist
- [ ] qa.json errors = 0; warnings read and covered on the assumptions slide
- [ ] every preview checked: no overflow, photos match captions, no supplier marks
- [ ] numbers identical across languages (only separators differ)
- [ ] no price / lead time / warranty; payback shown as quote ÷ saving
- [ ] open points (full-BOM cycle etc.) stated in the reply to Jason
