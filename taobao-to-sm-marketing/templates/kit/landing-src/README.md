# SMT Stencil Wiping Paper Rolls landing page (built 2026-11-19)
Rebuild: `bash landing-src/build_all.sh` (from anywhere).
- en_strings.py -> landing/i18n/en.json; blogs.py -> landing/blogs.json
- tr/<lang>.new.txt (new strings) + squeegee-kit tr/<lang>.txt (identical English strings, map tr/reuse-map.json) -> merge_tr.py -> tr/<lang>.txt -> tr2json.py -> landing/i18n/<lang>.json
- make_product.py -> landing/product.json (self-hosted promo/Shorts from out/video/, 540 px CRF 30 + posters)
- build_page_ext.py = skill build_page.py v1.2.0 + Size selector section (SIZE rows, op_*/sz_* keys) + calc_mode "rolls" (wiping-roll consumption planner)
- Output: out/landing/<file>.html + videos/, zip out/SM-Stencil-Wiping-Paper-Landing-Page.zip
Translations written directly by the build agent (no parallel subagents available).
