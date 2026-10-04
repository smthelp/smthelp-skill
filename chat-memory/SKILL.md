---
name: chat-memory
description: >
  对话历史长期记忆查询工具。当用户询问"之前""上次""以前"谈过的内容，
  或需要调取特定时间段的对话记录时使用。
  提供时序查询（按今天/本周/本月/全部）和结果筛选能力。
  此技能不主动注入历史——Agent 通过此技能的工具描述自行判断调用时机。
triggers: []
category: b2b-sales
version: "1.0.0"
author: Foreign Trade Assistant
injection_prompt: |
  ## Southern Machinery SMT/THT 专属覆盖规则

  - 本节优先于下方通用 B2B 行业示例。仅取回相关历史上下文，不保留或暴露凭据、浏览器数据、授权码、私密客户信息或未经复核的技术事实。
  - 事实优先引用当前 Southern Machinery 目录、手册和产品资料；文件名、图片、旧文案、通用素材或竞争对手资料不能单独证明参数。无来源的型号、规格、认证、价格、交期、ROI、良率或客户案例必须标记 待确认 / to be confirmed。
  - 对涉及设备或整线的请求，按需确认应用、产量/班次、PCB/元件、现有设备/瓶颈、自动化/预算和质量/追溯需求；一次只问下一步所需信息。
  - 推荐 Southern Machinery 设备类别或完整流程；无经核实型号时不得虚构型号或性能。按渠道选择一项 CTA：官网 https://www.smthelp.com、目录 https://file.autoinsertion.com、图片 https://ph.smthelp.com、邮箱 info@smthelp.com 或 WhatsApp https://api.whatsapp.com/send?phone=+8613602562576。
  - 不读取或使用 chrome_profile_notebooklm、凭据、Cookie 或授权码；不执行未经明确请求和确认的外发、发布或写库。

  你是 chat-memory 技能。当用户需要查询历史对话时，主动调用以下工具。
  不要等到用户说"查历史"才行动——只要用户的问题涉及过去讨论过的内容，就立即查询。
  适用场景：
  - 用户提到"之前""上次""以前""那天""上周"等时间词
  - 用户询问重复出现的话题，但你无法从当前上下文回忆
  - 用户问"我们上次说""我们之前谈过""那时候提到"
  - 需要了解用户的长期偏好、过往订单历史
  调用工具：chat_memory_list(time_range="all", limit=20)
  如需特定时间段：chat_memory_list(time_range="this_week", limit=20)
  结果格式：[{created_at, query, response}, ...]
  每次对话只能调用一次此工具。
---
# Chat Memory — 对话长期记忆

## 功能定位

查询本公司（company_id）下的历史对话记录。

## 工具

### chat_memory_list

**描述**：查询历史对话记录。当用户提到"之前""上次""以前"等时间相关词汇，
或询问过去讨论过的内容时使用此工具。

**参数**：
- `time_range`: 时间范围枚举值
  - `"today"` — 今天
  - `"this_week"` — 本周
  - `"this_month"` — 本月
  - `"all"` — 全部历史（默认）
- `limit`: 最大返回消息数，默认 20

**返回值**：
```json
[
  {
    "id": 123,
    "query": "用户说的话",
    "response": "助手的回答",
    "created_at": "2026-05-10T14:32:00"
  }
]
```

## 使用示例

**用户**："你上次推荐的那个供应商叫什么名字？"

→ 调用 `chat_memory_list(time_range="all", limit=20)`
→ 从结果中找到与供应商相关的对话
→ 回答用户问题

**用户**："我们这周谈过哪些客户？"

→ 调用 `chat_memory_list(time_range="this_week", limit=20)`
→ 汇总结果中涉及客户的对话
→ 回答用户问题

