---
name: obsidian-ai-knowledge-deploy
description: Use when deploying or validating the Obsidian AI knowledge base customer package.
---

# Obsidian AI 知识库部署总控

## 任务

指导 Agent 完成 Skill 安装、MCP 配置、插件安装、Vault 初始化和自检。

## 步骤

1. 读取 `README_先读我.md`。
2. 检查 `01_可用Skill源码`、`02_MCP源码与安装`、`03_Obsidian插件安装说明`。
3. 初始化 `04_Obsidian知识库模板`。
4. 运行 `06_客户Agent自检/run_customer_harness.py`。

## 安全边界

只在测试 Vault 上运行，MCP 写入/删除/同步动作必须等用户确认。
