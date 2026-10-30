#!/bin/bash
# usage: convert_ppt.sh <file.ppt> [out.pptx]
# Converts legacy .ppt to .pptx. Uses LibreOffice when installed, else a temporary Google Slides
# copy via the gws CLI (Drive account must be connected); the temporary copy is always deleted.
set -e
f="$1"; out="${2:-${f%.*}.pptx}"
if command -v soffice >/dev/null 2>&1; then
  soffice --headless --convert-to pptx --outdir "$(dirname "$out")" "$f" >/dev/null && exit 0
fi
id=$(gws drive files create --json '{"name":"_tmp_convert","mimeType":"application/vnd.google-apps.presentation"}' --upload "$f" --params '{"fields":"id"}' | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
trap 'gws drive files delete --params "{\"fileId\":\"$id\"}" >/dev/null 2>&1 || true' EXIT
gws drive files export --params "{\"fileId\":\"$id\",\"mimeType\":\"application/vnd.openxmlformats-officedocument.presentationml.presentation\"}" --output "$out" >/dev/null
rm -f download.html
echo "converted $out"
