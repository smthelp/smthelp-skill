#!/usr/bin/env bash
# Regression test: rebuild the reference example and run the full Playwright acceptance test.
# Run after ANY change to scripts/ or templates/, before bumping the version.
#   bash scripts/regress.sh [out-dir]
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-/tmp/smt-lp-regress}"
python3 "$HERE/scripts/build.py" "$HERE/examples/radial-splice-tape" --out "$OUT"
python3 "$HERE/scripts/verify.py" "$OUT/ai-radial-splicing-tape-3-5-6-hole-masking-kraft-paper-splice-cutter-southern-machinery.html" \
  --config "$HERE/examples/radial-splice-tape" --shots "$OUT/shots"
echo "regression OK -> $OUT (look at shots/light_top.png, ar_middle.png, mobile_ar_top.png)"
