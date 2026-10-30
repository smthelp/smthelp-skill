---
name: open-webui
description: "Open WebUI startup troubleshooting on macOS. Key finding: run from /tmp for reliable port 8080 binding. Init takes ~20s."
metadata:
  version: "0.1"
---

## Quick Start

```bash
cd /tmp && open-webui serve
# Wait ~20s for "Fetching 30 files" to complete
# Access: http://localhost:8080
```

## Working Directory Matters

Running `open-webui serve` from `/tmp` works reliably. Running from other directories can cause the process to start but fail to bind to port 8080 (process stays alive with no LISTEN port). This is related to macOS symlink behavior (`/tmp` -> `/private/tmp`) and how Open WebUI resolves data directory paths.

## Port

Default port: **8080** (http-alt)

## Data Directory

Data stored at `/private/tmp/` (or `$TMPDIR` on macOS). DB is SQLite. Secret key at `~/.webui_secret_key`.

## Init Time

First launch fetches 30 frontend files — takes ~20 seconds before the port is ready. Do NOT assume it's hung; wait before retrying.

## Known Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Process running, port 8080 not listening | Wrong working directory | Run from `/tmp` |
| `Cannot GET /` on port 3000 | Port 3000 is node, not open-webui | Use port 8080 |
| "Fetching 30 files" never finishes | Still initializing | Wait ~20s |

## §2 — Remote Diagnosis (Browserbase + Cloudflare Scenario)

> This section consolidated from `open-webui-remote-diagnosis` skill. Full reference content at `references/open-webui-remote-diagnosis.md`.

### When to Use Remote Diagnosis
Triggered when the user asks to log into a remote Open WebUI instance, sees 502 Bad Gateway, or when the service is unreachable.

### Diagnosis Flow

**Phase 1 — Network vs Application layer:**
```
Step 1: browser_navigate to target URL
  - Success → domain reachable, CDN/proxy may be OK
  - Timeout → service on VPN/vm/internal network

Step 2: browser_console check page state
  - document.title, document.body.innerHTML.length
  - SvelteKit SPA: wait for __sveltekit_ dynamic load

Step 3: Identify Cloudflare proxy
  - 502 + cloudflare.com link → Cloudflare OK, origin is down
  - Ray ID present → confirmed Cloudflare
```

**Phase 2 — 502 Bad Gateway排查:**
User needs to run on server:
```bash
docker ps | grep open-webui
docker logs open-webui --tail 50
netstat -tlnp | grep -E '3000|8080|8000'
docker restart open-webui
cloudflared tunnel list
cloudflared tunnel run <tunnel-name>
```

**Phase 3 — Network Isolation识别:**
```
198.18.x.x: RFC 2544 benchmark address
→ Service on VPN/VM/internal network
→ Need Cloudflare Tunnel or ngrok to expose publicly
```

### Key Learnings (from sui.3dsmt.com case)
1. Browserbase browser and curl don't route the same — Browserbase success + curl timeout = exit routing issue, not service down
2. SvelteKit SPA needs 5-10 seconds for `__sveltekit_` dynamic imports
3. 502 from Cloudflare is a cached response — origin may already be recovered
4. First browser_navigate timeout doesn't mean failure — SvelteKit lazy-loads JS, retry

### Quick Detection Commands
```bash
# Check if Cloudflare proxy
curl -sI "https://target.com" | grep -i "cf-ray\|cloudflare"

# Check origin bypassing CDN cache
curl -s -H "Cache-Control: no-cache" "https://target.com"
```

## §3 — Docker Install (hermes-webui on macOS)

> This section consolidated from `hermes-webui-docker-install` skill. Full reference content at `references/hermes-webui-docker-install.md`.

### Key Findings
- **Do NOT build locally** — use `ghcr.io/nesquena/hermes-webui:latest` pre-built image (local build times out)
- **macOS UID/GID** — not 1000, set explicitly in `.env` (`UID=501`, `GID=20` or use `id -u`/`id -g`)
- **Remote access** — map port as `8787:8787` (without `127.0.0.1:` prefix binds `0.0.0.0`)
- **Security warning** — default binds `0.0.0.0` with NO password when unset

### Standard Install

```bash
# 1. Pull pre-built image
docker pull ghcr.io/nesquena/hermes-webui:latest

# 2. Prepare dir and .env
mkdir -p ~/hermes-webui && cd ~/hermes-webui
cat > .env << 'EOF'
UID=$(id -u)
GID=$(id -g)
HERMES_WEBUI_HOST=0.0.0.0
HERMES_WEBUI_PORT=8787
HERMES_WEBUI_STATE_DIR=~/.hermes/webui-mvp
HERMES_HOME=~/.hermes
EOF

# 3. docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: "3.8"
services:
  hermes-webui:
    image: ghcr.io/nesquena/hermes-webui:latest
    ports:
      - "8787:8787"
    volumes:
      - ${HERMES_HOME:-${HOME}/.hermes}:/home/hermeswebui/.hermes
      - ${HERMES_WORKSPACE:-${HOME}/workspace}:/workspace
    environment:
      - WANTED_UID=${UID:-1000}
      - WANTED_GID=${GID:-1000}
      - HERMES_WEBUI_HOST=0.0.0.0
      - HERMES_WEBUI_PORT=8787
      - HERMES_WEBUI_STATE_DIR=/home/hermeswebui/.hermes/webui
    restart: unless-stopped
EOF

# 4. Start and verify
docker compose up -d
sleep 8
curl -s -o /dev/null -w "%{http_code}" http://localhost:8787/health
docker logs hermes-webui-hermes-webui-1 --tail 20

# 5. LaunchAgent for boot (macOS)
# Save plist to ~/Library/LaunchAgents/ai.hermes.webui.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.webui.plist
```

### Remote Access
```bash
# Same LAN: browser http://<machine-ip>:8787
# Or SSH tunnel (more secure):
ssh -N -L 8787:127.0.0.1:8787 user@<machine-ip>
# Then http://localhost:8787
```

### Security
Set a password via `HERMES_WEBUI_PASSWORD=your_secure_password` in `.env` before starting.

### Maintenance
```bash
docker ps | grep hermes-webui
docker logs -f hermes-webui-hermes-webui-1
docker compose restart  # in ~/hermes-webui
docker compose down
# Uninstall: docker compose down + launchctl bootout gui/$(id -u)/ai.hermes.webui
```

For the full plist XML, Docker Compose details, and all maintenance commands, refer to `references/hermes-webui-docker-install.md`.
| No response on 8080 | Startup not complete | Wait longer |

## Verification Commands

```bash
# Check if running
ps aux | grep "[o]pen-webui serve"

# Check port
lsof -i :8080

# Check HTTP response
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080
```

---

## Database Access (SQLite)

**DB path:** `/opt/homebrew/lib/python3.11/site-packages/open_webui/data/webui.db`

```bash
sqlite3 /opt/homebrew/lib/python3.11/site-packages/open_webui/data/webui.db ".tables"
sqlite3 /opt/homebrew/lib/python3.11/site-packages/open_webui/data/webui.db "SELECT email, name, role FROM user LIMIT 5;"
# Auth table (separate from user table):
sqlite3 /opt/homebrew/lib/python3.11/site-packages/open_webui/data/webui.db "SELECT email, active FROM auth;"
```

**Schema note:** `user` table holds metadata (name, email, role); `auth` table holds credentials (email, password hash, active flag). They are separate.

## Auth API Endpoint

**Correct:** `POST /api/v1/auths/signin` (NOT `/api/v1/auth/login`)

The 405 "Method Not Allowed" on `/auth/login` means you're hitting the wrong endpoint. Use `/auths/signin`.

## Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `405 Method Not Allowed` on `/api/v1/auth/login` | Wrong endpoint | Use `/api/v1/auths/signin` |
| `400` on valid-looking password | Password incorrect | Reset via DB or use `WEBUI_SECRET_KEY` |
| `enable_signup: false` in config | Registration blocked | Use existing account or disable via env var `WEBUI_DISABLE_SIGNUP=false` |
| No users in `auth` table | First launch, no account created | Set `WEBUI_ADMIN_EMAIL` + `WEBUI_ADMIN_PASSWORD` env vars on first start |

---

## Integrating with free-Claude-code Gateway

free-Claude-code runs a local Anthropic-compatible proxy on `localhost:8082`.

**1. Start Open WebUI (from /tmp to bind port 8080 reliably):**
```bash
cd /tmp && open-webui serve
# Wait ~20s
```

**2. In Open WebUI Admin Panel → Models:**
- Add custom model with:
  - **API Base URL:** `http://localhost:8082/v1`
  - **API Key:** `freecc` (the `ANTHROPIC_AUTH_TOKEN` value)
  - **Model Name:** any label, e.g. `free-cc-proxy`

Or set via environment before starting open-webui:
```bash
export OPENAI_API_BASE_URL="http://localhost:8082/v1"
export OPENAI_API_KEY="freecc"
cd /tmp && open-webui serve
```

**3. Verify gateway is reachable:**
```bash
curl -s -H "Authorization: Bearer freecc" http://localhost:8082/v1/models | python3 -c "import sys,json; d=json.load(sys.stdin); print(str(len(d['data']))+' models available')"
```

**4. free-Claude-code gateway auth:** Requires `Authorization: Bearer freecc` header on all requests. Without it: `{"detail":"Missing API key"}`.
