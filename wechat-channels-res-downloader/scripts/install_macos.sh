#!/usr/bin/env bash
# Install res-downloader on macOS. Default: latest 4.x beta. STABLE=1 -> latest stable (3.1.x).
set -euo pipefail
REPO="putyy/res-downloader"
ARCH="$(uname -m)"
api="https://api.github.com/repos/$REPO/releases?per_page=30"
json="$(curl -fsSL "$api")"
pick() { python3 -c '
import json,sys,os
rels=json.loads(sys.stdin.read()); stable=os.environ.get("STABLE")=="1"; arch=sys.argv[1]
for r in rels:
    if stable and r["prerelease"]: continue
    names={a["name"]:a["browser_download_url"] for a in r["assets"] if a["name"].endswith(".dmg") and "_mac" in a["name"]}
    if not names: continue
    want=["mac_arm64.dmg" if arch=="arm64" else "mac_amd64.dmg","mac_universal.dmg","_mac.dmg"]
    for w in want:
        for n,u in names.items():
            if n.endswith(w): print(r["tag_name"], u); sys.exit()
' "$ARCH"; }
read -r TAG URL < <(printf '%s' "$json" | STABLE="${STABLE:-0}" pick)
echo "Installing res-downloader $TAG for $ARCH"
tmp="$(mktemp -d)"; dmg="$tmp/rd.dmg"
curl -fL "$URL" -o "$dmg"
mnt="$(hdiutil attach -nobrowse -readonly "$dmg" | awk -F'\t' '/\/Volumes\//{print $NF}' | tail -1)"
app="$(find "$mnt" -maxdepth 2 -name 'res-downloader*.app' | head -1)"
[ -d /Applications/res-downloader.app ] && osascript -e 'quit app "res-downloader"' 2>/dev/null || true
rm -rf /Applications/res-downloader.app
cp -R "$app" /Applications/res-downloader.app
hdiutil detach "$mnt" -quiet || true
xattr -dr com.apple.quarantine /Applications/res-downloader.app 2>/dev/null || true
rm -rf "$tmp"
mkdir -p "$HOME/Movies/SMT-WeChat-Channels"
echo "Done. Open res-downloader, install the certificate when asked, then click 开启抓取."
open -a /Applications/res-downloader.app || true
