#!/bin/bash
# 批量分析脚本

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
INDUSTRY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['industry'])")

# 展开路径
OUTPUT_DIR=$(eval echo "$OUTPUT_DIR")

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== 批量分析脚本 ===${NC}"
echo ""

# 检查输出目录
if [ ! -d "$OUTPUT_DIR" ]; then
    echo -e "${RED}错误: 输出目录不存在: $OUTPUT_DIR${NC}"
    exit 1
fi

# 统计
TOTAL=0
SUCCESS=0
FAILED=0

# 分析课程
for dir in "$OUTPUT_DIR"/*/MD; do
    if [ -d "$dir" ]; then
        course_name=$(basename "$(dirname "$dir")")
        echo -e "${YELLOW}--- 分析课程: $course_name ---${NC}"
        
        ((TOTAL++))
        
        # 运行分析器
        if python3 "$SCRIPT_DIR/analyze.py" "$dir" --industry "$INDUSTRY" 2>&1; then
            echo -e "${GREEN}✓ 课程分析完成${NC}"
            ((SUCCESS++))
        else
            echo -e "${RED}✗ 课程分析失败${NC}"
            ((FAILED++))
        fi
        
        echo ""
    fi
done

echo -e "${GREEN}=== 分析完成 ===${NC}"
echo "成功: $SUCCESS"
echo "失败: $FAILED"
echo "总计: $TOTAL"
