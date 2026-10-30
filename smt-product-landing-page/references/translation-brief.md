# Translation subagent brief (one per language, run in parallel)

Translate `<product_dir>/i18n/en.json` into <LANGUAGE> (<code>) and write `<product_dir>/i18n/<code>.json`.
- Same keys, every value translated, valid UTF-8 JSON (ensure_ascii=False); verify key parity with python.
- `__meta`: es {"dir":"ltr","label":"Español","short":"ES"}, pt {"Português","PT"}, fr {"Français","FR"}, ar {"dir":"rtl","label":"العربية","short":"AR"}, ru {"Русский","RU"}, zh {"中文","ZH"}.
- Keep untranslated: Southern Machinery, machine/feeder brands and model codes, CCD/LCD/LED, URLs, emails, phone numbers, domains, front-panel key names, numbers and units exactly as written. Arabic keeps Latin script and Western digits for these.
- Industrial B2B tone, correct SMT terms (zh: 飞达, 取料位置, 抛料, 吸嘴, 十字线, 校准尺, 治具). Add no claims.
- Title-like keys (ending t, _h2, _h, title; q{n}) must not contain hook/diagnosis/framework/vehicle/loop/CTA or translations (zh 钩子/诊断/框架/载体/循环/行动号召).
Reply with only the file path and key count.
