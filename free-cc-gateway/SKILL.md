---
name: free-cc-gateway
description: "free-Claude-code local Anthropic proxy gateway — LaunchAgent setup, env vars, Hermes integration, Open WebUI client. Runs on port 8082, requires Bearer token auth."
metadata:
  source: hermes
  origin: "devops/free-cc-gateway"
---
## What It Is

free-Claude-code is a local Anthropic API proxy that routes requests through free/third-party LLM backends (NVIDIA NIM, OpenRouter, etc.) instead of paying for official Anthropic API. It exposes an OpenAI-compatible API at `localhost:8082`.

**Auth:** `Authorization: Bearer freecc` (all requests)
**Endpoint:** `http://localhost:8082/v1`
**Models list:** `GET /v1/models`

---

## Quick Start

```bash
# Already installed at ~/free-Claude-code
cd ~/free-Claude-code
uv run uvicorn server:app --host 0.0.0.0 --port 8082 --timeout-graceful-shutdown 5
```

---

## LaunchAgent (macOS Auto-Start)

**File:** `~/Library/LaunchAgents/com.free-Claude-code.server.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.free-Claude-code.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/uv</string>
        <string>run</string>
        <string>uvicorn</string>
        <string>server:app</string>
        <string>--host</string>
        <string>0.0.0.0</string>
        <string>--port</string>
        <string>8082</string>
        <string>--timeout-graceful-shutdown</string>
        <string>5</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/jasonwu/free-Claude-code</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/jasonwu/free-Claude-code/server.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/jasonwu/free-Claude-code/server.log</string>
    <key>ProcessType</key>
    <string>Background</string>
</dict>
</plist>
```

```bash
# Load / unload
launchctl load ~/Library/LaunchAgents/com.free-Claude-code.server.plist
launchctl unload ~/Library/LaunchAgents/com.free-Claude-code.server.plist

# Verify
launchctl list | grep free-Claude-code
lsof -i :8082 | grep LISTEN
```

---

## Environment Variables

### In `~/.zshrc` (for shell sessions)
```bash
export ANTHROPIC_AUTH_TOKEN="freecc"
export ANTHROPIC_BASE_URL="http://localhost:8082"
```

### In `~/.hermes/config.yaml` (terminal section)
```yaml
terminal:
  env_passthrough:
    - ANTHROPIC_AUTH_TOKEN
    - ANTHROPIC_BASE_URL
  shell_init_files:
    - ~/.zshrc
```

### Why Both?
- `~/.zshrc` → makes vars available in terminal shells (so Claude Code CLI picks them up)
- `env_passthrough` in Hermes config → ensures Hermes passes them to sub-processes (Claude Code, OpenCode agents)
- Without `env_passthrough`, sub-process agents bypass the local gateway and connect directly to official Anthropic API

---

## Session Startup Checklist

Run these before starting any Claude Code / OpenCode sub-agent:

```bash
# 1. Check env_passthrough in Hermes config
grep -A3 "env_passthrough:" ~/.hermes/config.yaml

# 2. Check .zshrc exports
grep -E "ANTHROPIC_(AUTH_TOKEN|BASE_URL)" ~/.zshrc

# 3. Confirm gateway is up
curl -s -H "Authorization: Bearer freecc" http://localhost:8082/v1/models | python3 -c "import sys,json; d=json.load(sys.stdin); print(str(len(d['data']))+' models')" 2>/dev/null || echo "GATEWAY DOWN"

# 4. Check current ANTHROPIC_BASE_URL in shell
echo $ANTHROPIC_BASE_URL  # should print http://localhost:8082
```

If `ANTHROPIC_BASE_URL` is not `http://localhost:8082`, run:
```bash
source ~/.zshrc
```

If gateway is down:
```bash
launchctl load ~/Library/LaunchAgents/com.free-Claude-code.server.plist
sleep 3
curl -s -H "Authorization: Bearer freecc" http://localhost:8082/v1/models | head -c 100
```

---

## Integration with Open WebUI

Open WebUI (at `http://localhost:8080`) can use free-Claude-code as a custom OpenAI-compatible backend.

**In Open WebUI → Admin → Models:**
- API Base URL: `http://localhost:8082/v1`
- API Key: `freecc`

**Or via environment before starting Open WebUI:**
```bash
export OPENAI_API_BASE_URL="http://localhost:8082/v1"
export OPENAI_API_KEY="freecc"
cd /tmp && open-webui serve
```

**Verify from Open WebUI:** Send a test message using any model — check `~/free-Claude-code/server.log` for incoming requests.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `{"detail":"Missing API key"}` | Missing `Authorization: Bearer freecc` header | Add header to all requests |
| `400` from Open WebUI | Wrong API key or base URL | Verify `freecc` and `http://localhost:8082/v1` |
| Gateway not reachable | Service not loaded | `launchctl load ~/Library/LaunchAgents/com.free-Claude-code.server.plist` |
| Sub-agent uses official API | `env_passthrough` missing from Hermes config | Add to `~/.hermes/config.yaml` terminal section |
| Port 8082 already in use | Another process on 8082 | `lsof -i :8082` to find conflict |

---

## Log File

`~/free-Claude-code/server.log` — contains uvicorn access logs and application startup messages.

```bash
tail -f ~/free-Claude-code/server.log
```
