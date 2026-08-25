# smthelp.com Outage Reference
> Last Verified: 2026-06-20

## Confirmed Outage

| Endpoint | Status | Notes |
|---|---|---|
| `https://www.smthelp.com` | ❌ TIMEOUT | Both HTTP/HTTPS fail |
| `http://www.smthelp.com` | ❌ TIMEOUT | — |
| `mail.3dsmt.com` | ❌ DNS/ALPN error | — |
| `webmail.3dsmt.com` | ❌ DNS/ALPN error | — |

## Working Alternatives

| Purpose | URL | Status |
|---|---|---|
| 产品落地页 | `https://www.3dsmt.com` | ✅ Working |
| 图床/文件上传 | `https://ph.smthelp.com` | ✅ Working |
| YouTube Channel | `https://www.youtube.com/c/Smthelping` | ✅ Working |
| Wiki产品库 | `~/wiki/southern-machinery-wiki.md` | ✅ Local |

## Impact on Daily Report

- EDM 追踪链接 → 不可用，标注 `[官网数据待恢复]`
- 官网表单询盘数据 → 不可用
- 邮件签名 smthelp.com 链接 → 临时替换为 `3dsmt.com`

## Should NOT retry today

Do NOT loop-retry smthelp.com within the same session. If curl returns non-200 or timeout, immediately use alternatives. Re-check only in next daily-report cycle.
