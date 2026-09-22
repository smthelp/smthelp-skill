#!/usr/bin/env bash
# hermes-mcp-audit: 3-step MCP availability diagnostic for a Hermes Agent install.
# Idempotent. Safe to re-run. Exits 0 unless a hard error occurs.
#
# Usage:  bash audit-mcp.sh
#         bash audit-mcp.sh /path/to/hermes-home   (custom HERMES_HOME)
#
# Outputs a structured report:
#   1. Config:  mcp_servers: block presence + server count
#   2. Venv:    `mcp` package presence + version
#   3. Extras:  declared `[mcp]` extra contents
#   4. Install: re-runs the install with the right venv prefix (idempotent)
#
# Honors HERMES_HOME if set. Falls back to ~/.hermes.

set -uo pipefail

HERMES_HOME="${1:-${HERMES_HOME:-$HOME/.hermes}}"
HERMES_AGENT_DIR="$HERMES_HOME/hermes-agent"
VENV_DIR="$HERMES_AGENT_DIR/venv"
PY_VER=$(ls -1 "$VENV_DIR/lib/" 2>/dev/null | grep -E "^python[0-9.]+$" | head -1)
SITE_PACKAGES="$VENV_DIR/lib/${PY_VER}/site-packages"

hr() { printf '\n=== %s ===\n' "$1"; }

hr "Hermes MCP audit"
echo "HERMES_HOME        = $HERMES_HOME"
echo "Hermes agent dir   = $HERMES_AGENT_DIR"
echo "Venv               = $VENV_DIR"
echo "Python             = ${PY_VER:-<not found>}"

# --- Step 1: config ---
hr "1. Config — mcp_servers: in $HERMES_HOME/config.yaml"
CONFIG_FILE="$HERMES_HOME/config.yaml"
if [[ -f "$CONFIG_FILE" ]]; then
  if grep -qE "^[[:space:]]*mcp_servers:" "$CONFIG_FILE"; then
    echo "PRESENT — extracting server list..."
    # Show the mcp_servers: block and any indented keys (top-level server names)
    awk '/^[[:space:]]*mcp_servers:/{flag=1; print; next} flag && /^[[:space:]]{2}[a-zA-Z0-9_-]+:/{print "  • server:", $0} flag && /^[[:space:]]*[^[:space:]].*:/{flag=0}' "$CONFIG_FILE"
  else
    echo "ABSENT — no mcp_servers: block. 0 MCP-backed tools will be exposed regardless of installed packages."
  fi
else
  echo "MISSING — $CONFIG_FILE not found."
fi

# --- Step 2: venv ---
hr "2. Venv — mcp client package"
if [[ -d "$SITE_PACKAGES" ]]; then
  MCP_PKG=$(ls -1 "$SITE_PACKAGES" 2>/dev/null | grep -E "^mcp(-[0-9].*)?\.dist-info$" | head -1)
  if [[ -n "$MCP_PKG" ]]; then
    MCP_VER=$(echo "$MCP_PKG" | sed -E 's/^mcp-(.+)\.dist-info$/\1/')
    echo "INSTALLED — mcp $MCP_VER (at $SITE_PACKAGES)"
  else
    echo "MISSING — mcp package not in venv. Run the install step below."
  fi
else
  echo "VENV NOT FOUND — $SITE_PACKAGES does not exist."
fi

# --- Step 3: extras ---
hr "3. Extras — pyproject.toml [mcp] declaration"
PYPROJECT="$HERMES_AGENT_DIR/pyproject.toml"
if [[ -f "$PYPROJECT" ]]; then
  python3 -c "
import re, sys
text = open(r'''$PYPROJECT''').read()
m = re.search(r'^mcp\s*=\s*(\[[^\]]+\])', text, re.M)
if m:
    print('DECLARED:', m.group(1))
else:
    print('NOT DECLARED in pyproject.toml')
" 2>/dev/null || echo "(python3 not available; could not parse pyproject.toml)"
else
  echo "pyproject.toml not found at $PYPROJECT"
fi

# --- Step 4: install (idempotent no-op if already satisfied) ---
hr "4. Install — uv pip install -e .[mcp] (idempotent)"
if command -v uv >/dev/null 2>&1 && [[ -d "$VENV_DIR" ]]; then
  VIRTUAL_ENV="$VENV_DIR" uv pip install -e "$HERMES_AGENT_DIR[mcp]" 2>&1 | tail -8
else
  echo "SKIPPED — uv not on PATH or venv missing. Install uv (brew install uv) or create venv first."
fi

hr "Summary"
echo "Config:  $( [[ -f "$CONFIG_FILE" ]] && grep -qE '^[[:space:]]*mcp_servers:' "$CONFIG_FILE" && echo 'configured' || echo 'empty' )"
echo "Venv:    $( [[ -n "${MCP_VER:-}" ]] && echo "mcp $MCP_VER" || echo 'no mcp package' )"
echo "Action:  edit $CONFIG_FILE to add mcp_servers:, then restart the Hermes session."
