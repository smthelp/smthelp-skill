---
name: taobao-to-sm-marketing
description: 把淘宝/天猫/1688 商品页（PDF 或链接）转换成 Southern Machinery 统一品牌风格的英文营销全套物料 - facts 表、SKU 型号表、17 页 PPT、7 语言落地页、宣传片 + Shorts + SEO 文案，以及单独的 USD 价格表。Use when Jason sends Taobao product pages (钢网擦拭纸、刮刀、钢网架 等 SMT 耗材/配件/设备) and asks to 转换为 Southern Machinery 品牌风格营销文案, 做全套物料, 按某店铺价格出报价, or to process all printer brands while keeping original model numbers.
metadata:
  version: 1.0.0
  updated: 2026-11-20
  owner: Jason Wu / Southern Machinery
  depends_on: smt-brand-kit (voice, video), smt-product-ppt-rebrand (PPT), smt-product-landing-page (HTML)
  first_kits: stencil storage rack S-Series, SMT printer squeegees, stencil wiping paper rolls (2026-11-19)
---

# Taobao page -> Southern Machinery marketing kit

一个产品 = 一个 kit 文件夹。事实只写一次（facts.md + models.py），四个渲染器生成全部物料，一个检查门（scrub_check.py）保证没有供应商痕迹。价格永远只放在单独的报价文件里。

## 1. 什么时候用
- Jason 发来淘宝商品页 PDF/链接，要 SM 品牌营销文案、PPT、落地页、视频、报价中任意一项或全套。
- 同类商品多家店铺（例：10 家擦拭纸）→ 合并成一套 SKU，保留原机型（DEK / MPM / GKG / 德森 / 松下 / 雅马哈 …）。
- 不适用：供应商自己的说明书/规格书（用 smt-brand-kit）；只改已有 PPT 模板（用 smt-product-ppt-rebrand）。

## 2. 输入规范
| 输入 | 必需 | 说明 |
|---|---|---|
| 淘宝页 PDF（浏览器“打印为 PDF”）或商品链接 | 是 | 放 `sources/`；系统常会自动抽取到 `files/extracted/<id>/content.md` + images/ |
| 价格依据 | 报价时必需 | 指定店铺（如“按优左的”）+ 取价规则（lowest_variant 卡片最低价 / per_sku 逐规格价） |
| 价格公式 | 默认 | USD = round(CNY × 2 ÷ 6.6)；改动写入 kit.yaml |
| SM 自有资料 | 可选 | SM 旧 PPT/PDF、视频，优先级高于淘宝描述 |
| 型号编码规则 | 可选 | 例：钢网架 S+深/10+高/10+层数+间距；擦拭纸 SM-WP-管长-纸宽-卷长-开口 |
| 联系方式 | 默认 | info@smthelp.com · WhatsApp +86 136 0256 2576 · www.smthelp.com |

缺价格依据时：先做营销物料，报价脚本保持 cny=None 并拒绝渲染，同时问 Jason 一句（店铺 + 取价规则）。

## 3. 输出规范（kit 内 `out/`）
| 文件 | 规范 |
|---|---|
| `facts.md` | 每条事实带来源标签；冲突写 “to be confirmed”；供应商名/商品 id 只出现在这里 |
| `models.py` | `GROUPS`、`ROWS`（group, code, brand, model 原文, size, opening, cny, status, src）、`usd()` |
| `<SEO-slug>-Southern-Machinery.pptx` | 17 页，smt-product-ppt-rebrand `run.py` 必须 PASS |
| `out/landing/<slug>.html` + `videos/` + `SM-<Product>-Landing-Page.zip` | 7 语言 en es pt fr ar ru zh，`check_page.py` OK，含选型表 + FAQ + 计算器 |
| `out/video/SM-<Product>-Promo-EN.mp4`（60-95 s，横版）、`-Shorts-EN.mp4`（20-26 s，竖版）、`.srt`、`-clean.mp4` | ffprobe 确认有 AAC 音轨 |
| `out/video/SM-<Product>-YouTube-SEO-EN.txt` | 3 个标题、描述、章节、标签、联系行 |
| `out/quote/Southern-Machinery-Price-List-<Product>-USD.{xlsx,pdf}` | 唯一允许出现价格的文件；起价说明 + 条款占位 |

文件名用英文 SEO 关键词（产品 + 主要适配品牌 + Southern-Machinery）。

## 4. 可配置参数（`kit.yaml`，模板 `config/config.example.yaml`）
product.name_en / slug / code_prefix · sources.price_shop / price_rule · pricing.markup / fx / incoterm / placeholders · brand.contacts / allow_brands / not_affiliated_line · outputs.ppt.slides / landing.languages / landing.calculator / video 时长 / seo_txt · delivery.drive_parent / github_push。

## 5. 核心流程
0. **建 kit**：`python3 scripts/new_kit.py <project>/work/<product>-kit --name "..." --slug SM-... --prefix SM-XX`，把 PDF 放进 `sources/`。先加载 smt-brand-kit、smt-product-ppt-rebrand、smt-product-landing-page。
1. **抽取**：读 `content.md`；未抽取的大 PDF 用 `pdftotext -l 3` + `pdfimages`。记录每家：店铺（内部）、卡片价、规格列表、适配机型、材质/参数、详情图。
2. **facts.md**：合并多家规格，按品牌归组；读懂尺寸含义（例：410×300×10 m = 管长×纸宽×卷长，不是卷径）；冲突值写 to be confirmed；把新店铺名加入 `config/never_publish.txt`。
3. **models.py**：每个 SKU 一行，保留原机型文字，给 SM 编码，status = listed / single / table；cny 按价格依据填写，否则 None。
4. **图片清洗**：裁掉/模糊 logo、水印、电话、二维码、中文叠字 → `assets/`；逐张看图确认；近似重复图只留一张。
5. **PPT**：照 `templates/kit/spec.example.json` 写 `spec.json`（FAB：Feature → Advantage → Benefit，选型表，材料/工艺，使用步骤，FAQ，联系页）→ ppt-rebrand `run.py spec.json assets out --name <file>.pptx` → 必须 PASS。被拦的兼容品牌名用 `meta.allow_brands`。
6. **视频**：`video-promo.json` / `video-short.json`（照 example）→ smt-brand-kit `make_video.py`；edge-tts 某句 NoAudio 时重跑或改写那一句；ffprobe 查音轨和时长；抽几帧看裁切。写 SEO txt。
7. **落地页**：`landing-src/`：en_strings.py → blogs.py → 翻译 tr/<lang>.txt → tr2json.py → make_product.py → build_page_ext.py → check_page.py → zip，一条命令 `bash landing-src/build_all.sh`（先改脚本里的产品名和 zip 名）。阿语、俄语提醒做母语复核。
8. **报价**：`python3 quote/make_quote.py`（有 cny=None 时拒绝；`--skip-unpriced` 只出已定价行）→ XLSX + PDF（需 `pip install weasyprint openpyxl`）。
9. **检查门**：`python3 scripts/scrub_check.py <kit>` 必须 OK；人工再看：价格只在 quote/，承诺类（交期/质保/现货/认证）为占位或不出现，品牌名旁有 not-affiliated 说明。
10. **交付**：附件发给 Jason + 待确认清单（价格依据、冲突参数、未清洗干净的图）。Drive 上传、GitHub、邮件只在他要求时做。

## 6. 硬规则（不可配置）
- 营销物料中不出现：供应商/店铺名、淘宝/天猫/1688、¥/CNY 价格、店铺电话/QQ、水印、供应商 logo。
- 不发布：价格、交期、质保、“现货”、未有证据的 CE/RoHS/ISO、节省百分比（SM 自有数据须注明“SM figure, depends on …”）。
- 原厂机型只作兼容标识，加 “not affiliated” 一句。
- 不改动 Jason 已给出的价格公式；换算结果四舍五入为整数美元。

## 7. 版本与升级
- `VERSION` + SKILL.md 元数据 + `CHANGELOG.md` 同步，用 `python3 scripts/bump_version.py patch|minor|major "说明" --kit <产品>` 一次完成。
- 每做完一个新产品：把新店铺名补进 never_publish（patch）；新增输出/参数/脚本（minor）；流程或 I/O 改变（major）。把该产品的 facts.md / models.py / spec.json / video json 拷进 `examples/<product>/` 作为参考。
- 已知问题在 CHANGELOG 最新条目里维护。

## 8. 目录结构
```
taobao-to-sm-marketing/
  SKILL.md  VERSION  CHANGELOG.md
  config/config.example.yaml   config/never_publish.txt
  scripts/new_kit.py  scrub_check.py  price_usd.py  bump_version.py
  templates/kit/  spec.example.json  video-*.example.json  quote/make_quote.py  landing-src/*
  examples/squeegee/  examples/wiping-paper/
```
