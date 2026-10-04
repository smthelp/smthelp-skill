# smthelp.com / 3dsmt.com / webmail DNS & TLS Outage Reference
> Last Updated: 2026-07-01

## Confirmed Outages

### smthelp.com — Full HTTP/HTTPS Timeout
- **Status**: Unreachable since ~2026-06-19
- **Error**: `curl` times out on both HTTP and HTTPS (connect-timeout 5s)
- **Affected**: `www.smthelp.com`, `mail.3dsmt.com`, `webmail.3dsmt.com`
- **Root Cause**: Unknown — likely DNS resolution failure or upstream network issue

### webmail.3dsmt.com — TLS ALPN Failure
- **Error**: `net::ERR_DNS_NO_MATCHING_SUPPORTED_ALPN`
- **Symptom**: DNS resolves, but TLS handshake fails — browser refuses connection
- **Different from smthelp.com**: This is a TLS configuration issue on the mail server, not a network reachability issue
- **Impact**: Cannot use webmail as Himalayan IMAP fallback

## Functional Alternatives

| Resource | URL | Status |
|----------|-----|--------|
| Product landing pages | `https://www.3dsmt.com` | ✅ Working |
| Image hosting (Chevereto) | `https://ph.smthelp.com` | ✅ Working |
| YouTube channel | `https://www.youtube.com/c/Smthelping` | ✅ Working |
| Worktile CRM | `https://smthelp.worktile.com` | ✅ Dashboard accessible |
| Outlook 365 (if using M365) | `https://outlook.office365.com` | ⚠️ Untested |

## Email Sending Infrastructure

- **SMTP**: `smtp.exmail.qq.com:465` (Tencent Enterprise Email) — likely still functional
- **IMAP**: `imap.exmail.qq.com:993` — likely still functional
- **Himalaya config**: Accounts use `imap.tinkmail.me:993` — may be the source of sync failures
- **Personal email**: `jasonwu@smthelp.com` — configured as `jasonwu_work` in himalaya

## Daily Report Handling

In daily reports, replace all `www.smthelp.com` links with `www.3dsmt.com`.
Email signature links: change `smthelp.com` → `3dsmt.com`.
If product pages are needed: use `https://www.3dsmt.com` as the fallback URL.
