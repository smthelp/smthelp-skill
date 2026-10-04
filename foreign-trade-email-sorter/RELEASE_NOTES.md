# 📦 foreign-trade-email-sorter v1.0.0

**外贸邮件自动分类器 - Gmail 询盘智能识别与分级**

---

## 🎯 项目简介

这是一个专为外贸从业者设计的 Gmail 邮件自动分类工具，能够：

- ✉️ 自动读取 Gmail 邮件
- 🤖 智能识别询盘/营销/垃圾邮件
- 📊 按优先级分级（HIGH/MEDIUM/LOW）
- 📝 生成结构化日报
- 🔔 飞书实时通知（可选）

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Gmail API

详见 **[GMAIL_SETUP.md](./GMAIL_SETUP.md)**

简要步骤：
1. 创建 Google Cloud 项目
2. 启用 Gmail API
3. 下载 credentials.json
4. 首次运行自动授权

### 3. 运行

```bash
# 测试运行
python gmail_sorter.py --max 5

# 中文报告
python gmail_sorter_cn.py

# 带飞书通知
python gmail_sorter_notify.py
```

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `README.md` | 完整项目文档 |
| `QUICKSTART.md` | 5 分钟快速开始 |
| `GMAIL_SETUP.md` | Gmail API 配置指南 |
| `FEISHU_SETUP.md` | 飞书集成指南 |
| `gmail_sorter.py` | 主程序（英文报告） |
| `gmail_sorter_cn.py` | 主程序（中文报告） |
| `gmail_sorter_notify.py` | 带飞书通知版本 |
| `requirements.txt` | Python 依赖 |

---

## ⚠️ 重要提示

### 需要自行配置的文件

以下文件**不包含**在压缩包中，需要用户自行创建：

1. **credentials.json** - Google Cloud OAuth 凭据
   - 按照 GMAIL_SETUP.md 创建
   - 每个用户需要自己的凭据

2. **token.json** - 访问令牌
   - 首次运行时自动生成
   - 不要分享给他人

3. **环境变量**（可选）
   - `FEISHU_WEBHOOK_URL` - 飞书通知 Webhook

### 敏感信息

本项目已移除所有个人敏感信息：
- ❌ credentials.json（OAuth 凭据）
- ❌ token.json（访问令牌）
- ❌ 个人邮箱地址
- ❌ 历史报告文件

---

## 📖 完整文档

- **快速开始**: [QUICKSTART.md](./QUICKSTART.md)
- **完整文档**: [README.md](./README.md)
- **Gmail 配置**: [GMAIL_SETUP.md](./GMAIL_SETUP.md)
- **飞书集成**: [FEISHU_SETUP.md](./FEISHU_SETUP.md)
- **发布清单**: [PUBLISH_CHECKLIST.md](./PUBLISH_CHECKLIST.md)

---

## 🛠️ 技术栈

- Python 3.8+
- Gmail API
- Google OAuth 2.0
- 飞书开放平台（可选）

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 🙏 致谢

感谢使用本项目！如有问题请提交 Issue。

**GitHub**: https://github.com/YOUR_USERNAME/foreign-trade-email-sorter

---

*最后更新：2026-03-31*
