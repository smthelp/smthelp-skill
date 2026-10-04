#!/bin/bash
# 得到课程Skill安装脚本

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== 得到课程Skill安装程序 ===${NC}"
echo ""

# 检查系统
echo -e "${YELLOW}检查系统环境...${NC}"

# 检查bash
if ! command -v bash &> /dev/null; then
    echo -e "${RED}错误: bash 未安装${NC}"
    exit 1
fi

# 检查curl
if ! command -v curl &> /dev/null; then
    echo -e "${YELLOW}正在安装curl...${NC}"
    apt-get update && apt-get install -y curl
fi

# 检查git
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}正在安装git...${NC}"
    apt-get update && apt-get install -y git
fi

# 检查python3
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}正在安装python3...${NC}"
    apt-get update && apt-get install -y python3
fi

echo -e "${GREEN}✓ 系统环境检查完成${NC}"
echo ""

# 安装dedao-dl
echo -e "${YELLOW}检查dedao-dl...${NC}"

if command -v dedao-dl &> /dev/null; then
    echo -e "${GREEN}✓ dedao-dl 已安装${NC}"
else
    echo -e "${YELLOW}正在安装dedao-dl...${NC}"
    
    # 检测系统架构
    ARCH=$(uname -m)
    if [ "$ARCH" = "x86_64" ]; then
        DEDAO_URL="https://github.com/yann0917/dedao-dl/releases/download/v1.2.32/dedao-dl-linux-amd64.tar.gz"
    elif [ "$ARCH" = "aarch64" ]; then
        DEDAO_URL="https://github.com/yann0917/dedao-dl/releases/download/v1.2.32/dedao-dl-linux-arm64.tar.gz"
    else
        echo -e "${RED}错误: 不支持的系统架构: $ARCH${NC}"
        exit 1
    fi
    
    cd /tmp
    curl -sL -o dedao-dl.tar.gz "$DEDAO_URL"
    tar -xzf dedao-dl.tar.gz
    chmod +x dedao-dl-linux-*
    mv dedao-dl-linux-* /usr/local/bin/dedao-dl
    rm -f dedao-dl.tar.gz
    
    echo -e "${GREEN}✓ dedao-dl 安装完成${NC}"
fi

echo ""

# 设置脚本权限
echo -e "${YELLOW}设置脚本权限...${NC}"
chmod +x run.sh
chmod +x scripts/*.sh
chmod +x scripts/*.py

echo -e "${GREEN}✓ 脚本权限设置完成${NC}"
echo ""

# 创建配置目录
echo -e "${YELLOW}创建配置目录...${NC}"
mkdir -p config
mkdir -p output

# 检查配置文件
if [ ! -f config/config.json ]; then
    echo -e "${YELLOW}创建配置文件...${NC}"
    cp config/config.example.json config/config.json
    echo -e "${YELLOW}请编辑 config/config.json 填入你的配置${NC}"
fi

echo -e "${GREEN}✓ 配置目录创建完成${NC}"
echo ""

# 完成
echo -e "${GREEN}=== 安装完成 ===${NC}"
echo ""
echo "下一步："
echo "1. 编辑 config/config.json 填入你的得到cookie"
echo "2. 运行 ./run.sh 开始使用"
echo ""
echo "获取cookie的方法："
echo "1. 在浏览器中打开 https://www.dedao.cn 并登录"
echo "2. 按F12打开开发者工具"
echo "3. 切换到Application标签"
echo "4. 找到Cookies -> https://www.dedao.cn"
echo "5. 复制所有cookie值"
