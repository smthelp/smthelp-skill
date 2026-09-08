---
name: product-html-blog-pipeline
description: End-to-end pipeline that turns one document from the Obsidian "Product Html" folder into an English GEO+SEO B2B product blog on jasonwu.smthelp.eu and a matching image post on the Southern Machinery LinkedIn company page. Use for the hourly Product Html blog publisher automation, for manually publishing one product/marketing document, or for repairing a run where the blog published but LinkedIn failed.
version: 1.0.1
agent_created: true
upstream: https://github.com/smthelp/smthelp-skill/tree/main/product-html-blog-pipeline
---

# product-html-blog-pipeline

One source document → one English B2B blog → one LinkedIn company-page image post.
State-tracked, idempotent, no duplicate slugs, no duplicate LinkedIn posts.

Root (override with `PRODUCT_HTML_ROOT` or `--root`):
`/Volumes/MOVESPEED/baidunetdiskworkspace/Product Presentation/Product Html`

## When to use

- The hourly "Product Html Blog Publisher" automation
- "Publish the next product document" / "publish this file"
- "Repair LinkedIn for X" (blog live, LinkedIn failed or `needs_token`)
- Auditing what is left in the backlog

## One-time setup

```bash
mkdir -p ~/.config/smthelp && chmod 700 ~/.config/smthelp
printf '%s' '<blog token>'    > ~/.config/smthelp/blog_token
printf '%s' '<linkedin tok>'  > ~/.config/smthelp/linkedin_token
chmod 600 ~/.config/smthelp/*_token
```

Env vars `SMTHELP_BLOG_TOKEN` / `LINKEDIN_ACCESS_TOKEN` take precedence.
**Never** write a token into an article, a state file, Git, a log or a report.

## The five steps

### 1 — Select

```bash
PY=/Users/jasonwu/.workbuddy/binaries/python/versions/3.13.12/bin/python3
S=/Users/jasonwu/.workbuddy/skills/product-html-blog-pipeline/scripts
$PY $S/pipeline.py select --limit 12
```

Returns a ranked candidate list. `topicOverlap` is Jaccard similarity against
already-published slugs — **anything ≥ 0.35 means the topic is covered; you must change
the angle** (selection guide / line integration / cost comparison / maintenance /
programming) or pick another file. Pick **one** candidate, preferring high `score`,
low `topicOverlap`, high `specHits`.

Read the chosen document fully before writing anything.

### 2 — Images

```bash
$PY $S/images.py search --q "S7020" --q "eyelet" --limit 30   # model + category
$PY $S/images.py check  --url <u1> --url <u2>
```

Every URL must come back `"ok": true` before it goes anywhere near the payload.
Cover = best product shot. 2–4 more embedded where they fit, alt text always carries
the main keyword + product category. No stock photos. Leave `coverImage` empty rather
than use an unrelated image — but always try to get at least one.

### 3 — Write

Follow `references/article-brief.md`. All facts from the selected document only.
Save the payload as JSON next to the source (or in `/tmp`), then:

```bash
$PY $S/qa.py --payload payload.json --source-file "<chosen document>"
```

Fix every `FAIL` before publishing. `WARN` on gate 13 means numbers appear in the
article that are absent from the source — check each one, do not hand-wave.

### 4 — Publish

```bash
$PY $S/pipeline.py publish --payload payload.json --file "<chosen document>"
```

It POSTs, retries once with `<slug>-2` on collision, verifies the **public** blog URL
returns 200, and appends to the blog state file. Non-zero exit + `status: failed`
record on error — the blog state is never marked published unless the page is live.

### 5 — LinkedIn

Only after step 4 succeeded. Write the commentary to a file (English, short: pain →
solution → blog link → 3–5 hashtags; no invented specs, prices, lead times or ROI).

```bash
$PY $S/linkedin.py post --blog-slug <slug> --commentary-file comm.txt \
     [--image-url <png-url>] --alt-text "..."
```

It prefers the blog `coverImage` when `--image-url` is omitted, uploads it, posts,
recovers the URN when the 201 hides `x-restli-id`, and appends to the LinkedIn state
file. Re-running for a slug already marked `published` is refused.

Repair pass (blog published, LinkedIn missing/failed):

```bash
$PY $S/linkedin.py repair --limit 5    # newest 5 slugs with no successful LI post
```

`repair` only lists — it never auto-postes, because the commentary must be written per
article. The backlog is real and large (70+ historical posts were published while the
LinkedIn token was unset). **Do not drain it in one run** — a few per run at most, or the
company feed gets spammed. Older `postUrl` values may point at `smta.smthelp.eu`; verify
the link returns 200 before putting it in a commentary.

## Output contract

End every run with a short table: source file · product topic · image search keywords ·
blog status · blog URL · LinkedIn status · LinkedIn URL · failure reason / human action.
Nothing else.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `select` reports every file as unpublished | Hash compare used a prefix. `fileHash` is full sha256 — the script is correct, don't "optimise" it. |
| 403 `Cross-origin write requests are not allowed` | Add the `Origin` header (already set in `pipeline.py`). |
| Blog 200 in API but page 404 | Verify `https://jasonwu.smthelp.eu/blog/<slug>`, and use `data.slug` from the response — it may be `<slug>-2`. |
| LinkedIn 422 `is not an enum symbol` | `visibility` must be `PUBLIC`, never `PUBLISHED`. |
| LinkedIn 201 but no URN | Script falls back to `GET /rest/posts?q=author`. |
| LinkedIn `needs_token` | Set `LINKEDIN_ACCESS_TOKEN`. The blog stays published; never roll it back. |
| `GET /rest/images/{id}` → 400 | Expected. Polling is skipped; the URN is valid after the PUT. |

## Distribution

Upstream: `https://github.com/smthelp/smthelp-skill` (private) →
`product-html-blog-pipeline/`. Local copies: `~/.workbuddy/skills/` (this one, used by
WorkBuddy) and `~/.agents/skills/` (SMPilot sync source — keep it there or the next
SMPilot sync will drop the directory from the repo again).

After editing: bump `version`, add an Upgrade-log row, then re-sync all three
(`~/.workbuddy/skills` → `~/.agents/skills` → GitHub `main`).

## Upgrade log

Keep this section sorted newest-first. Bump `version` in the frontmatter with every
change, and add a row explaining **why** — future runs read this first.

### 1.0.1 — 2026-09-08
- Added `upstream` frontmatter + this Distribution section, and mirrored the skill into
  `~/.agents/skills/`. Without the mirror the next SMPilot sync (codex → agents → claude)
  would not see the directory and would drop it from the repo.

### 1.0.0 — 2026-09-08
- Initial extraction from the hourly automation prompt + 74 published runs.
- `pipeline.py` (select / publish), `linkedin.py` (post / repair),
  `images.py` (search / check), `qa.py` (14-gate pre-publish check).
- Encoded the four defects that actually cost runs: 16-char hash prefix false backlog,
  LinkedIn `visibility` enum, missing `x-restli-id`, `/rest/images` poll 400.
- References split into `article-brief.md` (writing) and `state-and-api.md` (contracts).

## Reference files

- `references/article-brief.md` — structure, keyword, truthfulness and payload rules
- `references/state-and-api.md` — schemas, endpoints, failure modes
- `scripts/pipeline.py`, `scripts/linkedin.py`, `scripts/images.py`, `scripts/qa.py`
