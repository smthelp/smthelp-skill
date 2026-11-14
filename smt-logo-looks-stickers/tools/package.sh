#!/bin/sh
# Build the skill zip: <name>-v<version>.zip next to the skill folder.
# Mirrors smt-3d-product-media tools/package.sh (zip, not .skill).
set -e
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NAME="$(basename "$SKILL_DIR")"
VER="$(cat "$SKILL_DIR/VERSION")"
OUT="$(dirname "$SKILL_DIR")/${NAME}-v${VER}.zip"
cd "$(dirname "$SKILL_DIR")"
rm -f "$OUT"
zip -rq "$OUT" "$NAME" -x '*/__pycache__/*' '*/.DS_Store'
echo "built $OUT"
ls -la "$OUT"
