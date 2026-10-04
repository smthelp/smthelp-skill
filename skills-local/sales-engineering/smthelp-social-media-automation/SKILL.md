---
name: smthelp-social-media-automation
description: Southern Machinery 社交媒体自动化项目 — LinkedIn/Twitter/Facebook/YouTube 自动发帖和评论管理
version: 2.0.0
date: 2026-04-20
triggers:
  - Twitter API申请
  - LinkedIn API申请
  - YouTube API申请
  - Facebook API申请
  - 社交媒体自动发帖
  - 自动回复评论
---

# Southern Machinery 社交媒体自动化项目

## 账号汇总

| 平台 | URL/ID | 状态 |
|---|---|---|
| LinkedIn公司页 | linkedin.com/company/smtmachine | Dev App ID 233750230，Marketing API申请中 ⏳ |
| LinkedIn个人页 | linkedin.com/in/smtsupplier | — |
| Twitter | @smtspecialist | 需5个X API凭证 ⏳ |
| Facebook | facebook.com/autoinsertion | 需创建App ⏳ |
| YouTube | Channel ID: UClX0iEG2bvJq8yUBEDamgDw | 凭证完整 ✅ |

## YouTube API凭据（完整）
- Channel ID: UClX0iEG2bvJq8yUBEDamgDw
- Data API Key: AIzaSyC_k1dnD-7xtiK2Bs6NyR2B7-xXDEfNwuM
- OAuth Client ID: 998061498769-qm0u7j2tu7ae9dk5kphjripbu574c7dd.apps.googleusercontent.com
- OAuth Client Secret: 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
- 状态: 凭证完整，可配置n8n工作流 ✅

## LinkedIn 申请文案（直接复制）
> "We are Southern Machinery, a Shenzhen-based manufacturer of SMT/THT automation equipment serving EMS/ODM factories globally. We need Marketing Developer Platform access to publish product updates, industry articles, and technical content to our LinkedIn Company Page (linkedin.com/company/smtmachine) — similar to using Hootsuite or Sprout Social. Posting frequency: 3–5 posts/week. All content is posted under our authentic company identity. We do not use this for advertising or personal data collection."

## 平台申请经验
### 关键教训：Browser会话无法保持社交平台登录状态
LinkedIn、Twitter等平台在headless browser中强制跳转登录页。解决方案：**提供详细文字指引 + 用户截图反馈**，而非尝试自动化操作。

## 自动评论规则
| 关键词 | 自动回复方向 |
|---|---|
| price/quote/报价 | 引导发邮件 jasonwu@smthelp.com |
| delivery/ship/货期 | 提供参考货期范围 |
| SMT/THT/insertion | 介绍 Southern Machinery 产品线 |
| specification/规格 | 提供产品规格文档下载链接 |

## 邮件提醒触发条件
1. 询价预估金额 > $50,000
2. 技术问题无预设规则可回复
3. 竞品对比求助
4. 重复投诉 ≥2次
5. 涉及合同/付款条件
## 目标

1. 定时发帖（每天自动发1-3条）
2. 自动读取+回复评论
3. 疑难评论邮件提醒吴总（jasonwu@smthelp.com）

## §2 — YouTube Upload Automation (n8n + YouTube OAuth)

> This section consolidated from `youtube-upload-automation` skill. Full reference at `references/youtube-upload-automation.md`.

### Context
- User: 吴总 (Jason Wu), CEO of Southern Machinery
- YouTube Channel: `UClX0iEG2bvJq8yUBEDamgDw` (smthelp.com)
- n8n instance: https://n8n.autoinsertion.com
- OAuth Credentials: ID + Secret collected, Refresh Token PENDING

### Files Generated
- `~/n8n_youtube_upload_workflow.json` — complete n8n workflow for automated YouTube upload
- `~/wave_soldering.py` — ManimGL animation script (7 scenes, ~22KB, fails headless)

### YouTube OAuth Setup (Critical)
To upload videos, need Refresh Token. Steps:
1. User opens auth URL with OAuth client ID
2. User gets authorization code from browser
3. Exchange code for Refresh Token via POST to Google OAuth

**Auth URL:**
```
https://accounts.google.com/o/oauth2/auth?client_id=998061498769-qm0u7j2tu7ae9dk5kphjripbu574c7dd.apps.googleusercontent.com&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&response_type=code&access_type=offline
```

### Hostinger API Diagnostics
- API Token `ikHAQZcf4PtDEHAnhXPhh9Me08msCINs5XssgLEg3f09ea6e`: Valid (200 OK)
- Cloud API returns empty `[]` for VMs — user has hPanel VPS, not Cloud VPS
- n8n server confirmed online at 198.18.24.15

### ManimGL on macOS
- `python3 -m pip install manimgl` ✅ installed
- Headless rendering fails (OpenGL/X11 not available in terminal)
- Need Xvfb (`brew install xorg-opengl`) or run with Xvfb
- Alternative: render on CI/CD runner or ask user to render locally

### n8n Workflow Pattern
```python
# n8n API to trigger workflow
POST https://n8n.autoinsertion.com:443/rest/workflows/{id}/run
Authorization: Bearer {api_key}
```

### "always" Command
User says "always" = keep going without asking for confirmation.

For full YouTube upload workflow details and OAuth troubleshooting, see `references/youtube-upload-automation.md`.
