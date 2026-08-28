---
name: smthelp-worktile-operations
description: "Southern Machinery Worktile CRM 日常运营操作手册 — 任务管理、客户跟进、报告提交、延期处理"
metadata:
  source: hermes
  origin: "sales-engineering/smthelp-worktile-operations"
---
# Southern Machinery Worktile CRM 运营手册

## 登录信息

> ⚠️ **凭证从环境变量读取，禁止硬编码。** 需要 `WORKTILE_USERNAME`（手机号）
> 与 `WORKTILE_PASSWORD`。泄露时在 Worktile 账号安全页改密码即可使旧密码失效。

| 项目 | 值 |
|------|---|
| URL | https://smthelp.worktile.com |
| 登录方式 | 手机号 + 密码（非邮箱） |
| 用户名 | `${WORKTILE_USERNAME}` |
| 密码 | `${WORKTILE_PASSWORD}` |
| 公司 | 深圳市南部机械销售服务有限公司 |

**注意**：Worktile 账号与 CRM/网站后台账号是**独立**的系统。手机号是主要登录名。

---

## 工作台概览（基准日期 2026-04-25）

| 指标 | 数值 |
|------|------|
| 全部任务 | ~1,400+ 个（持续增长，以系统显示为准） |
| 延期任务 | 24-25 个（持续存在，需定期清理） |
| 今日/本周/本月任务 | 0 个（当前名下无本周截止任务） |

> 注意：任务总数和延期数会随时间增长。所有数字均为实时读取，请勿硬编码到自动化脚本中。

---

## 重要任务分类

### 🔴 最高优先级（SCL前缀 = 特殊客户任务）

| 任务ID | 名称 | 状态 | 截止日期 | 项目 |
|--------|------|------|---------|------|
| SCL 35408 | 微信接入Openclaw | 未激活 | 3月22日 | JasonWu客户管理CRM |
| SCL 34008 | Opal.google 产品Deep Research | 首次交接 | 2025-11-18 | JasonWu客户管理CRM |
| SCL 33997 | LEANVAL S.A. 终端客户（阿根廷） | 首次交接 | 2025-11-18 | JasonWu客户管理CRM |
| SCL 24832 | 重点客户List | 一级客户 | 2024-12-31 | JasonWu客户管理CRM |

### 🟡 团队延期任务（年度客户开发，所有人已延期1年4个月）

所有标注 **一级客户** 且截止日期 **2024-12-31** 的任务均来自同一个年度客户开发计划：

| 任务ID | 负责人 | 项目 |
|--------|--------|------|
| 33829 | Kevin Yang | Kevin Yang外贸客户管理 |
| 33742 | Leo Liao | Leo Liao外贸客户管理 |
| 31930 | Jason | Jason客户CRM |
| 31175 | SMThelp | SMThelp客户开发 |
| 24879 | Wayne | Wayne客户管理 |
| 24870 | webb | webb客户管理 |
| SCL 24832 | JasonWu | JasonWu客户管理CRM |

---

## 报告/简报待提交（截至2026-04-25）

| 报告类型 | 状态 |
|---------|------|
| 月报-Apr（截止4月30日） | ⚠️ 未提交 |
| Weekly Sales Forecast Report-17th（截止4月25日） | ⚠️ 未提交 |
| 日报工作计划-Apr 25（截止4月25日） | ⚠️ 未提交 |
| 日报总结-Apr 25（截止4月25日） | ⚠️ 未提交 |
| 日报工作计划-Apr 24 | ⚠️ 未提交 |
| 日报总结-Apr 24 | ⚠️ 未提交 |
| 日报工作计划-Apr 23 | ⚠️ 未提交 |
| 日报总结-Apr 23 | ⚠️ 未提交 |
| 日报工作计划-Apr 22 | ⚠️ 未提交 |
| 日报总结-Apr 22 | ⚠️ 未提交 |

---

## 浏览器自动化要点（Playwright/CLI）

### 登录流程
```
1. 访问 https://smthelp.worktile.com/login
2. 填写手机号（不用邮箱）
3. 填写密码
4. 点击 Signin
5. 等待页面跳转到 /dashboard
```

### 任务列表页面结构
- 工作台URL: `https://smthelp.worktile.com/dashboard`
- 任务以 HTML table rows (`<tr>`) 渲染，每行包含:
  - 任务ID（第一列，如 SCL 35408）
  - 任务名称（第二列）
  - 状态（第三列，如 未激活、首次交接、一级客户、待开发）
  - 截止日期（第四列）
  - 所属项目（第五列，如 JasonWu客户管理CRM）

### CSS选择器注意事项
- Worktile 使用动态生成的 Angular class 名（如 `ng-star-inserted`）
- 不要依赖 CSS class 选择器，改用 `browser_console` JS eval 方式读取数据
- 任务详情面板需要点击任务名称打开，URL格式需通过 DOM 分析获取

### 关键 JS 查询表达式
```javascript
// 获取当前页面所有文本（用于调试）
document.body.innerText.substring(0, 3000)

// 查找任务行
document.querySelectorAll('tr')

// 查找所有链接
[...document.querySelectorAll('a[href]')].map(el => ({
  text: el.innerText.trim(),
  href: el.getAttribute('href')
})).filter(el => el.text.length > 3)
```

### PITFALL: browser_snapshot 无法获取任务详情面板内容

**症状**: 点击任务名称后，`browser_snapshot` 返回空或仅显示框架结构，完整的邮件往来、评论、活动记录均不可见。

**原因**: Worktile 的任务详情面板（右侧滑出）是 Shadow DOM 或懒加载组件，`browser_snapshot` 的 accessibility tree 无法穿透渲染后的内联文本。

**解决方案**: 使用 `browser_console` + `document.body.innerText` 提取完整文本内容：

```javascript
// 推荐表达式（优先查找任务详情容器）
document.querySelector('.task-detail-container, .task-detail, [class*="detail"]')?.innerText
  || document.body.innerText.substring(3000, 8000)

// 如果需要更精确地提取评论/邮件线程（截取 3000-8000 字符范围）
document.body.innerText.substring(3000, 8000)
```

**实测有效性**: 2026-05-30 成功提取 LEANVAL S.A. (SCL 33997) 完整任务详情，包含：
- 全部邮件往来原文（英文+西班牙文）
- 客户联系信息（Raphael Brylkowski, Agustin Martino, Integraltek）
- 工程规格参数（ISO 8 Cleanroom, ESD Flooring, Test Chamber）
- 供应商信息（深圳市晶凡硕新材料科技有限公司）
- 完整报价单邮件正文

### PITFALL: Session_search 可发现CRM未追踪的交易（2026-06-12 实测）

**现象**: Kimball Electronics Mexico 波峰焊项目在 session_search (2026-06-04) 中出现，但 Worktile CRM 中无对应任务。

**风险**: 依赖 CRM 作为唯一数据源会遗漏通过其他渠道（会话、邮件、WhatsApp）发现的交易机会。

**解决方案**: CEO 每周简报必须同时运行：
1. Worktile CRM 任务列表（含延期任务）
2. session_search 近期会话（查找客户名）
3. himalaya Sent folder 扫描（查找新增交易）
4. WhatsApp 文件时间戳 → 关联同日 CRM 跟进记录

⚠️ **规则**: session_search 发现的交易 ≠ CRM 活跃交易。必须人工确认归属（Kevin/Leo/Jason）后建立 CRM 任务。禁止基于 session_search 结果单独向 CEO 汇报而不标注"未在CRM中"。

> **⚠️ FTS5 Corruption**: session_search 在 2026-06-17 确认为**全库级**故障，所有 session 均不可读。详见 `smthelp-daily-report` skill 的 `references/session-search-fts5-corruption.md`。日报生成时直接跳过 session_search，不重试。
> **⚠️ 永久修复状态**: 此问题已确认无法自动恢复。CEO 周报生成时，known-accounts.md 作为唯一的历史上下文来源，不再依赖 session_search 交叉验证。
> **⚠️ LEANVAL S.A. 已添加到 known-accounts.md**: SCL 33997 是 JasonWu 客户管理CRM 中唯一verified $50K+ CapEx 账户，已在 ceo-pipeline-report-generator 的 references/known-accounts.md 中更新。

### PITFALL: Project Page URLs Consistently Time Out (2026-06-26)

**现象**: 直接 navigating to project URLs (e.g., https://smthelp.worktile.com/jasonwu客户管理CRM) times out after 60s. The dashboard (https://smthelp.worktile.com/dashboard) is reliably accessible.

**诊断**: Worktile project pages are heavily dynamic/Angular — they load task lists via additional XHR requests that fail under automation's shorter timeout.

**Workaround**: 
- Do NOT navigate directly to project page URLs.
- Extract task data from the dashboard view or search results.
- If task detail is needed: login → dashboard → search box → click task name → browser_console extract.
- Complete all browser operations in rapid sequence before session expires (~10-15 min).
- If dashboard also times out: fall back entirely to known-accounts.md reference file (the verified account records are more reliable than stale CRM reads).

**操作流程**:
1. `browser_navigate` → Worktile 工作台
2. 搜索框输入客户名 → `browser_press(Enter)`
3. 点击任务名称（打开详情面板）
4. `browser_console({ expression: "document.body.innerText.substring(3000, 8000)" })`
5. 从返回文本中提取客户信息、邮件时间线、规格参数

### 本周任务筛选（2026-05-30 实测）
- 工作台默认视图下，"本周 ·0个任务" = 截止日期在本周内且状态为"未完成"的任务
- 不同于"延期任务"（已过截止日期），本周新任务的截止日期落在当前自然周内
- 卡片筛选结构：`全部` → `今天` → `本周` → `本月` → `延期`（每项都是一个可点击的 filter card）
- 如果本周任务为0，检查是否有"新建任务"入口需要手动派发
- 注意：全部任务总数（1503）和延期任务数（25）是实时数据，勿硬编码到技能中

### Session 有效期
- Worktile session 有效期较短，操作间隔过长需要重新登录
- 建议在单个 session 内完成所有操作，避免重复登录
- 若 session 失效，Worktile 会重定向到 `/signin?returnUrl=/teams`，此时需重新走登录流程

### Step 2 — himalaya 邮件（⚠️ 2026-06-09 修正）

> **⚠️ `references/daily-summary-workflow.md` 此步骤有过时内容，以下为实测正确流程**

**`jasonwu_work` 账号 IMAP 超时**：直接用 `--account jasonwu_work` 会 timeout（`AUTHENTICATIONFAILED + 30s`）。
**正确路由**：用 `info_3dsmt`、`info_smthelp_eu`、`sale_3dsmt` 扫描。

```bash
# INBOX 扫描（跳过超时的 jasonwu_work）
for acct in info_3dsmt info_smthelp_eu sale_3dsmt service_3dsmt support_3dsmt; do
  echo "=== $acct INBOX ==="
  himalaya envelope list --account $acct --folder INBOX --page 1 --page-size 20 2>&1 | \
    grep -v "^2026\|WARN\|missing" | head -20
done

# Sent 文件夹（EDM 发送记录在此；INBOX 通常只有 "Welcome to TinkMail"）
for acct in info_3dsmt info_smthelp_eu sale_3dsmt; do
  echo "=== $acct SENT ==="
  himalaya envelope list --account $acct --folder Sent --page 1 --page-size 10 2>&1 | \
    grep -v "^2026\|WARN\|missing" | head -15
done
```

> **注**: 业务询盘邮件通常只出现在 **Sent**（发出的 EDM），不在 INBOX。需结合 B2B 平台后台 + WhatsApp 确认真实询盘。

### PITFALL: WhatsApp 图片归因缺失（2026-06-09 实测）

**现象**: `ls -lt ~/Downloads/*.{jpeg,jpg}` 扫出多张 WhatsApp 图片（如 `WhatsApp Image 2026-06-05 at 16.26.18.jpeg`），无客户名称。

**风险**: 5张图（Jun5下午）无法归因到具体客户，日报数字"⚠️ 需归因到客户"。

**规范流程**:
1. 文件名时间戳（Jun5 16:26）= 当日下午收到
2. 关联查找同日 CRM 跟进记录或 WhatsApp 聊天记录
3. 无法归因时标注"⚠️ 待人工核查"，禁止留空或随意填入假设客户名

## 附录：父需求信息

## 延期任务处理原则

1. **SCL任务（特殊客户）**：优先联系客户，更新需求状态
2. **年度客户List任务**：更新截止日期（如从2024-12-31改为新日期），保持"一级客户"状态
3. **未提交报告**：补交或说明原因

---

## 附录：父需求信息

- SCL 35408 微信接入Openclaw 的父需求: **SCL 35388 腾讯Qclaw本地电脑安装**
- 相关学习资源：
  - https://www.aivi.fyi/aiagents/OpenClaw-WeChat
  - https://www.dhzyw.com/archives/7959.html
  - https://youtu.be/i1QtXf9VzWg
  - https://www.bilibili.com/video/BV11HAGzqEUH/

## 参考文件

- `references/leanval-sa-customer-record.md` — LEANVAL S.A. 完整客户档案（含邮件时间线、工程规格、供应商信息、项目状态分析）。提取自 SCL 33997 实测数据，可直接查阅无需重复浏览器操作。
- `references/daily-summary-workflow.md` — 每日工作总结生成标准流程。覆盖6模块格式、IMAP+CRM+Worktile+本地文件多数据源拉取步骤、CRM核心客户速查表、输出校验清单。
