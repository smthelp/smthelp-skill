# Himalaya Sent Folder — Empty Results Reference
> Last Verified: 2026-06-20

## Symptom (Updated 2026-07-08)

**Sent folder data via `himalaya envelope list`**:
```bash
# info_3dsmt Sent — 1 message found (2026-04-28 last sync):
# ID 49643: "[Whirlpool Brazil] — 40% CapEx reduction on THT insertion lines"
#   From: SMT sales Service Specialist | Date: 2026-04-28 04:01+00:00

# info_smthelp_eu Sent — 4 messages found (2026-04-28 last sync):
# ID 49645: "[Varela Electrónica] — Cómo reducir el costo de inserción THT en un 38%"
#   From: smthelp.eu | Date: 2026-04-28 04:01+00:00
# ID 49646: "[Varela Electrónica] — Cúyo reducir..." (encoding artifact, duplicate)
# ID 49580/49581: "[TEST] SMT EDM System Check"
```

**INBOX partial recovery observed (2026-07-08)**:
```
# info_3dsmt INBOX:
# ID 393454: "Goodnews." from info@1haag.com | Date: 2026-07-03 11:26+07:00
# ID 11978: "Welcome to TinkMail" | Date: 2026-04-10
```
IMAP sync is slowly recovering — messages from 2026-07-03 onwards are appearing in INBOX.

**Critical finding — `message read` always times out**:
```bash
# ALL of these timeout at 30 seconds with no output:
himalaya message read 49643    # (info_3dsmt Sent, confirmed ID exists)
himalaya message read 49645    # (info_smthelp_eu Sent, confirmed ID exists)
himalaya message read 393454  # (info_3dsmt INBOX, 2026-07-03)
```
Root cause: IMAP server response is slow; 30s timeout is insufficient even for short messages.

## Corrected Syntax (2026-07-08)

**Correct**: `himalaya message read <ID>` — positional argument, NO flag
**Wrong**: `himalaya message read --id <ID>` → `unrecognized argument '--id' found`

Default account in himalaya: `jasonwu_work` (not `jasonwu`).
All `message read` calls require timeout ≥ 60s minimum — but even that may not be enough for the slow IMAP server.

## Root Cause Assessment

1. **IMAP sync freeze**: Server-side IMAP sync from 2026-04-28 to ~2026-07-03 was frozen
2. **Partial recovery**: INBOX messages from 2026-07-03 onwards now appearing; Sent folder still stops at 2026-04-28
3. **Message body unreadable**: Even with valid IDs from `envelope list`, `message read` cannot retrieve body within 30s timeout
4. **Webmail fallback blocked**: `webmail.3dsmt.com` returns DNS/ALPN error; browser login impossible

## Recommended Fallback

- **Browser**: `https://outlook.office365.com` (if jasonwu@smthelp.com uses Microsoft 365)
- **Browser**: `https://mail.google.com` (if using Google Workspace)
- Both require manual login; cannot be automated in this session
