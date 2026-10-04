# 📧 外贸邮件自动分类器 (Foreign Trade Email Sorter)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gmail API](https://img.shields.io/badge/Gmail-API-red.svg)](https://developers.google.com/gmail/api)

**自动识别 Gmail 中的外贸询盘邮件，智能分级并生成每日报告**

---

## 🌟 功能特性

- ✉️ **自动读取 Gmail 邮件** - 通过 Gmail API 安全读取
- 🤖 **AI 智能分类** - 自动识别询盘/营销/垃圾邮件
- 📊 **优先级分级** - HIGH/MEDIUM/LOW 三级分类
- 📝 **日报自动生成** - 结构化询盘报告，支持中文
- 🔔 **飞书通知** - 高优先级询盘实时推送（可选）
- 🔒 **安全可靠** - OAuth 2.0 授权，只读权限

---

## 📋 快速开始

### 前置要求

1. **Python 3.8+** 运行环境
2. **Gmail 账号**（支持 G Suite）
3. **Google Cloud 项目**（免费）

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Gmail API

详见 **[GMAIL_SETUP.md](./GMAIL_SETUP.md)**

### 3. 运行分类

```bash
# 测试运行（处理最近 10 封邮件）
python gmail_sorter.py --max 10

# 正式运行（处理最近 50 封）
python gmail_sorter.py --max 50

# 生成中文报告
python gmail_sorter_cn.py

# 仅查看，不生成报告
python gmail_sorter.py --max 20 --no-report
```

---

## 📂 项目结构

```
foreign-trade-email-sorter/
├── README.md                 # 本文件
├── GMAIL_SETUP.md           # Gmail API 配置指南
├── FEISHU_SETUP.md          # 飞书集成指南
├── requirements.txt         # Python 依赖
├── gmail_sorter.py          # 主程序（英文版）
├── gmail_sorter_cn.py       # 主程序（中文版）
├── check_inquiries.py       # 快速检查脚本
├── credentials.json         # [需自行配置] OAuth 凭证
├── token.json               # [自动生成] 访问令牌
├── reports/                 # 报告输出目录
│   └── inquiry-report-YYYY-MM-DD.txt
└── scripts/                 # 辅助脚本
    ├── gmail_auth.py        # 独立授权工具
    └── test_gmail.py        # 连接测试工具
```

---

## 📊 报告示例

```
📊 外贸询盘日报 - 2026-03-31
============================================================

📈 今日统计
  总邮件数：45 封
  ✉️ 询盘邮件：8 封 ⭐
    - 🔴 高优先级：3
    - 🟡 中优先级：3
    - 🟢 低优先级：2
  📢 营销邮件：28 封
  🗑️ 垃圾邮件：9 封

============================================================

🔴 高优先级询盘 (3)
============================================================

【询盘 #1】
----------------------------------------
邮箱：john@abctrading.com
主题：RFQ - 5000 units of LED Strip Lights
优先级：🔴 HIGH

摘要：客户明确需要 5000 条 LED 灯带，目标价$2.50，要求 30 天交期...

============================================================
📝 待回复清单
============================================================

1. john@abctrading.com - LED Strip Lights (HIGH)
2. maria@euroimport.es - Bluetooth Speakers (HIGH)
3. ...
```

---

## 🤖 邮件分类规则

### 询盘邮件 (Inquiry)
识别关键词：
- `quote`, `quotation`, `price`, `inquiry`, `RFQ`
- `order`, `purchase`, `buy`, `MOQ`
- `sample`, `catalog`, `lead time`, `payment terms`

### 营销邮件 (Marketing)
- 新闻订阅、促销信息
- 平台通知（Alibaba、Made-in-China）
- 展会邀请

### 垃圾邮件 (Spam)
- 钓鱼邮件、中奖通知
- 无关推销

---

## 🔔 飞书集成（可选）

详见 **[FEISHU_SETUP.md](./FEISHU_SETUP.md)**

### 快速配置

1. 在飞书群创建 Webhook 机器人
2. 获取 Webhook URL
3. 设置环境变量：

```bash
# Windows PowerShell
$env:FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# Linux/Mac
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

4. 运行带通知的版本：

```bash
python gmail_sorter_notify.py
```

---

## ⚙️ 高级配置

### 自定义分类关键词

编辑 `gmail_sorter.py` 中的关键词列表：

```python
INQUIRY_KEYWORDS = [
    'quote', 'quotation', 'price',  # 添加你的行业关键词
    'your_keyword_here'
]
```

### 调整优先级规则

```python
def get_priority(subject, body):
    text = (subject + " " + body).lower()
    # 自定义 HIGH 优先级判断
    if 'urgent' in text or 'asap' in text:
        return 'HIGH'
    # ...
```

### 定时运行

**Windows 任务计划程序：**

```powershell
# 创建每天 9:00 运行的任务
schtasks /create /tn "GmailSorter" /tr "python C:\path\to\gmail_sorter.py" /sc daily /st 09:00
```

**Linux Cron：**

```bash
# 编辑 crontab
crontab -e

# 添加每天 9:00 运行
0 9 * * * cd /path/to/foreign-trade-email-sorter && python gmail_sorter.py
```

---

## 🔒 安全说明

### 权限范围

本应用仅请求 **只读权限** (`gmail.readonly`)：
- ✅ 读取邮件内容和元数据
- ❌ 不能发送邮件
- ❌ 不能删除邮件
- ❌ 不能修改邮件

### 凭证安全

- `credentials.json` - 你的 OAuth 客户端凭证，**不要上传到 GitHub**
- `token.json` - 访问令牌，**不要分享给他人**

这两个文件已添加到 `.gitignore`，但仍需注意：

```bash
# 检查是否意外提交
git ls-files | grep -E "(credentials|token)\.json"
```

### 数据隐私

所有邮件处理都在**本地完成**，不会上传到任何第三方服务器（除 Gmail API 和可选的飞书通知）。

---

## 🛠️ 故障排查

### 问题 1: "credentials.json not found"

**解决方案：**
1. 按照 [GMAIL_SETUP.md](./GMAIL_SETUP.md) 创建 Google Cloud 项目
2. 下载 `credentials.json` 并放到项目根目录

### 问题 2: "Token expired"

**解决方案：**
```bash
# 删除过期 token，重新授权
rm token.json
python gmail_sorter.py
```

### 问题 3: "SSL 连接错误"

**解决方案：**
- 检查网络连接
- 如使用代理，设置环境变量：
  ```bash
  $env:HTTPS_PROXY="http://127.0.0.1:7890"  # Windows
  export HTTPS_PROXY="http://127.0.0.1:7890"  # Linux/Mac
  ```

### 问题 4: 分类不准确

**解决方案：**
1. 编辑 `INQUIRY_KEYWORDS` 添加行业特定词汇
2. 调整 `get_priority()` 函数逻辑
3. 提交 Issue 反馈误判案例

---

## 📝 常见问题

**Q: 支持中文邮件吗？**

A: 支持！使用 `gmail_sorter_cn.py` 可生成中文报告，分类逻辑同样支持中文关键词。

**Q: 可以处理已读邮件吗？**

A: 默认处理最近 3 天的所有邮件（包括已读）。可修改查询条件：

```python
# 仅未读邮件
query = 'is:unread'

# 最近 7 天
query = 'after:2026/03/24'
```

**Q: 如何批量处理历史邮件？**

A: 修改日期范围：

```bash
# 处理最近 30 天
python gmail_sorter.py --max 500
```

然后编辑脚本中的日期查询逻辑。

**Q: 飞书通知支持其他平台吗？**

A: 目前支持飞书。钉钉/企业微信集成见 [FEISHU_SETUP.md](./FEISHU_SETUP.md) 的"其他平台"章节。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

---

## 🙏 致谢

- [Gmail API](https://developers.google.com/gmail/api)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [飞书开放平台](https://open.feishu.cn/)

---

## 📬 联系方式

- 📧 Email: your-email@example.com
- 💬 Issues: [GitHub Issues](https://github.com/your-username/foreign-trade-email-sorter/issues)

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**
