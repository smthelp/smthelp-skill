# 安装指南

## 系统要求

- Linux (Ubuntu 18.04+, CentOS 7+)
- Bash 4.0+
- Python 3.6+
- curl
- git

## 安装步骤

### 1. 克隆Skill仓库

```bash
git clone https://github.com/username/dedao-skill.git
cd dedao-skill
```

### 2. 运行安装脚本

```bash
chmod +x install.sh
./install.sh
```

### 3. 配置得到账号

#### 方法一：使用Cookie登录

1. 在浏览器中打开 https://www.dedao.cn
2. 登录你的得到账号
3. 按F12打开开发者工具
4. 切换到"Application"（应用程序）标签
5. 在左侧找到"Cookies" -> "https://www.dedao.cn"
6. 复制所有cookie值
7. 运行以下命令：

```bash
dedao-dl login -c "你的cookie字符串"
```

#### 方法二：使用扫码登录

```bash
dedao-dl login -q
```

然后使用得到APP扫描终端中的二维码。

### 4. 配置Skill

编辑 `config/config.json` 文件：

```json
{
  "cookie": "你的cookie",
  "output_dir": "./output",
  "vault_dir": "~/obsidian-vault",
  "github_repo": "https://github.com/username/repo.git",
  "industry": "SMT设备外贸",
  "business_context": "Southern Machinery SMT机器设备外贸营销",
  "auto_sync": true,
  "generate_advice": true
}
```

### 5. 验证安装

```bash
# 检查dedao-dl是否安装
dedao-dl --help

# 检查登录状态
dedao-dl who

# 运行Skill
./run.sh --help
```

## 故障排除

### dedao-dl安装失败

如果自动安装失败，可以手动安装：

```bash
# 下载最新版本
curl -sL https://github.com/yann0917/dedao-dl/releases/download/v1.2.32/dedao-dl-linux-amd64.tar.gz | tar -xz

# 移动到系统路径
chmod +x dedao-dl-linux-amd64
sudo mv dedao-dl-linux-amd64 /usr/local/bin/dedao-dl
```

### 登录失败

如果登录失败，可能是cookie已过期。请重新获取cookie并登录：

```bash
dedao-dl login -c "新的cookie字符串"
```

### 权限问题

如果遇到权限问题，请确保脚本有执行权限：

```bash
chmod +x run.sh
chmod +x scripts/*.sh
chmod +x scripts/*.py
```
