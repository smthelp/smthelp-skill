---
name: xiaoman-crm-wave-solder-prospecting
description: 每周一上午8点自动登录小满CRM，抓取近期从中国进口波峰焊机的墨西哥/巴西企业，整理供应商信息和价格，推送到 Worktile Webhook。
tags:
  - crm
  - web-scraping
  - automation
  - wave-solder
  - smt
  - smthelp
created: 2026-04-25
updated: 2026-06-01
type: workflow
cron_schedule: "0 8 * * 1"
browser: chrome
---

# 小满 CRM 波峰焊客户抓取

## ⚠️ BLOCKER: 小满 CRM SMS 2FA (verified 2026-06-01)

**Login URL**: https://login.xiaoman.cn/login

After entering credentials, the system sends an SMS code to **13602562576** and shows a phone verification screen (ref=e11 = SMS input field). **This blocks fully autonomous cron execution.**

Verified element refs (from browser_snapshot on 2026-06-01):
| Element | Ref | Value |
|---------|-----|-------|
| Username input | e8 | jasonwu@smthelp.com |
| Password input | e9 | Nbjx-1806XM |
| Privacy checkbox | e22 | Must check before login enables |
| Login button | e10 | Enabled after checkbox checked |

**On successful login the system transitions to SMS verification — automation stalls here.**

Possible workarounds:
1. Investigate whether 小满 offers an API token or OAuth that bypasses 2FA
2. Check if browser session cookies persist past the 2FA gate after first manual login
3. If neither: this job must be semi-automated, notifying Jason to provide the SMS code

## 登录凭证（实测）

| 参数 | 值 |
|------|-----|
| CRM 首页 | https://crm.xiaoman.cn |
| 登录页 | https://login.xiaoman.cn/login |
| 用户名 | jasonwu@smthelp.com |
| 密码 | Nbjx-1806XM |
| 绑定手机 | 13602562576 |
| Webhook | https://hook.worktile.com/incoming/fab6e009a985434a8a9bf2fa6845c1e3 |

## 工作流程

### 第一步：登录小满 CRM（Hermes Browser Tools）

```
browser_navigate → https://login.xiaoman.cn/login
browser_snapshot  # 获取元素引用
browser_type ref=e8 → jasonwu@smthelp.com
browser_type ref=e9 → Nbjx-1806XM
browser_click ref=e22  # 勾选隐私政策（必须）
browser_click ref=e10  # 登录按钮
browser_snapshot  # 此时应看到 SMS 验证界面 — 自动化在此卡住
```

### 第二步：导航到客户列表/进口记录页面

```
browser_navigate → https://crm.xiaoman.cn/customers
browser_snapshot
```

### 第三步：搜索波峰焊相关记录

在搜索框输入关键词:
- browser_type ref=e5 → "Wave Soldering Machine"
- browser_press key=Enter
- browser_snapshot

或使用高级筛选:
- browser_click ref=e8  # 高级筛选按钮
- browser_type ref=e10 → "Wave Solder"
- browser_click ref=e14  # 应用筛选

### 第四步：抓取客户数据

使用 browser_console 在页面上下文执行 JavaScript 提取客户数据.

### 第五步：过滤墨西哥/巴西企业

```bash
jq '[.[] | select(.country | test("Mexico|Brasil|墨西哥|巴西"))] | .[0:20]' /tmp/prospects.json
```

### 第六步：发送到 Webhook

```bash
curl -X POST -H "Content-Type: application/json" \
  -d "{\"text\": $(cat /tmp/report.md | jq -Rs .)}" \
  https://hook.worktile.com/incoming/fab6e009a985434a8a9bf2fa6845c1e3
```

## 验证步骤

1. 检查 /tmp/filtered_prospects.json 有数据
2. 确认 Webhook 返回 200
3. 在 Worktile 查看推送消息

## 注意事项

- **首次运行**：需要人工确认元素引用是否与实际页面匹配
- **登录状态**：使用 browser 的 persistent profile 保存 Cookie
- **2FA 问题**：见上方 BLOCKER 说明 — 当前无法完全自动化
- **数据隐私**：抓取的数据仅用于 Southern Machinery 主动联系潜在客户

## 触发方式

```bash
# 手动触发（测试用）
python3 /Users/jasonwu/.hermes/scripts/xiaoman_crm_scraper.py

# Cron 自动（需先解决2FA问题）
0 8 * * 1 /Users/jasonwu/.hermes/scripts/xiaoman_crm_scraper.py >> /Users/jasonwu/.hermes/logs/crm_scraper.log 2>&1
```
