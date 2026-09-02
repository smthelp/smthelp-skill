---
name: smthelp-monthly-win-loss-review
description: "Monthly win-loss review for Southern Machinery SMT/THT equipment sales.\nRun on the 28th–31st of each month (Asia/Shanghai timezone).\nProduces a structured analysis of why deals advanced, stalled, or were lost,\nclassified into 7 loss categories, with 5 process and 5 messaging improvements.\nDesigned to run as a cron job with no user present — must handle data source\nunavailability gracefully.\n"
whenToUse: "monthly win-loss review，win loss report，monthly pipeline review，sales review，月报，月度复盘"
metadata:
  source: hermes
  origin: "sales-engineering/smthelp-monthly-win-loss-review"
---
# Southern Machinery Monthly Win-Loss Review

## Role
You are the win-loss review agent for Southern Machinery. Be honest, operational, and focused on what can improve sales execution.

## Objective
Summarize why opportunities advanced, stalled, or were lost during the month, classified into 7 loss categories, and turn those lessons into 5 process + 5 messaging improvements.

---

## Data Source Priority

**Primary:**
1. Worktile CRM — deal stages, pipeline data, follow-up records
2. Himalaya IMAP — email threads, proposal exchanges, reply patterns
3. Downloads directory — ROI files, PI/quote PDFs, campaign assets

**Fallback (all-sources-unavailable):**
- See `references/data-unavailability-fallback.md` — **mandatory fallback when CRM + email + session DB all fail**

---

## Execution Checklist

- [ ] Get current date: `date +%Y-%m-%d`
- [ ] Scan Downloads for recent business files (ROI, PI, proposals, campaign docs)
- [ ] Attempt Worktile CRM login → extract deal data
- [ ] Query Himalaya sent folder for outreach evidence
- [ ] Check smthelp.com reachability
- [ ] Assemble inferred pipeline health from file timestamps if all sources fail

---

## Output Format (6 sections, English)

### 1. Monthly Pattern Overview
- Outreach volume and channel mix (email/LinkedIn/ABM)
- Pipeline stage distribution (new leads, qualification, proposal, negotiation)
- Key product/campaign focus for the month
- Data confidence statement (confirmed vs inferred)

### 2. Win Reasons
- Top 3 reasons deals closed this month
- Specific product angles (S-70LD, custom feeders, wave soldering, etc.)
- Specific buyer segments or geographies

### 3. Loss Reasons
Classify into the 7 standard categories:
1. **Price** — budget constraints, cost sensitivity
2. **Specification mismatch** — wrong machine for the application
3. **Slow follow-up** — leads went cold, no sequence
4. **Insufficient qualification** — talking to non-buyers
5. **Service concern** — distrust of post-sale support
6. **Used-equipment competition** — JUKI/Yamaha/Universal used machines
7. **Timing or budget issue** — seasonal freeze, fiscal year constraints

Rank by frequency. Each category gets a brief mechanism explanation.

### 4. Process Improvements
5 concrete, actionable changes for next month (specific, not generic)

### 5. Messaging Improvements
5 concrete, actionable changes to outbound messaging, content, or positioning

### 6. Priority Actions
Table: Action | Owner | Deadline
Top 3 immediate actions for the first week of next month.

---

## Data Integrity Rules

1. **Never fabricate** deal counts, win/loss numbers, or pipeline percentages
2. **Flag inference level**: `[confirmed by CRM]` vs `[inferred from file timestamps]`
3. **When all sources fail**: use the `references/data-unavailability-fallback.md` checklist
4. **End with manual reconciliation request** if data gaps are critical

---

## Loss Classification Reference

| Category | Common Signal |
|---|---|
| Price | Prospect mentions budget ceiling; goes quiet after quote |
| Spec mismatch | Wrong PCB type, component size, or volume profile |
| Slow follow-up | No automated sequence; 5+ days between touches |
| Insufficient qualification | Broad outreach to non-decision-makers |
| Service concern | China equipment stigma; remote support skepticism |
| Used-equipment | Prospect mentions evaluating used JUKI/Yamaha |
| Timing/budget | Q3 shutdowns, fiscal year freeze, Q4 lock |

---

## Language
Output: **English**. Internal notes: Chinese acceptable. Technical terms: keep SMT, THT, PCB, PCBA, CPH, ROI, CapEx, FPY, BOM in English.

---

## Known Data Failure Modes (as of 2026-08-01)

| System | Failure | Since | Workaround |
|---|---|---|---|
| Worktile CRM | SSL cert invalid + demo login loop | Jun 2026 | Manual export or `pipeline-YYYY.csv` backup |
| Himalaya IMAP | Sync frozen | Apr 28, 2026 | Outlook webmail: outlook.office365.com |
| FTS5 session DB | Full corruption | Jun 17, 2026 | Skip; use Downloads + campaign files |
| smthelp.com | Was down | Jun 19 (restored Jul 6) | — |

---

## Support Files

- `references/data-unavailability-fallback.md` — mandatory checklist when all primary sources fail
