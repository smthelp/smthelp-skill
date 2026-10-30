#!/bin/bash
# cad3d-animation-video-landing pipeline driver (v2.1.0)
# usage: PROJ=/path/to/proj bash pipeline.sh <stage> [aspect]
# stages: setup | fetch | extract | pack | tts | preview | sheet | dbg | bench | render | encode | audio | srt | thumb | landing | testlanding | status
# Every stage is idempotent / resumable. Product-specific code (pack.py, engine.js, video.js, landing.js, build_landing.py)
# must already be adapted in $PROJ/build (start from examples/<closest product>/).
set -e
PROJ=${PROJ:-$(cd "$(dirname "$0")/.." && pwd)}; export PROJ
B=$PROJ/build; E=$PROJ/env
[ -f $PROJ/product.json ] && eval "$(python3 $B/cfg.py $PROJ/product.json)"
export PLAYWRIGHT_BROWSERS_PATH=$E/browsers LD_LIBRARY_PATH=$E/libs/usr/lib/aarch64-linux-gnu
PY=$E/venv/bin/python; cd $B
case "$1" in
  setup)   bash setup_env.sh; [ -d node_modules/three ] || npm i three@0.169.0 esbuild ;;
  fetch)   mkdir -p $PROJ/src; curl -sSL -o $PROJ/src/drawing.html "$DRAWING_URL"; curl -sSL -o $PROJ/src/landing.html "$LANDING_URL" ;;
  extract) timeout 1100 $PY extract_mesh.py $PROJ/src/drawing.html $PROJ/src/ ;;
  pack)    $PY pack.py ;;
  tts)     mkdir -p audio; $PY tts.py ;;
  preview) node_modules/.bin/esbuild video.js --bundle --format=iife --outfile=video.bundle.js --log-level=warning && $PY mkpage.py
           $PY preview.py ${2:-l} ${3:-5,20,40,60,80,100} 0.25 ;;
  sheet)   $PY sheet.py ${2:-l} ${3:-3} ${4:-640} ;;                    # contact sheet of work/prev/<aspect>_*.jpg
  dbg)     $PY dbg.py "$2" ;;                                              # JSON list of {st,tg,d,az,el} bare-stage shots
  bench)   $PY bench.py ${2:-0.6} x 0 0 ;;                                 # s/frame at 4K for the given R3D
  testlanding) PAGE=${PAGE:-$(ls $PROJ/deliverables/*.html | head -1)} $PY testlanding.py ;;
  render)  # SHARDS=1 recommended (v2.1: two shards gave no gain on 2 vCPU). Per-aspect R3D: R3D_L / R3D_P
           [ "${2:-l}" = p ] && export R3D=${R3D_P:-${R3D:-0.5}} || export R3D=${R3D_L:-${R3D:-0.6}}; export AA=${AA:-0}
           # launches $SHARDS resumable shards for one aspect and waits; rerun until "have N of N"
           for k in $(seq 0 $((SHARDS-1))); do SHARD=$k/$SHARDS bash run_render.sh ${2:-l} $CHUNK > $PROJ/work_render_${2:-l}_$k.log 2>&1 & sleep 15; done; wait
           tail -n1 $PROJ/work_render_${2:-l}_*.log ;;
  encode)  NSEG=$NSEG CODE=$CODE bash enc_all.sh ${2:-l} ;;
  audio)   $PY audio_mix.py ;;
  srt)     $PY make_srt.py $CODE ;;
  thumb)   CODE=$CODE $PY thumb.py ;;
  landing) $PY build_landing.py ;;
  status)  for a in $ASPECTS; do echo "$a: $(ls $PROJ/frames_$a 2>/dev/null | grep -c jpg) frames"; done; ls -la $PROJ/deliverables 2>/dev/null ;;
  *) echo "unknown stage"; exit 1 ;;
esac
