---
name: ceo-pipeline-report-generator
description: "Generate the Friday CEO Weekly High-Value Pipeline Intelligence Report for Southern Machinery CEO Jason Wu. Aggregates data from Worktile CRM, IMAP/himalaya email, WhatsApp files, and Hermes session history. Produces a strict 3-section executive brief: Section A ($50K+ CapEx deals with bottleneck mapping), Section B (Parameter Blocker Funnel), Section C (Monday Priority Targets - 3 SPIN-forced tactics). Runs as cron Friday 5:30 PM. Output bulleted, rapid-fire, zero filler, key terms UPPERCASE."
---

# CEO Pipeline Intelligence Report Generator

## When to Use This Skill

- The cron_ceo_pipeline_intelligence scheduled job fires (Friday 5:30 PM).
- User requests: generate CEO pipeline report, CEO周报, pipeline intelligence report, CEO weekly brief, CEO专属周报.

## Data Sources and Access Patterns

## Data Sources and Access Patterns

### known-accounts.md — OPERATIONAL PRIMARY SOURCE (2026-06-26)
- Path: `references/known-accounts.md` in this skill's directory.
- Status as of Jun 26: Worktile browser automation timed out, himalaya sent folders showed only Apr-28 EDM campaigns, kanban.db returned 0 rows, FTS5 permanently corrupted.
- **known-accounts.md is the only source with verified, current CapEx figures and bottleneck descriptions.** Always load it first. Use all other sources as cross-reference only.
- Update known-accounts.md immediately after each morning run if new deal intelligence is found via browser or himalaya.

### Worktile CRM
- URL: https://smthelp.worktile.com
- Login: 13602562576 / nbjxJY3-1806WJX (mobile + password)
- Dashboard: https://smthelp.worktile.com/dashboard — reliably accessible.
- ⚠️ DO NOT use xiaoman_crm_scraper.py — Worktile is the operative CRM, not Xiaoman CRM.
- ⚠️ NOT v5.viwolf.cn/admin888 — that domain has a broken SSL cert and demo login loop. Always use smthelp.worktile.com.
- ⚠️ PROJECT PAGE URLS TIME OUT (e.g., https://smthelp.worktile.com/jasonwu客户管理CRM). Do NOT navigate directly to project pages — extract task data from the dashboard view instead.
- ⚠️ NOT v5.viwolf.cn/admin888 — that domain has a broken SSL cert and demo login. Use smthelp.worktile.com.
- Primary query: all tasks, overdue tasks, active deals with $50K+ CapEx potential.
- CRM Task Detail Extraction: click task row → browser_console("document.body.innerText.substring(3000, 8000)")
- ⚠️ Known issue: Task detail panels are Shadow DOM/lazy-load — use browser_console expression above, NOT browser_snapshot.
- ⚠️ DO NOT use xiaoman_crm_scraper.py — Worktile is the operative CRM, not Xiaoman CRM.
- Session expires in ~10-15 minutes of inactivity. Complete all browser operations in rapid sequence before logging out.
- ⚠️ DO NOT use xiaoman_crm_scraper.py — Worktile is the operative CRM, not Xiaoman CRM.
- Session expires in ~10-15 minutes of inactivity. Complete all browser operations in rapid sequence before logging out.

### IMAP / Himalaya Email
- Accounts: info_3dsmt, info_smthelp_eu, sale_3dsmt
- Command: himalaya envelope list --account <acct> --folder Sent --page 1 --page-size 5
- Known issue: Inboxes show only TinkMail welcome messages, not real emails. Use sent folder as primary source.
- If both inbox and sent are empty of real correspondence, note the gap. Do not fabricate email activity.

### WhatsApp
- Path: ~/Library/Containers/net.whatsapp.WhatsApp/Data/Library/Application Support/net.whatsapp.WhatsApp/
- Structural limitation: In headless cron (no GUI), WhatsApp container is NOT accessible. File timestamps cannot be read.
- Workaround: Morning run (10:17 AM Friday) may have GUI access - capture WhatsApp context then. Evening run cannot supplement it.
- If WhatsApp data was not accessible, state explicitly in the report.

### Hermes Session History (state.db)
- Query: sqlite3 ~/.hermes/state.db "SELECT substr(content, 1, 300) FROM messages WHERE content LIKE '%<company>%' ORDER BY rowid DESC LIMIT 3;"
- Session search: session_search(query="<company>", limit=5, sort="newest")
- Primary value: deal status updates, bottleneck descriptions, contact names from prior sessions.
- Key accounts: E.G.O. Spain, GRSYS Brazil, ALARMTRADE.RU, VOSSLOH-SCHWABE Germany, Fitech Poland, Kimball Electronics Mexico, Liteon Brazil.

### Kanban DB
- Path: ~/.hermes/kanban.db
- Query: sqlite3 ~/.hermes/kanban.db "SELECT id, name, status, priority FROM tasks WHERE status NOT IN ('done','cancelled') ORDER BY priority DESC LIMIT 20;"
- Note: As of mid-2026, task table often returns 0 rows. Do not rely on kanban as primary deal tracker.

## Report Structure (Strict - 3 Sections Only)

### SECTION A: HIGH-VALUE ACTIVE DEALS ($50K+ CapEx) - BOTTLENECK MAPPING

For each deal:
- Company + Country
- CapEx range (confirmed or TBD)
- BOTTLENECK: One precise sentence. Use: EMAIL DRAFT NOT YET DISPATCHED / CE/IPC/JEDEC CERTIFICATION BLOCK / NO FORMAL PO ISSUED / TECHNICAL DISCUSSION STALLED / etc.
- ACTION REQUIRED: One specific actionable next step.
- If account appears in session research but has NO active CRM task: mark with warning + instruct to verify with Kevin/Leo.

Known accounts to verify before reporting:
- E.G.O. Spain (EUR 280K-320K CapEx) — 6-module THT/SMT proposal, new CEO + CFO. CRM task EXISTS: SCL35097 under Kevin Yang's project. Kevin to dispatch proposal. ✅ CONFIRMED Jul 24.
- GRSYS Brazil (~$34K CapEx) — 11 active tasks confirmed (Aug 7, 2026: SCL32286, SCL33912, SCL35048, SCL35893, SCL35199, SCL35664, SCL35651, SCL34873, SCL36445, SCL36623, SCL32404). Post-factory-visit. AOI expansion needed to breach $50K. Search is reliable — do NOT flag as integrity issue.
- Fitech Poland (USD 7,500-9,800) — feeder orders, confirmed from session Jun 10
- ALARMTRADE.RU ($13K-15K CapEx) — vacuum bunching machine, CE cert block
- VOSSLOH-SCHWABE SERBIA (TBD CapEx) — S-7000 THT, no bare board dimensions. ⚠️ 6 CRM TASKS FOUND Jul 24 (SCL34978, SCL34982, SCL34977, SCL36284, SCL36292, SCL34975). Serbia entity confirmed in task descriptions. Germany entity is separate — verify which is active commercial prospect.

Caution: Names like CE3 Electronics Canada in the cron prompt are EXAMPLES only - not confirmed accounts. Do not include without CRM or session data verification.

### SECTION B: PARAMETER BLOCKER FUNNEL - CLIENTS LOCKED PENDING TECHNICAL DATA

Itemize all accounts blocked on:
- Bare board dimensions (PCB size, thickness, hole size)
- CPH targets (production volume, shifts)
- JEDEC tray dimensions / N2 purity (vacuum equipment)
- Existing feeder model numbers (feeder cross-reference)
- Max THT component height range

For each:
- Country + company
- Specific missing parameter
- One concrete unblocker (e.g., send JIS/JEDEC tolerance form + pre-filled layout preview)

### SECTION C: MONDAY PRIORITY TARGETS - 3 SPIN-FORCED BREAKTHROUGH TACTICS (7-DAY)

Each tactic:
- Target account + SPIN type
- Exact phrasing for each SPIN stage (write the actual questions/statements)
- Channel: Email / WhatsApp / both
- Contact name and coordinates if known

Standard SPIN tactic templates:

Tactic 1 - Commercial breakthrough (new CFO/CEO transition):
SPIN: Situation to Problem to Implication to Need-Payoff
Channel: Email + WhatsApp follow-up 48h later

Tactic 2 - Technical + commercial decision (post-factory-visit stall):
SPIN: Problem Agitation + Budget Justification + Urgency Lever
Channel: WhatsApp direct + remote FAT offer

Tactic 3 - Technical spec clarity (quotation blocked by missing parameters):
SPIN: Implication + Need-Payoff
Channel: Email with data form + WhatsApp voice note follow-up

## Output Format Rules

- UPPERCASE for: CEO, CRM, SMT, THT, PCB, CPH, CapEx, SPIN, IMAP, PO, ROI, GM, EMS, OEM, AOI, SPI, MES, CAD, FAT, DIP
- Bulleted, rapid-fire executive style
- Zero filler: no Great question, no Im happy to help, no In conclusion
- One precise bottleneck sentence per deal - no vague engagement ongoing language
- No section introductions - output starts directly with SECTION A

## Dual-Run Friday Logic

Cron fires twice Friday:
- Morning (10:17 AM): Primary data aggregation. Full 3-section report.
- Evening (5:30 PM): Supplements morning with same-day email/WhatsApp responses post-cutoff.

Evening run decision rules:
1. Check if morning report session exists (session_search for CEO Weekly High-Value Pipeline Intelligence Report from today).
2. Query himalaya for new sent emails since morning timestamp.
3. New emails found - include as bottleneck update in relevant deal.
4. NO new data + morning report comprehensive - output [SILENT] to suppress redundant delivery.
5. WhatsApp data not accessible - note in report, do not claim it.

### New Overdue Task Discovered (2026-07-03)
- **SCL 36628**: "策划免费试用方案（有条件PO）" — OVERDUE SINCE JUNE 22. Appears in Worktile overdue task list. Must appear in report administrative notes section.
- This task is in the JasonWu客户管理CRM project and appears in both the "全部" and "延期" task views.

## Pitfalls

### FTS5 DB Corruption — PERMANENT
- session_search has been offline since 2026-06-17 (full DB corruption). Do NOT retry. Use Worktile CRM + himalaya as primary sources only.
- If prior session context is needed for a deal, fall back to known-accounts.md reference file.

### Himalaya Inboxes Unreliable
- info_3dsmt INBOX shows only TinkMail welcome messages (2026-04-10). Real trade emails are NOT appearing.
- Use Sent folder as primary email source. If both empty, note explicitly in report — do not fabricate email activity.

### WhatsApp Inaccessible in Cron
- ~/Downloads/ WhatsApp images (e.g. "WhatsApp Image 2026-06-05 at 16.26.18.jpeg") cannot be attributed to specific clients without GUI access.
- Do not claim WhatsApp context in evening run unless morning run captured it. State limitation explicitly.

### CRM Task Detail Extraction — Cascading Substring Protocol

**Observation (2026-07-17)**: `substring(3000, 8000)` returned EMPTY for SCL 36628 (short task description). `substring(0, 5000)` succeeded on the same task. Longer tasks (e.g., SCL 33997 LEANVAL with full email thread) may need the higher offset.

**Always use a cascading protocol — never try just one range**:
1. First try: `document.body.innerText.substring(0, 5000)` — short to medium task descriptions
2. If empty, try: `document.body.innerText.substring(3000, 8000)` — long tasks with extended email threads
3. If still empty, try: `document.body.innerText.substring(0, 10000)` — full dump
4. Re-navigate to task and re-extract in the same session — stale reads return empty

**Rule**: browser_snapshot CANNOT read task detail panel content (Shadow DOM / lazy-load). ALWAYS use browser_console. Session expires in ~10-15 minutes — complete all detail extraction in rapid sequence before logging out.

### Worktile Task Detail Panel Workaround
- CRM task MUST exist before including an account in Section A or B.
- Accounts found in session history but NOT in Worktile CRM must be flagged: "⚠️ VERIFICATION REQUIRED — NO CRM TASK" and assigned to the correct owner (Kevin/Leo/Jason) before promotion.
- Do NOT include CE3 Electronics Canada or any name that appears only in the cron prompt as a verified account.

### Live CRM Search Returning No Results for Known Accounts — REVISED (2026-07-10)
- AS OF 2026-07-03: E.G.O. Spain, VOSSLOH-SCHWABE listed as "CRM task NOT FOUND" in known-accounts.md.
- REVISED FINDING (2026-07-10): E.G.O. Spain DOES have a CRM task — SCL35097 "背调客户：E.G.O. Appliance Controls, S.L.U." — but it lives in Kevin Yang's project ("Kevin Yang外贸客户管理"), not Jason's project. Worktile's search box returns cross-project results, so Kevin's task IS visible from Jason's dashboard search.
- GRSYS Brazil: 11 active tasks confirmed under JasonWu客户管理CRM on 2026-07-10 (SCL32286, SCL33912, SCL35048, SCL35893, SCL35199, SCL35664, SCL35651, SCL34873, SCL36445, SCL36623). The Jul 3 "CRM task NOT FOUND" flag was INCORRECT.
- Action: When named search returns no Jason-account task, always scroll the search results to check Kevin/Leo project tasks before flagging as unverified. Cross-project search is the correct verification methodology — it surfaces tasks regardless of project ownership.

### Advanced Search Dialog Freeze — Refined (2026-07-31)
- Symptom: Searching for "Kimball", "E.G.O.", or any term with special characters (dots, spaces) triggers advanced search dialog that freezes page render. browser_snapshot and browser_console both time out.
- Root cause: Advanced search dialog initiates slow server-side indexing; UI becomes unresponsive during this phase.
- Workaround (REVISED):
  1. After pressing Enter and seeing the dialog appear, press Escape IMMEDIATELY — do not wait for results.
  2. The search box may now refuse direct typing for ~10-30 seconds (timeout error).
  3. **FIX:** Click the search box first to re-focus it, THEN type. Direct type-after-escape without prior click causes a 30-second timeout.
  4. If dialog freeze persists: navigate directly to https://smthelp.worktile.com/dashboard to reset session.
- Known accounts that trigger this: Kimball Electronics Mexico, E.G.O. Spain (any term with dots/special chars).

### GRSYS Search — PATTERN REVISED (2026-08-07)
- Prior run-logs (Jul 10, Jul 24, Jul 31) all reported "0 tasks" for GRSYS — flagged as recurring search failure.
- REVISED FINDING (2026-08-07): Search term "GRSYS" (clean ASCII, no special characters) returned all 11 tasks normally — SCL32286, SCL33912, SCL35048, SCL35893, SCL35199, SCL35664, SCL35651, SCL34873, SCL36445, SCL36623, SCL32404.
- Root cause of prior failures: SESSION TIMEOUTS, not a CRM search defect. The search itself is reliable.
- ACTION: The "do not retry" and "integrity issue" guidance in prior run-logs is REVOKED. Use clean ASCII search term "GRSYS". If 0 tasks returned on a future run, re-login and retry once before flagging as integrity issue.

### GRSYS Brazil — Recurring CRM Search Failure (2026-07-31) — SUPERSEDED
- The "do not retry" guidance from this section is REVOKED as of 2026-08-07. See GRSYS Search — PATTERN REVISED above.
