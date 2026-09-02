# State File Schemas

Both files live in `F:\baidunetdiskworkspace\Product Presentation\product html\.automation-state\`.

Write with `[System.IO.File]::WriteAllText` + `UTF8Encoding($false)` (no BOM). Read with `[System.IO.File]::ReadAllText` + UTF8. Never use `Get-Content -Raw | ConvertTo-Json` round-trips for payloads (see SKILL.md Step 5 rules).

## product-html-blog-publisher-state.json

```json
{
  "records": [
    {
      "filePath": "S-EPCOS Capacitor Lead Cut and Forming Machine Landing Page.html",
      "fileHash": "29D9E6A5D45064F5536C5A4F671F79BC5F2A3DF74B48F843A0B2C184BABCCCE4",
      "sourceMtime": "2026-09-01T10:05:25Z",
      "title": "Capacitor Lead Cut & Forming Machine: From Bulk EPCOS Parts to PCB-Ready in One Pass by Southern Machinery",
      "slug": "capacitor-lead-cut-forming-machine-s-epcos",
      "site": "smta.smthelp.eu",
      "postId": "post_0bba7ea9-5859-440e-be53-152d8743cc98",
      "postUrl": "https://smta.smthelp.eu/blog/capacitor-lead-cut-forming-machine-s-epcos",
      "publishedAt": "2026-09-02T01:54:38Z",
      "updatedAt": "2026-09-02T02:30:55Z",
      "contentVersion": 2,
      "status": "published",
      "error": "",
      "imageUrls": [
        "https://ph.smthelp.com/images/2023/08/11/Bowl-Capacitor-Lead-Cut--forming-machine-1.md.png",
        "https://ph.smthelp.com/images/2026/08/09/southern-machinery-bowl-feeder-1-bowl-feeder-lead-cutter-for-various-size-capacitor-0001.md.webp",
        "https://ph.smthelp.com/images/2023/08/11/Bowl-Capacitor-Lead-Cut--forming-machine-3.md.png"
      ]
    }
  ]
}
```

Notes:
- One record **per site** — a blog published to both sites has two records (same `filePath/fileHash/slug`, different `site/postId/postUrl`).
- `fileHash` = SHA256 uppercase of the source file. If a file's current hash matches a `published` record → skip. If hash changed → PATCH existing postIds (keep slug unless forced new), bump `updatedAt/contentVersion`.
- Duplicate copies (same hash, different paths, e.g. root vs `Product landing Page\`) → single publish, record the path actually used.
- Allowed fields only: `filePath, fileHash, sourceMtime, title, slug, site, postId, postUrl, publishedAt, updatedAt, contentVersion, status, error, imageUrls`. **No tokens. No full content.**

## product-html-linkedin-publisher-state.json

```json
{
  "records": [
    {
      "blogSlug": "capacitor-lead-cut-forming-machine-s-epcos",
      "blogPostUrl": "https://smta.smthelp.eu/blog/capacitor-lead-cut-forming-machine-s-epcos",
      "blogPublishedAt": "2026-09-02T01:54:38Z",
      "linkedInPostUrn": "urn:li:share:7500764845940752384",
      "linkedInPostUrl": "https://www.linkedin.com/feed/update/urn:li:share:7500764845940752384",
      "linkedInPublishedAt": "2026-09-02T02:52:00Z",
      "status": "published",
      "error": "",
      "imageUrl": "https://ph.smthelp.com/images/2023/08/11/Bowl-Capacitor-Lead-Cut--forming-machine-1.md.png",
      "imageUrn": "urn:li:image:D5610AQGOsn5Xci9NGA"
    }
  ]
}
```

Notes:
- One record per blog (not per site). `blogPostUrl` points at the smta (primary) URL.
- Backfill rule: record exists with `status` in `failed|needs_token` and empty `linkedInPostUrn` → retry LinkedIn only (Step 6). Never re-POST a blog for a LinkedIn backfill, never repost an existing URN.
- Allowed fields only: `blogSlug, blogPostUrl, blogPublishedAt, linkedInPostUrn, linkedInPostUrl, linkedInPublishedAt, status, error, imageUrl, imageUrn`. **No tokens.**

## Status semantics

| Status | Meaning | Next action |
|---|---|---|
| `published` | Verified live (URL 200 + API status) | none |
| `failed` | API error; `error` holds sanitized message | retry next run or skip to next file |
| `needs_token` | LinkedIn token missing | backfill when `LINKEDIN_ACCESS_TOKEN` set |
| `skipped` | Deduped / ineligible | none |

## Leak check (run before finishing)

```powershell
foreach($f in @($liPath,$blogPath,$memoryPath)){
  $c=[System.IO.File]::ReadAllText($f)
  if($c -match 'AQX[A-Za-z0-9_-]{50,}'){"LEAK(linkedin) in $f"}
  elseif($c -match 'blogcms_[a-f0-9]{20,}'){"LEAK(blogcms) in $f"}
  else{"clean: $([System.IO.Path]::GetFileName($f))"}
}
```

## PowerShell 5.1 pitfalls (root causes observed 2026-09-02)

1. `Get-Content -Raw` on a file piped into `ConvertTo-Json` payload → `contentMarkdown` serialized as object with `value/PSPath` → API 400. Always `[System.IO.File]::ReadAllText($p,[System.Text.Encoding]::UTF8)`.
2. Default `Set-Content`/`Out-File` add BOM → some APIs reject. Use `[System.IO.File]::WriteAllText($p,$s,(New-Object System.Text.UTF8Encoding($false)))`.
3. Complex inline commands break on quote escaping → write a temp `.ps1` under `.automation-state\tmp\`, run it, then delete the folder.
4. `Invoke-WebRequest` error bodies are mojibake in PS 5.1 console → use `[System.Net.HttpWebRequest]` + read error stream for readable diagnostics.
