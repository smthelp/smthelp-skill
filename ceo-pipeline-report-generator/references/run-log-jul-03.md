# CEO Pipeline Report — Session Run 2026-07-03

## Live CRM Findings

### Verified: SCL 33997 LEANVAL S.A.
- Search by "LEANVAL" → returns SCL 33997 task ✓
- Task detail extracted via `document.body.innerText.substring(3000, 8000)`
- Key bottleneck confirmed: **INTEGRALTEK (intermediate) has NOT confirmed SMT/THT procurement authority**
- Last email exchange: 2026-03-18 — 90+ days of silence
- Email thread shows: technical specs fully exchanged, cleanroom/ESD docs delivered, but commercial negotiation for SMT/THT machine portion completely stalled
- INTEGRALTEK contacts: Raphael Brylkowski + Agustin Martino

### NOT FOUND in live CRM search (2026-07-03):
- "E.G.O." / "E.G.O. Spain" → only generic annual tasks, NO company-specific task
- "GRSYS" → only generic annual tasks, NO company-specific task
- "VOSSLOH" → only generic annual tasks, NO company-specific task
- "Kimball" → only generic annual tasks, NO company-specific task

**Conclusion**: known-accounts.md verified status does NOT guarantee a live CRM task exists. All accounts must be confirmed against live search on run day.

## New Overdue Task Discovered
- **SCL 36628**: "策划免费试用方案（有条件PO）" — OVERDUE SINCE JUNE 22. Appears in overdue task list. Must appear in report administrative notes.

## Email/Himalaya Status (2026-07-03)
- info_smthelp_eu INBOX: only TinkMail welcome (2026-04-09) ✓ expected
- info_smthelp_eu SENT: 4 entries (2 test + 2 EDM with UTF-8 corruption on Spanish chars) — sparse, consistent with known-issues
- info_3dsmt + sale_3dsmt: IMAP connection failures confirmed (connection closed / TLS errors)
- No new high-value email threads discovered

## WhatsApp
- ~/Downloads/ shows 1 file: Fitech_Feeder_Report_2024_preview.png (Jun 10) — NOT new this week
- Cron run (5:30 PM) cannot access WhatsApp GUI — consistent with known limitation

## Known-Accounts.md Bottleneck Updates Needed
1. **LEANVAL**: Update bottleneck text — INTEGRALTEK lacks SMT/THT procurement authority, not just "no reply". This is more specific and actionable.
2. **E.G.O. Spain**: Note — no CRM task found. known-accounts.md shows EUR 280K-320K but live CRM has no active task. Kevin/Leo must confirm and reinstate.
3. **GRSYS Brazil**: CapEx confirmed ~$34K — SUB-$50K threshold. Cannot appear in Section A without AOI expansion to breach threshold.
4. **VOSSLOH-SCHWABE**: No CRM task found. Parameter blocker (bare board dims + CPH) confirmed from prior session — still valid for Section B.
