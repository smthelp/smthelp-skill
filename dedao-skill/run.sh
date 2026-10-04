#!/bin/bash
# 得到课程Skill主入口脚本

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 加载配置
source "$SCRIPT_DIR/config/config.json" 2>/dev/null || true

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认配置
CONFIG_FILE="$SCRIPT_DIR/config/config.json"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/output}"
VAULT_DIR="${VAULT_DIR:-$HOME/obsidian-vault}"

# 显示帮助
show_help() {
    echo -e "${GREEN}得到课程Skill - 主入口脚本${NC}"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -l, --list                    列出可用课程"
    echo "  -d, --download <课程ID>       下载指定课程"
    echo "  -a, --analyze <课程目录>      分析课程内容"
    echo "  -g, --generate                生成SMT外贸营销建议"
    echo "  -s, --sync                    同步到Obsidian仓库"
    echo "  -b, --batch-download          批量下载所有课程"
    echo "  -B, --batch-analyze           批量分析所有课程"
    echo "  -S, --batch-sync              批量同步所有课程"
    echo "  -i, --industry <行业>         指定行业领域"
    echo "  -c, --config <配置文件>       指定配置文件"
    echo "  -h, --help                    显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 -l                          # 列出课程"
    echo "  $0 -d 656                      # 下载课程"
    echo "  $0 -a output/课程名            # 分析课程"
    echo "  $0 -g -i 'SMT设备外贸'        # 生成建议"
    echo "  $0 -s                          # 同步到Obsidian"
    echo "  $0 -b                          # 批量下载"
    echo ""
}

# 检查依赖
check_dependencies() {
    if ! command -v dedao-dl &> /dev/null; then
        echo -e "${RED}错误: dedao-dl 未安装${NC}"
        echo "请运行: ./install.sh"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误: python3 未安装${NC}"
        exit 1
    fi
}

# 检查登录状态
check_login() {
    if dedao-dl who &> /dev/null; then
        echo -e "${GREEN}✓ 已登录得到账号${NC}"
    else
        echo -e "${YELLOW}未登录，请先运行: dedao-dl login -c '你的cookie'${NC}"
        exit 1
    fi
}

# 列出课程
list_courses() {
    echo -e "${GREEN}正在获取课程列表...${NC}"
    dedao-dl course
}

# 下载课程
download_course() {
    local course_id=$1
    
    if [ -z "$course_id" ]; then
        echo -e "${RED}错误: 请提供课程ID${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}正在下载课程 $course_id...${NC}"
    mkdir -p "$OUTPUT_DIR"
    cd "$OUTPUT_DIR"
    
    dedao-dl dl "$course_id" -t 3 -m
    
    echo -e "${GREEN}✓ 课程下载完成${NC}"
}

# 分析课程
analyze_course() {
    local course_dir=$1
    
    if [ -z "$course_dir" ]; then
        echo -e "${RED}错误: 请提供课程目录${NC}"
        exit 1
    fi
    
    if [ ! -d "$course_dir" ]; then
        echo -e "${RED}错误: 目录不存在: $course_dir${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}正在分析课程: $course_dir${NC}"
    python3 "$SCRIPT_DIR/scripts/analyze.py" "$course_dir"
}

# 生成建议
generate_advice() {
    local industry=$1
    
    if [ -z "$industry" ]; then
        industry="SMT设备外贸"
    fi
    
    echo -e "${GREEN}正在生成${industry}营销建议...${NC}"
    python3 "$SCRIPT_DIR/scripts/generate_advice.py" --industry "$industry"
}

# 同步到Obsidian
sync_to_obsidian() {
    echo -e "${GREEN}正在同步到Obsidian...${NC}"
    bash "$SCRIPT_DIR/scripts/sync_obsidian.sh"
}

# 批量下载
batch_download() {
    echo -e "${GREEN}正在批量下载课程...${NC}"
    bash "$SCRIPT_DIR/scripts/batch_download.sh"
}

# 批量分析
batch_analyze() {
    echo -e "${GREEN}正在批量分析课程...${NC}"
    bash "$SCRIPT_DIR/scripts/batch_analyze.sh"
}

# 批量同步
batch_sync() {
    echo -e "${GREEN}正在批量同步课程...${NC}"
    bash "$SCRIPT_DIR/scripts/batch_sync.sh"
}

# 主流程
main() {
    # 检查参数
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    # 检查依赖
    check_dependencies
    
    # 解析参数
    while [ $# -gt 0 ]; do
        case "$1" in
            -l|--list)
                check_login
                list_courses
                shift
                ;;
            -d|--download)
                check_login
                download_course "$2"
                shift 2
                ;;
            -a|--analyze)
                analyze_course "$2"
                shift 2
                ;;
            -g|--generate)
                generate_advice "$2"
                shift 2
                ;;
            -s|--sync)
                sync_to_obsidian
                shift
                ;;
            -b|--batch-download)
                check_login
                batch_download
                shift
                ;;
            -B|--batch-analyze)
                batch_analyze
                shift
                ;;
            -S|--batch-sync)
                batch_sync
                shift
                ;;
            -i|--industry)
                INDUSTRY="$2"
                shift 2
                ;;
            -c|--config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}未知选项: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
}

main "$@"
