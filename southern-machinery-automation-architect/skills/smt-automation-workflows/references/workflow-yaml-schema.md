# TAOC 工作流 YAML Schema 完整字段说明

## 顶层结构

```yaml
workflow:        # 工作流元信息
trigger:         # 触发条件
steps:           # 执行步骤（数组）
output:          # 输出结果
cta:             # 下一步动作
```

## 字段详解

### workflow（工作流元信息）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 工作流名称，中英文均可 |
| `category` | enum | 是 | `sales` / `marketing` / `intelligence` / `knowledge` |
| `business_goal` | string | 是 | 一句话说明提升什么业务指标 |
| `target_metric` | enum | 是 | `Leads` / `Response Time` / `Conversion` / `Content Output` / `Knowledge Reuse` |
| `owner` | string | 否 | 流程负责人，默认 Jason Wu |
| `schedule` | string | 否 | 运行频率说明，如"每日 08:30""每周一 09:00" |

### trigger（触发条件）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | enum | 是 | `schedule` / `webhook` / `email` / `form` / `manual` |
| `condition` | string | 是 | 精确触发条件 |
| `source` | string | 是 | 数据来源说明 |

**trigger.type 取值说明：**

| type | condition 写法 | 适用场景 |
|------|---------------|----------|
| `schedule` | cron 表达式，如 `0 9 * * *`（每日 9 点） | 定时任务：每日内容生成、每周竞品报告 |
| `webhook` | 路径，如 `/inquiry/new` | 外部系统推送：网站表单、Zapier 转发 |
| `email` | 邮件规则，如 `subject contains "inquiry" AND from != internal` | 询盘到达、客户回复 |
| `form` | 表单 ID 或来源，如 `website_contact_form` | 官网联系表单提交 |
| `manual` | `on_demand` | 用户手动触发，如"现在跑一次竞品扫描" |

### steps（执行步骤数组）

每个步骤对象包含：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 步骤名称，动词开头（如"解析邮件内容"） |
| `tool` | string | 是 | 使用的工具/Skill/API，必须具体 |
| `input` | string | 是 | 输入数据来源 |
| `output` | string | 是 | 输出数据格式 |
| `note` | string | 否 | 注意事项或约束 |

**步骤数要求：3-8 步**
- 少于 3 步：说明拆解不足，流程过于粗糙
- 多于 8 步：说明粒度太细，应合并或拆成子工作流

**tool 字段写法示例：**
- ✅ `gmail.read` / `gmail.send_draft`
- ✅ `web_scraper.extract`
- ✅ `image_gen.create`
- ✅ `obsidian.write`
- ✅ `telegram.send`
- ❌ `AI 处理`（太模糊）
- ❌ `处理一下`（不可执行）

### output（输出结果）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `format` | enum | 是 | `table` / `pdf` / `markdown` / `json` / `email_draft` / `slides` |
| `location` | string | 是 | 存放位置 |
| `fields` | string[] | 是 | 输出包含的字段列表 |

**location 写法约定：**

| 目标 | 写法 |
|------|------|
| Obsidian | `obsidian://FolderPath/Filename` |
| Telegram | `telegram://chat_id` |
| 邮件 | `email://recipient@domain.com` |
| 本地文件 | `file:///path/to/file` |
| CRM | `crm://entity_type` |
| Notion | `notion://database_id` |

### cta（下一步动作）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | string | 是 | 可执行的下一步动作描述 |
| `target` | string | 是 | 动作对象 |
| `auto` | boolean | 是 | `true`=自动执行，`false`=需人工确认 |

**auto 字段规则（铁律）：**

| 场景 | auto 值 | 原因 |
|------|---------|------|
| 对外发邮件 | `false` | 必须人工审核后发送 |
| 发 LinkedIn 帖子 | `false` | 必须人工审核后发布 |
| 发 WhatsApp 消息 | `false` | 必须人工审核后发送 |
| 写入 Obsidian | `true` | 内部归档可自动 |
| 生成 PDF 存档 | `true` | 内部存档可自动 |
| 推送 Telegram 通知 | `true` | 内部通知可自动 |
| 更新知识索引 | `true` | 内部维护可自动 |
| 涉及价格/报价 | `false` | 数字与价格必须人工审核 |
