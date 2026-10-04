#!/bin/bash
# Obsidian同步脚本

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 加载配置
CONFIG_FILE="${SKILL_DIR}/config/config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 配置文件不存在: $CONFIG_FILE"
    exit 1
fi

# 解析配置
VAULT_DIR=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['vault_dir'])")
GITHUB_REPO=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['github_repo'])")
OUTPUT_DIR=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['output_dir'])")

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== Obsidian同步脚本 ===${NC}"
echo ""

# 展开路径
VAULT_DIR=$(eval echo "$VAULT_DIR")
OUTPUT_DIR=$(eval echo "$OUTPUT_DIR")

# 检查输出目录
if [ ! -d "$OUTPUT_DIR" ]; then
    echo -e "${RED}错误: 输出目录不存在: $OUTPUT_DIR${NC}"
    exit 1
fi

# 创建vault目录
mkdir -p "$VAULT_DIR/得到课程"

# 同步课程
echo -e "${YELLOW}正在同步课程到Obsidian...${NC}"

for dir in "$OUTPUT_DIR"/*/; do
    if [ -d "$dir/MD" ]; then
        course_name=$(basename "$dir")
        echo "同步: $course_name"
        mkdir -p "$VAULT_DIR/得到课程/$course_name"
        cp "$dir/MD/"*.md "$VAULT_DIR/得到课程/$course_name/" 2>/dev/null || true
    fi
done

echo -e "${GREEN}✓ 课程同步完成${NC}"
echo ""

# 推送到GitHub（如果配置了仓库）
if [ -n "$GITHUB_REPO" ]; then
    echo -e "${YELLOW}正在推送到GitHub...${NC}"
    
    cd "$VAULT_DIR"
    
    # 初始化git（如果需要）
    if [ ! -d ".git" ]; then
        git init
        git remote add origin "$GITHUB_REPO"
    fi
    
    # 添加文件
    git add .
    
    # 检查是否有更改
    if git diff --cached --quiet; then
        echo -e "${YELLOW}没有新的更改需要提交${NC}"
    else
        # 提交
        git commit -m "更新得到课程笔记 $(date '+%Y-%m-%d %H:%M:%S')"
        
        # 推送
        git push origin main 2>&1 || {
            echo -e "${YELLOW}推送失败，尝试强制推送...${NC}"
            git push origin main --force 2>&1 || {
                echo -e "${RED}推送失败，请检查GitHub仓库配置${NC}"
            }
        }
        
        echo -e "${GREEN}✓ 推送完成${NC}"
    fi
else
    echo -e "${YELLOW}未配置GitHub仓库，跳过推送${NC}"
fi

echo ""
echo -e "${GREEN}=== 同步完成 ===${NC}"
