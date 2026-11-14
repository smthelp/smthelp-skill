#!/usr/bin/env bash
# Install ltaoo/wx_channels_download on macOS into ~/Applications/wx_channels_download
set -euo pipefail
REPO="ltaoo/wx_channels_download"
case "$(uname -m)" in arm64) SUF="darwin_arm64";; x86_64) SUF="darwin_x86_64";; *) echo "unsupported arch"; exit 1;; esac
DEST="${DEST:-$HOME/Applications/wx_channels_download}"
read -r TAG URL < <(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" | python3 -c '
import json,sys; r=json.load(sys.stdin); suf=sys.argv[1]
u=[a["browser_download_url"] for a in r["assets"] if a["name"].endswith(suf+".zip")]
print(r["tag_name"], u[0])' "$SUF")
echo "Installing wx_channels_download $TAG ($SUF) -> $DEST"
tmp="$(mktemp -d)"; curl -fL "$URL" -o "$tmp/wx.zip"
mkdir -p "$DEST"; unzip -o -q "$tmp/wx.zip" -d "$tmp/x"
bin="$(find "$tmp/x" -type f -name 'wx_video_download' | head -1)"
cp -R "$(dirname "$bin")"/. "$DEST"/
chmod +x "$DEST/wx_video_download"
xattr -dr com.apple.quarantine "$DEST" 2>/dev/null || true
OUT="$HOME/Movies/SMT-WeChat-Channels"; mkdir -p "$OUT"
if [ ! -f "$DEST/config.yaml" ]; then
  sed "s#/Users/YOUR_USER/Movies/SMT-WeChat-Channels#$OUT#" "$(dirname "$0")/../config/config.example.yaml" > "$DEST/config.yaml"
fi
rm -rf "$tmp"
echo "$TAG" > "$DEST/.installed_version"
cat <<MSG
Done. First run (installs root cert + system proxy, asks for your Mac password):
  cd "$DEST" && sudo ./wx_video_download
Wait for 「代理服务启动成功」, then open 视频号 in Mac WeChat — a 下载 button appears under each video.
If macOS blocks it: 系统设置 → 隐私与安全性 → 仍要打开, then run again.
MSG
