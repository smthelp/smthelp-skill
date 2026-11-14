#!/usr/bin/env bash
# Thin wrapper over the res-downloader CLI (v4+, desktop app must be running).
BIN="${RD_BIN:-/Applications/res-downloader.app/Contents/MacOS/res-downloader}"
exec "$BIN" cli "$@" --json
