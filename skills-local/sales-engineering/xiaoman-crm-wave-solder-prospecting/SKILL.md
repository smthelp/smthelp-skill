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
updated: 2026-04-25
type: workflow
sources:
  - 小满CRM (https:// Xiaoman CRM URL - 需要填写)
  - Worktile Webhook (https://hook.worktile.com/incoming/fab6e009a985434a8a9bf2fa6845c1e3)

config:
  crm_url: "https://crm.xiaoman.cn"
  crm_username: "jasonwu@smthelp.com"
  crm_password: "${XIAOMAN_CRM_PASSWORD}"  # 环境变量方式存储敏感密码
  webhook_url: "https://hook.worktile.com/incoming/fab6e009a985434a8a9bf2fa6845c1e3"
  search_keywords:
    - "波峰焊"
    - "Wave Soldering Machine"
    - "波峰焊机"
  target_countries:
    - "Mexico"
    - "Brasil"
    - "墨西哥"
    - "巴西"
  webhook_url: "https://hook.worktile.com/incoming/fab6e009a985434a8a9bf2fa6845c1e3"
  # 搜索关键词（中英双语）
  search_keywords:
    - "波峰焊"
    - "Wave Soldering Machine"
    - "波峰焊机"
  # 目标国家
  target_countries:
    - "Mexico"
    - "Brasil"
    - "巴西"
    - "墨西哥"
  # ==============================

cron_schedule: "0 8 * * 1"  # 每周一上午8点
browser: chrome
persistent_profile: true
---

# 小满 CRM 波峰焊客户抓取工作流

## 工作流程

### 第一步：登录小满 CRM

```bash
playwright-cli open --browser=chrome --persistent https://{crm_url}/login
playwright-cli snapshot

# 填写登录表单（根据实际页面调整元素引用）
playwright-cli fill e1 "{crm_username}"
playwright-cli fill e2 "{crm_password}"
playwright-cli click e3  # 登录按钮
playwright-cli snapshot
```

### 第二步：导航到客户列表/进口记录页面

```bash
# 根据CRM实际结构导航到客户搜索页面
playwright-cli goto https://{crm_url}/customers
playwright-cli snapshot
```

### 第三步：搜索波峰焊相关记录

```bash
# 在搜索框输入关键词
playwright-cli fill e5 "Wave Soldering Machine"
playwright-cli press Enter
playwright-cli snapshot

# 或者使用高级筛选（根据CRM功能调整）
playwright-cli click e8  # 高级筛选按钮
playwright-cli snapshot
playwright-cli fill e10 "Wave Solder"
playwright-cli select e12 "Mexico"  # 筛选墨西哥
playwright-cli click e14  # 应用筛选
playwright-cli snapshot
```

### 第四步：抓取客户数据

```bash
# 提取所有客户卡片/表格行
playwright-cli --raw eval "
[...document.querySelectorAll('.customer-card, tr.customer-row, div[data-type=client]')].map(el => ({
  company: el.querySelector('.company-name, td:nth-child(2)')?.textContent?.trim(),
  country: el.querySelector('.country, td:nth-child(3)')?.textContent?.trim(),
  product: el.querySelector('.product, td:nth-child(4)')?.textContent?.trim(),
  price: el.querySelector('.price, td:nth-child(5)')?.textContent?.trim(),
  date: el.querySelector('.date, td:nth-child(6)')?.textContent?.trim(),
  supplier: el.querySelector('.supplier, td:nth-child(7)')?.textContent?.trim(),
  contact: el.querySelector('.contact, td:nth-child(8)')?.textContent?.trim()
}))
" > /tmp/wave_solder_prospects.json

cat /tmp/wave_solder_prospects.json
```

### 第五步：过滤墨西哥/巴西企业

```bash
# 使用 jq 过滤目标国家
cat /tmp/wave_solder_prospects.json | jq '[.[] | select(.country | test("Mexico|Brasil|墨西哥|巴西"))] | .[0:20]' > /tmp/filtered_prospects.json

cat /tmp/filtered_prospects.json
```

### 第六步：格式化并发送到 Webhook

```bash
# 格式化数据为 Markdown 报告
REPORT=$(cat << 'EOF'
# 🌊 波峰焊机进口客户情报
**抓取时间**: $(date '+%Y-%m-%d %H:%M')
**数据来源**: 小满 CRM

## 墨西哥/巴西潜在客户

| 公司名称 | 国家 | 产品 | 价格 | 供应商 | 日期 |
|---------|------|------|------|--------|------|
EOF
)

# 添加表格行
cat /tmp/filtered_prospects.json | jq -r '.[] | "| \(.company) | \(.country) | \(.product) | \(.price) | \(.supplier) | \(.date) |"' >> /tmp/report.md

# 发送到 Webhook
curl -X POST \
  -H "Content-Type: application/json" \
  -d "{\"text\": $(cat /tmp/report.md | jq -Rs .)}" \
  https://hook.worktile.com/incoming/fab6e009a985434a8a9bf2fa6845c1e3

playwright-cli close
```

## 备选方案：如果 CRM 有 API

```bash
# 如果小满CRM提供REST API，直接调用
curl -X GET "https://{crm_url}/api/customers?keyword=Wave+Solder&country=Mexico,Brazil" \
  -H "Authorization: Bearer {api_token}" \
  -o /tmp/crm_response.json

# 处理响应
cat /tmp/crm_response.json | jq '.data[] | {company, country, product, price}' > /tmp/prospects.json
```

## 验证步骤

1. 检查 `/tmp/filtered_prospects.json` 有数据
2. 确认 Webhook 返回 200
3. 在 Worktile 查看推送消息

## 注意事项

- **首次运行**：需要人工确认元素引用（e1, e2 等）是否与实际页面匹配
- **登录状态**：使用 `--persistent` 保存 Cookie，避免每次都要登录
- **反爬限制**：如遇限制添加 `playwright-cli wait 2000` 延时
- **数据隐私**：抓取的数据仅用于 Southern Machinery 主动联系潜在客户

## 触发方式

```bash
# 手动触发（测试用）
./scripts/run_xiaoman_crm_scraper.sh

# Cron 自动（每周一 8:00）
0 8 * * 1 /path/to/scripts/run_xiaoman_crm_scraper.sh >> /var/log/crm_scraper.log 2>&1
```
