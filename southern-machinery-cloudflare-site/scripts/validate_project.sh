#!/bin/sh
set -eu

project_dir=${1:-.}
cd "$project_dir"

fail=0

check_file() {
  if [ ! -f "$1" ]; then
    printf 'MISSING  %s\n' "$1"
    fail=1
  else
    printf 'OK       %s\n' "$1"
  fi
}

check_file AGENTS.md
check_file package.json

if [ ! -f wrangler.toml ] && [ ! -f wrangler.pages.toml ]; then
  printf 'MISSING  wrangler.toml or wrangler.pages.toml\n'
  fail=1
else
  printf 'OK       Cloudflare configuration found\n'
fi

if [ ! -d schema ] && [ ! -d migrations ]; then
  printf 'WARN     No schema/ or migrations/ directory found\n'
fi

if command -v rg >/dev/null 2>&1; then
  if rg -n --hidden --glob '!.git/**' --glob '!node_modules/**' \
    '(JWT_SECRET|password)[[:space:]]*=[[:space:]]*"[^<$]|BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY' .; then
    printf 'REVIEW   Possible committed secret or password found\n'
    fail=1
  else
    printf 'OK       No obvious committed secret pattern found\n'
  fi
fi

exit "$fail"
