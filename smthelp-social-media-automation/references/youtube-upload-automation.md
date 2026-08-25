---
name: youtube-upload-automation
description: Southern Machinery YouTube upload automation via n8n + YouTube OAuth
archived: 2026-06-14
absorbed_into: sales-engineering/smthelp-social-media-automation (as §2)
---

# YouTube Upload Automation Workflow

## Context
- User: 吴总 (Jason Wu), CEO of Southern Machinery
- YouTube Channel: `UClX0iEG2bvJq8yUBEDamgDw` (smthelp.com)
- n8n instance: https://n8n.autoinsertion.com
- OAuth Credentials: ID + Secret collected, Refresh Token PENDING

## Files Generated
- `~/n8n_youtube_upload_workflow.json` — complete n8n workflow for automated YouTube upload
- `~/wave_soldering.py` — ManimGL animation script (7 scenes, ~22KB, fails headless)

## YouTube OAuth Setup (Critical)
To upload videos, need Refresh Token. Steps:
1. User opens auth URL with OAuth client ID
2. User gets authorization code from browser
3. Exchange code for Refresh Token via POST to Google OAuth

**Auth URL:**
```
https://accounts.google.com/o/oauth2/auth?client_id=998061498769-qm0u7j2tu7ae9dk5kphjripbu574c7dd.apps.googleusercontent.com&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&response_type=code&access_type=offline
```

## Hostinger API Diagnostics
- API Token `ikHAQZcf4PtDEHAnhXPhh9Me08msCINs5XssgLEg3f09ea6e`: Valid (200 OK)
- Cloud API returns empty `[]` for VMs — user has hPanel VPS, not Cloud VPS
- n8n server confirmed online at 198.18.24.15

## ManimGL on macOS
- `python3 -m pip install manimgl` ✅ installed
- Headless rendering fails (OpenGL/X11 not available in terminal)
- Need Xvfb (`brew install xorg-opengl`) or run with Xvfb
- Alternative: render on CI/CD runner or ask user to render locally

## n8n Workflow Pattern
```python
# n8n API to trigger workflow
POST https://n8n.autoinsertion.com:443/rest/workflows/{id}/run
Authorization: Bearer {api_key}
```

## "always" Command
User says "always" = keep going without asking for confirmation.
