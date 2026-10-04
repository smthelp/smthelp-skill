#!/bin/bash
# Skill测试脚本

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== 得到课程Skill测试 ===${NC}"
echo ""

# 测试1: 检查脚本权限
echo -e "${YELLOW}测试1: 检查脚本权限${NC}"
if [ -x "./run.sh" ]; then
    echo -e "${GREEN}✓ run.sh 有执行权限${NC}"
else
    echo -e "${RED}✗ run.sh 没有执行权限${NC}"
fi

if [ -x "./install.sh" ]; then
    echo -e "${GREEN}✓ install.sh 有执行权限${NC}"
else
    echo -e "${RED}✗ install.sh 没有执行权限${NC}"
fi

echo ""

# 测试2: 检查配置文件
echo -e "${YELLOW}测试2: 检查配置文件${NC}"
if [ -f "./config/config.example.json" ]; then
    echo -e "${GREEN}✓ 配置模板存在${NC}"
else
    echo -e "${RED}✗ 配置模板不存在${NC}"
fi

echo ""

# 测试3: 检查脚本文件
echo -e "${YELLOW}测试3: 检查脚本文件${NC}"
for script in analyze.py sync_obsidian.sh batch_download.sh batch_analyze.sh batch_sync.sh; do
    if [ -f "./scripts/$script" ]; then
        echo -e "${GREEN}✓ scripts/$script 存在${NC}"
    else
        echo -e "${RED}✗ scripts/$script 不存在${NC}"
    fi
done

echo ""

# 测试4: 检查文档
echo -e "${YELLOW}测试4: 检查文档${NC}"
for doc in SETUP.md USAGE.md TROUBLESHOOTING.md; do
    if [ -f "./docs/$doc" ]; then
        echo -e "${GREEN}✓ docs/$doc 存在${NC}"
    else
        echo -e "${RED}✗ docs/$doc 不存在${NC}"
    fi
done

echo ""

# 测试5: 检查dedao-dl
echo -e "${YELLOW}测试5: 检查dedao-dl${NC}"
if command -v dedao-dl &> /dev/null; then
    echo -e "${GREEN}✓ dedao-dl 已安装${NC}"
else
    echo -e "${RED}✗ dedao-dl 未安装${NC}"
fi

echo ""

# 测试6: 检查python3
echo -e "${YELLOW}测试6: 检查python3${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ python3 已安装${NC}"
else
    echo -e "${RED}✗ python3 未安装${NC}"
fi

echo ""

# 测试7: 检查帮助信息
echo -e "${YELLOW}测试7: 检查帮助信息${NC}"
if ./run.sh --help > /dev/null 2>&1; then
    echo -e "${GREEN}✓ run.sh --help 正常工作${NC}"
else
    echo -e "${RED}✗ run.sh --help 工作异常${NC}"
fi

echo ""

echo -e "${GREEN}=== 测试完成 ===${NC}"
