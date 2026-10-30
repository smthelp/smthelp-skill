# 多语言指南（i18n-guide）

## 1. 机制

- `i18n/en.json` 是母版：扁平 `key → 纯文本`（用 textContent 渲染，**不要放 HTML**）
- 其他语言 `i18n/<lang>.json` 只放需要翻译的 key；缺的 key 自动回落英文（型号、数字、单位故意不翻：`m1v`、`mc1t`、`spr9v` 等）
- build.py 生成的每个元素带 `data-i18n="key"`（alt 用 `data-i18n-alt`，aria-label 用 `data-i18n-aria`，title 用 `data-i18n-title`）
- runtime.js `applyLang()`：替换文本、`<html lang dir>`、`document.title`、meta description、OG/Twitter，写 localStorage
- 启动顺序：`?lang=` > localStorage > en；主题：localStorage > `prefers-color-scheme`
- 语言顺序固定：en, es, pt, fr, ar, ru, zh（菜单与 hreflang 同序）

## 2. RTL（阿拉伯语）

- `LANG_META["ar"] = rtl`，`<html dir="rtl">`；CSS 用 logical properties（`inset-inline-start`、`border-inline-start`）
- 混排：runtime 的 `isolateRuns()` 给阿拉伯文里的拉丁/数字片段加 U+2066/U+2069 隔离，防 "12.7 mm" 被翻转
- 纯数字/型号值在 product.json 里列入 `metrics.ltr`、`models.ltr_titles`、`spec.ltr`，渲染成 `dir="ltr"`
- FAB tabs 键盘方向在 RTL 下左右互换（runtime 已处理）

## 3. Key 约定（section → key）

| Section | Keys |
|---|---|
| meta | `seo_title` `seo_desc` `seo_keys`(仅 en) `og_title` `og_desc` |
| chrome | `topbar` `brand_sub` `nav_*` `aria_theme` `aria_lang` `aria_menu` `aria_close` `aria_viewer` `aria_wa` `aria_top` `lb_alt` |
| hero | `hero_badge` `hero_h1a` `hero_h1b` `hero_sub` `hero_cta1` `hero_cta2` `hero_note` `hero_cap` + 每张图的 alt key（通常复用 gallery 的 `gN`） |
| metrics / trust | `m{N}v` `m{N}l` / `trust{N}` |
| summary | `sum_kick` `sum_h2` `sum_p` `sf{N}k` `sf{N}v` |
| pain | `why_kick` `why_h2` `why_lead` `w{N}t` `w{N}d` |
| how | `how_kick` `how_h2` `how_lead` `s{N}t` `s{N}d` `how_ev` `how_safe` + legend keys |
| fab | `fab_kick` `fab_h2` `fab_lead` `lab_f` `lab_a` `lab_b` `fab{N}n/f/a/b` |
| models | `models_kick` `models_h2` `models_lead` `mc{N}t/s/d` `fit_h` `fit_c1..3` `fr{N}a/b/c` |
| spec | `spec_kick` `spec_h2` `spec_lead` `sp_c1..3` `ev_v` `ev_c` `ev_t` `spr{N}n` `spr{N}v` `spec_note` |
| disclosure | `disc_kick` `disc_h2` `disc_lead` `dc_c1..4` `dr{N}a/b/c/d` |
| calc | `calc_kick` `calc_h2` `calc_lead` `calc_t` `calc_s` `calc_note` + 每个输入/输出的 key（如 `cf1`、`cr1`） |
| gallery | `gal_kick` `gal_h2` `gal_lead` + 每张图 key（`g1`…） |
| videos | `vid_kick` `vid_h2` `vid_lead` `vf_all` + 每个筛选 key `vid_play`（视频标题保留英文原题，`lang="en"`） |
| blog | `blog_kick` `blog_h2` `blog_lead` `blog_note` `b_read` `b_min` `b{N}t` `b{N}s` |
| docs | `docs_kick` `docs_h2` `docs_lead` `doc_open` `doc_prev` `<key>t` `<key>d` `dk_vb` `dk_vbd` `dk_cb` `dk_cbd` |
| service / faq | `svc_kick` `svc_h2` `sv{N}t/d` / `faq_kick` `faq_h2` `q{N}t` `q{N}a` |
| family | `fam_kick` `fam_h2` + 每个链接 key |
| contact | `ct_kick` `ct_h2` `ct_lead` `wa_btn` `mail_btn` 表单字段 key（`f_name`…）`f_send` `f_note` `f_subject` |
| footer | `foot_about` `foot_h1` 产品链接 key `foot_h2` `fl5..fl8` `foot_h3` `foot_wa` `foot_addr` `foot_browse` `foot_contact` `foot_rights` `soc_lic` `soc_lip` `soc_tw` `soc_fb` `soc_yt` |

## 4. 翻译流程

1. 先定稿 en.json（verify 英文通过后再翻）
2. 逐语言整份翻译（专业术语表：splice/接料、feeder/飞达、radial/立式(径向)、axial/卧式(轴向)、pitch/间距）
3. 翻译后跑 `build.py --check`：会报多余 key、标题禁用词
4. 跑 verify：每种语言 h1 必须与英文不同、无裸 key、标题无禁用词
5. 博客译文可选：`blogs.json` 增加 `"zh": [...]`，结构与 en 一一对应
