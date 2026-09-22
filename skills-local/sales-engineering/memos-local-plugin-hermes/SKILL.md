---
name: memos-local-plugin-hermes
description: MemOS Local (Reflect2Evolve V7) 安装与配置 — 给 Hermes Agent 添加分层记忆系统（L1 Trace / L2 Policy / L3 World Model / Skill）。覆盖手动安装步骤、配置说明、验证方法。
triggers:
  - memos local install
  - memos-local-plugin hermes
  - memos local hermes
  - MemOS install
---

# MemOS Local — Hermes 安装手册

## 项目概述

**MemOS Local** (`@memtensor/memos-local-plugin`) 是一个本地优先、文件存储的记忆系统，为 AI Agent 提供四层协作记忆 + 反馈驱动自进化闭环。

- **L1 Trace**：步骤级记录（action + observation + reflection + value）
- **L2 Policy**：跨 trace 归纳的子任务策略
- **L3 World Model**：从 L2 + L1 压缩出的环境认知
- **Skill**：Agent 可直接调用的结晶化能力

**GitHub**: https://github.com/MemTensor/MemOS (18.4k stars)
**npm**: `@memtensor/memos-local-plugin@2.0.0-beta.1`

---

## 安装步骤（完整手动流程）

### Step 1: 下载 npm 包

```bash
cd /tmp && npm pack @memtensor/memos-local-plugin@2.0.0-beta.1
```

### Step 2: 解压到 Hermes 插件目录

```bash
mkdir -p ~/.hermes/memos-plugin
tar xzf /tmp/memtensor-memos-local-plugin-*.tgz \
  -C ~/.hermes/memos-plugin --strip-components=1
chmod 700 ~/.hermes/memos-plugin
```

### Step 3: 安装 npm 依赖

```bash
cd ~/.hermes/memos-plugin
npm install --omit=dev --no-fund --no-audit
# (better-sqlite3 会自动编译)
```

### Step 4: 创建运行时目录

```bash
mkdir -p ~/.hermes/memos-plugin/{data,skills,logs,daemon}
chmod 700 ~/.hermes/memos-plugin/data
```

### Step 5: 配置 config.yaml

配置文件路径：`~/.hermes/memos-plugin/config.yaml`

必须填写的字段：
```yaml
version: 1

viewer:
  port: 18799           # 与 Hermes 18800 区分

embedding:
  provider: local       # 使用 ONNX 本地向量（无需 API key）
  apiKey: ""            # 本地模式留空

llm:
  provider: openai_compatible
  apiKey: ""            # ⚠️ 必须填写你的 API key
  model: "MiniMax-M2.7-highspeed"
  baseUrl: "https://v1.aicodee.com/v1"

hub:
  enabled: false

telemetry:
  enabled: false        # 隐私优先，关闭遥测

logging:
  level: info
```

### Step 6: 配置 Hermes 主 config.yaml

在 `~/.hermes/config.yaml` 中找到 `memory` 部分：

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  provider: memtensor    # ← 原来是空字符串，已改为 memtensor
```

### Step 7: 部署 Hermes Python Adapter

```bash
# 记录 bridge 路径
echo "~/.hermes/memos-plugin/bridge.cts" \
  > ~/.hermes/memos-plugin/adapters/hermes/bridge_path.txt

# Symlink provider
ln -sf ~/.hermes/memos-plugin/adapters/hermes/memos_provider \
       ~/.hermes/hermes-agent/plugins/memory/memtensor

# 复制 plugin.yaml
cp ~/.hermes/memos-plugin/adapters/hermes/plugin.yaml \
   ~/.hermes/hermes-agent/plugins/memory/memtensor/plugin.yaml
```

### Step 8: 验证安装

```bash
# 验证 Hermes 内存 provider
cd ~/.hermes/hermes-agent && python3 -c "
from plugins.memory import load_memory_provider, discover_memory_providers
available = discover_memory_providers()
print('Available providers:')
for name, desc, avail in available:
    print(f'  {name}: {\"✅\" if avail else \"❌\"} - {desc[:50]}')
p = load_memory_provider('memtensor')
print(f'Memtensor: {\"✅ loaded\" if p else \"❌ failed\"}')"
```

预期输出：
```
Available providers:
  memtensor: ✅ - MemOS Local — Reflect2Evolve V7...
Memtensor: ✅ loaded
```

---

## 架构说明

```
Hermes Agent (Python)
    ↕ JSON-RPC over stdio (bridge.cts)
MemOS Core (Node.js)
    ↕
SQLite DB (L1/L2/L3/Skill/Episode/Feedback)
Memory Viewer (HTTP :18799)
```

- **数据位置**：`~/.hermes/memos-plugin/data/memos.db`
- **日志位置**：`~/.hermes/memos-plugin/logs/`
- **Bridge 路径**：`~/.hermes/memos-plugin/bridge.cts`

---

## 重要配置说明

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `viewer.port` | 18799 | Memory Viewer HTTP 端口 |
| `embedding.provider` | local | 使用 ONNX 本地嵌入（无需 API） |
| `llm.apiKey` | **必须填写** | OpenAI-compatible API Key |
| `llm.model` | (blank) | 模型名称 |
| `telemetry.enabled` | true | 建议改为 false 保护隐私 |

---

## 已知问题

### LLM API Key 未填写
`llm.apiKey` 为空会导致 MemOS 无法执行：
- L2 策略归纳（cross-task policy induction）
- L3 世界模型抽象
- Skill 结晶化（Crystallization）

**解决方法**：编辑 `~/.hermes/memos-plugin/config.yaml`，填写有效的 OpenAI-compatible API key。

---

## 更新 MemOS

```bash
cd /tmp
npm pack @memtensor/memos-local-plugin@latest
tar xzf memtensor-memos-local-plugin-*.tgz \
  -C ~/.hermes/memos-plugin --strip-components=1
# 注意：data/、skills/、logs/ 不会被覆盖
```

---

## Southern Machinery 使用价值

**核心价值**：让 Hermes Agent 拥有"自我反思 + 跨任务学习"能力，成为真正的销售工程师助理。

### 具体场景：
1. **SMT 整线方案学习**：L2 层归纳每次 ROI 计算的成功模式，形成最佳实践
2. **客户记忆**：L1 层记录每次与客户沟通的内容，自动追踪需求变化
3. **竞品情报沉淀**：L3 层构建竞争对手知识库，Agent 可随时检索
4. **Skill 自动化**：高价值操作模式结晶为可复用 Skill，一键执行复杂任务
5. **反馈闭环**：客户的每次确认/拒绝都是 Reward Signal，驱动策略优化
