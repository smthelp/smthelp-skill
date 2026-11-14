#!/usr/bin/env bash
# Remove root cert installed by wx_channels_download, then the app folder.
set -euo pipefail
DEST="${DEST:-$HOME/Applications/wx_channels_download}"
[ -x "$DEST/wx_video_download" ] && sudo "$DEST/wx_video_download" uninstall || true
echo "Cert removed. Turn off system proxy if network fails: 系统设置 → 网络 → 详细信息 → 代理."
read -r -p "Delete $DEST too? [y/N] " a; [ "$a" = y ] && rm -rf "$DEST"
