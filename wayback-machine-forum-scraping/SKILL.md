---
name: wayback-machine-forum-scraping
description: "如何通过 Wayback Machine 抓取已下线或无法直接访问的论坛内容。适用于技术论坛、行业社区的信息收集场景。"
whenToUse: "抓取论坛，Wayback Machine，bbs.smthome.net，archive.org 存档，无法访问的网站，urllib 抓取 论坛，browser_console 失效"
metadata:
  source: hermes
  origin: "research/wayback-machine-forum-scraping"
---
# Wayback Machine 论坛抓取方法论

## 问题场景
目标论坛/网站无法直接访问（ERR_CONNECTION_CLOSED、ERR_EMPTY_RESPONSE 等），但需要获取其中的内容。

## 解决方案：Wayback Machine 存档抓取

### Step 1: 确认存档存在
访问：`https://web.archive.org/web/*/目标域名`
例如：`https://web.archive.org/web/*/bbs.smthome.net`

**关键指标**：
- Saved N times — 存档总数
- between 日期 and 日期 — 存档时间范围
- 713 times between Sep 2004 and Mar 2026 → 大量存档可用

### Step 2: 查找可访问的存档快照
1. **Calendar 视图** — 查看哪天有存档
2. **URLs 列表** — 查看所有存档的 URL
3. **Summary** — 查看 MIME-type 统计（确认有 text/html）

### Step 3: 访问存档
格式：`https://web.archive.org/web/YYYYMMDDHHMMSS/原始URL`

**技巧**：
- 用年份通配符试试：`https://web.archive.org/web/2025/目标URL`
- 最新存档优先：`https://web.archive.org/web/20260310*/bbs.smthome.net`

### Step 4: 提取结构化数据 — 关键：优先使用 Python urllib

**⚠️ 不要依赖 browser_console / browser_snapshot**：Wayback Machine 页面是 JS 渲染的，browser_console 在 Wayback 页面几乎总是返回空结果。browser_snapshot 也只能看到 Wayback 自己的导航 UI，实际论坛内容在 shadow DOM 或 iframe 中。

**正确方法：用 Python urllib 直接抓取 HTML**

```python
import urllib.request
import re

url = "https://web.archive.org/web/20251113015844/http://bbs.smthome.net/"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
response = urllib.request.urlopen(req, timeout=20)
html = response.read().decode('gbk', errors='ignore')  # 注意编码！
print(f"Page length: {len(html)} chars")

# 提取 forum fid → 板块名 映射
patterns = re.findall(r'<a[^>]+href=["\'][^"\']*fid=(\d+)[^"\']*["\'][^>]*>([^<]+)</a>', html)
for fid, name in patterns:
    name = re.sub(r'\s+', ' ', name.strip())
    if name and 1 < len(name) < 50:
        print(f"  fid={fid}: {name}")

# 提取帖子标题
titles = re.findall(r'<a[^>]+href=["\'][^"\']*read-htm-tid-(\d+)[^"\']*["\'][^>]*>([^<]+)</a>', html)
for tid, title in titles:
    clean = re.sub(r'\s+', ' ', title.strip())
    if len(clean) > 10:
        print(f"  [{tid}] {clean}")
```

### Step 5: 常见问题与解决

| 问题 | 原因 | 解决 |
|------|------|------|
| "Hrm. The Wayback Machine has not archived that URL" | 该 URL 无存档 | 尝试上级目录或其他日期 |
| 页面加载超时 | 存档太大/网络慢 | 减少访问频率 |
| "系统数据更新升级中" | 论坛维护状态 | 尝试其他日期的存档 |
| browser_console 返回空 {} | Wayback JS 渲染页面无法被 browser_console 访问 | 改用 Python urllib 直接抓 HTML |
| browser_snapshot 只看到 Wayback 导航 | 论坛内容在 shadow DOM 或延迟加载 | 改用 Python urllib |
| 帖子页 404 | 论坛 URL 是相对路径，缺少 base URL | 首页链接是绝对 URL `https://web.archive.org/...`，分类页链接是相对路径 |
| 编码乱码 | GBK/GB2312 编码中文论坛 | `decode('gbk', errors='ignore')` |
| Donation banner 遮挡 | Wayback Machine 弹捐款提示 | 不影响 HTML 抓取（不看浏览器渲染） |

### Step 6: 备选方案（若 Wayback 也不行）
1. Google Cache: `cache:目标URL`
2. Bing Cache
3. 直接联系网站管理员
4. 搜索引用/镜像该内容 的其他网站

## 实战经验（bbs.smthome.net 案例）

**发现**：
- 论坛有 713 次存档，688,366 个 HTML 页面
- 直接访问 bbs.smthome.net → ERR_EMPTY_RESPONSE（论坛维护中）
- 通过 Wayback Machine 存档 `20251113015844` → 成功获取首页快照（81KB HTML）

**Forum fid 板块映射**（从首页正则提取）：
```
fid=23: SMT设备
fid=24: 波峰焊接
fid=4:  SMT工艺
fid=22: SMT软件
fid=5:  SMT123
fid=43: PANASONIC贴片机
fid=44: YAMAHA贴片机
fid=49: JUKI贴片机
fid=55: Hanwha设备
fid=56: 国产SMT
```

**访问板块帖子列表**：`https://web.archive.org/web/{timestamp}/{base_url}thread.php?fid={N}`

**注意**：
- 帖子页 URL 格式：`read-htm-tid-{tid}.html`（相对路径，需拼接 base URL）
- 首页上的帖子链接多为绝对 URL（`https://web.archive.org/...`），板块页返回的链接多为相对路径
- 编码必须用 `gbk`，很多中文论坛不用 UTF-8

## 验证清单
- [ ] 确认 Wayback Machine 有该域名的存档
- [ ] 确认存档日期在合理范围内（不过期）
- [ ] 确认有 text/html 类型存档
- [ ] 成功获取首页或关键页面快照
- [ ] 使用 browser_console 提取结构化数据
- [ ] 记录存档 URL 供后续引用

---
*Created: 2026-04-23 | Source: bbs.smthome.net 抓取实战*
