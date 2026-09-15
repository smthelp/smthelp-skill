# 🚀 快速开始指南

**5 分钟完成配置，开始自动分类询盘！**

---

## 第一步：安装依赖（1 分钟）

```bash
pip install -r requirements.txt
```

---

## 第二步：配置 Gmail API（3 分钟）

### 2.1 创建 Google Cloud 项目

1. 访问：https://console.cloud.google.com/
2. 点击 "NEW PROJECT"
3. 输入项目名称：`Email Sorter`
4. 点击 "CREATE"

### 2.2 启用 Gmail API

1. 菜单 → "APIs & Services" → "Library"
2. 搜索 "Gmail API"
3. 点击 "ENABLE"

### 2.3 创建 OAuth 凭据

1. 菜单 → "APIs & Services" → "Credentials"
2. "+ CREATE CREDENTIALS" → "OAuth client ID"
3. 首次使用会提示配置同意屏幕：
   - 选择 "External"
   - 填写应用名称和邮箱
   - 添加你的邮箱为测试用户
4. 创建 OAuth 客户端：
   - Application type: **Desktop app**
   - Name: **Email Sorter**
5. 下载 `credentials.json`

### 2.4 放置文件

将 `credentials.json` 放到项目根目录

---

## 第三步：运行测试（1 分钟）

```bash
python gmail_sorter.py --max 5
```

首次运行会打开浏览器授权，点击 "Allow" 即可。

---

## ✅ 完成！

现在可以正常使用：

```bash
# 查看最近 20 封邮件
python gmail_sorter.py --max 20

# 生成中文报告
python gmail_sorter_cn.py
```

---

## （可选）配置飞书通知

详见：[FEISHU_SETUP.md](./FEISHU_SETUP.md)

---

## 需要帮助？

- Gmail 配置问题：[GMAIL_SETUP.md](./GMAIL_SETUP.md)
- 提交 Issue：https://github.com/your-username/foreign-trade-email-sorter/issues
