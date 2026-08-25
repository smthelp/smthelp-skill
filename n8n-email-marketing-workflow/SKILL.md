---
name: n8n-email-marketing-workflow
description: "n8n automated email marketing setup for Southern Machinery S-70LD campaigns — SMTP credentials, workflow config, and send strategy"
metadata:
  source: hermes
  origin: "sales-engineering/n8n-email-marketing-workflow"
---
# n8n Email Marketing Workflow Setup — Southern Machinery

## Context
Jason Wu (CEO of Southern Machinery) uses n8n for automated email marketing campaigns targeting global EMS/ODM leads. This skill documents the complete setup for S-70LD campaign.

---

## n8n Instance
- **URL**: https://n8n.autoinsertion.com/
- **API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZDc0MTM1ZS01ZDYxLTRhZjQtOTdlMC03YmFjNzYwMWIyODUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZDE0OWE5NDEtMGRiYS00NTk4LWJkOWItOGMxYjNiZTNiNTU1IiwiaWF0IjoxNzc0MDc4OTcwfQ.UizhfjEgUHNovAcIhLn0pjnQ9Bp-tAEuS_BnmsgVa_E`

## SMTP Configuration
**Provider**: tinkmail.me (IMAP/SMTP service)

| Field | Value |
|-------|-------|
| IMAP Server | `imap.tinkmail.me` |
| IMAP Port | `993` (SSL/TLS) |
| SMTP Server | `smtp.tinkmail.me` |
| SMTP Port | `465` (SSL) or `587` (TLS) |
| Encryption | SSL/TLS |

**5 Sender Emails (all verified on tinkmail.me)**:
1. `sale@3dsmt.com` — credential ID: `bmAya39Zn0zP9yDH`
2. `service@3dsmt.com` — credential ID: `JYx1R9snbyuQrmwT`
3. `info@3dsmt.com` — credential ID: `iEppH7PnHXZaiU2j`
4. `support@3dsmt.com` — credential ID: `msCku8TpUYe1kKx5`
5. `info@smthelp.eu` — credential ID: `nRpSmQThSO0OK4aL`

**Passwords** (all 16-char app passwords from tinkmail.me):
- `LNEJXCKSTGUVKER4`, `1QADRZT666P5LQZX`, `9V46R8Z24ZI9RA3X`, `1UJVQA3WILI1QK2F`, `19I98XK4AWEWZKD1`

## n8n Workflow
- **S-70LD Email Marketing Workflow**: https://n8n.autoinsertion.com/workflow/lojK9lZdYQZZGKDe
- **Strategy**: Round-robin across 5 emails, batch 50 per run, <100/day per email

## Data Files
- Contact CSV: `~/Desktop/SMThelp_Data/CRM_Import/Mautic_Import_S70LD_Contacts.csv` (324 contacts)
- Workflow JSON: `~/Desktop/SMThelp_Data/CRM_Import/S70LD_Email_Marketing_Workflow.json`
- Personalized emails: `~/Desktop/SMThelp_Data/Email_Templates/Personalized_S70LD/`

## Key Endpoints
- n8n REST: `POST /api/v1/workflows` (create), `GET /api/v1/workflows` (list)
- n8n Credentials: `POST /api/v1/credentials`

## Complete Credentials Inventory
**See `references/n8n-credentials-inventory.md`** — 扫描了 n8n 100+ workflows，提取了 **37 个唯一凭证**：

| 凭证 | n8n ID | 用途 | Hermes状态 |
|-----|--------|-----|----------|
| `openAiApi` | muLaOXjMkdd9Gs4H | 64+ workflows AI核心 | 需配置 API key |
| `googlePalmApi` | STquDRE7YZ2EYkFE | Gemini AI (39+ workflows) | 需配置 |
| `tavilyApi` | xlg4GFbaUMFmNaNQ | Tavily搜索 (4+ workflows) | **需配置** |
| `feishuApi` | q5eS7vUUArexxc1K | 飞书通知 (14+ workflows) | **需配置** |
| `nocoDbApiToken` | UWcovOBjHHScH0ul | NocoDB CRM (12+ workflows) | **需配置** |
| `telegramApi` | WIIaijOVKMJFPq3V | Telegram Bot (9+ workflows) | **需配置** |
| `openRouterApi` | IhNO4wFMGxXSPq04 | OpenRouter (13+ workflows) | ✅ auth.json 已配置 |

> ⚠️ n8n 凭证加密存储，无法通过 API 提取实际密钥。需在对应平台重新获取后配置。

## Important Notes
- Each SMTP credential must be manually selected in each Send Email node in n8n UI
- Daily limit: <100 emails per sender email (5 emails × 50 batch = safe margin)
- Workflow must be manually activated in n8n UI after CSV path is confirmed
