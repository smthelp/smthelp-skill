# n8n Credentials Inventory — Southern Machinery

> Complete credential inventory from `https://n8n.autoinsertion.com`  
> Generated: 2026-04-19  
> Total: **37 unique credentials** across **100+ workflows**

---

## 🔑 Priority Credentials for Hermes Integration

These credentials are most relevant for the Southern Machinery sales engineering copilot:

### High Priority

| Credential | n8n ID | Used In | Hermes Action |
|-----------|--------|---------|--------------|
| `tavilyApi` | `xlg4GFbaUMFmNaNQ` | THT Newsletter, SEO workflows | **配置为 custom_provider** — 需提供 API key |
| `openAiApi` | `muLaOXjMkdd9Gs4H` | 64+ workflows (AI backbone) | **配置为 custom_provider** — 需提供 API key |
| `feishuApi` | `q5eS7vUUArexxc1K` | 14+ workflows (飞书通知) | **配置飞书机器人** — 需提供 App ID/Secret |
| `nocoDbApiToken` | `UWcovOBjHHScH0ul` | 12+ workflows (CRM数据) | **配置 NocoDB HTTP 工具** — 需提供 URL+Token |
| `telegramApi` | `WIIaijOVKMJFPq3V` | 9+ workflows (消息通知) | **配置 Telegram Bot** — 需提供 Bot Token |

### Medium Priority

| Credential | n8n ID | Used In | Hermes Action |
|-----------|--------|---------|--------------|
| `gmailOAuth2` | `yFdOJv9ZyTglzTP7` | Newsletter发送 | Google OAuth2 配置 |
| `googleSheetsOAuth2Api` | `4gE9qCl2xNhcu89w` | CRM联系人/发送记录 | Google Workspace 配置 |
| `perplexityApi` | `MYObXKQcELmobTMJ` | SMT_marketing_team_agent | 配置为 custom_provider |
| `slackApi` | `H9f6ZHrFyzO8XyH7` | Twitter工具通知 | 配置为 custom_provider |
| `serpApi` | `nJkwffsD6EgKCYF9` | 关键词研究 | 配置为 custom_provider |
| `openRouterApi` | `IhNO4wFMGxXSPq04` | 13+ workflows | ✅ 已在 auth.json 配置 |

### Already Integrated

| Credential | n8n ID | Status |
|-----------|--------|--------|
| `openRouterApi` | `IhNO4wFMGxXSPq04` | ✅ auth.json 中已配置 |

---

## 📋 Complete 37 Credential Inventory

| # | Type | n8n ID | Use Case | Workflow Count |
|---|------|--------|---------|--------------|
| 1 | openAiApi | muLaOXjMkdd9Gs4H | OpenAI GPT AI | 64+ |
| 2 | googlePalmApi | STquDRE7YZ2EYkFE | Google Gemini AI | 39+ |
| 3 | googleSheetsOAuth2Api | 4gE9qCl2xNhcu89w | Google Sheets R/W | 26+ |
| 4 | httpHeaderAuth | FmO9scu8BZAG9sIh | HTTP Header Auth | 35+ |
| 5 | openRouterApi | IhNO4wFMGxXSPq04 | OpenRouter AI路由 | 13+ |
| 6 | feishuApi | q5eS7vUUArexxc1K | 飞书消息 | 14+ |
| 7 | nocoDbApiToken | UWcovOBjHHScH0ul | NocoDB | 12+ |
| 8 | telegramApi | WIIaijOVKMJFPq3V | Telegram Bot | 9+ |
| 9 | supabaseApi | X3jHu3IhNtBnMrqH | Supabase | 9+ |
| 10 | notionApi | IaBXrSyEVfoRj6pc | Notion | 12+ |
| 11 | tavilyApi | xlg4GFbaUMFmNaNQ | Tavily搜索 | 4+ |
| 12 | httpBearerAuth | 8VxsT65CAvHQ9UcH | HTTP Bearer (MCP) | 6+ |
| 13 | gmailOAuth2 | yFdOJv9ZyTglzTP7 | Gmail发送 | 5+ |
| 14 | googleDriveOAuth2Api | 2UBJl7nk7fDl58BB | Google Drive | 12+ |
| 15 | imap | 5y2uBw9xaKR2vi9T | info@SMThelp 收件 | 2 |
| 16 | whatsAppTriggerApi | OYiPqcQG2DFCrFib | WhatsApp Business | 1 |
| 17 | slackApi | H9f6ZHrFyzO8XyH7 | Slack | 1 |
| 18 | perplexityApi | MYObXKQcELmobTMJ | Perplexity搜索 | 1 |
| 19 | serpApi | nJkwffsD6EgKCYF9 | Google SerpAPI | 1 |
| 20 | deepSeekApi | qldM0mDcbxPFEBMQ | DeepSeek AI | 4 |
| 21 | ollamaApi | omAqeszLOScMTIaa | Ollama本地LLM | 1 |
| 22 | pineconeApi | T25yxspOSRffX9rr | Pinecone向量库 | 3 |
| 23 | postgres | GeZuZqpKnSgpDd76 | PostgreSQL | 1 |
| 24 | githubApi | LjHpZskvTBumrUz7 | GitHub API | 1 |
| 25 | airtableTokenApi | vzXvWO1If9x1Gtcb | Airtable | 1 |
| 26 | linkedInOAuth2Api | NBhJTLhQ8Mv35Z9A | LinkedIn | 2 |
| 27 | twitterOAuth2Api | mfBfJa3FSioefgq6 | Twitter/X | 1 |
| 28 | youTubeOAuth2Api | jJUuhfvXa6Pm3F4G | YouTube API | 3 |
| 29 | jimengCredentialsApi | cgC3Spj444nCilif | 即梦图像 | 1 |
| 30 | facebookGraphApi | Gw0538BjGKKRxk76 | Facebook Graph | 1 |
| 31 | n8nApi | jx1tR2H6WwUS1IYQ | n8n自调用 | 2 |
| 32 | anthropicApi | X6RVrd0hwBejn65o | Anthropic Claude | 1 |
| 33 | httpQueryAuth | 28KdaflvUHbIQGUX | HTTP Query | 2 |
| 34 | googleOAuth2Api | ZbZ42kOirvj6dtJU | Google OAuth2 | 1 |
| 35 | googleDocsOAuth2Api | ZtPeN2dhYJXoGKlD | Google Docs | 1 |
| 36 | baiduWpApi | PDdJb7EHKKV1U8Vf | 百度WP | 1 |
| 37 | mcpClientApi | RNuV7GAihennyvTi | MCP Client | 1 |

---

## ⚡ Hermes 集成操作指南

### 第一步：配置环境变量（需要用户提供以下 key）

```bash
# AI / 搜索
export TAVILY_API_KEY="tvly-xxxxx"          # https://tavily.com
export OPENAI_API_KEY="sk-xxxxx"            # OpenAI
export TELEGRAM_BOT_TOKEN="123456:ABC-xxx"  # Telegram BotFather
export FEISHU_APP_ID="cli_xxx"              # 飞书应用 App ID
export FEISHU_APP_SECRET="xxx"              # 飞书应用 App Secret
export PERPLEXITY_API_KEY="pplx-xxx"        # perplexity.ai
export SLACK_BOT_TOKEN="xoxb-xxx"           # Slack OAuth
export DEEPSEEK_API_KEY="sk-xxx"            # DeepSeek

# 数据库 / CRM
export NOCODB_URL="https://nocodb.smthelp.com"
export NOCODB_API_TOKEN="xxx"
```

### 第二步：添加到 Hermes config.yaml

```yaml
custom_providers:
  - name: tavily
    base_url: https://api.tavily.com/v1
    api_key: ${TAVILY_API_KEY}
    model: tavily-search
  - name: openai-gpt4
    base_url: https://api.openai.com/v1
    api_key: ${OPENAI_API_KEY}
    model: gpt-4o
  - name: deepseek
    base_url: https://api.deepseek.com/v1
    api_key: ${DEEPSEEK_API_KEY}
    model: deepseek-chat
```

### 第三步：通过飞书/Telegram 触发 n8n Workflow

| 触发方式 | n8n Workflow ID | 说明 |
|---------|----------------|------|
| 飞书机器人 | `EOzTkIluhIcBtkRP` | THT Newsletter AI Agent V2 |
| Telegram | `DSwqFn4OUEdxKTlI` | WhatsApp 2576 Chat V0 |
| HTTP Webhook | `9m0WlYKryPYATNZk` | Jason MCP V0 |

---

## 🔍 验证凭证可用性

```python
# 验证 n8n 连接
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "https://n8n.autoinsertion.com/api/v1/workflows?limit=1"

# 验证 Tavily
curl -s -H "Authorization: tvly-$TAVILY_API_KEY" \
  "https://api.tavily.com/v1/search?query=test"

# 验证 Telegram Bot
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
```

---

## 📝 备注

- n8n 凭证在数据库中**加密存储**，API 无法读取实际密钥
- 需要在对应平台重新获取 API key 后配置到 Hermes
- Hermes 使用 `custom_providers` 方式集成，API key 通过环境变量注入
- 已配置的凭证（OpenRouter）可直接使用，无需重复配置
