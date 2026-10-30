---
name: smt-source-to-landing-page
description: 根据「产品源素材（PDF/1688/淘宝/产品 URL/图片）+ 主题」生成 Southern Machinery 品牌的营销型单文件 HTML 产品 Landing Page：FAB 文案、可选的交互式「元件→供料器/吸嘴」快速匹配表（matcher）与 NPI 步骤器、8 篇六步法博客（页面任何标题禁止出现 Dan Koe 及六步名称）、7 语言（含阿拉伯语 RTL）、暗黑/明亮主题、SEO+GEO、Chatwoot 客服、Playwright 验收，并推送到 smthelping/smt-product-landing-html。参数化构建：新产品只写 product.json + i18n + blogs，不改代码。Use when user gives product source files or links plus a theme and asks for 产品落地页 / Landing Page / 单HTML / 营销页 / 产品页 / product landing page.
version: 1.1.0
---

# SMT Source → Landing Page（源素材到单文件落地页）

把 2026-10-13「AI 立式接料带」项目的完整做法固化为可复现流水线。
母技能 `../smt-product-landing-page/`（v1.6.0）沉淀了 1688 爬取、WebDAV、3D 动画等经验，本技能在其设计系统上做了**参数化**：
`product.json + i18n/*.json + blogs.json (+ matcher.json) → scripts/build.py → 单 HTML → scripts/verify.py（基础 34 项；启用 matcher + npi 时 47 项）→ scripts/publish.py`。

参考实现：`examples/radial-splice-tape/`（重建即得已发布页面，也是回归测试夹具）。matcher/npi 的参考实现：`smthelping/smt-product-landing-html` 的 `feeders-nozzles/odd-form-insertion-customized-feeder-nozzle-catalog-v03-component-matcher-southern-machinery.html`（2026-10-22）。

## 触发条件

触发：
- 用户给出产品源素材（淘宝/1688 PDF、规格书、产品 URL、图片）**和**一个主题，要求做 产品落地页 / Landing Page / 单 HTML / 营销页 / 产品详情页
- 用户说「按接料带那个页面的做法再做一个」「用 skill 生成 xx 的落地页」
- 已有页面要加语言、加博客、换素材后重建（改 product 文件夹后重跑 build）

不触发：
- 只要文案/翻译、不要页面 → 直接写文案
- 只给 1688 链接、要求纯英文无多语言的老式页 → 用母技能 `smt-product-landing-page`
- 网站整站、多页面站点 → 不在本技能范围

## 输入规范

详见 `references/input-spec.md`。

**必需**：产品源素材（至少一种）+ 主题（一句话）。

**可选**（不给用默认）：品牌偏好（logo、颜色、联系方式、社媒）、参考模板 URL、目标仓库/路径、语言、博客篇数（默认 8）、Chatwoot 配置、产品线文件夹、是否 WebDAV 发布。

**Southern Machinery 默认值**（`templates/brand-southern-machinery.json`）：
- Logo `https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`（页眉左上）
- WhatsApp `https://wa.me/8613602562576`，邮箱 `info@smthelp.com`
- 社媒五件套：LinkedIn 公司 `linkedin.com/company/smtmachine`、LinkedIn 个人 `cn.linkedin.com/in/smtsupplier`、Twitter `twitter.com/smtspecialist`、Facebook `facebook.com/autoinsertion`、YouTube `youtube.com/c/Smthelping`
- 机器目录 `file.autoinsertion.com`（Catalog Board / Video Board），机器图片 `ph.smthelp.com`
- Chatwoot：`https://chat.smthelp.com`，token `saMcpgSupcmd1VQwytgPLfbK`，`{"position":"right","type":"standard","launcherTitle":"Southern Machinery Global Support"}`

**Intake 检查**：素材可读 → 主题能写成 H1 与 SEO 文件名 → 产品线文件夹 → 查重（smt-product-landing-html README）→ 价格/店名/他牌水印已识别 → 是否 WebDAV。
缺信息时**最多问 2 个问题**，带默认选项：①「主题按 *X* 做、放 `<line>/`，可以吗？」②「要同时发布到 file.autoinsertion.com 吗？」其余全部用默认值。

## 工作流

工作目录：`work/<slug>/`（product 文件夹 + src/ + dist/ + shots/）。

### 1. 源素材提取
```bash
python3 scripts/extract_sources.py <pdf或文件夹...> --out work/<slug>/src
```
- PDF：`pdftotext -layout` 取文字层；`pdftoppm -r 110` 渲染每页；`pdfimages -png` 抽图。淘宝/1688 打印 PDF 的卖点多在图里 → **逐页读渲染图**
- 产品 URL：web_fetch（smthelp.com 产品页给型号代码、包装、交期、官方卖点）；淘宝详情常登录墙 → 以用户 PDF 为准
- 图片裁切：PIL 裁出产品区域，避开供应商水印；≤800 px、q≈78，放 `assets/`，config 写 `asset:xxx.jpg` 自动 base64 内嵌
- **红线**：价格（¥/元/RMB）、供应商名/店铺名、他牌水印永不上页；`verify.forbidden_terms` 里列出本次的店铺名，build 会扫所有语言
- 所有事实记到 `work/<slug>/NOTES.md`：数字 + 来源；来源冲突的列出来，后面进 disclosure 表

### 2. 资产搜索
- **图片**：`https://ph.smthelp.com/search/images/?q=<关键词>`（curl -L），逐个打开取 og:image 原图；`.md.webp` 作缩略、原图作 lightbox。**每张都目检水印**（曾遇 Southern Electronics、GIANNG、Southern Screen 他家水印 → 弃用）。smthelp.com 产品页的 myqcloud `shop_imgs` 图可用（品牌自有）
- **视频**：抓 Video Board HTML，grep `data-video-id` 与标题关键词（splice / radial / taping …），按 2-4 个分类建筛选；每个 ID 用 oEmbed 验活：`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<ID>&format=json`（404 剔除），标题用 oEmbed 原题，时长取自视频墙
- **目录 PDF**：抓 Catalog Board，grep 产品名/系列名找 PDF（`Southern Machinery Product/`、`Southern Machinery Manual/`、`SMT machine 3D drawing/`），记录大小；页面上给「Open」+「Preview」（iframe 弹窗）
- **同系列页**：`file.autoinsertion.com/public/Product%20landing%20Page/` 里的相关页做 family 互链

### 3. 领域知识
读 `smthelp/smthelp-skill/learn-SMT-in-3-hours`（私有仓库；Jason 的 SMT 三小时课程：curriculum、process-and-operations、troubleshooting-and-maintenance、visual-language）。用它校准工艺术语（radial/axial、pitch、lead span、feeder、splice）与痛点场景，保证文案像工程师写的。

### 4. FAB 文案（i18n/en.json）
按 `references/copy-standards.md`：6 痛点卡 → 4 步 how → 6 组 F/A/B → 型号卡 + 适配表 → 规格表（每行证据标签 v/c/t）→ disclosure → 10 FAQ → 5 步服务。数字优先、无价格、询盘导向。先 `python3 scripts/scaffold.py work/<slug>/product --filename <seo>.html --line <line>` 生成骨架，再**整份重写** en.json（scaffold 保留的是接料带文本，build `--check` 会拦截残留）。

### 4b. 可选：元件→供料器快速匹配表（section `matcher`，1.1.0 起）
适用：需要「元件类型 → 供料器型号/吸嘴」查表的页面（供料器、吸嘴、编带、插件机配套）。组件完全由配置驱动，代码不改：
- `product.json`：`"matcher": {"data": "matcher.json", "check_part": true, "jsonld_itemlist": true}`，并把 `"matcher"` 放进 `sections` 与 `nav`
- `matcher.json`（产品文件夹内，建议用脚本生成，见示例 `tools/make_matcher.py` 的写法）：
  - `categories` / `packaging` / `nozzles` / `statuses` / `sources`：代码表，显示文字全部来自 i18n：`mx_c_<cat>`、`mx_p_<pack>`、`mx_n_<nozzle>`、`mx_s_<status>`、`mx_src_<src>`
  - `feeders[]`：`id, model, page, pack[], env{L,W,H,wt,ld:[min,max]}, envtxt, image?, url?, own?`；文字 `mx_f_<id>n`（名称）、`mx_f_<id>d`（说明）、`mx_fo_<id>`（筛选下拉项）。`own:false` 表示非本公司型号（如主机自带载带供料器），JSON-LD 不挂品牌
  - `bins`：`pitch / size / leads / ld` 区间 `[lo, hi, "标签"]`，判定 `lo < v ≤ hi`
  - `rows[]`：`id, type, spec, cat, pack, L, W, H, OH, pitch, leads, ld, feeder, alt, nozzle, status, note, src`；类型文字 `mx_t_<type>`，备注 `mx_note_<note>`。L ≥ W 为占地尺寸，H 为本体高，OH 为总高；源里没有的值**留空不编**（筛选时由「包含无数据行」复选框决定去留）
- UI 文案 key：`mx_kick/h2/lead/search/search_ph/cat/pack/feeder/pitch/L/W/H/leads/ld/any/unknown/unknown_v/reset/count({n},{total})/empty/note`、`mx_col_*`（10 列）、`mx_d_*`（详情）、`mx_ask_wa/mail/msg/subj`、`mx_chk_*` 与 `mx_cL/cW/cH/cWt/cLd`（自查框）。build `--check` 会列出缺失 key、未声明代码、未知 feeder
- 行为：文本搜索（当前语言 + 英文）、9 个筛选、结果计数、重置、空结果提示；行点击/回车打开详情（供料器说明、目录页码、备注、来源）+ WhatsApp/邮件按钮，消息预填元件规格；自查框按目录 envelope 比对；≤760 px 表格变卡片；切语言整表重渲染；数据以 `<script type="application/json" id="matcherData">` 内嵌
- 状态约定：`fit` 来源评估通过且在目录范围内；`conf` 已确认的匹配但供料器不在目录内（如主机自带载带供料器、非目录型号；示例用 product.css 的 `.mx-s-conf` 着色）；`custom` 来源评估要求定制；`tbc` 超出目录范围或有条件；`fam` 只按包装归族（源无尺寸）。未知映射一律写 To be confirmed
- 红线：客户名、料号、供应商、价格不进 matcher.json；来源用匿名代号（evaluation A/B…）。product.json 的 `verify.forbidden_terms` 可列客户名做扫描，但这类名单只留在 work/，不进 skill 仓库
- 完整示例：`examples/odd-form-feeder-matcher/`（product 文件夹 + `tools/make_matcher.py`、`en_src.py`、`blogs_src.py`，脚本输出到示例文件夹本身）；`python3 scripts/build.py examples/odd-form-feeder-matcher --out /tmp/x` 即可重建 2026-10-23 修订后的发布页

### 4c. 可选：NPI / 选型步骤器（section `npi`，1.1.0 起）
`"npi": {"steps": 5, "checks": [3,3,3,3,3]}`；key：`npi_kick/h2/lead/prev/next/cta/prog({d},{n})`、`n{i}t`、`n{i}d`、`n{i}c{j}`。左侧步骤 tab（键盘方向键、RTL 反向）、右侧说明 + 勾选清单 + 进度条，最后一步按钮跳 `#contact`。`jsonld.howto.step` 写 `"{{npi_steps}}"` 自动生成 HowToStep（含 HowToDirection）。hero 第二个按钮可用 `hero.cta2_href` 指向 `#matcher`。

### 5. 八篇博客（blogs.json）
六步内容法（方法论出自 Dan Koe）：Hook → Diagnosis → Framework → Vehicle → Loop → CTA，每篇 4-6 个小标题、350-600 词。**任何语言的任何标题（含博客小标题、视频标题 h3）都不得出现** "Dan Koe"、hook / diagnosis / framework / vehicle / loop / CTA 及其译词（清单在 copy-standards.md，代码在 build.py `BANNED`；"dan koe" 自 1.1.0 起在清单内）。页面正文也不要写方法论作者名。标题和摘要写进 en.json `b{N}t` / `b{N}s`。注意视频标题也是 h3：YouTube 原标题含 "Vehicle" 等词会触发禁用词检查 → 换一个视频。

### 6. SEO + GEO
按 `references/seo-geo-checklist.md`：SEO 文件名（由原文件名/主题关键词英译）、title ≤70、description 140-200、canonical `https://www.smthelp.com/<filename>`、hreflang ×7 + x-default、OG/Twitter；JSON-LD 由 build 自动生成 Organization / WebPage / Breadcrumb / FAQPage / BlogPosting 列表 / VideoObject 列表，product.json 只补 `jsonld.products`、`howto`、`terms`（DefinedTermSet）、`breadcrumb`。GEO：summary 可引用总结 + 6 条实体事实、FAQ 首句直答、术语定义。

### 7. 多语言（i18n/<lang>.json）
en 定稿 → 翻译 es、pt、fr、ar（RTL）、ru、zh（`references/i18n-guide.md`）。型号/数字 key 不翻（回落英文）。localStorage 记忆语言与主题，`?lang=` 可覆盖，切换时 `<html lang dir>`、title、meta、alt、aria 全同步。博客正文默认英文 + `blog_note` 提示；有译文时在 blogs.json 加对应语言即可自动切换。

### 8. 主题、Chatwoot、披露表
- 暗黑/明亮：base.css 已含完整暗色 token，默认跟随系统，切换后持久
- Chatwoot：build 自动插到 `</body>` 前，强制 https（http 在 https 页是混合内容被拦）
- 来源冲突 → `disclosure` 区（数值 / 来源 A / 来源 B / 处理），单一来源未核实 → `To be confirmed` 标签

### 9. 构建 → 验收 → 目检
```bash
python3 scripts/build.py work/<slug>/product --out work/<slug>/dist        # 有 WARN 必须修
python3 scripts/verify.py work/<slug>/dist/<file>.html --config work/<slug>/product --shots work/<slug>/shots
```
verify 全 PASS 才继续（基础 34 项；matcher 加 12 项：行数、包装筛选减少行数、组合筛选与计数一致、重置、搜索、空状态、详情询盘链接、关闭、自查框、标签全语言已译、390 px 卡片无溢出 en+ar；npi 加 1 项；有 npi 时 JSON-LD 必须含 HowTo。清单见 output-spec.md）。然后**用 read_file 看至少 3 张截图**：`light_top.png`、`ar_middle.png`、`mobile_ar_top.png`（再加 `dark_middle.png`、`sec_gallery.png` 更好；有 matcher 时加看 `light_matcher.png`、`mobile_en_matcher.png`、`ar_matcher.png`），查：文字溢出、对比度、RTL 镜像、图片水印、空白区。verify 单次约 90 秒；shell 有 120 秒上限时用 `nohup … &` 再读日志。

### 10. 保存与推送
```bash
python3 scripts/publish.py github work/<slug>/dist/<file>.html --line <product-line> --title "<页面标题>" --push
```
自动 clone/pull `smthelping/smt-product-landing-html`，复制到 `<line>/`，README 对应表格加/改一行并重算「N pages in M product lines」，commit + push。README 的产品段落说明（一段话）需手工补写。本地副本留在 `work/<slug>/dist/` 并复制到项目 `output/`。Hark 沙盒：git 命令的 shell 调用带 `credentials: [{"provider": "github"}]`；可先 `--dry-run`，补写 README 段落后再手动 commit + push。

### 11. 可选：WebDAV 发布
仅当用户要求：`python3 scripts/publish.py webdav <file> [--dir "Product%20landing%20Page"]`。用户名 smtfile，**密码每次现问（getpass 或 SMFILE_PASS 环境变量），不入库、不写文件、不进日志**；发布后核对公网 200 与字节数，再对公网 URL 跑一次 verify。

## 输出规范

详见 `references/output-spec.md`。要点：
- **单 HTML**：head（meta/OG/hreflang/JSON-LD/内联 CSS）→ header（logo 左上、nav、主题、语言）→ main：hero · metrics · trust · summary · pain · how · matcher · npi · fab · models · spec · disclosure · calc · gallery · videos · blog · docs · service · faq · family · contact → footer（社媒五件套、目录站、图床、视频墙、目录墙、邮箱、WhatsApp）→ 浮层 → runtime → Chatwoot。section 顺序与取舍由 `product.json.sections` 决定
- **响应式**：390 px 无横滚（en+ar），断点 1240/1040/760/640，RTL 镜像，reduced-motion 冻结动画，print 展开全部文章，file:// 双击可用，无 CDN 框架
- **设计文案**：英文母版、数字优先、无价格、询盘导向、无他牌水印/供应商名、证据标签
- **验收**：verify.py 全 PASS + 3 张以上截图目检 + GitHub 推送成功

## Pitfalls（踩过的坑）

1. **Chatwoot 跨域打不开**：`chat.smthelp.com/widget` 返回 `X-Frame-Options: SAMEORIGIN`，在 file.autoinsertion.com、GitHub 等其他域名上气泡能出现但对话窗 iframe 被拒。页面代码无解，需在 Chatwoot 服务器/反代去掉 XFO 或改 `Content-Security-Policy: frame-ancestors` 白名单。verify 只能证明 sdk 已加载
2. **沙盒会清掉 Playwright/Chromium**：重开会话后 `import playwright` 报错。`pip install playwright`；arm64 沙盒里 `playwright install chromium` 被 CDN 403 → `sudo apt-get update && sudo apt-get install -y chromium`（不先 update 会报 Unable to locate package；verify 自动找 `/usr/bin/chromium`）。沙盒浏览器不能过代理认证 → verify 默认用 Python 代取所有请求（`--no-route` 关闭）
3. **导航按钮 CSS 类名冲突**：base.css 里 nav 的「Get a quote」原用类 `.cta`，与联系区大块 `.cta`（渐变底、44px 内边距、两栏 grid）同名，导航按钮被撑成大色块 → 导航按钮改用专用类 `nav.mn a.navcta`（components.css 已含）；新组件起类名前先 grep base.css 查重
4. **吸顶 header 遮挡锚点**：点导航后标题被 sticky header 盖住 → `section[id],[id^="article-"]{scroll-margin-top:84px}`（已含）；改 header 高度要同步改
5. **YouTube uploadDate 拿不到**：Video Board 与 oEmbed 都不给上传日期 → VideoObject 不写 uploadDate，绝不编造（Google 会报"缺少推荐字段"，可接受）
6. **canonical 约定**：统一 `https://www.smthelp.com/<filename>`，hreflang 用 `?lang=xx`；页面实际先在 GitHub/file.autoinsertion.com 也不改，正式迁址时只改 `canonical_base`
7. **他牌水印**：图床同名图可能是别家公司水印，搜到就目检，不确定就弃用
8. **价格泄漏**：淘宝 PDF 每页都有 ¥，build 的价格扫描只查 en.json，翻译后 verify 前再肉眼扫一次
9. **Chatwoot 用户原稿是 http**：一律改 https，否则 https 页面被拦
10. **空 `src=""`** 会被浏览器请求成当前页 → lightbox/iframe 占位不写 src（runtime 已按需赋值）
11. **Python `%` 格式化与 URL 里的 `%20`** 冲突 → URL 只作参数传入模板，不要拼进格式串
12. **shell 120 秒上限**：verify 约 90 秒，大页面可能超时 → `nohup python3 scripts/verify.py … > log 2>&1 &` 后 sleep 再读；别在上一次还没跑完时再起一次（两个进程写同一日志）
13. **base.css 的 `table{min-width:640px}`**：新表格组件在手机上被撑出横滚 → 组件 CSS 里显式 `min-width:0`（matcher 已处理）；10 列以上的桌面表头允许换行、压缩内边距，否则在 1180 px 容器里右侧列被截
14. **视频标题是 h3**：原标题里的 "Vehicle"、"Loop" 等会触发禁用词检查，换视频而不是改标题
15. **计算器输出为 0 时显示 "—"**，verify 的 calc 检查会 FAIL；不要放默认值为 0 的金额输入（也避免暗示价格），只算工时
16. **阿拉伯语混排括号**：「الجسم L × W × H (مم)」这类阿英混排 + 括号会被 bidi 打乱 → 阿语标签去掉括号（如「أبعاد الجسم بالمم L×W×H」）
17. **临时 Playwright 截图卡在 load**：Chatwoot/YouTube 让 load 事件迟迟不来 → 自写脚本用 `wait_until="domcontentloaded"`（verify 已代取请求，不受影响）

## 升级维护方式

- **语义化版本**（frontmatter `version`）：
  - PATCH `1.0.x`：修 bug、改文案标准措辞、加 pitfall，不改 config 格式
  - MINOR `1.x.0`：新增可选 section / 可选 config 字段 / 新检查项，旧 product.json 仍能构建
  - MAJOR `x.0.0`：config 结构不兼容（改 key 约定、改 sections 语义），需写迁移说明并升级 example
- **CHANGELOG.md**：每次变更追加一条（日期、版本、改了什么、为什么、来自哪个项目）
- **每个项目结束后**：在本项目的 NOTES.md 记「这次手工做了而 skill 没覆盖的事」→ 能参数化的进 build/verify/templates，经验进 Pitfalls，文案规律进 references；新的优秀页面可作为 `examples/<slug>/` 第二个夹具
- **回归测试（必做）**：任何 scripts/ 或 templates/ 改动后跑 `bash scripts/regress.sh`：重建接料带示例（不含 matcher，验证新可选组件不影响旧配置）+ verify 34 项全过 + 看截图，才允许 bump 版本和提交
- **同步**：提交到 `smthelp/smthelp-skill-1` 后，QwenWork 端运行仓库根目录 `./sync-skills.sh`（只同步单个 skill 子目录）；Hark 端用 skill create 重新导入 SKILL.md（同名覆盖，保留顶部 Hark 使用说明）
- 母技能 `smt-product-landing-page` 保持不动；两者共用品牌资产，品牌信息变更时两边一起改
