# 业务指标映射表

设计工作流时，必须从以下 5 个业务指标中选择一个作为 `target_metric`，并在"业务价值"段落中说明该流程如何提升它。

## 指标定义

| 指标 | 英文 | 含义 | Southern Machinery 适用场景 |
|------|------|------|---------------------------|
| 线索量 | Leads | 新增潜在客户数量 | LinkedIn 抓取、展会线索入库、网站表单转化 |
| 响应效率 | Response Time | 询盘从收到到首次回复的时间 | 询盘自动分类、A 类询盘 24h 响应、自动发目录 |
| 转化率 | Conversion | 询盘到成单的转化比例 | 跟进话术生成、ROI 计算、报价方案自动化 |
| 内容产出量 | Content Output | 每周产出的营销内容数量 | 每日内容生成、EDM 序列、LinkedIn 帖子 |
| 知识复用率 | Knowledge Reuse | 知识库被检索和引用的频率 | YouTube 笔记入库、竞品情报库、产品知识卡 |

## 指标与场景匹配

| 自动化场景 | 主要指标 | 次要指标 |
|-----------|---------|---------|
| 询盘自动分类与分级 | Response Time | Conversion |
| 竞品价格监控 | Knowledge Reuse | Conversion |
| LinkedIn 线索抓取 | Leads | Response Time |
| 每日营销内容生成 | Content Output | Leads |
| YouTube 视频笔记入库 | Knowledge Reuse | Content Output |
| 报价方案自动化 | Conversion | Response Time |
| 客户跟进序列 | Conversion | Response Time |
| 展会线索入库 | Leads | Response Time |

## 业务价值段落模板

每个工作流必须包含以下格式的业务价值说明：

```markdown
## 业务价值
- **提升指标**：{指标名}（{具体改善描述}）
- **预估节省**：{每周节省 X 小时人工}
- **业务影响**：{对 Southern Machinery 线索/效率/转化的具体影响}
```

## 节省时间估算参考

| 场景 | 人工耗时 | 自动化后 | 节省 |
|------|---------|---------|------|
| 询盘分级（每条） | 10 分钟 | 1 分钟 | 9 分钟/条 |
| 竞品信息搜集（每周） | 3 小时 | 15 分钟 | 2.75 小时/周 |
| LinkedIn 搜索（每日） | 1 小时 | 10 分钟 | 50 分钟/天 |
| 内容创作（每篇） | 45 分钟 | 10 分钟 | 35 分钟/篇 |
| 视频笔记整理（每个） | 30 分钟 | 5 分钟 | 25 分钟/个 |
