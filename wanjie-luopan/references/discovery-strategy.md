# 项目发现策略

## 查询展开

把用户目标拆成四组词：

- 问题词：用户想解决的任务，例如 transcript、video editing、agent browser
- 实现词：app、tool、library、framework、skill、workflow、server、CLI
- 运行词：local、self-hosted、offline、macOS、Windows、Docker
- 生态词：替代品、awesome list、topic、模板、插件、MCP、SDK

至少组合三类查询：

1. 精确任务 + 项目形态
2. 任务同义词 + 平台/运行约束
3. 已知项目 + alternative / related / topic

## 来源优先级

1. GitHub 仓库、Release、Issues、提交记录
2. 项目官网和官方文档
3. 官方包管理器或镜像注册表
4. 作者发布页、社区讨论和真实使用案例
5. 聚合榜单、搜索摘要和社交帖子仅用于发现线索

搜索摘要不能单独证明仓库能力。发现链接后回到原始仓库核实。

## 候选池规则

- 快速模式目标为 10–20 个原始候选，最终保留 3–8 个。
- 合并同一仓库的旧名、新名、镜像和 Fork。
- 区分上游项目、二次封装、UI 外壳、托管服务和教程仓库。
- 同时保留成熟项目与少量新颖项目，避免只按 Star 排序。
- 当三次不同查询已覆盖主要项目且新增结果持续低质量时停止扩搜。

## 搜索简报模板

```text
目标：
项目形态：
必须项：
排除项：
平台/技术栈：
时间范围：
默认假设：
```
