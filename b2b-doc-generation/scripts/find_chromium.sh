#!/bin/bash
# find_chromium.sh — locate chromium_headless_shell on macOS
# Usage: bash find_chromium.sh
# Returns: absolute path to chrome-headless-shell, or empty string if not found

CHROMIUM=$(find ~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell -type f 2>/dev/null | head -1)

if [ -z "$CHROMIUM" ]; then
    echo "WARNING: chromium_headless_shell not found in ~/Library/Caches/ms-playwright/"
    exit 1
else
    echo "$CHROMIUM"
    exit 0
fi
