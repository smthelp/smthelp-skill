---
name: smt-product-landing-page
description: 从 1688/产品链接一键生成 Southern Machinery 品牌风格的纯英文外贸单文件产品 Landing Page（FAB 销售模型），覆盖爬取、文案转换、品牌模板渲染、Playwright 双环境校验、WebDAV 发布到 file.autoinsertion.com 与 Puter.js 产品聊天窗。Use when user asks 做产品页/landing page/详情页/1688链接转外贸页/上传 file.autoinsertion.com/product presentation HTML.
version: 1.3.4
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
复制 `assets/reference-s680a.html` 为骨架替换内容；设计系统与组件清单见 `references/design-system.md` 与 `references/required-blocks.md`。硬要求：
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

- v1.3.5：第三张系列页（SMT PCB Buffer Machine，4 链接合并）。新增参考例 `assets/reference-pcb-buffer.html`。再次验证"图床挖宝"打法：搜品类名（buffer）挖到官方规格卡图（EDM300/330/360 完整参数表）+ RoHS 证书 + Board Handling System 家族图，官方规格卡图直接作为 Type A 面板主图兼事实来源（图即 datasheet）。xcrawl 并发 4 连发偶发 fetch failed/timeout → 失败的重试即可，或改 wait_until=load 降超时率。信任锚点三件套模式成型：品牌规格卡 + 认证证书 + 官方家族概览图放 Gallery 前三
- v1.3.4：第二张系列页（SMT ESD PCB Magazine Rack，含 4 链接合并）。新增参考例 `assets/reference-magazine-rack.html` 与 `assets/reference-stencil-rack-series.html`（均为图片占位符版模板，data URI 用正则还原为 {{IMG:name}} 后入库）。新经验：① 图床搜 "certification" 可能挖出 CE/RoHS 证书图（如 magazine rack G6801-G6805 的 HTT CoC）——官方型号+认证事实直接成为页面信任锚点与 series 命名依据，优先用；② 复用上一页模板时抽 `<style>`/`<script>` 块 + 新写 body 拼接，script 里 SYSTEM_PROMPT 用正则整体替换，th/td 手误要在构建时自检；③ Video Board 的卡片带 data-title/data-video-id/data-embed 完整属性，直接 grep article 标签即可拿全；④ gallery 信任块第一张放证书图，转化力强
- v1.3.3：新增系列页打法（4 个 1688 同品类链接合并为一个系列页：SMT Stencil Storage Rack Series，发布于 /public/Product landing Pag/）。新坑：① `.system-detail{display:grid}` 覆盖 UA 的 `[hidden]{display:none}` → tab 面板全堆叠，必须显式写 `.system-detail[hidden]{display:none}`；② zsh `for id in $ids` 不分词导致批量 curl 静默失败 → 用显式命令；③ `VAR=x curl -u "u:$VAR"` 中 $VAR 在展开时尚未设置 → 401，凭据直接写参数；④ verify.py 硬编码找 `#system-name`，自建模板结构不同会 Timeout → 按页结构写 verify_custom.py（断言单面板可见 `d.offsetParent!==null`）；⑤ 本机连不上 YouTube（oEmbed 000 超时非 404）→ Video Board 导出的 ID 视为已验证；⑥ 图床 PNG 拼图转 JPEG 用 ffmpeg `-vf scale -q:v 7`（sips PNG→JPEG 色彩异常）
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
