# State files, API contracts and known failure modes

## Locations

| Item | Path |
|---|---|
| Workspace | `/Volumes/MOVESPEED/baidunetdiskworkspace/Product Presentation/Product Html` |
| Blog state | `<root>/.automation-state/product-html-blog-publisher-state.json` |
| LinkedIn state | `<root>/.automation-state/product-html-linkedin-publisher-state.json` |

Both state files are **JSON arrays** (not objects). The pipeline appends one record per
run and writes a `.bak` before every overwrite. The prompt references the blog state file
without the directory separator — the real, authoritative path is inside `.automation-state/`.

## Blog state record schema

```json
{
  "filePath": "...", "fileHash": "<full sha256>", "sourceMtime": 1787801916,
  "title": "...", "slug": "...", "postId": "post_<uuid>",
  "postUrl": "https://jasonwu.smthelp.eu/blog/<slug>",
  "publishedAt": "ISO8601", "status": "published|failed",
  "error": "", "imageUrls": ["https://ph.smthelp.com/..."]
}
```

`fileHash` is the **full** sha256 hex digest. Comparing a 16-char prefix makes every
file look unpublished (this actually happened and produced a 140-item false backlog).

## LinkedIn state record schema

```json
{
  "blogSlug": "...", "blogPostUrl": "...", "blogPublishedAt": "ISO8601",
  "linkedInPostUrn": "urn:li:share:<id>",
  "linkedInPostUrl": "https://www.linkedin.com/feed/update/urn:li:share:<id>",
  "linkedInPublishedAt": "ISO8601",
  "status": "published|failed|needs_token", "error": "",
  "imageUrl": "...", "imageUrn": "urn:li:image:<id>"
}
```

No token is ever written to either file.

## Known data quirks in the existing state files

- Older `postUrl` values point at **`smta.smthelp.eu`**, not `jasonwu.smthelp.eu`. Before
  using one in a LinkedIn commentary, curl it (or its `jasonwu.smthelp.eu` equivalent) and
  confirm 200 — otherwise the post links to a page the reader may not reach.
- Some historical `coverImage` / `imageUrls` entries are on
  `hk03-1251009151.file.myqcloud.com` instead of `ph.smthelp.com`. They are still usable
  images, but prefer a `ph.smthelp.com` asset when one exists, and always re-validate.
- One row has `status: failed` for a slug that also has a `published` row
  (`s300as-desktop-pcb-router-pcb-depaneling-...`). De-duplicate on `slug` before counting.

## Blog API — jasonwu.smthelp.eu

| Method | Path | Notes |
|---|---|---|
| POST | `/api/posts` | Create. Auth `Bearer <token>`. Sending `Origin: https://jasonwu.smthelp.eu` is harmless and protects against the 403 "Cross-origin write" guard seen on sibling hosts. |
| GET | `/api/posts/{slug}` | Returns `{data:{status, id, publishedAt, ...}}` |
| GET | `/api/posts?page=1` | Has returned 500 on this host — the list endpoint serialises full markdown for every post. Do not rely on it; use the state file as the idempotency source of truth. |

**Verify on the public route**, not the API: `https://jasonwu.smthelp.eu/blog/<slug>` must
return 200. `GET /api/posts/<slug>` can 403 with a perfectly valid token.

Slug collision: the server renames to `<slug>-2`. Always re-read `data.slug` from the
response and store that — never assume your requested slug survived.

## LinkedIn API

| Step | Call |
|---|---|
| Init upload | `POST /rest/images?action=initializeUpload` body `{"initializeUploadRequest":{"owner":"urn:li:organization:3039402"}}` |
| Upload bytes | `PUT <uploadUrl>` with `Content-Type: application/octet-stream` |
| Create post | `POST /rest/posts` |

Headers on every call: `Authorization: Bearer <token>` and `Linkedin-Version: 202601`.

Post body:

```json
{
  "author": "urn:li:organization:3039402",
  "commentary": "...",
  "visibility": "PUBLIC",
  "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
  "lifecycleState": "PUBLISHED",
  "content": {"media": {"id": "urn:li:image:<id>", "altText": "..."}}
}
```

### Failure modes already hit

1. `"visibility": "PUBLISHED"` → **422 `"PUBLISHED" is not an enum symbol`**. Use `PUBLIC`.
2. 201 with **no `x-restli-id`**. Recover the URN with
   `GET /rest/posts?q=author&author=urn:li:organization:3039402&count=5` → `elements[0].id`
   (match on a commentary prefix, fall back to the newest).
3. `GET /rest/images/{id}` → 400. The polling URL form is wrong; skip polling entirely —
   the image URN works immediately after the PUT.
4. `.webp` covers are accepted by the blog but are a poor choice for LinkedIn — pick a
   PNG/JPEG sibling asset.

## Token handling

- Blog token: env `SMTHELP_BLOG_TOKEN`, fallback `~/.config/smthelp/blog_token` (chmod 600).
- LinkedIn token: env `LINKEDIN_ACCESS_TOKEN`, fallback `~/.config/smthelp/linkedin_token`.
- Never echo a token. In reports show at most `blogcms_...663e`-style masking for the
  blog token and nothing at all for LinkedIn.
- If `LINKEDIN_ACCESS_TOKEN` is absent: the blog still publishes; LinkedIn is recorded as
  `needs_token` and the report says only "configure LINKEDIN_ACCESS_TOKEN".
