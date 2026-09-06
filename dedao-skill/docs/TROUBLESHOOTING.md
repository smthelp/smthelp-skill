# 故障排除

## 常见问题

### 1. dedao-dl安装失败

**症状**：运行 `dedao-dl --help` 提示命令未找到

**解决方案**：
```bash
# 手动下载并安装
curl -sL https://github.com/yann0917/dedao-dl/releases/download/v1.2.32/dedao-dl-linux-amd64.tar.gz | tar -xz
chmod +x dedao-dl-linux-amd64
sudo mv dedao-dl-linux-amd64 /usr/local/bin/dedao-dl

# 验证安装
dedao-dl --help
```

### 2. 登录失败

**症状**：运行 `dedao-dl who` 提示未登录

**解决方案**：
```bash
# 重新登录
dedao-dl login -c "你的cookie字符串"

# 验证登录状态
dedao-dl who
```

### 3. Cookie过期

**症状**：下载课程时提示需要登录

**解决方案**：
1. 在浏览器中重新登录得到
2. 获取新的cookie
3. 重新登录：
```bash
dedao-dl login -c "新的cookie字符串"
```

### 4. 下载失败

**症状**：下载课程时出现错误

**解决方案**：
```bash
# 清理缓存
dedao-dl clean

# 重试下载
dedao-dl dl <课程ID> -t 3 -m
```

### 5. 同步失败

**症状**：推送到GitHub时出现错误

**解决方案**：
```bash
# 检查GitHub连接
git remote -v

# 手动同步
cd /path/to/vault
git add .
git commit -m "更新课程笔记"
git push
```

### 6. 分析失败

**症状**：运行分析脚本时出现错误

**解决方案**：
```bash
# 检查Python版本
python3 --version

# 检查文件权限
chmod +x scripts/analyze.py

# 手动运行分析
python3 scripts/analyze.py "output/课程名/MD"
```

### 7. 配置文件错误

**症状**：运行脚本时提示配置文件不存在

**解决方案**：
```bash
# 创建配置目录
mkdir -p config

# 复制配置模板
cp config/config.example.json config/config.json

# 编辑配置文件
vim config/config.json
```

### 8. 权限问题

**症状**：运行脚本时提示权限不足

**解决方案**：
```bash
# 设置脚本权限
chmod +x run.sh
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

### 9. 网络问题

**症状**：下载或同步时出现网络错误

**解决方案**：
```bash
# 检查网络连接
ping github.com

# 检查代理设置
echo $http_proxy
echo $https_proxy

# 如果需要代理，设置环境变量
export http_proxy=http://proxy:port
export https_proxy=http://proxy:port
```

### 10. 磁盘空间不足

**症状**：下载课程时提示磁盘空间不足

**解决方案**：
```bash
# 检查磁盘空间
df -h

# 清理不需要的文件
rm -rf output/.cache

# 移动输出目录到其他位置
mv output /path/to/larger/disk
```

## 调试模式

### 启用详细输出

```bash
# 使用--json参数查看详细输出
dedao-dl course --json
dedao-dl dl <课程ID> --json
```

### 查看日志

```bash
# 查看dedao-dl日志
ls -la ~/.config/dedao/

# 查看配置文件
cat ~/.config/dedao/config.json
```

### 手动测试

```bash
# 测试登录
dedao-dl who

# 测试下载
dedao-dl dl 656 -t 3 -m

# 测试分析
python3 scripts/analyze.py "output/阿里国际站·怎样做好跨境电商/MD"
```

## 获取帮助

如果以上方法都无法解决问题，请：

1. 查看dedao-dl文档：https://github.com/yann0917/dedao-dl
2. 提交Issue到GitHub仓库
3. 联系维护者
