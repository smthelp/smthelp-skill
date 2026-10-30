# SEO / GEO 检查清单

## 文件名
- 小写、连字符、英文；结构：`<核心关键词>-<规格/变体>-<配套品>-southern-machinery.html`
- 例：`ai-radial-splicing-tape-3-5-6-hole-masking-kraft-paper-splice-cutter-southern-machinery.html`
- 基于原文件名/原标题里的中文关键词翻译成买家搜索词（"三孔/五孔/六孔 美纹纸 牛皮纸 接料带" → `3-5-6-hole-masking-kraft-paper`）

## Head
- [ ] `<title>` ≤ 70 字符（verify 超过 75 警告）：`<产品> <规格> & <配套> | Southern Machinery`
- [ ] meta description 140-200 字符，含 2-3 个核心词与一个数字
- [ ] meta keywords（只英文，10-15 个）
- [ ] canonical：`https://www.smthelp.com/<filename>`（约定：canonical 统一指向 smthelp.com 根路径的同名文件，即使实际先发布在 file.autoinsertion.com 或 GitHub；上线到别的正式地址时改 `canonical_base`）
- [ ] hreflang：每种语言 `?lang=xx` + `x-default`
- [ ] OG：type=product、title、description、url、image（ph.smthelp.com 大图）、image:alt、locale + alternate
- [ ] Twitter：summary_large_image + site @smtspecialist
- [ ] theme-color、color-scheme light dark、robots max-image-preview:large

## JSON-LD @graph（build.py 自动生成 + product.json 补充）
- [ ] Organization（全称、alternateName、logo、foundingDate 2011、email、telephone、address、sameAs 社媒五件套）
- [ ] WebPage（inLanguage 全语言、datePublished、mainEntity → Product、speakable `.sump` `.fqs .ans`）
- [ ] BreadcrumbList（品牌 → 品类 → 本页）
- [ ] Product ×N（主产品 + 配套品；brand、manufacturer、model、material、additionalProperty；**无 offers/price**）
- [ ] HowTo（tool、supply、step 与 how 区同源）
- [ ] FAQPage（与页面 FAQ 同源）
- [ ] ItemList of BlogPosting（headline、description、url #article-N、wordCount、articleBody）
- [ ] ItemList of VideoObject（name、thumbnailUrl、embedUrl、duration；**不写 uploadDate**，视频墙不提供，禁止编造）
- [ ] DefinedTermSet（4-6 个术语）

## GEO
- [ ] summary 框可独立引用；6 条实体事实
- [ ] FAQ 答案首句直给结论 + 数字
- [ ] 证据标签与 disclosure 表让引用者知道哪些数字已核实
- [ ] 内链：family 区互链同系列页（file.autoinsertion.com Product landing Page 目录）
- [ ] 外链：smthelp.com 产品页、目录 PDF、视频墙、目录墙
