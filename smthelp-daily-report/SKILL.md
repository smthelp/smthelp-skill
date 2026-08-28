---
name: smthelp-daily-report
description: "Southern Machinery 外贸销售工程师每日工作总结生成器。触发场景：生成日报/日结报告、客户互动矩阵、营销漏斗统计、明日优先级规划。每周五追加 KPI 周对比模块。"
whenToUse: "日报，日结，每日工作总结，daily report，生成报告，今日工作成果，客户互动矩阵，营销漏斗"
metadata:
  source: hermes
  origin: "sales-engineering/smthelp-daily-report"
---
# Southern Machinery 外贸日报生成器

## 任务定位

为 Southern Machinery 外贸销售工程师（Jason Wu）生成结构化、可扫描的每日工作总结。强调：SMT/THT 行业术语、数据驱动、B2B 结果导向。

---

## 输出格式（6个固定模块）

### 模块1：今日核心工作成果
- 以动词开头（跟进、寄出、制作、发布）
- 列出：客户开发、询盘分析、技术方案设计（SMT/THT 产线配置提案）
- 每个事项一行，简洁

### 模块2：核心客户互动与询盘矩阵
表格，4列：
| 客户名称/国家 | 产品类型 | 询盘设备需求 | 痛点/推进阶段 |
- 推进阶段示例：等待BOM / 评估ROI / 约标 / 等待客户回复 / 报价中 / 验厂中

### 模块3：营销引流与新增线索统计
- 按来源分列：WhatsApp / LinkedIn / 官网 / YouTube / 展会留资 / SDR开发
- 有效询盘数量合计

### 模块4：待跟进技术/商务阻碍点
- 技术团队协助需求（定制Feeder/Nozzle方案、BOM配线分析）
- 待交付物清单（ROI计算书、竞品对比表）
- 标注系统限制（如FTS5 corruption导致的数据缺失）

### 模块5：明日Top 3优先级安排
- 每个优先级包含：客户名、Hook（跟进钩子）、交付物
- SPIN问题嵌入每个优先级的跟进话术中

### 模块6：【周五特别复盘】（仅周五执行）
- 本周KPI对比：总询盘量 / 方案报价单发出数 / Demo完成度 vs 周目标
- 下周大客攻坚计划
- LinkedIn/YouTube内容发布排期

---

## 数据源与优先级

**Important Constraints on delegate_task（关键约束）:**

⚠️ **`delegate_task` 最多同时触发 3 个子任务**：技能内的 4 个并行检查项（日期+Downloads+smthelp.com + 3个邮箱账号）必须分成 **两批** delegate_task 调用，每批 ≤ 3 个任务。超出 3 个会返回 `Too many tasks` 错误。

**正确分批示例：**
```
# 第一批：3个
- 任务1: date +w（判断周五）
- 任务2: find Downloads 目录
- 任务3: curl smthelp.com

# 第二批：3个
- 任务4: himalaya info_3dsmt Sent
- 任务5: himalaya info_smthelp_eu Sent
- 任务6: himalaya sale_3dsmt Sent
```

⚠️ **execute_code 的 subprocess 调用会被拦截**：所有需要 shell 命令的操作（date、find、curl、himalaya）必须通过 `delegate_task` + `terminal` toolset 执行，禁止使用 `execute_code` 的 subprocess。execute_code 可安全用于纯 Python 数据处理（读取 Wiki、解析 JSON 等）。

---

**Primary Sources（优先使用）：**
1. **Worktile CRM** — 客户状态、询盘漏斗数据
2. **Himalaya IMAP** — 今日邮件往来（himalaya envelope list --folder "INBOX"）
3. **LinkedIn Company Insights** — 今日互动数据
4. **本地 Downloads 目录扫描** — `ls -t ~/Downloads/*.{pdf,xlsx} | head -20` 查找今日新建的 ROI 计算书、报价单、Feeder 报告等交付物（经验证：Fitech Feeder Report 来自此路径）

**Fallback Sources（主数据源失效时使用）：**
4. **Wiki产品知识库** — ~/wiki/southern-machinery-wiki.md（产品规格参考）

**数据不可用时的处理规则：**
- 某项数据缺失 → 明确标注 `[数据待CRM同步]` / `[数据待Himalaya同步]`
- 禁止捏造数据或百分比
- 在报告末尾注明"数据说明"段落

**已知数据缺口（建议在日报末尾标注）：**
- LinkedIn 实时互动数据 → 需手动登录 linkedin.com 核查
- WhatsApp 图片/文件归因 → 需关联同日聊天记录，人工核查
- himalaya Sent folder → 如 subagent 返回空，换用浏览器直接登录 WebMail 读取

**本周报告新增已知故障（2026-06-20 确认，持续至 2026-06-30）：**
- LinkedIn Analytics → 强制要求登录，公司页分析数据无法自动抓取，需人工登录 linkedin.com/company/smtmachine/analytics 读取
- `info_3dsmt` INBOX 仅含 TinkMail 欢迎邮件（2026-04-10），无真实询盘数据
- `jasonwu_work`（对应 `jasonwu@smthelp.com`）INBOX 查询超时 45秒不够，需设 ≥ 60秒
- Sent folder 大量空返回（IMAP 同步损坏），命令本身不报 error，只有 WARN 日志
- 遇到超时或空返回 → 不重试 → 在报告中标注 `[邮件数据 — 查询超时]` 或 `[邮件数据 — Sent Folder返回空]`
- YouTube @Smthelping 频道数据（2300订阅 / 1734视频）可通过 `browser_navigate('https://www.youtube.com/c/Smthelping')` 正常抓取，建议作为本周社媒数据的 fallback 数据源
- Downloads 目录 `southern machinery dashboard.html` — 此文件为 Hermes Agent Mission Control 前端模板（含假数据占位符），非业务数据，扫描时过滤排除
- Downloads 中 `SOUL.md` 为 Hermes Agent Persona 定义文件，非业务数据，扫描时注意过滤

## 执行检查清单

- [ ] 获取当前日期，判断是否周五（模块6条件触发）或周六（本周报告变体）

## SMT/THT行业术语规范

输出中必须保留以下英文原词（不翻译）：
SMT, THT, PCB, PCBA, CPH, Feeder, Nozzle, Reflow Oven, Wave Soldering, Pick and Place, SPI, AOI, MES, EMS, ODM, FPY, BOM, CapEx, ROI, ICC, Active Clinching

其他技术词汇可中英混用，以专业简洁为准。

---

## SPIN销售问题嵌入规则

在模块5（明日Top 3优先级）的每个客户跟进中，按以下结构嵌入1-2个SPIN问题：

**Situation（现状问题）**：
- "您目前的THT产线日产能是多少 CPH？"
- "您现在用多少名操作员负责这个工序？"

**Problem（痛点问题）**：
- "人工插入环节的不良率对整体 FPY 的影响有多大？"
- "现有设备的故障停机频率是多少？每次停机损失多少产能？"

**Implication（影响问题）**：
- "如果按当前良率计算，每个月的返工成本大约是多少？"
- "换线时间如果减少30%，对您的月产能意味着什么？"

**Need-payoff（价值问题）**：
- "如果这套方案能把换线时间缩短一半，您会优先用在哪个产品线上？"

每次跟进选择 Situation + Problem 或 Problem + Implication 组合，避免四个问题连续发问。

---

## 今日日期判断逻辑

- 获取当前日期：`date +%Y-%m-%d`
- 周五判断：`date +%w` 返回 `5` 时，触发模块6
- 周六判断：若报告在周六生成（`date +%w` 返回 `6`），且用户明确要求"本周复盘"，执行模块6的周报逻辑，但标注报告生成日期为"周六补生成"
- 非周五/周六：跳过模块6，在末尾注明"⚠️ 数据说明"

---

## 输出语言

- 默认：**中文**（B2B外贸专业语气）
- 表格内技术参数可中英混写
- SPIN问题：中文 + 英文术语

---

## Related Skills

- **smt-ems-geographic-intelligence** — Thursday 9:15 AM weekly ABM report for Mexico/Brazil EMS hubs. **This is a separate cron job — do NOT generate this inside the daily report.**
- `smthelp-knowledge-base` — Southern Machinery 全产品参数
- **Worktile CRM**: `smthelp-worktile-operations` — CRM操作手册
- **周五CEO报告**: `ceo-pipeline-report-generator` — 周五KPI总结模板
- **EDM Campaign**: `smthelp-edm-campaign` — 邮件营销数据（与日报共享数据源）
- **Wiki**: `smthelp-wiki-maintenance` — 产品规格查询路径
- **月度Win-Loss Review**: `smthelp-monthly-win-loss-review` — 月度pipeline复盘（与日报共享数据源，当所有源失效时使用其`references/data-unavailability-fallback.md`）

---

## 已知限制记录

⚠️ **FTS5 Corruption Bug**：session_search 在 2026-06-17 确认为**全库级**故障，所有 session 均不可读。已从 Fallback Sources 中移除。详见 `references/session-search-fts5-corruption.md`。

⚠️ **Worktile CRM SSL + Demo Login 双重故障**（新增 2026-06-19）：
- URL: `https://v5.viwolf.cn/${SMTHELP_WEB_ADMIN_PATH}` — SSL 证书无效（`ERR_CERT_AUTHORITY_INVALID`）
- 自动重定向至 `http://demo.v5.viwolf.cn/${SMTHELP_WEB_ADMIN_PATH}/login.html` — 该 demo 站点登录表单提交后返回空白页，**非真实 CRM 系统**
- 应对：当日报数据源失效时，在报告模块2/3中明确标注 `[CRM暂不可用 — SSL证书异常]`，禁止等待或重试，当日直接使用 Fallback Sources
- 参考：`references/worktile-crm-failures.md`

⚠️ **smthelp.com 官网不可达**（确认于 2026-06-19；**恢复于 2026-07-06**）：
- 2026-06-19：`www.smthelp.com` 全线 timeout（HTTP/HTTPS 均不可达）
- 2026-07-06 验证：`curl -s -o /dev/null -w '%{http_code}' https://www.smthelp.com` 返回 **200 OK** — 官网完全恢复
- `https://www.3dsmt.com` 全程稳定可用（作为镜像备用）
- 相关子域名（`mail.3dsmt.com`, `webmail.3dsmt.com`）DNS/ALPN 错误仍然存在，不影响主站
- 影响（已解除）：EDM 追踪链接、官网表单询盘数据现已可正常获取
- **当前状态**：无需再用 3dsmt.com 替代，可直接使用 smthelp.com

⚠️ **Himalaya 全账号IMAP同步冻结**（确认于 2026-07-06，持续性故障）：
- **所有账号**（`info_3dsmt`, `info_smthelp_eu`, `sale_3dsmt`, `service_3dsmt`, `jasonwu_work`）INBOX 和 Sent folder **全部返回空**
- `jasonwu_work` INBOX 查询在 90秒 timeout 下依然超时；Sent folder 在 60秒 timeout 下也超时
- 根本原因：IMAP 同步自 2026-04-28 起完全冻结，所有后续新邮件均未同步到本地 himalaya 缓存
- **影响**：今日外发邮件无法追溯，真实询盘数据无法通过 himalaya 获取
- **新发现（2026-07-08）**：`info_3dsmt` INBOX 自2026-07-03起有部分新邮件同步（"Goodnews." from info@1haag.com），说明 IMAP 同步正在**缓慢恢复**，但 message body 读取仍全部超时（30秒）
- **应对**：在报告中标注 `[邮件数据 — IMAP同步冻结至4月28日]`，不重试，不等待
- 已知临时替代：浏览器直接登录 WebMail（`webmail.3dsmt.com` 仍报 ALPN 错误）；建议通过 `https://outlook.office365.com` 或联系邮件服务商检查 IMAP 同步状态

⚠️ **Himalaya `message read` 命令语法与超时问题**（确认于 2026-07-08）：
- **正确语法**：`himalaya message read <ID>` — **无需任何标志**，直接传 ID 数字字符串
- **错误语法**：`himalaya message read --id <ID>` → 返回 `unrecognized argument '--id' found`
- 正确 account 名：`jasonwu_work`（是 himalaya account list 中的默认账号）
- **所有 message read 操作在 30秒 timeout 下全部超时**（包括已确认存在于 Sent folder 的 ID 49643/49645），即 envelope list 能返回 ID，但 message body 读取无法完成
- **结论**：这是服务端 IMAP 响应超时问题，非命令语法问题；30秒不足以完成正文拉取
- 建议 fallback：改用浏览器直接登录 WebMail（`https://outlook.office365.com`）读取邮件正文

⚠️ **Himalaya 查询超时**（更新于 2026-07-08）：
- `jasonwu_work` INBOX 查询超时（45秒不够）；建议 timeout ≥ 60秒
- 部分账号 Sent folder 返回空表格（IMAP 同步损坏），但命令本身不报错误
- 遇到超时时不重试，直接在报告中标注 `[邮件数据 — 查询超时]`

⚠️ **YouTube @Smthelping 实测数据**（2026-07-08）：
- 当前：2310 订阅 / 1736 视频（`browser_navigate('https://www.youtube.com/c/Smthelping')` 验证）
- 参考值（2026-06-20）：2300 订阅 / 1734 视频
- 增量：+10 订阅 / +2 视频（2周增量，变化极小）
- **用途**：作为本周社媒数据的稳定 fallback 数据源，无需登录即可抓取

⚠️ **Downloads 目录过滤规则**（确认于 2026-07-08）：
- `southern machinery dashboard.html` = Hermes Agent Mission Control 前端模板，非业务数据，**过滤排除**
- `SOUL.md` = Hermes Agent Persona 定义文件，非业务数据，**过滤排除**
- **7月7日新增**：12个 Southern Machinery 营销 HTML 页面（THT Auto Insertion / Wave Soldering / Feeders & Nozzles / Board Handling / SMT Line / Depaneling / Cleaning 等），均为 smthelp 产品资源页，非当日业务交付物，扫描时注意时间戳
- 近期业务文件：Jun 30 的 `SM-306B Bulk Capacitor Lead cutting & Forming machine.pptx`、Jun 15 的 ALCOELECTRO 系列 PI/发票文件

⚠️ **webmail.3dsmt.com DNS 失败**（新增于 2026-07-01）：
- 错误：`net::ERR_DNS_NO_MATCHING_SUPPORTED_ALPN` — DNS 解析成功但 TLS ALPN 握手失败
- 有别于 smthelp.com 的 HTTP 超时——这是邮件服务器 TLS 配置问题
- 浏览器直接登录无效，无法作为 WebMail fallback
- 实际替代：使用 himalaya 命令行（需注意超时设长）；或通过 `https://outlook.office365.com`（如使用 Microsoft 365）
- 参考：`references/smthelp-dns-outage.md`

⚠️ **delegate_task 子任务进程丢失**（新增于 2026-07-01）：
- 本次月报生成时，3个 delegate_task 进程全部返回 `not_found`（而非失败报错）
- 可能原因：进程在 subagent 完成前就被主会话的进程管理错误地清理
- 实际日期通过 `terminal` 直接调用 `date +%Y-%m-%d` 成功获取
- **结论**：关键系统命令（date、ls、find 等）优先用 `terminal` 直接调用，不依赖 delegate_task

⚠️ **Downloads 目录 southern machinery dashboard.html**（新增于 2026-07-01）：
- 此文件是 Hermes Agent Mission Control 的前端模板（HTML/CSS/JS），非业务数据
- 内含假数据占位符（`--`、`No live events loaded yet`），不可作为销售数据源
- 扫描 Downloads 时注意过滤，关键词：`southern machinery dashboard`

---

## 🚨 All-Sources-Unavailable Mode

When **Worktile CRM + Himalaya email + FTS5 session DB all fail simultaneously** (confirmed triple failure), fall back to:

1. **Downloads scan**:
   ```bash
   find ~/Downloads/ -maxdepth 1 -type f \
     \( -name "*.pdf" -o -name "*.xlsx" -o -name "*.docx" -o -name "*.pptx" -o -name "*.md" \) \
     -mtime -30 2>/dev/null | head -30
   ```
2. **File timestamp analysis** — no new PI/quote/ROI files in 45+ days = zero confirmed closed deals
3. **Campaign asset review** — check for `capex_trigger_campaign_*.md`, ABM reports, `FeederSalesDeck/` — these reveal what was active that month
4. **Output with data confidence flags**: `[confirmed by CRM]` vs `[inferred from file timestamps]`

See: `sales-engineering/smthelp-monthly-win-loss-review/references/data-unavailability-fallback.md`

**If ALL three primary sources are down, the daily report MUST still execute — use the Downloads scan approach and flag every inference clearly.**

---

## 执行检查清单

- [ ] 获取当前日期，判断是否周五（模块6条件触发）
  - **必须通过 delegate_task + terminal toolset**，execute_code 的 subprocess 调用会被 one-shot approval 拦截
- [ ] 扫描 Downloads 目录（terminal toolset，勿用 execute_code subprocess）
  ```bash
  ls -lt ~/Downloads/ | head -20
  find ~/Downloads/ -maxdepth 1 -type f \( -name "*.pdf" -o -name "*.xlsx" -o -name "*.docx" \) -mtime -2
  ```
- [ ] 登录 Worktile CRM（手机号 `${WORKTILE_USERNAME}` / 密码 `${WORKTILE_PASSWORD}`，从环境变量读取）
  - Session 通常保持登录状态，无需每次重新登录
  - 使用 `browser_console({ expression: "document.body.innerText.substring(0, 5000)" })` 提取任务数据
- [ ] 查询 Himalaya 邮件（**Sent folder**，INBOX 通常只有 Welcome 邮件）
  ```bash
  for acct in info_3dsmt info_smthelp_eu sale_3dsmt; do
    himalaya envelope list --account $acct --folder Sent --page 1 --page-size 10
  done
  ```
  - ⚠️ 如果 subagent 返回空或仅含 tool trace 数据为空，换用浏览器直接登录邮箱
  - ⚠️ `himalaya message read <ID>` — **无标志**，直接传 ID；不要写 `--id`；所有正文读取在 30秒 timeout 下均超时（服务端慢），遇到超时直接跳过不重试
  - ⚠️ IMAP 同步正在缓慢恢复（2026-07-03 起 INBOX 有新邮件），但 Sent folder 仍停在 2026-04-28
- [ ] ~~session_search~~ — **永久跳过**：FTS5 全库级损坏，详见 `references/session-search-fts5-corruption.md`
- [ ] 检查 smthelp.com 是否可达
  ```bash
  curl -s -o /dev/null -w '%{http_code}' https://www.smthelp.com --connect-timeout 5
  ```
  - 若返回非 200 或超时：`[官网数据待恢复]`，落地页改用 `https://www.3dsmt.com`，图床使用 `https://ph.smthelp.com`
  - 注意：`--connect-timeout` 必须在 curl 命令末尾，否则 flag 会被忽略（bash 解析顺序问题）
  - 备选验证（若 curl 超时）：用 `browser_navigate('https://www.3dsmt.com')` 直接打开
- [ ] 查询 wiki 产品规格（如需补充设备参数）
- [ ] 按6模块格式输出
- [ ] 每个 Top 优先级嵌入 1-2 个 SPIN 问题
- [ ] 标注所有数据缺失项（格式：`[数据源 — 具体原因]`，例：`[CRM — SSL证书异常]`）
- [ ] 检查 SMT/THT 术语是否保留英文原词
