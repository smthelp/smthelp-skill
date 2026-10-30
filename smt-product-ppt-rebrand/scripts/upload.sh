#!/bin/bash
# usage: upload.sh <deck.pptx> <SEO-file-name.pptx> <drive_folder_id>
# Uploads as a real .pptx (not converted to Google Slides, so the template stays exact).
# If a file with the same name exists in the folder it is updated in place (keeps link + Drive version history).
set -e
f="$1"; name="$2"; folder="$3"; M=application/vnd.openxmlformats-officedocument.presentationml.presentation
old=$(gws drive files list --params "{\"q\":\"name='$name' and '$folder' in parents and trashed=false\",\"fields\":\"files(id)\"}" | python3 -c "import json,sys;f=json.load(sys.stdin).get('files',[]);print(f[0]['id'] if f else '')")
if [ -n "$old" ]; then
  gws drive files update --params "{\"fileId\":\"$old\",\"fields\":\"id,name,webViewLink\"}" --upload "$f"
else
  gws drive files create --json "{\"name\":\"$name\",\"parents\":[\"$folder\"],\"mimeType\":\"$M\"}" --upload "$f" --params '{"fields":"id,name,webViewLink"}'
fi
