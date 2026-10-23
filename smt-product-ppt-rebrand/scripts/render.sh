#!/bin/bash
# usage: render.sh <deck.pptx>  -> <deck>.pdf + <deck>_p-NN.png (60 dpi) for visual QA.
# LibreOffice when installed; else temporary Google Slides conversion (deleted after).
# NOTE: Google substitutes 微软雅黑 with a wider font, so a line that wraps here may fit in PowerPoint.
set -e
f="$1"; b="${f%.pptx}"
if command -v soffice >/dev/null 2>&1; then
  soffice --headless --convert-to pdf --outdir "$(dirname "$f")" "$f" >/dev/null
else
  id=$(gws drive files create --json '{"name":"_tmp_render","mimeType":"application/vnd.google-apps.presentation"}' --upload "$f" --params '{"fields":"id"}' | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
  trap 'gws drive files delete --params "{\"fileId\":\"$id\"}" >/dev/null 2>&1 || true' EXIT
  gws drive files export --params "{\"fileId\":\"$id\",\"mimeType\":\"application/pdf\"}" --output "$b.pdf" >/dev/null
  rm -f download.html
fi
rm -f "${b}"_p-*.png; pdftoppm -r 60 -png "$b.pdf" "${b}_p"
ls "${b}"_p-*.png | wc -l
