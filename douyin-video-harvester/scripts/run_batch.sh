#!/usr/bin/env bash
# Two-phase batch. Phase A (automatic): scrape -> rank -> filter -> download -> frames -> dedupe.
# Then REVIEW the contact sheets + 03_candidates.json and fill 07_selection.json (see references/selection-guide.md).
# Phase B: select -> verify -> upload.
# Usage: scripts/run_batch.sh A config.json   |   scripts/run_batch.sh B config.json [manifest_copy.csv]
set -euo pipefail
cd "$(dirname "$0")/.."
phase=$1; cfg=$2
case $phase in
  A) python3 -m dyh auto -c "$cfg"; python3 -m dyh list -c "$cfg"; python3 -m dyh select-template -c "$cfg" ;;
  B) python3 -m dyh select -c "$cfg"; python3 -m dyh verify -c "$cfg"
     python3 -m dyh upload -c "$cfg" ${3:+--manifest-copy "$3"} ;;
  *) echo "phase must be A or B"; exit 2 ;;
esac
