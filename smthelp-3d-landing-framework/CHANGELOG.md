# Changelog

本 skill 的版本记录。改动必须同步 `SKILL.md` 的 `version` 字段。
版本规则见 `references/05-upgrade-playbook.md` §5。

---

## 1.4.0 — 2026-09-06 · 发布管线（GitHub + Pages）

**核心目标**：补上「生成之后怎么上线」这一环。新增 `references/09-deploy-github-pages.md`。

**实测踩到的 8 个坑（已写进 09 号文档）**

1. **`gh` 登录的是 `smthelp`，对 `smthelp111/*` 只有 pull 无 push** —— 跨账号仓库必须用目标账号自己的 PAT
2. 本机无 SSH 密钥（`~/.ssh` 无 `.pub`），SSH 路线不可行
3. **PAT 长度校验**：经典 PAT 必须 40 位（`ghp_` + 36）。收到 24 位 token 时应先验证再动手，
   否则会白跑一轮推送。验证命令：`curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user`
4. 克隆时把 token 写进 remote URL，后续 `git push` 无需重复输凭据、不触发审批
5. 网盘同步卷会生成 AppleDouble `._*` 垃圾文件 → `.gitignore` 加 `._*` 兜底
6. HTML 落盘后 Notion 注入 `data-page-node-id`（约 695 处 / +30 KB），推送前必须 `re.sub` 清掉
7. **该仓库 Pages 源是 `master` 而非 `main`**，且 `master` / `gh-pages` 上已有
   `s100b-southern-machinery-3d-landing.html`（另一机型）—— 不要覆盖
8. **改完 Pages 源不会自动重建**，必须 `git commit --allow-empty` + push 触发，约 25 秒后生效

**已知待办（写进 09 号文档 §5）**
- canonical 指向 `www.SMThelp.com/products/...`，与 Pages 实际地址不一致，每次部署前需确认
- Chatwoot `baseUrl` 为 `http://chat.smthelp.com`，Pages 是 HTTPS，混合内容会被浏览器拦截

---

## 1.3.0 — 2026-09-06 · 真实素材接入 + 视频/目录/图床资源管线 + Dan Koe 博客 + SEO 命名

**核心目标**：从「可发布的框架」升级为「能直接 SEO 引流的成品页」。
围绕 S-WS450 落地页 v2 实装了一整套外部资源接入。

**真实素材接入（取代工程剖视 SVG 占位）**
- Hero 主视觉：S-WS450 官方视频 ID `dEeBOEpMoec`（168s 工业 4.0 全景），maxresdefault 缩略图 + 点击弹 lightbox 嵌入 youtube-nocookie iframe
- Marquee 12 张：同类别 + 邻近类别各 6 张的真实频道缩略图，每张链到 YouTube 完整视频
- 新增 Videos 区块：featured + 6 张过程视频网格，覆盖 process / setup / yield / QA 四类
- 新增 Downloads 区块：6 张直接链接到 file.autoinsertion.com 的 PDF / 3D 浏览器图
  （S-WS450 PC User Manual / S-WS450A install steps / S-WS450C product sheet / 2 张工艺控制 PDF / 1 张 3D 浏览器图）

**公司社媒 + 资源站 Footer**
- LinkedIn Company / LinkedIn Profile / Twitter / Facebook / YouTube Channel 五条链接
- Resources 列：file.autoinsertion.com（机器目录） + ph.smthelp.com（产品图库） + www.SMThelp.com + email + WhatsApp
- Meta 行：© + 工厂地址 + CE / CCC / UL / ISO 9001 认证

**Chatwoot 客服集成**
- 全局右下角 SDK，`chat.smthelp.com` 自托管，token `saMcpgSupcmd1VQwytgPLfbK`
- 脚本 `<head>` 内加载；不写降级提示（脚本静默失败即可，海外用户正常）
- 本机网络下 DNS 黑洞（198.18.0.80）会使 SDK 不加载，对生产环境无影响

**Dan Koe 6 步法博客 ×3（嵌入页面，原生 details 折叠）**
- 01 Joint quality — "Grey, dull joints after the wave? It's rarely the alloy"
- 02 Heavy boards — "Why a 450 kg solder pot changes everything on heavy boards"
- 03 Line integration — "Add THT to your SMT line in three answers, not three months"
- 每篇严格 5 段（CTA 集中到全页 quote 区块）：Hook→Diagnosis→Framework→Vehicle→Loop
- **标题硬约束**：禁止出现 hook / diagnosis / framework / vehicle / loop / cta 6 个词
  （grep 校验已写进 08 号文档 §7）
- 350–550 字/篇，引用至少 2 个 S-WS450 已确认参数（不引用 On request）
- 三篇覆盖 Joint quality / Heavy board / Line integration 三个不抢流量的搜索意图

**SEO 优化（文件名 + 元数据 + Schema.org）**
- 文件名：`s-ws450-wave-soldering-machine-450mm-pcb-lead-free-dual-wave.html`（slug + 双关主词）
- title：`S-WS450 Wave Soldering Machine | 450 mm PCB, Dual Wave, Lead-Free | Southern Machinery`
- meta description 155 字符内，含 5 个关键数字
- canonical：`https://www.SMThelp.com/products/wave-soldering/s-ws450`
- Schema.org Product（含 offers 0 美元 + InStock，明确不发价）
- OG + Twitter Card（image 与 Schema 同源，maxresdefault.jpg 1280×720）

**ph.smthelp.com 不可达回退方案（本机网络问题）**
- 实测三个 DNS（8.8.8.8 / 1.1.1.1 / 223.5.5.5）都把 ph.smthelp.com / smthelp.com 解析到 `198.18.0.80`（黑洞 IP）
- 本机预览与海外访问是两套结果：海外用 ph.smthelp.com 是正常图床；本机只能用 YouTube 缩略图作为回退
- 每个 `<img>` 保留 `data-ph-asset="<ph.smthelp.com 路径>"` 作为"将来切换"的索引
- Hero 缩略图用 `maxresdefault.jpg`，`onerror` 回退 `hqdefault.jpg`（maxres 命中率约 60%）
- Logo 用 `file.aismt.kdns.fr/raw/Southern%20Machinery%20logo.png`（实测 200，1020×283 PNG）

**新增 references**
- `07-resource-pipeline.md`：YouTube Video Board + Product Catalog Board 抓取模式、
  ph.smthelp.com 不可达回退、Chatwoot 接入、SEO 命名规则、Footer 资源约定
- `08-dan-koe-blog.md`：六步法段落映射、标题硬约束（6 词禁列）、折叠实现、
  选题三指标、发布前自检清单

**新发现坑**
- Notion 工作区同步会自动往每个 HTML 元素注入 `data-page-node-id="<Notion block id>"`
  属性（约 +30% 文件大小、零功能性），写完落盘后用 `re.sub(r'\s*data-page-node-id="[^"]+"', "", s)` 清掉
- 落地页发布的 src 都用绝对 URL（不靠 `<base>`），部署到任意子路径都不会断链

**回归**：10/10 机型 prompt 生成 + 自检仍 0 ERROR；v2 HTML 6 项校验全绿。

---

## 1.2.0 — 2026-09-06 · 一手规格书回写 + 单文件 HTML 渲染规格

**数据：官方 PDF 优先级高于术语库锚点**
- `machines/S-WS450.json` 用 `Product Presentation/Wave Solder Series/` 下三份官方规格书
  （S-WS450A 2018 / S-WS450C / SWS450M Big Board）重写，覆盖原 term bank 锚点。
- 修正三处冲突：预热 `280 °C → 250 °C`、锡炉 `460 kg → 450 kg (A/C) / 480 kg (M)`、炉温 `300 °C → 350 °C (A/C)`。
- 新增变体维度：A / C / M 三个型号的差异（预热长度、波峰高度、元件限高、喷嘴、氮气、功率）进 `params_confirmed`。
- 原"Conveyor Speed 写 On request"作废——规格书已确认 `0–2000 mm/min (A)` / `1500–1800 mm/min (C/M)`。
- 保留 3 条 `params_withheld`：氮气（仅 C 有数据）、M 预热功率 8 kW vs 22 kW 冲突、M 炉温精度 ±10 vs ±1–2 °C 冲突。
- **规则固化**：`machines/*.json` 的 `source` 字段必须写明数据出处；一手规格书 > 术语库锚点。

**新增 `references/06-html-render-spec.md`**
Prompt → 单文件 HTML 的原生实现规格：
- framer-motion → IntersectionObserver / sticky / rAF 逐项对照表
- 设计令牌、8 段落位顺序、`prefers-reduced-motion` 降级
- **素材槽位约定**：无真实素材时留 `data-asset` 槽位，禁止 Unsplash 抽象图或 AI 生成的"像机器"的图
- Hero 无渲染图时用**工程剖视示意图 SVG**（按真实结构画），不虚构产品照
- 交付前 6 项校验脚本 + 3 个已知坑（跑马灯 N² clone、Hero 层级、变体表独立成横向滚动表）

**首个成品**：`Product Presentation/SM-3D-Landing-Framework/S-WS450-wave-soldering.html`
（8 段齐全、57 KB 单文件、无外部依赖除 Google Fonts，校验全绿）

---

## 1.1.0 — 2026-09-06 · skill 化重构（模板与数据分离）

把 v1.0 的两份静态文档重构为可升级、可复用、可自检的 skill 包。

**架构**
- 拆出 `templates/prompt-master-EN.md` 作为**唯一真源**占位符模板，用 `<!-- BEGIN PROMPT -->` / `<!-- END PROMPT -->` 标记界定
- 拆出 `machines/*.json` 承载机型数据，与模板解耦
- 新增 `scripts/build_prompt.py`：模板 + 数据 → 可执行 Prompt，支持 `--list / --model / --all / --out / --out-dir / --validate`
- 新增 `scripts/validate_prompt.py`：合规自检 E1–E5（硬错误）/ W1–W4（提醒），支持 `--strict`

**内置机型（10 个）**
S-WS450、S-70LD、S-7900、S-7020T、S-3000、STF1003、BF-2002D、SUL460、SME5200、SFY03
全部参数取自 `smthelp-brand-voice` 术语库「二·B 已确认参数锚点」，`params_withheld` 记录未确认项。

**参考文档模块化**（原 21KB 单文件拆成 5 个，按需加载）
- `01-block-mapping.md` — 原框架 → B2B 映射与改造原理
- `02-section-specs.md` — 8 段区块详细规格
- `03-components-and-tech.md` — 组件、性能、降级、SEO、已知坑
- `04-compliance-and-copy.md` — 参数溯源、报价熔断、CTA、禁用词
- `05-upgrade-playbook.md` — 升级手册（加机型 / 改版式 / 加页面类型 / 加自检项）

**SKILL.md 瘦身**
从「把全部内容塞进 skill 主文件」改为**路由层**：工作流 → 硬约束速查 → 色板 → 区块顺序 → 目录索引。细节按需读 references。

**自检器的两个已知陷阱已修**
- 模板自身列举禁用词 → 检查前先挖掉 `Banned filler words:` 行
- Tailwind 类名误命中（如 `leading-none`）→ 改用 `(?<![-\w])word(?![-\w])` 词边界

---

## 1.0.0 — 2026-09-06 · 首版

从 Azou《DeepSeek Harness 工具包》第 5 节 "3D Creator-style portfolio landing page" Prompt Spec 改造。

- 建立原框架 → B2B 工业版的映射表（抽象 3D 肖像 → 设备主视觉、抽象 GIF → 真实动作素材、Tracks → Specs 参数墙、Projects → 应用场景叠卡）
- 区块从 5 段扩到 8 段，新增 Trust/ROI/报价熔断/FAQ/sticky WhatsApp
- 确立品牌色板 `#0B0E0F` / `#0AA5A5` / `#90C641` / `#D7E2EA` 与 Archivo 字体
- 写入业务硬约束：参数溯源、报价熔断、整线连带、强制 CTA 两行
- 交付两份文档（单机型页框架 + S-WS450 / S-70LD 填空示例）

**抓取备注**：该 Google Doc 用 WebFetch 只返回登录墙，必须用
`curl -sL "https://docs.google.com/document/d/<ID>/export?format=txt"` 才能拿到正文。
