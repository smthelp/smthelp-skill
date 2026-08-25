---
name: smt-product-landing-page
description: 从 1688/产品链接一键生成 Southern Machinery 品牌风格的纯英文外贸单文件产品 Landing Page（FAB 销售模型），覆盖爬取、文案转换、品牌模板渲染、Playwright 双环境校验、WebDAV 发布到 file.autoinsertion.com 与 Puter.js 产品聊天窗。Use when user asks 做产品页/landing page/详情页/1688链接转外贸页/上传 file.autoinsertion.com/product presentation HTML.
version: 1.6.0
---

# SMT Product Landing Page Factory

把「1688 产品链接 → Southern Machinery 品牌英文 Landing Page → 线上发布实测」固化为可复用流程。v1.0.0 由 S-680A SMT Reel Scrap Tape Cutter 项目沉淀。

## 适用场景

- 用户给出 1688/供应商链接或产品型号，要求生成外贸产品页 / landing page / product presentation HTML
- 要求 Southern Machinery 品牌风格、FAB 销售模型、纯英文、单文件、双击可用
- 要求发布到 file.autoinsertion.com 并实测（含 AI 聊天窗）

## 前置条件

1. 爬虫：workspace venv 内的 crawl4ai-skill（系统 pip 受 PEP668 限制）。若无：`python3 -m venv venv && ./venv/bin/pip install crawl4ai-skill && ./venv/bin/crawl4ai-skill setup`
2. WebDAV 凭据：file.autoinsertion.com 上传走 `https://file.autoinsertion.com/dav/`，`/dav/<目录>` 对应网站 `/public/<目录>`。用户名 smtfile，**密码每次向用户索取，不入库、不写进任何文件**
3. 品牌资产速查：Logo `https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`；WhatsApp `https://wa.me/8613602562576`；邮箱 info@smthelp.com；社媒五件套（LinkedIn 公司/个人、Twitter、Facebook、YouTube）与 catalog/ph 站点链接见 `references/required-blocks.md`

## 工作流（7 步）

### 1. Intake
确认：产品型号与英文品名、1688/参考链接、目标保存路径（用户选定文件夹）、是否覆盖旧文件（覆盖前必备份到 workspace）。

### 2. Crawl
```bash
./venv/bin/crawl4ai-skill crawl "<1688-url>" --format raw_markdown --timeout 120 --include-metadata -o product.md
```
注意：CLI 只有 `--wait-for`，没有 `--wait-until/--delay`（SKILL 文档曾误写）。1688 详情区 lazy-load 常爬空 → 必须下载主图（cbu01.alicdn.com/img/ibank/... 去掉 `_.webp` 后缀）并用 Read 逐张看图提取事实（适配机型、卖点文案、控制面板细节）。

### 3. 资产审计
- 品牌图优先用 ph.smthelp.com 已有图；供应商 alicdn 图**禁止直接外链**（防盗链：带 Referer 请求返回 403，线上必碎图）→ 经 WebDAV 自托管到 `/public/<产品目录>/images/` 后引用自有 URL
- YouTube 视频用 oEmbed 校验存活：`curl "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<ID>&format=json"`，404 即剔除
- 交叉核对旧版页面/记忆中的规格，冲突时以爬取+图片证据为准，拿不准写 qualification 注释

### 4. 文案（FAB + 外贸转化）
按 `references/fab-copy-framework.md`：先痛点共鸣（6 卡），再 6 组 Feature→Advantage→Benefit（feature 写真实参数、advantage 写技术含义、benefit 写"对客户意味着什么"：省人/防错/提效/过审）；数字优先（76 mm/s、<70 dB、4× blade life）；信任区（出口国、成立年份、24h 报价）；FAQ 覆盖 tape 兼容/适配机型/操作/维护/安全/报价流程。纯英文，术语顺手解释。

### 5. 渲染
复制 `assets/reference-s680a.html` 为骨架替换内容；设计系统与组件清单见 `references/design-system.md` 与 `references/required-blocks.md`。**多页批量**：直接 `from lp_helpers import ...`（内置 `scripts/lp_helpers.py`，import 前设 `READY_DIR` 环境变量指向压缩图目录；FAB stations 与聊天 system prompt 走 `<script type="application/json">` 数据块，无转义坑），批次脚本只写页面 dict 调 `assemble(...)`。硬要求：
- 单文件、原生 HTML/CSS/JS（禁 Tailwind CDN），双击 file:// 可用
- Header 左上 Logo；Footer 含全部指定 CTA；WhatsApp FAB + CTA 按钮
- Puter.js 聊天窗：**仅 http/https 动态注入** `https://js.puter.com/v2/`，file:// 给联系兜底文案（否则 Puter 弹阻断式错误框毁掉双击体验）；90s 超时降级
- 视频 click-to-load（youtube-nocookie 式懒加载 iframe）、gallery lightbox、spec 表、离线提示、reduced-motion、print 样式

### 6. 校验
`scripts/verify.py <file-or-http-url>`（Playwright，用 workspace venv 的 python）：断言无 pageerror、无 broken img、无 HTTP≥400；截图 top/fab/gallery/footer 并**用 Read 目检**；http 环境额外验证 Puter 加载（首次提问弹 puter.com 登录窗属正常）。

### 7. 发布
```bash
SMFILE_PASS='<用户提供>' bash scripts/publish_webdav.sh "<本地html>" "Southern%20Machinery%20Product/<文件名>.html"
# 新目录先 MKCOL；图片同法上传到 .../images/
```
发布后 curl 公网 URL 核对 200 与字节数，再跑 `verify.py <https-url>`。

## Pitfalls

- Puter.js 在 file:// 弹 "Unsupported Protocol" 阻断框 → 动态加载 + 兜底，绝不静态引 script
- alicdn 防盗链 403 → 图片自托管；顺带避免暴露货源
- 系统 pip 被 PEP668 挡 → venv；crawl4ai 需先 `crawl4ai-skill setup` 装浏览器
- 覆盖用户旧页前必备份到 workspace 并告知路径
- 1688 价格（¥6000 等）是内贸参考，外贸页不写价格，引导询盘
- 空 `src=""` 的 img 会被浏览器请求成页面 URL → lightbox 占位图不要写 src 属性

## 验证清单

- [ ] file:// 打开：无阻断框、无 console error、tabs/lightbox/chat/视频按钮可点
- [ ] https 打开：零 403、零坏图、聊天窗 http 模式正常
- [ ] 公网 URL 200 且 size 与本地一致
- [ ] 页脚 CTA、Logo、WhatsApp 链接逐一核对与需求逐字一致

## 版本与迭代

- v1.6.0：清洗机家族批次（PCBA Fixture & Pallet Cleaning、SME-6300 Inline、SME5600D Batch、S-168 Brush 四页，全 base64 内嵌 + WebDAV 发布）。新能力：① **Chatwoot 智能客服**固定右下角：`window.chatwootSettings={"position":"right","type":"standard","launcherTitle":"Southern Machinery Global Support"}` + sdk 注入 **https://chat.smthelp.com**（http 在 https 页混合内容被拦），token `saMcpgSupcmd1VQwytgPLfbK`，`</body>` 前插脚本；② **3D 交互式工作原理动画**两种形态：批量腔体（立方体 6 面 + 旋转篮筐 basket-ring/post + 水滴 + 热波）和三腔体产线（WASH/RINSE/DRY 并排 + 板沿传送带移动 + 旋转毛刷 brushSpin + 气泡 + 热波）；交互 JS：pointerdown/move 拖拽旋转 + wheel 缩放 + auto-rotate toggle（`cube.classList.toggle('auto')` + `@keyframes spin3d`）+ `prefers-reduced-motion` 全部冻结；③ 坑：Python 源码里三引号字符串互相嵌套（`'''` 内嵌 `"""`）易踩 "unterminated triple-quoted string" → 大块替换内容写独立 .txt 文件读取；④ 坑：替换 `HERO = hero([...])` 调用块时只删到 `\n]` 会残留旧参数尾（`), "old eyebrow"...`）→ 用 `src.find('")', i)` 找 hero-note 串尾再 `find('\n\n')` 定位整块；⑤ 清洗机家族共享 ph 图：ph-pcba-cleaning-room / ph-pallet-batch / ph-air-blower（图床无 SME5600/S-168 专图）；⑥ 视频映射：SME-5200→9HBoNAb1Is4/z44XY1Nk0PQ/gaBQ5wjoJz0/0Q9slVY3eG4，SME-6300→Tu3ObkB9bQw/QeBL1s5fL_8/tCdZgJu6oMw/DTVppmKrAK0，SME5600D→QeBL1s5fL_8/tCdZgJu6oMw/z44XY1Nk0PQ/bi24UcdIYNM，S-168→yWO-fxwpoq8/Tu3ObkB9bQw/tCdZgJu6oMw/QeBL1s5fL_8（DTVppmKrAK 无尾 0 失效、DTVppmKrAK0 存活，oEmbed 逐个验）；⑦ 参考模板 SME6300-PCBA-Cleaning-Machine-Landing.html 在服务器 Product landing Page/；SME-6300 2020 / SME5600D 2021 / SCM5600 手册 / S-168 手册均已传 Southern Machinery Product/。
- v1.4.8：批次6 沉淀（S-300B 全自动高速成型编带机独立页 + 批次5系列页更新互链）。经验：① 新批次产品属于已有系列页家族时，除新子页外**回写更新系列页**（选型卡+链接，重新生成发布），保持家族互链完整；② DOCX 附件可能是演示讲稿而非规格（S-300B 的 docx 是 PPT 讲稿含市场数据，规格在 PDF）→ docx 用 zipfile 解 word/document.xml 提取；③ 无规格 PDF 的型号（S-120FC 等）在系列页以品名+范围呈现；④ S-300B 视频沿用编带家族映射（8gsWp7j6UJA/_ixWTgu1ejM/m2Mytl5D1EU）。
- v1.4.7：批次5 沉淀（SMD 编带机：SJL80A 半自动 + 自动成型编带家族 S-120FC/S-250ART/S-300BSTD/S-300RT/S-350/S-60TP）。经验：① 4 个 1688 链接**整批全被登录墙拦截**（首见）→ 先问 Jason 是否「本地素材先做」，确认后基于附件 PDF + 图床家族图构建；② 规格表数值冲突（PDF 文本层 L170×W60×H60 vs 渲染 OCR L375×W40×H40）→ 以文本层为准并放大核对 spec 单元格；③ 图床有图无规格 PDF 的家族型号（S-120FC 等）以品名+产品范围呈现 + qualification「规格按图纸另询」；④ 编带视频映射：_ixWTgu1ejM（散装转径向编带）/m2Mytl5D1EU（电容编带极性检测）/8gsWp7j6UJA（大电容自动编带）/djJ8zjSwZpY（卷带拼接）/CMoQ-RQWKkQ（HD 拼接演示）。
- v1.4.6：`doc_band`（文档目录卡，批次2 定义）正式入库 `scripts/lp_helpers.py`，至此组件库 = 13 区块 + options/roi/install/doc 四卡；批次4 沉淀（SM-650 视觉旗舰 BGA 返修台 ← ZM-R7220A、SR-430A 光学对位 ← ZM-B750、系列页 BGA Rework）。经验：① 服务器缺的产品 PDF 先补传 `Southern Machinery Product/` 再引用（S-B001/S-B002 本例）；② 手册类在 `Southern Machinery Manual/`；③ BGA 视频仅 3 条（VREGTSBDvGA/N-JNx4txhU0/81UVQBKF2io）页面可共用；④ 图床无返修台直拍图时品牌图全用官方 PDF 渲染页。
- v1.4.5：新增三个页面板块组件进 `scripts/lp_helpers.py`：`options_band`（设备选项建议 6 卡）、`roi_band`（暗底 4 数字 + ROI 说明）、`install_band`（安装指南 5 步 + utility chips）；批次3 沉淀（S-C5331R 双工位焊锡机器人 ← 双头双工位焊锡机、S-HX331R 四轴旋转 ← 六轴恒温双拼焊锡机、系列页 Soldering Automation）。经验：① 用户要求"设备选项建议/ROI/安装指南"时用这三个组件，导航加 #options/#install 锚点；② 批次脚本里的 HTML 长字符串含 URL-encoded `%20` 时不能用 `%` 格式化（Python 把 %2 当占位符）→ 用 f-string 或 .replace；③ 2.5MB+ base64 页线上 goto 可能超 30s → Playwright `set_default_navigation_timeout(90000)` + `wait_until="domcontentloaded"`；④ 手册类 PDF（User manual V7.3）在 `Southern Machinery Manual/` 目录，与产品 PDF 分开放。焊锡视频映射：S-C5331R→O8SMPKIl3AY/HX4TqtlSyFY/AWCtEGKPIgU/TpZOkBJHWvc；S-HX331R→qY7Se7SfPFk/Z6SWUVstVBw/LrYkWNavimQ/D441-8WGwAY；系列页→AWCtEGKPIgU/qY7Se7SfPFk/O8SMPKIl3AY/TpZOkBJHWvc。
- v1.4.4：把批量渲染器沉淀为内置模块 `scripts/lp_helpers.py`（含 13 个页面区块组件 + assemble；`READY_DIR` 环境变量指定压缩图目录；REF 模板路径改为相对 skill 目录，跨机器可用）；渲染步骤文档同步更新。批次脚本范式：设 READY_DIR → import lp_helpers → 写页面 dict → assemble 输出单文件 base64 页。
- v1.4.3：批次2 两个独立单页（S7020T 端子/AC弹片 ← IST-M6000-2、S7900 Odd Form ← DD-8600 在线端子机）。沉淀：① 1688 主图 banner 常带与 SKU 规格表不同的第二套参数 → 以 SKU 规格表为准，banner 数字只进 qualification；② 批量复用：把渲染器抽成 lp_helpers.py（READY_DIR 环境变量指定图片目录），新批次脚本只写页面 dict；③ 新增 doc_band 文档目录卡组件（3 张 PDF 卡+Open the PDF 按钮），放在 FAQ 前、导航加 Catalogs 锚点；④ 图床 S7020/S7900 图均为 Southern 自家水印（smthelp.com）可直接内嵌；⑤ 规格冲突处理示例：S7020T 页官方 datasheet（12,000 CPH/380×280/1200kg）为主表，1688 平台数据为 Production reference 副表。
- v1.4.2：Radial 系列页+2 子页（S3000 经济型 ← 1688 714770702134 / S3010A 高性能 ← 1066739310954，全图 base64 内嵌单文件发布 Product landing Page/）。沉淀：① 用户要求"图片全部内嵌 html"时走 base64 data URI（每页 25 图≈2.6MB 可接受），无需 WebDAV 自托管 alicdn 图；② 模板化时把 FAB stations 与 SYSTEM_PROMPT 放 `<script type="application/json">` 数据块，JS 里 JSON.parse，彻底规避撇号/引号转义坑；③ ph.smthelp.com 搜 "S3000" 命中的 CAD 渲染图带供应商水印 "GIANNG www.cn-guang.com" 必须弃用（Read 目检发现），S3000 真机图以官方 PDF p1 裁切为准；④ 发布前 grep 校验 `tel:+86` href 数字与页脚逐位一致（曾生成 62576 多打一个 6）；⑤ 系列页 lineup 卡互链子页（相对文件名），子页 footer 互链系列页；⑥ Radial 视频映射：S3000→WP61N6pmDJU/NUvAg0JvGYY/0iKa7qjICCg/51JqMMJlVA4，S3010A→jI5O2w86n1A/Y6v_U97S_Ho/xSHWpqCgaoQ/EXbYdskdXkM，系列页→NUvAg0JvGYY/T5JxQTrP27I/4O5ZjZ5CwAg（全存活）。
- v1.5.0：PCB Conveyor 综合单文件页（7 个 1688 链接主题：接驳台，5 个被验证码墙 → 用 2 个成功爬取 + 本地目录）。新能力：① **图片 base64 内嵌**（用户要求"所有图片嵌入 html"）——PIL resize ≤800px q78 → data URI，HTML 用 `DATA:assets/x.jpg` 占位 + 正则替换，FAB stations 数组里的 `image: 'path'` 也要一并替换；② 模板新增 4 个区块占位符：%%ANIMATION%%（工作原理 CSS 动画：机器→皮带→缓冲→下机，PCB keyframes 移动 + 传感器闪烁，prefers-reduced-motion 冻结）、%%ROI%%（暗色带 ROI 数字 + 备注）、%%OPTIONS%%（设备选型建议表）、%%INSTALL%%（安装指南步骤，参考 S-460C 手册：场地/水平/接线 SMEMA/皮带检查/试运行）；③ 坑：Python 三引号字符串尾逗号会把变量变 tuple 导致 replace 报错（CTA/PAIN 中过招），构建后 AST 检查 tuple；④ 目录服务器状态核对：S-350C/SFBC05/S350C serial 已在线，Dual Link Conveyor.pdf 需上传。S-460C 手册参数：板 50×50–460×460mm、高 900±20mm、速度 0.5–12m/min、SMEMA 信号 Y2/CM2 X1/GND Y3/COM3 X2/GND。
- v1.4.1：Feeder/Nozzle 批量页（系列页+编带飞达+Samsung 标签飞达）。淘宝 item.taobao.com 详情页登录墙（PC+H5+Playwright 均跳登录），crawl4ai 抓不到 → 直接请用户提供商品标题+主图；1688 详情页可爬。图床搜图关键词：feeder/nozzle/gripper nozzle/solder chip feeder 命中多张品牌图。Feeder Nozzle Catalog V03 及各型号（SAF1001/SLF100X/SBF1001/STF1003/STP1001...）PDF 已在服务器 Southern Machinery Product/ 可直接引用。YouTube 匹配：label feeder(Oh9W9qnHpjE/KxhQlW6qhpY)、axial tape feeder(JmYHPfN69yY/OCPt-18Lmrk/bOYijZA4Msc)、nozzle(cbvWhqnld2M/RJt3nJx21oQ/nKkwd9ooJGw) 全存活。
- v1.4.0：新增多页批量构建模式（ESD 挂篮车系列页+3 子页沉淀）。reference HTML 转 `%%占位符%%` 模板 + Python dict 渲染 N 页。新坑：① stations 数组占位符后残留模板的 `];` → JS 报 `Unexpected token ]`（占位符替换后逐页 grep 校验 JS 括号平衡）；② section-head（pain/gallery/videos/service）、静态 FAB 内容（system-image/system-name/fab-rows）、chat placeholder/greeting 必须全部模板化，否则泄漏上一产品文案（如 S-680A）；③ meta 块替换时误留双 `<style><style>` → :root CSS 变量失效 → `.btn.light` 白字白底不可见（用 computed style 排查：`getComputedStyle(document.documentElement).getPropertyValue('--teal-dark')` 为空即中招）；④ 视频/图库/聊天交互用 Playwright 实测（click .video-load → iframe 数、lightbox open/close、chat intro 文案）。多源图片策略：品牌 PDF 页转 JPG（pymupdf dpi 110 + PIL q82）+ ph.smthelp.com 图 + 1688 实拍图（带中文营销字的可作 gallery，hero 慎用）统一放 `esd-trolley-assets/images/` 相对路径引用，file:// 与 https 通吃。ESD 系列页视频选题：ESD PCB Magazine Rack install/assembly、SMT PCB magazine、AGV trolley、feeder cart（oEmbed 全存活）。
- v1.3.2：新增 `assets/reference-ai-splice-tape.html`（耗材类，AI 接料带 Radial/Axial Lead）。新坑：图床唯一 AI 接料带图水印是 "Southern Electronics"（他家公司）→ 弃用；图床无正确水印接料带图时，可裁切 1688 实拍图的自托管（避开供应商 DHR/ESOCOO 水印区）+ 图床正确水印的工具/推车/接料机图组合。参考图纸 PDF（Universal Instruments C24782000）可 WebDAV 自托管后作为 catalog 卡
- v1.3.1：新增 `assets/reference-splice-tape.html`（耗材类，多源组合：SMT Splice Tape Leader Tape）。新踩坑：JS 单引号字符串内不能出现未转义的撇号（feeder's 会语法错误）→ 用无撇号写法。多源组合打法：1688 给规格 → ph.smthelp.com 搜图（关键词 splice/接料）→ YouTube Video Board 里 grep `data-video-id`/`data-embed` 找匹配视频（youtube-nocookie embed）→ Catalog Board 里 grep 产品名找 PDF（如 Splice Tape and Splice tools.pdf）
- v1.3.0：新增 `assets/reference-pcb-router.html`（机器类：S300AS Desktop PCB Router Separator）。机器类内容模式：hero 轮播 → signals → 痛点(手工 vs 自动对比) → 工艺 dark band(四步流程) → FAB 六组 → specs 全表 → gallery → service flow(免费打样/配置/培训/售后/质保) → FAQ。价值锚点用"手工 ~60 板/时 vs 自动 ~120 板/时"的量化对比。无已验证 YouTube 视频时不放视频区（页脚仍链频道）
- v1.2.2：三页（S-680A/wiper/claw）统一换图床真实照 + hero 轮播。要点：图床选图必须 Read 目检水印（曾遇到 w13 是 "Southern Screen" 他家水印，弃用）；FAB 卡 JS 里 `image: IMG + '短名'` 的拼接写法替换时不会命中全 URL，需单独映射；S-680A 的 s680a-install-*（alicdn 裁图）已被图床机图/产线实拍替换
- v1.2.1：图床换图 + hero 轮播。ph.smthelp.com 是 Chevereto 图床，搜索走 `https://ph.smthelp.com/search/images/?q=<词>`（需 -L 跟随 301），逐页抓 og:image 拿原图直链；换图时品牌图优先 ph.smthelp.com 真实产品图（自带品牌水印，可直接外链），全页统一替换。Hero 轮播模式：6 张绝对定位 img + `heroFade 36s` 交错 animation-delay（6s×6），active 段 opacity .8 实现"半透明"；`prefers-reduced-motion` 下冻结为第一张静态图
- v1.2.0：新增 `assets/reference-titanium-claws.html`（备件类参考例：Wave Soldering Titanium Claws Fingers）。备件页与机器/耗材页差异：服务流用品牌 3-step match（Identify/Verify/Replicate 50/90/100%）；规格可引原始图纸（如 Vitronics Dover Soltec L 423210 drawing GSC#5721-1）；**本地 mp4 视频可 WebDAV 自托管 + click-to-load `<video>`（readyState 实测可播，无需 YouTube）**；NotebookLM 生成 deck 的 PDF 常把整页渲染成一张内嵌图，需 Pillow 裁切图区；/Volumes 挂载点会掉线，素材读取优先 MOVESPEED 副本
- v1.1.0：新增 `assets/reference-wiper-paper.html`（耗材类参考例：SMT Stencil Cleaning Wiper Paper Roll）。耗材页与机器页差异：无视频区；增加 "Why It Matters" 工艺背书区（wet/vacuum/dry + 转移效率数字，可引 IPC APEX 论文）与 Fit Guide 兼容表；图片来源可自品牌 PDF 用 pymupdf 抽取 + Pillow 裁切（1688 主图常带中文营销字，不宜直接用）
- 每次流程/模板变更：`qwenwork_skill_manage patch` 更新本文 + bump version
- 备份 zip 命名 `smt-product-landing-page-v<version>.zip`（zip 整个技能目录；改后缀 .skill 可直接安装到他机）
- 新产品的成功页面可回灌为 assets/ 新参考例
