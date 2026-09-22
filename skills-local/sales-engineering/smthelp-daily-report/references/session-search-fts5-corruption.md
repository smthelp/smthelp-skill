# session_search FTS5 Corruption — Permanent Failure

**Status**: Confirmed 2026-06-17 — Full database-level failure. All sessions unreadable.

**Symptom**: `session_search` returns `database disk image is malformed` on any query, including empty/browse mode.

**Impact**: Historical conversation recall completely unavailable. Cannot search past sessions for customer context, deal history, or prior technical decisions.

**Workaround**: 
- Use **Worktile CRM** as primary customer state source
- Use **Himalaya IMAP** for email history
- Use **Downloads directory** file timestamps to infer activity
- Browser-based email/Gmail login for manual email review

**What NOT to do**:
- Do NOT retry session_search in the same session
- Do NOT attempt to repair the SQLite DB manually
- Do NOT reinstall or reconfigure the session DB

**Last verified**: 2026-06-18 — still broken.

**Owner**: Jason Wu — consider restoring from backup if session history is business-critical.
