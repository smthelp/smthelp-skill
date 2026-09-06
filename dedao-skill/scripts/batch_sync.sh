#!/bin/bash
# 批量同步脚本

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 运行同步脚本
bash "$SCRIPT_DIR/sync_obsidian.sh"
