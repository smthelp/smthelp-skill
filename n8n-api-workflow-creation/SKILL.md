---
name: n8n-api-workflow-creation
description: "n8n REST API v1 workflow creation — gotchas, field restrictions, and trial-and-error learnings for programmatically creating and managing workflows."
whenToUse: "create n8n workflow via API，n8n API 400 error，n8n workflow POST fails，n8n tags read-only"
metadata:
  source: hermes
  origin: "productivity/n8n-api-workflow-creation"
---
# n8n REST API v1 — Workflow Creation Notes

**Learned through trial and error with n8n v1 public API.**

---

## YouTube Auto-Upload Workflow Pattern

**OAuth Refresh Token** — YouTube upload requires OAuth, not just an API Key. One-time browser authorization is needed to get a Refresh Token:

1. Direct user to: `https://accounts.google.com/o/oauth2/auth?client_id=<CLIENT_ID>&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&response_type=code&access_type=offline`
2. User pastes the returned authorization code
3. Exchange for Refresh Token via: `POST https://oauth2.googleapis.com/token` with `grant_type=authorization_code`
4. Store Refresh Token securely in n8n Credentials — it does not expire (until revoked)

**Resumable upload flow (YouTube API v3):**
1. `POST /upload/youtube/v3/videos?uploadType=resumable&part=snippet,status` — initiate upload, returns `{uploadUrl}`
2. `PUT {uploadUrl}` — binary upload with `Content-Type: video/mp4` header
3. Video ID returned in response headers

**Complete n8n workflow JSON saved to:** `~/n8n_youtube_upload_workflow.json`

---

## Verified Working: Create Workflow (POST /api/v1/workflows)

```python
import urllib.request, json

workflow_payload = {
    "name": "Workflow Name",
    "nodes": [...],
    "connections": {...},
    "settings": {
        "executionOrder": "v1",
        "saveManualExecutions": True,
        "callerPolicy": "workflowsFromSameOwner"
    }
}
# DO NOT include: tags, staticData, versionId, triggerCount, updatedAt

req = urllib.request.Request(
    f"{N8N_URL}/api/v1/workflows",
    data=json.dumps(workflow_payload).encode('utf-8'),
    headers={"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"},
    method="POST"
)
```

---

## Known Errors and Fixes

### "request/body must NOT have additional properties"
**Cause:** Payload includes fields n8n API doesn't accept (tags, staticData, versionId, triggerCount, updatedAt).
**Fix:** Strip payload to only name, nodes, connections, settings.

### "request/body must have required property 'settings'"
**Cause:** settings is required even if empty.
**Fix:** Always include "settings": {"executionOrder": "v1"}.

### "tags is read-only" (on PATCH)
**Cause:** Tags cannot be updated via PATCH in this n8n version.
**Fix:** Add tags manually in the n8n UI after creation.

### 405 Method Not Allowed on credentials endpoint
**Cause:** Credentials are managed per-user in n8n UI, not via public API.
**Fix:** Create credentials manually in n8n Settings → Credentials, then reference by name in workflow nodes.

### 401 'X-N8N-API-KEY' header required
**Cause:** Must use X-N8N-API-KEY header, not Authorization: Bearer.
**Fix:**
```python
headers = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}
```

---

## Safe Payload Fields

| Field | Required | Notes |
|-------|----------|-------|
| name | YES | Workflow name |
| nodes | YES | Array of node objects |
| connections | YES | Connections between nodes |
| settings | YES | Must include executionOrder: v1 |
| tags | NO | Read-only on create |
| staticData | NO | Exclude |
| versionId | NO | Exclude |
| triggerCount | NO | Exclude |
| updatedAt | NO | Exclude |

---

## Verified API Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| List workflows | GET | /api/v1/workflows |
| Get workflow | GET | /api/v1/workflows/{id} |
| Create workflow | POST | /api/v1/workflows |
| Credentials | (UI only) | Create in n8n Settings → Credentials |

---

## JWT Token Decoding

```python
import base64, json
token = "eyJ..."
parts = token.split('.')
payload = parts[1]
padding = 4 - len(payload) % 4
if padding != 4:
    payload += '=' * padding
data = json.loads(base64.urlsafe_b64decode(payload))
print(data['sub'])  # n8n user ID
```
