#!/usr/bin/env bash
# Publish a local file to file.autoinsertion.com via WebDAV.
# /dav/<dir> maps to web /public/<dir>.
#
# Usage:
#   SMFILE_PASS='***' ./publish_webdav.sh <local-file> <remote-path-under-/dav/>
#   SMFILE_PASS='***' ./publish_webdav.sh page.html "Southern%20Machinery%20Product/page.html"
#
# Env: SMFILE_USER (default smtfile), SMFILE_PASS (required, never stored),
#      SMFILE_BASE  (default https://file.autoinsertion.com/dav)
set -euo pipefail
LOCAL="${1:?local file required}"
REMOTE="${2:?remote path required}"
BASE="${SMFILE_BASE:-https://file.autoinsertion.com/dav}"
USER="${SMFILE_USER:-smtfile}"
: "${SMFILE_PASS:?SMFILE_PASS env var required}"

# create parent collections if missing (idempotent: ignore 405/201/409)
parent="$(dirname "$REMOTE")"
if [ "$parent" != "." ]; then
  curl -s -o /dev/null -u "$USER:$SMFILE_PASS" -X MKCOL "$BASE/$parent/" -w "MKCOL $parent -> %{http_code}\n" || true
fi
curl -s -u "$USER:$SMFILE_PASS" -T "$LOCAL" "$BASE/$REMOTE" -w "PUT -> %{http_code}, %{size_upload} bytes\n"
web="${REMOTE//%20/ }"
curl -s -o /dev/null -w "public check -> %{http_code} %{size_download} bytes\n" \
  "https://file.autoinsertion.com/public/$REMOTE"
