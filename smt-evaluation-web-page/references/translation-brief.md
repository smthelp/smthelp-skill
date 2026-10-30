# Translation brief (one sub-agent per 1–2 languages)

Input: `<case>/web/strings_en.json`. Output: `<case>/web/i18n/<lang>.json`, written with `json.dump(..., ensure_ascii=False, indent=1)`.
- Exactly the same keys; every value translated (es neutral Latin American, pt Brazilian, fr, ar Modern Standard with Western digits, ru, zh Simplified).
- Numbers, units, ±, %, ×, ≤, ≥, ~, °, ranges exactly as English (English number format).
- Keep untranslated: brand (Southern Machinery), model names, SMT/THT/PCB/SPD/CCD/CPK/CPH/SMEMA/MES/ESD/BOM/DFM, YouTube, WhatsApp, Windows, aliases (Board 1, Module X).
- Headings must not contain the forbidden words or their translations (vehículo/veículo/véhicule/транспортное средство/车辆 → use car/汽车).
- zh terms: 异形插件机, 插件头, 剪脚打弯, 托盘飞达, 管装飞达, 定制夹爪, 波峰焊, 浮高, 治具, 贴片机, 回流焊, 上板机/下板机.
- No added or dropped information. Verify key set equality before replying.
