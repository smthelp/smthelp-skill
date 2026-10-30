# 📧 Gmail API 配置指南

本指南将帮助你配置 Gmail API，使邮件分类器能够读取你的 Gmail 邮件。

---

## 📋 前置准备

- 一个 Google 账号（Gmail 或 G Suite）
- 10-15 分钟时间
- 稳定的网络连接

---

## 步骤 1：创建 Google Cloud 项目

### 1.1 访问 Google Cloud Console

打开浏览器，访问：https://console.cloud.google.com/

### 1.2 创建新项目

1. 点击顶部的项目选择器（显示 "Select a project"）
2. 在弹出的窗口中，点击右上角的 **"NEW PROJECT"**
3. 输入项目名称，例如：`Foreign Trade Email Sorter`
4. 点击 **"CREATE"**

> 💡 提示：项目创建可能需要 30 秒，完成后会自动选中。

---

## 步骤 2：启用 Gmail API

### 2.1 打开 API 库

1. 点击左上角的菜单按钮（☰）
2. 选择 **"APIs & Services"** → **"Library"**

### 2.2 搜索并启用 Gmail API

1. 在搜索框中输入：`Gmail API`
2. 点击搜索结果中的 **"Gmail API"**
3. 点击 **"ENABLE"** 按钮

> ✅ 启用成功后会显示绿色对勾。

---

## 步骤 3：配置 OAuth 同意屏幕

### 3.1 进入同意屏幕配置

1. 点击左侧菜单 **"APIs & Services"** → **"OAuth consent screen"**
2. 选择 **"External"**（外部用户）
3. 点击 **"CREATE"**

### 3.2 填写应用信息

| 字段 | 填写内容 |
|------|----------|
| **App name** | Foreign Trade Email Sorter |
| **User support email** | 你的邮箱地址 |
| **App logo** | （可选） |
| **Application home page** | （可选） |
| **Authorized domains** | （留空） |
| **Developer contact** | 你的邮箱地址 |

### 3.3 添加测试用户

1. 点击 **"SAVE AND CONTINUE"**
2. 点击 **"ADD USERS"**
3. 输入你的 Gmail 地址
4. 点击 **"ADD"**
5. 点击 **"SAVE AND CONTINUE"**

> ⚠️ 重要：在应用通过 Google 审核前，只有测试用户才能使用。

---

## 步骤 4：创建 OAuth 2.0 凭据

### 4.1 进入凭据页面

1. 点击左侧菜单 **"APIs & Services"** → **"Credentials"**
2. 点击顶部的 **"+ CREATE CREDENTIALS"**
3. 选择 **"OAuth client ID"**

### 4.2 配置客户端

| 字段 | 选择/填写 |
|------|----------|
| **Application type** | Desktop app |
| **Name** | Email Sorter Client |

### 4.3 下载凭据

1. 点击 **"CREATE"**
2. 在弹出的窗口中，点击 **"DOWNLOAD JSON"**
3. 将下载的文件重命名为：`credentials.json`

---

## 步骤 5：放置凭据文件

将下载的 `credentials.json` 文件移动到项目根目录：

```
foreign-trade-email-sorter/
├── credentials.json    ← 放这里
├── gmail_sorter.py
└── ...
```

---

## 步骤 6：首次授权运行

### 6.1 安装依赖（如果还没安装）

```bash
pip install -r requirements.txt
```

### 6.2 运行授权

```bash
python gmail_sorter.py --max 5
```

### 6.3 完成授权

1. 脚本会自动打开浏览器
2. 登录你的 Gmail 账号
3. 看到 **"This app isn't verified"** 警告时：
   - 点击 **"Advanced"**（高级）
   - 点击 **"Go to Foreign Trade Email Sorter (unsafe)"**
4. 点击 **"Allow"** 授权
5. 授权成功后，浏览器会显示 "Authentication successful"

### 6.4 验证

授权成功后，项目根目录会生成 `token.json` 文件：

```
foreign-trade-email-sorter/
├── credentials.json    ← 你下载的
├── token.json          ← 自动生成的
└── ...
```

> ✅ 现在可以正常运行邮件分类了！

---

## 🔍 验证配置

运行测试命令：

```bash
python gmail_sorter.py --max 5
```

成功输出示例：

```
============================================================
Foreign Trade Email Sorter
============================================================

Connected to: your-email@gmail.com

Fetching up to 5 unread emails...
Found 5 unread emails. Processing...

Report saved to: reports/inquiry-report-2026-03-31.txt

Done!
```

---

## ❓ 常见问题

### Q1: "credentials.json not found"

**A:** 确保文件在项目根目录，文件名完全正确（区分大小写）。

### Q2: "This app isn't verified"

**A:** 这是正常的。点击 "Advanced" → "Go to ... (unsafe)" 继续。

### Q3: Token 过期了怎么办？

**A:** 删除 `token.json`，重新运行脚本会自动刷新。

```bash
rm token.json
python gmail_sorter.py
```

### Q4: 权限被拒绝

**A:** 访问 https://myaccount.google.com/permissions，移除本应用授权，重新运行脚本。

### Q5: SSL 连接错误

**A:** 网络问题，检查网络连接或代理设置。

---

## 🔒 安全提醒

1. **不要分享** `credentials.json` 和 `token.json`
2. 这两个文件已添加到 `.gitignore`，但仍需注意
3. 本应用只请求**只读权限**，不会修改或删除邮件

---

## 📞 需要帮助？

如遇到问题，请提交 Issue：https://github.com/your-username/foreign-trade-email-sorter/issues

---

**配置完成！继续查看 [README.md](./README.md) 了解使用方法。**
