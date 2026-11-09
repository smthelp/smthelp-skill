#!/usr/bin/env bash
# Build dist/<name>-v<VERSION>.zip and .skill (same zip) for offline install / backup (repo convention).
set -euo pipefail
SK="$(cd "$(dirname "$0")/.." && pwd)"; NAME="$(basename "$SK")"; VER="$(cat "$SK/VERSION")"; OUT="${1:-$SK/../dist}"
mkdir -p "$OUT"; cd "$SK/.."
zip -qr "$OUT/$NAME-v$VER.zip" "$NAME" -x "*/__pycache__/*" "*/out*/*" "*.pyc"
cp "$OUT/$NAME-v$VER.zip" "$OUT/$NAME-v$VER.skill"; echo "$OUT/$NAME-v$VER.zip"
