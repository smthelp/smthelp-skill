# Monthly Win-Loss Review — Data Unavailability Fallback Checklist

> **MANDATORY FALLBACK**: Use this when Worktile CRM + Himalaya email + FTS5 session DB ALL fail simultaneously.
> See: `sales-engineering/smthelp-monthly-win-loss-review/SKILL.md`

---

## Quick Diagnostic

Run these 3 commands in parallel to assess what's available:
```bash
# 1. Current date
date +%Y-%m-%d

# 2. smthelp.com reachability
curl -s -o /dev/null -w '%{http_code}' https://www.smthelp.com --connect-timeout 5

# 3. Recent business files in Downloads (30 days)
find ~/Downloads/ -maxdepth 1 -type f \
  \( -name "*.pdf" -o -name "*.xlsx" -o -name "*.docx" -o -name "*.pptx" -o -name "*.md" \) \
  -mtime -30 2>/dev/null | head -30
```

---

## Downloads Signal Reference

| File Pattern | What It Tells You |
|---|---|
| `*capex_trigger_campaign_YYYY-MM-DD.md*` | CapEx urgency angle was active that month |
| `*ABM*` or `*geographic*` report | Geographic targeting priority |
| `FeederSalesDeck/` or `*feeder*` training | Custom feeder push in play |
| `Southern-Machinery-Marketing-and-ROI-Tools.html` | ROI tools being distributed to prospects |
| `Components for MVF_SM*.xlsx` (multiple revisions) | Active negotiation on a specific deal |
| `PI*.pdf` or `Invoice*.pdf` | Confirmed deal stage — check date for recency |
| `*ROI*` or `*Quote*` files | Proposal activity — check date for recency |
| No new business files in 45+ days | Zero closed deals; no active proposals |

---

## Infer Pipeline Health from Signals

| Observed | Inferred Meaning |
|---|---|
| No PI/quote files in 45+ days | **Zero confirmed closed deals** this period |
| Multiple revisions of same spreadsheet | Active negotiation — not closed yet |
| CapEx campaign doc dated mid-month | Outreach was active that month |
| FeederSalesDeck/ training materials | Product focus = likely custom feeders push |
| ABM reports generated | Geographic expansion priority |
| Campaign trigger doc from month-end | CapEx urgency angle in play |

---

## Known Failures (2026-08-01 snapshot)

| System | Failure | Since | Workaround |
|---|---|---|---|
| Worktile CRM (v5.viwolf.cn) | SSL cert invalid + demo login loops | ~Jun 2026 | Manual CRM export; build `pipeline-YYYY.csv` |
| Himalaya IMAP | Sync frozen | Apr 28, 2026 | `https://outlook.office365.com` manual export |
| FTS5 session DB | Full corruption | Jun 17, 2026 | Skip; use Downloads + campaign files |
| smthelp.com | Was down | Jun 19 (restored Jul 6) | None needed now |

---

## Output Integrity Rules

1. **Never fabricate** deal counts or win/loss numbers
2. **Always flag**: `[confirmed by CRM]` vs `[inferred from file timestamps]`
3. **Classify losses** using the 7-category framework (price, spec mismatch, slow follow-up, insufficient qualification, service concern, used-equipment competition, timing/budget)
4. **End every report with**: manual reconciliation request if data gaps are critical
5. **Use this format** in the report's data limitations table:

```
| Source | Status | Notes |
|---|---|---|
| Worktile CRM | ❌ [specific failure] | — |
| Himalaya Email | ⚠️ [specific failure] | — |
| Session DB | ❌ [specific failure] | — |
| Local Files | ℹ️ [what was found] | — |

**Verdict:** Pipeline health is inferred, not confirmed.
Treat closed-won/lost counts as directional, not factual.
```
