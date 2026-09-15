# 🔔 飞书通知集成指南

本指南将帮助你配置飞书通知，当有高优先级询盘时自动推送消息。

---

## 📋 功能说明

- 🔴 **高优先级询盘** - 实时推送到飞书群
- 📊 **日报汇总** - 每天定时发送询盘统计
- 👥 **@指定成员** - 可自动@销售人员

---

## 步骤 1：创建飞书机器人

### 1.1 打开飞书群

1. 打开飞书客户端
2. 进入要接收通知的群聊（或创建新群）

### 1.2 添加自定义机器人

1. 点击右上角的 **"..."** 或 **"设置"**
2. 选择 **"添加机器人"**
3. 点击 **"自定义机器人"**
4. 点击 **"添加"**

### 1.3 配置机器人

| 配置项 | 建议设置 |
|--------|----------|
| **机器人名称** | 询盘助手 |
| **机器人头像** | （可选） |
| **Webhook 地址** | 自动生成（复制保存） |

### 1.4 安全设置（推荐）

选择 **"自定义关键词"**，添加关键词：

```
询盘
高优先级
外贸
```

> ⚠️ 重要：消息中必须包含关键词，否则发送会失败。

### 1.5 保存 Webhook URL

复制 Webhook 地址，格式类似：

```
https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## 步骤 2：配置环境变量

### Windows (PowerShell)

**临时设置（当前会话）：**

```powershell
$env:FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

**永久设置：**

1. 右键"此电脑" → "属性"
2. "高级系统设置" → "环境变量"
3. 在"用户变量"中点击"新建"
4. 变量名：`FEISHU_WEBHOOK_URL`
5. 变量值：你的 Webhook URL
6. 点击"确定"

### Linux / macOS

**临时设置：**

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

**永久设置：**

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"' >> ~/.bashrc
source ~/.bashrc
```

---

## 步骤 3：测试通知

### 3.1 运行测试脚本

```bash
python scripts/test_feishu.py
```

### 3.2 检查飞书群

应该收到测试消息：

```
🔔 询盘通知测试

这是一条测试消息，确认飞书集成正常工作。

测试时间：2026-03-31 18:00
```

---

## 步骤 4：运行带通知的分类器

### 方式 1：使用通知版本

```bash
python gmail_sorter_notify.py
```

### 方式 2：设置命令行参数

```bash
python gmail_sorter.py --notify-feishu
```

---

## 📝 通知消息格式

### 高优先级询盘通知

```
🔥 新的高优先级询盘！

📧 发件人：john@abctrading.com
📝 主题：RFQ - 5000 units of LED Strip Lights
⚡ 优先级：HIGH

💬 摘要：
客户明确需要 5000 条 LED 灯带，目标价$2.50...

---
请及时跟进回复！
```

### 日报汇总通知

```
📊 外贸询盘日报 - 2026-03-31

📈 今日统计
• 总邮件：45 封
• 询盘邮件：8 封 ⭐
  - 高优先级：3
  - 中优先级：3
  - 低优先级：2

🔥 待处理高优询盘：3 封
请尽快跟进！
```

---

## ⚙️ 高级配置

### 配置@指定成员

编辑 `gmail_sorter_notify.py`，添加：

```python
# 要@的用户 ID（飞书用户 ID）
MENTION_USERS = ["ou_xxxxxxxx", "ou_yyyyyyyy"]
```

### 配置发送时间

```python
# 日报发送时间（24 小时制）
DAILY_REPORT_TIME = "18:00"
```

### 配置通知阈值

```python
# 只通知 HIGH 优先级
NOTIFY_PRIORITY_THRESHOLD = "HIGH"

# 或通知 HIGH + MEDIUM
NOTIFY_PRIORITY_THRESHOLD = ["HIGH", "MEDIUM"]
```

---

## 🔧 其他平台集成

### 钉钉

1. 群设置 → 智能群助手 → 添加机器人
2. 选择"自定义"
3. 获取 Webhook URL
4. 设置环境变量：`DINGTALK_WEBHOOK_URL`

### 企业微信

1. 群聊 → 右上角"..." → 添加群机器人
2. 新建机器人
3. 获取 Webhook URL
4. 设置环境变量：`WECOM_WEBHOOK_URL`

---

## ❓ 常见问题

### Q1: 消息发送失败

**A:** 检查：
- Webhook URL 是否正确
- 是否设置了关键词（需要在消息中包含）
- 网络连接是否正常

### Q2: 没有收到通知

**A:** 检查：
- 环境变量是否设置成功
- 是否有高优先级询盘
- 查看脚本输出日志

### Q3: 如何关闭通知？

**A:** 不设置环境变量即可，或运行：

```bash
python gmail_sorter.py --no-notify
```

---

## 📞 需要帮助？

提交 Issue：https://github.com/your-username/foreign-trade-email-sorter/issues

---

**配置完成！返回 [README.md](./README.md) 查看完整用法。**
