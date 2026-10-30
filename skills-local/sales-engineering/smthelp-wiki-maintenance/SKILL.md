---
name: smthelp-wiki-maintenance
description: Southern Machinery LLM Wiki 维护与扩展工作流 — 基于 Karpathy LLM Wiki 模式
created: 2026-04-24
updated: 2026-04-24
---

# Southern Machinery LLM Wiki 维护与扩展

## Wiki 根目录
`~/wiki/`

## 目录结构

```
wiki/
├── entities/
│   ├── machines/
│   │   ├── tht-inserters/      # THT插入机（按型号分）
│   │   ├── wave-solder/         # 波峰焊
│   │   ├── cleaning/            # 清洗设备
│   │   ├── board-handling/      # 收板机/AGV
│   │   └── smt-peripherals/     # SMT周边设备
│   └── concepts/                # 技术/商业概念
├── comparisons/                 # 竞品对比
├── concepts/                    # 技术基础概念（smt/tht/wave-soldering）
├── queries/                     # 查询指南
├── raw/articles/               # 原始采集数据
├── _archive/                   # 过期归档
├── index.md                    # 完整索引
├── SCHEMA.md                   # 规范文档
└── log.md                      # 操作日志
```

## 页面规范（每次必须遵守）

### Frontmatter 必填字段
```yaml
---
title: [页面标题]
created: 2026-04-24
updated: 2026-04-24
type: entity | concept | comparison
tags: [tht-inserter, wave-solder, ...]
sources: [smthelp.com, youtube/c/Smthelping]
summary: [2-3句话中文摘要]
---
```

### Wikilinks 规则
- 每个页面**至少 2 个** `[[wikilink]]` 到其他页面
- 链接不存在的页面会创建占位页

### 文件命名
- 小写 + 连字符，无空格
- 例：`s-70ld-odd-form-inserter.md`

### 更新要求
1. 新增页面 → 同步更新 `index.md`
2. 所有操作 → 记录到 `log.md`

## 扩展检查清单

### 1. 新增 Entity 页
- [ ] 产品规格（速度/精度/产能）全部引用 `smthelp.com` 或 YouTube 来源
- [ ] 至少 2 个 `[[wikilink]]`
- [ ] Frontmatter 含 `sources`
- [ ] 在 `index.md` 添加表格行
- [ ] 在 `log.md` 记录

### 2. 新增 Comparison 页
- [ ] 包含对比表格（Markdown 格式）
- [ ] 包含"典型场景"推荐
- [ ] 销售话术（FABE 格式）
- [ ] 至少 3 个 `[[wikilink]]`
- [ ] 在 `index.md` 添加条目

### 3. 新增 Concept 页
- [ ] 定义（中文）
- [ ] 技术原理或商业逻辑
- [ ] 关联 Southern Machinery 产品（具体型号）
- [ ] 销售话术或应用场景
- [ ] 至少 2 个 `[[wikilink]]`
- [ ] 在 `index.md` 添加条目

### 4. 新增 Raw Article
- [ ] 存放原始采集内容（网页复制/AI总结）
- [ ] 标注来源 URL 和采集时间
- [ ] 不加 frontmatter（原始数据）

## 核心产品清单（已有页面）

| 型号 | 类型 | 状态 |
|------|------|------|
| S-7900 | 异形旗舰 | ✅ 完整 |
| S-7020T | 端子插入 | ✅ 完整 |
| S-70LD | 异形性价比 | ✅ 完整 |
| S-4000 | 轴向高速 | ✅ 完整 |
| S-3000 | 径向高可靠 | ✅ 完整 |
| S-WS450 | 波峰焊 | ✅ 完整 |
| SME-5500 | 清洗机 | ✅ 完整 |
| SUL460 | 收板机 | ✅ 完整 |
| SFY03 | AGV | ✅ 完整 |
| SIS-7000A | 料盘架 | ✅ 完整 |

## 缺失页面（待扩展）

- Reflow Oven（回流焊机）实体页
- AOI 自动光学检测实体页
- SMT 贴片机对比页
- 客户案例研究页
- `raw/articles/` 原始采集数据

## 常用查询路径

| 需求 | 查询关键词 | 页面 |
|------|----------|------|
| 产品规格 | s-70ld, s-4000, s-ws450 | entities/machines/tht-inserters/ |
| 技术原理 | active-clinching, wave-soldering | entities/concepts/ |
| 竞品对比 | sm vs japanese, sm vs ersa | comparisons/ |
| ROI算账 | capex-vs-roi | entities/concepts/ |
| 选型指南 | tht-inserter-comparison | comparisons/ |

## 查询示例（执行方法）

用 `search_files` 搜索 wiki 内容：
```python
search_files(path="~/wiki", pattern="S-70LD")
search_files(path="~/wiki", pattern="Active Clinching")
search_files(path="~/wiki/concepts", pattern="IPC.*Class")
```
