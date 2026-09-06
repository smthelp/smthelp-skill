# 使用指南

## 快速开始

### 列出可用课程

```bash
./run.sh --list
```

### 下载单个课程

```bash
./run.sh --download <课程ID>
```

### 分析课程

```bash
./run.sh --analyze "output/课程名/MD"
```

### 生成建议

```bash
./run.sh --generate --industry "SMT设备外贸"
```

### 同步到Obsidian

```bash
./run.sh --sync
```

## 批量操作

### 批量下载所有课程

```bash
./run.sh --batch-download
```

### 批量分析所有课程

```bash
./run.sh --batch-analyze
```

### 批量同步所有课程

```bash
./run.sh --batch-sync
```

## 高级用法

### 自定义行业模板

1. 编辑 `config/config.json`
2. 在 `advice_templates` 中添加新的行业模板
3. 运行 `./run.sh --industry "新行业" --generate`

### 自定义建议内容

1. 编辑 `scripts/analyze.py`
2. 修改 `SMTAdviceGenerator` 类
3. 添加新的建议模板

### 集成到CI/CD

在GitHub Actions中添加以下工作流：

```yaml
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

## 输出文件说明

### 课程目录结构

```
output/
├── 课程名/
│   ├── MD/
│   │   ├── 01 章节1.md
│   │   ├── 02 章节2.md
│   │   ├── ...
│   │   └── 00-SMT外贸营销建议.md
│   └── ...
└── ...
```

### Obsidian目录结构

```
得到课程/
├── 课程名/
│   ├── 01 章节1.md
│   ├── 02 章节2.md
│   ├── ...
│   └── 00-SMT外贸营销建议.md
└── ...
```

## 常见问题

### Q: 如何获取得到的cookie？

A: 
1. 在浏览器中打开 https://www.dedao.cn
2. 登录你的账号
3. 按F12打开开发者工具
4. 切换到"Application"标签
5. 找到Cookies -> https://www.dedao.cn
6. 复制所有cookie值

### Q: 如何更新得到课程？

A: 
1. 运行 `./run.sh --batch-download` 下载新课程
2. 运行 `./run.sh --batch-analyze` 分析新课程
3. 运行 `./run.sh --batch-sync` 同步到Obsidian

### Q: 如何添加新的行业模板？

A: 
1. 编辑 `config/config.json`
2. 在 `advice_templates` 中添加新的行业模板
3. 参考现有的SMT设备外贸模板格式

### Q: 如何自定义建议内容？

A: 
1. 编辑 `scripts/analyze.py`
2. 修改 `SMTAdviceGenerator` 类
3. 添加新的建议模板

### Q: 如何集成到CI/CD？

A: 
1. 在GitHub仓库中创建 `.github/workflows/dedao-sync.yml`
2. 添加定时触发器
3. 运行 `./run.sh --batch-sync`
