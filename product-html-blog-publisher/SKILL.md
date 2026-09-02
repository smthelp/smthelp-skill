---
name: product-html-blog-publisher
description: "Southern Machinery product-html blog auto-publisher. Picks one unpublished/updated product or marketing doc from the local 'product html' library, rewrites it into a Dan-Koe-style 6-step English GEO+SEO B2B blog, publishes it via API to smta.smthelp.eu and jasonwu.smthelp.eu, syncs an image post to the company LinkedIn page (urn:li:organization:3039402), and records state in local .automation-state JSON files. Use when asked to run the 6-hourly blog publishing round, publish/repost a product html doc as a blog, backfill a failed LinkedIn sync, or check publishing state."
whenToUse: "运行 product html 博客自动发布轮次、把产品/营销 HTML 文档改写为英文 SEO 博客并发布到 smta/jasonwu 站点、补发 LinkedIn 图文动态、查询或修复发布状态文件时使用。"
metadata:
  source: hermes
  origin: "sales-engineering/product-html-blog-publisher"
---

# Product HTML Blog Publisher (Southern Machinery)

## Overview

One run = **one blog, fully published**:

1. Select 1 eligible source doc from the local `product html` library.
2. Rewrite it into an English GEO+SEO B2B blog (Dan Koe 6-step structure, 1,000–1,500 words).
3. POST to **both** blog CMS sites, verify HTTP 200 / published.
4. Sync an image post to LinkedIn (only after blog success).
5. Update two local state files; output a short report.

**Never publish the same source file twice** (unless its hash changed). Never leak tokens.

## Identity, Endpoints, Credentials

| Item | Value |
|---|---|
| Blog sites | `https://smta.smthelp.eu` and `https://jasonwu.smthelp.eu` |
| Blog API | `POST /api/posts` (create), `PATCH /api/posts/{id}` (update), verify via article URL |
| Auth header | `Authorization: Bearer <AI Publisher Token>` |
| smta token env | `SMTA_BLOG_TOKEN` (fallback: prompt user for `blogcms_...` value) |
| jasonwu token env | `JASONWU_BLOG_TOKEN` (fallback: prompt user) |
| Account | jasonwu / jasonwu@smthelp.com |
| LinkedIn API | `POST https://api.linkedin.com/rest/posts`, version header `Linkedin-Version: 202601`, protocol `X-Restli-Protocol-Version: 2.0.0` |
| LinkedIn owner | `urn:li:organization:3039402` (company page linkedin.com/company/smtmachine) |
| LinkedIn token | env `LINKEDIN_ACCESS_TOKEN` at runtime — **never** store in files/prompts/reports |

**Token discipline (absolute):**
- Blog tokens: display only as `blogcms_...` (first 8 + last 3 chars).
- LinkedIn token: never echo anywhere; on 401 `INVALID_ACCESS_TOKEN` mark `failed` and ask for a fresh token.
- Before finishing any run, grep state files + memory for `blogcms_[a-f0-9]{20,}` and LinkedIn token prefixes; confirm clean.

## Workspace Paths

| Item | Path |
|---|---|
| Source library | `F:\baidunetdiskworkspace\Product Presentation\product html` (business files at root, in `Product landing Page\`, and `Feeder\`) |
| Blog state | `<library>\.automation-state\product-html-blog-publisher-state.json` |
| LinkedIn state | `<library>\.automation-state\product-html-linkedin-publisher-state.json` |
| Session memory | `<library>\.workbuddy\memory\YYYY-MM-DD.md` (append a note after substantive runs) |

If the state-file path in an invoking prompt differs (e.g. a `/Volumes/...` path), use the path the user last confirmed — on this Windows machine that is the local `.automation-state` above.

## State Contracts

Both files: JSON object `{ "records": [ ... ] }`. Create with `{"records":[]}` if missing. Allowed fields only — **no tokens, no full content**:

- Blog record: `filePath, fileHash, sourceMtime, title, slug, postId, postUrl, publishedAt, status, error, imageUrls` (+ per-site `site`, optional `updatedAt, contentVersion`).
- LinkedIn record: `blogSlug, blogPostUrl, blogPublishedAt, linkedInPostUrn, linkedInPostUrl, linkedInPublishedAt, status, error, imageUrl, imageUrn`.

Status values: `published | failed | needs_token | skipped`. On file-hash match with a published record → skip. On hash change → prefer PATCH (update in place); fall back to new slug only if PATCH is impossible. One blog record per site (two records per published blog).

## Run Flow

### Step 0 — Load state
Read both state files. If missing, create `{"records":[]}`.

### Step 1 — Select source doc
- Scan `*.html, *.md, *.txt, *.svg` in the library (root + `Product landing Page\` + `Feeder\`), excluding: `AGENTS.md`, `CLAUDE.md`, `VScode.code-workspace`, `.cursor/`, `.superdesign/`, `.automation-state/`, `.workbuddy/`, `.vs/`, `chrome_profile_notebooklm/`, `output/`, config/rule/template-only files, pure forms, corrupted files.
- Skip files whose hash matches a `published` record (duplicate copies with identical hash → publish once, use root copy).
- Priority: newest mtime first; among near-duplicates pick the most complete, image-richest, publication-ready version.
- Topic-dedup: compare against all state-file slugs; if the theme is near-duplicate, require a new angle (selection guide / line integration / cost comparison / maintenance).
- If nothing eligible → report "no pending docs", stop. Do not republish.

### Step 2 — Extract material
Read the full source. Extract: product/model, key specs, process/feature structure, ROI inputs, FAQs, contact info, and all `https://ph.smthelp.com/...` image URLs.
Truth rules: every number from this doc; missing → "not specified in source — contact Southern Machinery to confirm"; suspicious values keep the source flag (e.g. air supply typo noted in source); ROI/price labeled `example — depends on configuration — subject to final technical confirmation`.

### Step 3 — Images
1. Reuse source-doc image URLs when present.
2. Else search `https://ph.smthelp.com/search/images/?q=<keywords>` (model, product category, component type).
3. **Validate every URL**: HTTP 200 + `Content-Type: image/*`. 404/HTML → discard.
4. Prefer real product/detail/line shots; no unrelated stock photos; no invented URLs.
5. Target 1 coverImage + 2–4 inline images, alt text = main keyword + product category.
6. None reliable → leave coverImage empty and say so.

### Step 4 — Write the blog
English, 1,000–1,500 words, for EMS/ODM/automotive/medical/industrial buyers. Structure:

- **H1**: main keyword + product category/model + "by Southern Machinery" (≤60 chars).
- **Direct-answer block** (first 2–3 sentences) answering "What is this machine used for?" for AI Overviews/Perplexity.
- **Dan Koe 6-step body** — but **headings must NOT contain the words "Hook", "Diagnosis", "Vehicle", "Loop", "CTA"** (user rule). Use natural titles instead, e.g.:
  - Hook → "One Operator, 1,000 Shaped Capacitors Per Hour" (counter-intuitive claim/data/pain)
  - Diagnosis → "Why Hand-Forming Fails Your Through-Hole Line"
  - Framework → "The 8-Station Cycle to Judge Any Forming Machine" (reusable checklist/model)
  - Vehicle → "The S-EPCOS Capacitor Lead Cut & Forming Machine"
  - Loop → "From Drawing to Running Line in Five Steps" + next-post teaser
  - CTA → "Send Your Drawing for a Tooling Review"
- **SEO/AEO**: main keyword in H1 + first 100 words + one H2; comparison/cost/lifecycle buyer questions as H2s; H3 subsections every 100–150 words; FAQ 4–6 Q&A pairs; selection-parameter table; ROI formula block + example; internal links only to verified www.smthelp.com pages; excerpt 80–160 words (AI-quotable, labor-saving + quality + line-integration value).
- **Brand**: Shenzhen manufacturer founded 2011, 237+ global customers, complete SMT/THT/wave/board-handling/inspection lines, global service/spares/training. No invented claims.

### Step 5 — Publish to both blog sites
Payload fields: `title, slug, excerpt, coverImage, contentMarkdown, status:"published", source:"ai", seoTitle (≤60 chars, "keyword | Southern Machinery"), seoDescription (140–160 chars), tags (from: SMT Line, THT Automation, Wave Soldering, Board Handling, PCB Assembly Automation, EMS Manufacturing, Factory ROI, Terminal Insertion, Odd Form Insertion), locale:"en"`.

**Windows PowerShell 5.1 critical rules** (root cause of past failures):
- Read/write files with `[System.IO.File]::ReadAllText/WriteAllText` + `UTF8Encoding($false)` — `Get-Content -Raw | ConvertTo-Json` corrupts payloads (serializes PSObject with `value/PSPath` → 400 "Validation failed: contentMarkdown").
- Send with `[System.Net.HttpWebRequest]` + `ContentType: application/json; charset=utf-8` and UTF8 bytes; complex logic in a `.ps1` temp script, not one-liners (quote escaping breaks).
- 409/slug conflict → more specific slug (add model/use), retry.
- On hash-change republish of an existing post → use `PATCH /api/posts/{postId}` (works, returns 200); verify article URL returns 200 and forbidden heading words absent.
- After success verify: article URL HTTP 200; response `status:"published"`; tags list length correct.
- Clean up any API probe/test drafts (DELETE) before finishing.

### Step 6 — LinkedIn sync (only after blog verified)
1. Token: `[System.Environment]::GetEnvironmentVariable('LINKEDIN_ACCESS_TOKEN','User')`. Missing → record `needs_token`, stop (blog stays published; next run backfills).
2. Image: coverImage (or first validated image) → download bytes.
3. `POST https://api.linkedin.com/rest/images?action=initializeUpload` with `{"initializeUploadRequest":{"owner":"urn:li:organization:3039402"}}` → get `value.image` (URN) + `value.uploadUrl`.
4. `PUT` image bytes to uploadUrl (`Content-Type: image/png|webp`) → 201.
5. Poll `GET https://api.linkedin.com/rest/images/{urlencoded URN}` until `status:"AVAILABLE"`.
6. Commentary (English, natural, short): pain point → Southern Machinery solution → blog URL → 3–5 hashtags. No unverified params/prices/ROI.
7. `POST https://api.linkedin.com/rest/posts`:
```json
{
  "author": "urn:li:organization:3039402",
  "commentary": "...",
  "visibility": "PUBLIC",
  "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
  "lifecycleState": "PUBLISHED",
  "content": {"media": {"id": "<imageUrn>", "altText": "<keyword + product category>"}}
}
```
   Do **NOT** include `isReshareDisabled` (422 unrecognized field).
8. 201 → post URN from `x-restli-id` header; verify `GET /rest/posts/{urn}` returns 200 PUBLISHED. Record `linkedInPostUrl = https://www.linkedin.com/feed/update/{urn}`.
9. 401 → `failed` (invalid/expired token, ask user for fresh one). LinkedIn failure never rolls back the blog.

### Step 7 — State + report
- Update blog state (one record per site) and LinkedIn state.
- Append a brief note to `.workbuddy/memory/YYYY-MM-DD.md` (pages published, decisions, gotchas — no tokens, no transient output).
- Output short report only: 源文件 / 产品主题 / 图片搜索关键词 / 博客发布状态 / 博客 URL / LinkedIn 状态 / LinkedIn URL / 失败原因或人工介入需求.

## Backfill Mode (no new blog)

If no new blog this round but LinkedIn state has `failed`/`needs_token` for a published blog: re-run Step 6 only. Do not republish the blog; do not repost an existing `linkedInPostUrn`.

## Scripts And References

| File | Purpose |
|---|---|
| `scripts/publish-blog.ps1` | Parameterized publisher: source-file → blog content md → payload → POST/PATCH both sites → verify. Handles PS 5.1 UTF-8 pitfalls. |
| `scripts/linkedin-sync.ps1` | LinkedIn image init → upload → poll → post → verify; token from env only. |
| `references/state-schemas.md` | Exact JSON schemas + status semantics + dedup/hash rules. |
| `references/blog-template.md` | Blog skeleton (H1/answer block/6-step natural headings/FAQ/CTA) + SEO field rules. |

Run examples (Claude fills values, scripts are helpers — review each run):
```powershell
# publish (creates/updates both sites)
& .\scripts\publish-blog.ps1 -ContentPath <md> -Slug <slug> -Title <title> -SmtaToken $env:SMTA_BLOG_TOKEN -JasonwuToken $env:JASONWU_BLOG_TOKEN
# linkedin sync (token must be in env)
& .\scripts\linkedin-sync.ps1 -ImageUrl <cover> -BlogUrl <postUrl> -Commentary "<text>"
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| 400 `Validation failed: contentMarkdown` | `Get-Content -Raw` object serialization / non-UTF8 bytes | Use `[System.IO.File]::ReadAllText` + `UTF8Encoding($false)`, re-send |
| 409 slug conflict | Slug exists | Append model/use to slug, retry |
| LinkedIn 401 `INVALID_ACCESS_TOKEN` | Expired/revoked token | Mark `failed`, ask user for fresh token, backfill next run |
| LinkedIn 422 `unrecognized field` | Extra payload field | Remove offending field (e.g. `isReshareDisabled`), retry |
| Images fail validation | 404 / HTML page | Discard candidate; leave coverImage empty if none reliable |
| jasonwu `GET ?status=draft` 500 | API quirk | List via `?limit=100`; verify by article URL instead |

## Quality Gates (14-item SEO self-check before publish)

Title / Meta / Keywords / URL slug / H1–H3 hierarchy / image Alt / UX readability / FAQ schema-ready / canonical / OG tags / Twitter Card / breadcrumb internal links / alternate-keyword strategy / content richness — each post needs ≥1 citable data point or comparison table.
