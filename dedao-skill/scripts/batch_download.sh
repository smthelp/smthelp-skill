#!/bin/bash
# 批量下载脚本

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
OUTPUT_DIR=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['output_dir'])")
BATCH_SIZE=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('batch_size', 10))")
DELAY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('delay_between_downloads', 2))")

# 展开路径
OUTPUT_DIR=$(eval echo "$OUTPUT_DIR")

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== 批量下载脚本 ===${NC}"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 获取课程列表
echo -e "${YELLOW}正在获取课程列表...${NC}"
COURSE_IDS=$(dedao-dl course --json | python3 -c "
import sys, json
data = json.load(sys.stdin)
courses = data.get('list', [])
for c in courses:
    print(c['id'])
")

if [ -z "$COURSE_IDS" ]; then
    echo -e "${RED}错误: 无法获取课程列表${NC}"
    exit 1
fi

# 统计
TOTAL=$(echo "$COURSE_IDS" | wc -l)
SUCCESS=0
FAILED=0
SKIPPED=0

echo -e "${GREEN}共 $TOTAL 个课程待下载${NC}"
echo ""

# 下载课程
for COURSE_ID in $COURSE_IDS; do
    echo -e "${YELLOW}--- 下载课程 $COURSE_ID ---${NC}"
    
    # 检查是否已下载
    COURSE_DIR=$(find "$OUTPUT_DIR" -maxdepth 1 -type d -name "*$COURSE_ID*" 2>/dev/null | head -1)
    
    if [ -n "$COURSE_DIR" ]; then
        echo -e "${YELLOW}跳过: 课程已下载${NC}"
        ((SKIPPED++))
        continue
    fi
    
    # 下载
    cd "$OUTPUT_DIR"
    if dedao-dl dl "$COURSE_ID" -t 3 -m 2>&1 | tail -5; then
        echo -e "${GREEN}✓ 课程 $COURSE_ID 下载完成${NC}"
        ((SUCCESS++))
    else
        echo -e "${RED}✗ 课程 $COURSE_ID 下载失败${NC}"
        ((FAILED++))
    fi
    
    echo ""
    sleep "$DELAY"
done

echo -e "${GREEN}=== 下载完成 ===${NC}"
echo "成功: $SUCCESS"
echo "失败: $FAILED"
echo "跳过: $SKIPPED"
echo "总计: $TOTAL"
