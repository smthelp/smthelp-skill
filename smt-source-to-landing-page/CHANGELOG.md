# Changelog — smt-source-to-landing-page

格式：`## 版本 — 日期`，下面写改了什么、为什么、来自哪个项目。版本规则见 SKILL.md「升级维护方式」。

## 1.1.0 (PATCH 示例内容) — 2026-10-23

来源项目：Odd-form 插件供料器匹配页修订（Jason 的决定）。只改示例数据与文案，scripts/ 与 templates/ 未改，不升版本号。

- `examples/odd-form-feeder-matcher/`：SBF2002（目录 V03 皮带供料器）与 S-MVF01（往复式皮带供料器，旧资料与视频）是**两个不同型号**、供不同元件：删除各处「是否同一型号待确认」（披露表 6→5 行、7 语言），matcher 新增 feeder `smvf01`（无 envelope，不编规格，链接其落地页），S-MVF01 评估模板的 4 行改挂 S-MVF01；FAQ 第 1 条、family 互链加 S-MVF01
- 32 mm 载带元件「主机自带 32 mm 载带供料器 + Southern Machinery 吸嘴」改为已确认匹配（7 语言）；matcher 新增状态码 `conf`（Confirmed mapping，样式在示例 product.css 的 `.mx-s-conf`，无代码改动）。状态：fit 15 / conf 8 / custom 9 / tbc 10 / fam 34
- 博客 2-8 篇扩写到 371-485 词（六步结构不变，标题无禁用词）
- 新增 `tools/i18n_patch_20261023.py`（把本次改动的 key 写进 6 个译文文件，幂等）
- 经验：新增 matcher 状态码只需 `statuses` + `mx_s_<code>`（7 语言）+ product.css 里一条 `.mx-s-<code>`；非目录型号的行不要用 `fit`（标签是「Fits catalog」）
- 验收：示例重建与发布页逐字节一致；odd-form 页 verify 47/47；regress.sh 34/34

## 1.1.0 — 2026-10-22

来源项目：Odd-form 插件供料器匹配页（Customized Feeder Nozzle Catalog V03，Jason 的需求：元件类型 → 供料器型号快速匹配、NPI 五步选型、Dan Koe 禁用）。

- 新增可选 section `matcher`（build.py `s_matcher` + runtime.js `mxInit` + components.css `.mx-*`）：配置驱动的「元件 → 供料器/吸嘴」查表组件，数据在 `product/matcher.json`（categories / packaging / feeders+envelope / bins / rows），9 个筛选 + 文本搜索 + 计数 + 重置 + 空状态 + 行详情（WhatsApp/邮件预填规格）+ 目录 envelope 自查框 + 手机卡片视图，切语言整表重渲染；build `--check` 校验 matcher 的 key、代码与 feeder 引用；自动生成 feeder `ItemList`（Product）JSON-LD
- 新增可选 section `npi`（`s_npi` + `npiInit` + `.npi-*`）：N 步步骤器 + 每步勾选清单 + 进度条；`{{npi_steps}}` 自动生成 HowTo 步骤
- `hero.cta2_href` 可配置（默认仍是 `#spec`）；runtime 支持 `data-i18n-ph`（placeholder 翻译）；CFG 带上 WhatsApp
- `BANNED` 加入 "dan koe"；SKILL.md / copy-standards.md 写明页面任何标题、正文都不出现方法论作者名
- verify.py：matcher 12 项 + npi 1 项检查，有 npi 时 JSON-LD 必须含 HowTo；matcher/npi 截图；语言循环里顺带收集各语言的 matcher 表头
- 新增第二个示例 `examples/odd-form-feeder-matcher/`（matcher + npi 全量配置与数据生成脚本，重建结果与 2026-10-22 发布页逐字节一致；客户名单不入库）
- 回归：`scripts/regress.sh` 重建接料带示例（不含新组件）verify 34/34 通过；odd-form 页 verify 47/47 通过
- Pitfalls 新增 13-17（表格 min-width、视频标题禁用词、计算器 0 值、阿语括号 bidi、临时截图 load 卡住）

## 1.0.0 — 2026-10-19

首版。来源项目：AI Radial Splicing Tape 落地页（2026-10-13，Jason 的 9 条需求：logo、页脚 CTA、图床图片、视频墙视频、目录墙目录、8 篇六步法博客、Chatwoot、SEO/GEO 文件名、暗黑/明亮 + 7 语言）。

- 参数化构建 `scripts/build.py`：product.json + i18n/*.json + blogs.json → 单 HTML，19 种 section 可选可排序，JSON-LD 自动生成，`asset:` 图片 base64 内嵌，计算器公式写在 config
- `scripts/verify.py`：34 项 Playwright 检查（7 语言持久化、RTL、全语言标题禁用词、JSON-LD 类型、坏图、390 px 横滚 en+ar、主题持久化、交互、Chatwoot 位置、无 CDN），截图 30 张
- `scripts/publish.py`：GitHub 推送到 smthelping/smt-product-landing-html 并更新 README 表格与页数；WebDAV 上传（密码每次现问）
- `scripts/extract_sources.py`、`scripts/scaffold.py`、`scripts/regress.sh`
- `templates/`：base.css（S-300B 设计系统）、components.css、runtime.js（主题 + i18n 引擎 + 组件，新增博客多语言切换、通用表单与计算器）、brand-southern-machinery.json
- `examples/radial-splice-tape/`：重建结果与 2026-10-13 发布页逐段一致（head/JSON-LD 完全相同，body 仅文章容器多 `data-blang` 属性）
- 行为变化：英文版不再显示「文章保持英文」提示（只在非英文且无译文时显示）
