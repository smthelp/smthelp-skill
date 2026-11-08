#!/usr/bin/env bash
# Low-res end-to-end run of examples/s7040p (320x180, 6 fps): check -> inspect -> render -> real -> compose (no voice/deck by default).
# usage: tests/smoke.sh <job_dir_with_inputs>   (a copy of examples/s7040p with inputs/ filled)   [--full: also voice + deck]
set -euo pipefail
SK="$(cd "$(dirname "$0")/.." && pwd)"; J="${1:?job dir}"; FULL="${2:-}"
C="python3 $SK/scripts/smt3dmedia.py"
SET="--set output.dir=\"out-smoke\" --set render.width=320 --set render.height=180 --set render.fps=6 --set render.supersample=1"
[ "$FULL" = "--full" ] || SET="$SET --set voice.enabled=false --set deck.enabled=false"
eval $C doctor
for st in check inspect render real voice compose deck; do eval $C $st "$J/job.json" $SET; done
for L in EN ZH; do f=$(ls "$J"/out-smoke/video/*-$L.mp4); d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"); echo "$f $d s"; done
echo PASS
