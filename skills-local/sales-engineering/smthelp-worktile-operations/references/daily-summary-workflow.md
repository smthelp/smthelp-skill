# Daily Work Summary Workflow — 每日工作总结生成流程

**Skill**: `smthelp-worktile-operations` (子模块)
**触发场景**: 用户要求生成日报/周报、工作总结、每日汇报
**数据依赖**: session_search + IMAP邮箱 + Worktile + 本地文件 + WhatsApp
**最后更新**: 2026-06-09（修复 IMAP 账号路由 + Worktile 提取方式）

---

## 0. 前置数据源（按优先级）

| 数据源 | 工具/方法 | 覆盖内容 |
|--------|-----------|----------|
| 本日对话记录 | `session_search(sort='newest', limit=3)` | 今日所有 Hermes 对话上下文 |
| 邮件往来 | `himalaya` CLI（多账号轮询） | 客户询盘、EDM 发送记录 |
| Worktile | `browser_console` JS 提取 | 任务延期、报告提交状态 |
| 本地文件 | `ls -lt ~/Downloads/` | ROI PDF、报价单、图片附件 |
| WhatsApp | 文件名时间戳归因 | 图片客户溯源 |

---

## 1. 6模块日报格式标准（Jason Wu 专用）

```
## 1. 今日核心工作成果
- 以动词开头（跟进、寄出、制作、发布）
- 具体到：客户名称、设备型号、交付物名称

## 2. 核心客户互动与询盘矩阵
表格4列：客户名称/国家 | 产品类型 | 询盘设备 | 痛点/阶段

## 3. 营销引流与新增线索统计
按来源分row：LinkedIn / 官网 / WhatsApp / 展会 / SDR
合计数字要精确（非估算）

## 4. 待跟进技术/商务阻碍点
按优先级列出卡点，标注需要什么人协助

## 5. 明日 Top 3 优先级安排
每个客户注明 Hook 或具体交付物

## 6. 【周五特别复盘】（仅周五）
本周KPI + 下周攻坚计划 + LinkedIn/YouTube排期
```

---

## 2. 数据拉取标准流程

### Step 1 — session_search（找今日对话）
```python
session_search(query="SMT OR THT OR EMS OR 客户 OR 询盘", sort="newest", limit=3)
```
读取最新 session 的前20条消息，识别今日关键工作项。

### Step 2 — himalaya 邮件（⚠️ 2026-06-09 修正）

> ⚠️ **`jasonwu_work` 账号 IMAP 超时**：直接用会报 `AUTHENTICATIONFAILED + 30s` timeout。
> **正确做法**：用 `info_3dsmt`、`info_smthelp_eu`、`sale_3dsmt` 等备用账号。

```bash
# INBOX 扫描（跳过超时的 jasonwu_work）
for acct in info_3dsmt info_smthelp_eu sale_3dsmt service_3dsmt support_3dsmt; do
  echo "=== $acct INBOX ==="
  himalaya envelope list --account $acct --folder INBOX --page 1 --page-size 20 2>&1 | \
    grep -v "^2026\|WARN\|missing" | head -20
done

# Sent 文件夹（EDM 发送记录业务询盘在此；INBOX 通常只有 "Welcome to TinkMail"）
for acct in info_3dsmt info_smthelp_eu sale_3dsmt; do
  echo "=== $acct SENT ==="
  himalaya envelope list --account $acct --folder Sent --page 1 --page-size 10 2>&1 | \
    grep -v "^2026\|WARN\|missing" | head -15
done
```

**关键发现（2026-06-09 实测）**：
- INBOX 全部为 "Welcome to TinkMail" 垃圾邮件，**无真实业务询盘**
- EDM 发送记录在 **Sent** 文件夹（如 Varela Electrónica、Whirlpool Brazil）
- 真实询盘需结合 **B2B 平台后台 + WhatsApp 人工核查**

### Step 3 — Worktile 任务提取

⚠️ **PITFALL**: `row.querySelector('.overdue')` 永远返回 `null`（Worktile 延期行没有 `.overdue` CSS class）。

✅ **实测有效写法**：

```javascript
// 方案A（推荐）：直接取整页 innerText，适合 Dashboard / 任务列表页
document.body.innerText.substring(0, 10000)

// 方案B：按日期格式正则过滤任务行
document.querySelectorAll('tr').forEach(row => {
  const text = row.innerText;
  // 匹配：Jun9 / 6月9日 / 2024年12月31日 / 延期
  if (text.match(/\d+月\d+日|延期|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec\s+\d+/)) {
    console.log(text.substring(0, 300));
  }
});
```

**操作流程**：
1. `browser_navigate` → Worktile 工作台（`https://smthelp.worktile.com`）
2. 登录（手机号 `13602562576` + 密码 `nbjxJY3-1806WJX`）
3. 直接在输入 `document.body.innerText.substring(0, 10000)` 拉取全量文本
4. 搜索客户名 → `browser_press(Enter)` → 点击任务名打开详情面板
5. `browser_console({ expression: "document.body.innerText.substring(3000, 8000)" })` 提取详情

### Step 4 — WhatsApp 图片归因

WhatsApp 图片文件名格式：`WhatsApp Image YYYY-MM-DD at HH.MM.SS.jpeg`

**归因流程**：
1. 时间戳（Jun5 16:26 = 当日下午收到）→ 关联同日 CRM 跟进记录或 WhatsApp 聊天记录
2. 在 CRM 中查找同一日期的跟进记录 → 匹配客户
3. 如无法归因 → 标注"⚠️ 需人工核查"，禁止留空

```bash
# 扫描 Downloads 中的 WhatsApp 图片（按时间倒序）
ls -lt ~/Downloads/*.{jpeg,jpg} 2>/dev/null | head -20
```

### Step 5 — 本地文件（Downloads 扫描）

```bash
ls -t ~/Downloads/*2026* | head -20        # 本月所有文件
ls -t ~/Downloads/*.pdf | head -15         # ROI PDF / 报价单
ls -t ~/Downloads/WhatsApp*.jpeg | head -10 # WhatsApp 图片
```

---

## 3. CRM 核心客户速查表（生成日报时必须核对）

来自 `smthelp-crm-real-customers` skill + 本日 Worktile 实测数据：

| 客户 | 国家 | 优先级 | 今日状态 |
|------|------|--------|---------|
| CE3 Electronics (Daniel Gonzalez) | [CA] 加拿大 | 🔴 高 | SQC460 合规包待发 |
| Kimball Electronics (KEMX) | [MX] 墨西哥 | 🔴 高 | 定制 Feeder 评估报告待收 |
| GRsys / Micromed | [BR] 巴西 | 🟡 中 | 降维提案待发出 |
| BYR Electronics | [TR] 土耳其 | 🟡 中 | MLCC 振动盘 R&D 进行中 |
| LEANVAL S.A. | [AR] 阿根廷 | 🟡 中 | 报价单已发，周度触达 |
| M2M Services Ltd. | [BG] 保加利亚 | 🔴 高 | 复联 Email 待发出 |
| E.G.O. Appliance Controls | [ES] 西班牙 | 🔴 高 | 等待吴总审批 Email |

---

## 4. 输出校验清单

生成日报前确认以下全部完成：
- [ ] session_search 已读取今日所有对话
- [ ] 邮件已按账号扫描（`info_3dsmt`/`info_smthelp_eu`/`sale_3dsmt`，非 `jasonwu_work`）
- [ ] WhatsApp 图片已归因到客户（禁止留空）
- [ ] ROI PDF 文件已在本地存在（如 `S-70LD_ROI_*.pdf`）
- [ ] 所有设备型号使用 Southern Machinery 标准命名（S-70LD、S-WS450、S3000 等）
- [ ] 英文术语保留大写：SMT, THT, PCB, PCBA, CPH, Feeder, Nozzle, Reflow Oven, Wave Soldering, SPI, AOI, MES
- [ ] 数字必须是真实统计值，禁止使用"若干"、"多个"等模糊词

---

## 5. 常见错误与修复（2026-06-09 更新）

| 错误 | 原因 | 修复 |
|------|------|------|
| `AUTHENTICATIONFAILED` + 30s 超时 | `jasonwu_work` IMAP 不稳定 | 换用 `info_3dsmt`/`info_smthelp_eu`/`sale_3dsmt` |
| INBOX 全是 "Welcome to TinkMail" | 业务邮件不在 INBOX | 查 **Sent** 文件夹 + B2B 平台后台 |
| Worktile 任务行 `console.log` 不触发 | `row.querySelector('.overdue')` 永远 null | 用 `document.body.innerText.substring(0, 10000)` |
| WhatsApp 图片无法归因 | 文件名无客户信息 | 时间戳关联 CRM 同日跟进记录 |
| 日报数字全靠估算 | 未实际连接邮件/CRM | 明确告知用户"⚠️ 请补充数据" |
| 客户国家 emoji 渲染异常 | 系统不支持彩色 emoji | 改用 ISO 代码如 [CA] [MX] [BR] |
