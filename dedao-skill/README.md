# 得到课程内容提取与分析 Skill

## 功能概述

自动化从得到APP提取课程内容，转换为Markdown格式，针对特定业务场景生成实用建议，并同步到Obsidian笔记仓库。

## 适用场景

- **外贸营销**：SMT机器设备、电子产品、工业设备等
- **内容创作**：知识付费、在线教育、培训课程
- **个人学习**：课程笔记、知识管理、终身学习

## 快速开始

### 1. 安装依赖

```bash
# 安装 dedao-dl
curl -sL https://github.com/yann0917/dedao-dl/releases/download/v1.2.32/dedao-dl-linux-amd64.tar.gz | tar -xz
chmod +x dedao-dl-linux-amd64
mv dedao-dl-linux-amd64 /usr/local/bin/dedao-dl
```

### 2. 登录得到账号

```bash
# 使用cookie登录
dedao-dl login -c "你的cookie字符串"

# 或使用扫码登录
dedao-dl login -q
```

### 3. 配置Skill

```bash
# 复制配置模板
cp config/config.example.json config/config.json

# 编辑配置文件
vim config/config.json
```

### 4. 运行Skill

```bash
# 交互式运行
./run.sh

# 或直接运行
./run.sh --course-id 656 --industry "SMT设备外贸"
```

## 目录结构

```
dedao-skill/
├── README.md              # 本文件
├── run.sh                 # 主入口脚本
├── install.sh             # 安装脚本
├── config/
│   ├── config.example.json # 配置模板
│   └── config.json        # 配置文件（git忽略）
├── scripts/
│   ├── download.sh        # 课程下载脚本
│   ├── analyze.py         # 内容分析脚本
│   ├── generate_advice.py # 建议生成脚本
│   └── sync_obsidian.sh   # Obsidian同步脚本
├── templates/
│   ├── advice_template.md # 建议模板
│   └── note_template.md   # 笔记模板
├── docs/
│   ├── SETUP.md           # 安装指南
│   ├── USAGE.md           # 使用指南
│   └── TROUBLESHOOTING.md # 故障排除
└── output/                # 输出目录（git忽略）
```

## 配置说明

### config.json

```json
{
  "cookie": "你的得到cookie",
  "output_dir": "./output",
  "vault_dir": "~/obsidian-vault",
  "github_repo": "https://github.com/username/repo.git",
  "industry": "SMT设备外贸",
  "business_context": "Southern Machinery SMT机器设备外贸营销",
  "auto_sync": true,
  "generate_advice": true
}
```

### 配置参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| cookie | 得到APP的cookie字符串 | 必填 |
| output_dir | 课程输出目录 | ./output |
| vault_dir | Obsidian笔记仓库路径 | ~/obsidian-vault |
| github_repo | GitHub仓库地址 | 可选 |
| industry | 行业领域 | 必填 |
| business_context | 业务场景描述 | 必填 |
| auto_sync | 是否自动同步到Obsidian | true |
| generate_advice | 是否生成建议 | true |

## 使用流程

### 流程1：处理单个课程

```bash
# 1. 列出可用课程
./run.sh --list

# 2. 下载指定课程
./run.sh --download 656

# 3. 分析课程并生成建议
./run.sh --analyze "output/阿里国际站·怎样做好跨境电商"

# 4. 同步到Obsidian
./run.sh --sync
```

### 流程2：批量处理

```bash
# 批量下载所有课程
./run.sh --batch-download

# 批量分析所有课程
./run.sh --batch-analyze

# 批量同步
./run.sh --batch-sync
```

### 流程3：自定义行业模板

```bash
# 生成SMT设备外贸建议
./run.sh --industry "SMT设备外贸" --generate

# 生成电子产品外贸建议
./run.sh --industry "电子产品外贸" --generate

# 生成工业设备外贸建议
./run.sh --industry "工业设备外贸" --generate
```

## 生成的建议内容

针对SMT设备外贸营销，生成以下10个实用建议：

1. **建立专业的B2B数字化展示平台**
2. **打造差异化内容营销**
3. **构建信任体系**
4. **优化供应链透明度**
5. **利用数据驱动决策**
6. **建立多渠道营销矩阵**
7. **提供本地化服务**
8. **制定灵活的定价策略**
9. **建立长期客户关系**
10. **打造品牌故事**

## 扩展与定制

### 添加新行业模板

1. 在 `templates/` 目录下创建新的行业模板
2. 编辑 `config.json` 添加行业配置
3. 运行 `./run.sh --industry "新行业" --generate`

### 自定义建议生成

1. 编辑 `scripts/generate_advice.py`
2. 修改 `SMT_KEYWORDS` 和 `TRADE_KEYWORDS`
3. 添加新的建议模板

### 集成到CI/CD

```yaml
# .github/workflows/dedao-sync.yml
name: 得到课程同步
on:
  schedule:
    - cron: '0 0 * * 0'  # 每周日执行
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: 同步得到课程
        run: ./run.sh --batch-sync
```

## 故障排除

### 登录失败

```bash
# 检查登录状态
dedao-dl who

# 重新登录
dedao-dl login -c "新的cookie"
```

### 下载失败

```bash
# 清理缓存
dedao-dl clean

# 重试下载
dedao-dl dl <课程ID> -t 3 -m
```

### 同步失败

```bash
# 检查GitHub连接
git remote -v

# 手动同步
cd /path/to/vault
git add .
git commit -m "更新课程笔记"
git push
```

## 更新日志

### v1.0.0 (2026-09-06)
- 初始版本
- 支持课程下载和Markdown转换
- 支持内容分析和建议生成
- 支持Obsidian笔记同步

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
