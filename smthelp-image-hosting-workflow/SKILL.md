---
name: smthelp-image-hosting-workflow
description: "Southern Machinery 图床（Chevereto）上传工作流 — 将 AI 生成图片或本地图片上传至 https://ph.smthelp.com 并获取永久 URL。用于营销素材上传到公司图床。"
whenToUse: "上传图片到图床，上传到ph.smthelp.com，Chevereto上传，上传营销素材，Southern Machinery图床"
metadata:
  source: hermes
  origin: "marketing/smthelp-image-hosting-workflow"
---
# Southern Machinery 图床上传工作流

## 凭证信息

| 项目 | 值 |
|------|-----|
| 图床地址 | https://ph.smthelp.com |
| 用户名 | admin |
| 密码 | Nbjx |
| API Key | `da4723b27ffac80ef3c8af30a8110838` |
| API 接口 | `POST http://ph.smthelp.com/api/1/upload` |
| Chevereto 版本 | v4 API v1 |

## 上传方式

### 方式一：curl（推荐用于脚本）

```bash
curl --fail-with-body -X POST \
  -H "X-API-Key: da4723b27ffac80ef3c8af30a8110838" \
  -H "Content-Type: multipart/form-data" \
  -F "source=@/path/to/image.jpg" \
  -F "format=json" \
  http://ph.smthelp.com/api/1/upload
```

### 方式二：Python（推荐用于自动化工作流）

```python
import requests
import json

def upload_to_smthelp(image_path: str, api_key: str = "da4723b27ffac80ef3c8af30a8110838") -> dict:
    """
    上传图片到 Southern Machinery 图床
    返回: {"id", "url", "medium", "thumb", "display_url", "original"}
    """
    with open(image_path, "rb") as f:
        files = {"source": f}
        headers = {"X-API-Key": api_key}
        response = requests.post(
            "http://ph.smthelp.com/api/1/upload",
            files=files,
            headers=headers,
            timeout=30
        )
    return response.json()

# 使用
result = upload_to_smthelp("/tmp/marketing_image.jpg")
print(result["url"])        # 直接可用的图片 URL
print(result["thumb"])      # 缩略图 URL
print(result["display_url"])# 显示用 URL
```

### 方式三：Python + base64（远程服务器无文件访问时）

```python
import requests
import base64

def upload_base64_to_smthelp(image_bytes: bytes, filename: str = "image.jpg") -> dict:
    b64 = base64.b64encode(image_bytes).decode()
    payload = {
        "source": f"data:image/jpeg;base64,{b64}",
        "format": "json"
    }
    headers = {"X-API-Key": "da4723b27ffac80ef3c8af30a8110838"}
    response = requests.post(
        "http://ph.smthelp.com/api/1/upload",
        data=payload,
        headers=headers,
        timeout=30
    )
    return response.json()
```

## 返回值示例

```json
{
  "id": "abc123",
  "url": "https://ph.smthelp.com/images/2026/04/29/filename.jpg",
  "medium": {
    "url": "https://ph.smthelp.com/images/2026/04/29/filename-medium.jpg",
    "width": 800,
    "height": 600
  },
  "thumb": {
    "url": "https://ph.smthelp.com/images/2026/04/29/filename-thumb.jpg",
    "width": 320,
    "height": 240
  },
  "display_url": "https://ph.smthelp.com/images/2026/04/29/filename.jpg",
  "original": {
    "url": "https://ph.smthelp.com/images/2026/04/29/filename-origin.jpg",
    "width": 3840,
    "height": 2160,
    "size": 2048576,
    "mime": "image/jpeg"
  },
  "name": "filename.jpg",
  "title": "",
  "description": ""
}
```

## 典型工作流（AI图片生成 + 上传）

```python
import requests
import json
import time

API_KEY = "da4723b27ffac80ef3c8af30a8110838"
UPLOAD_URL = "http://ph.smthelp.com/api/1/upload"

def upload_image(image_path: str) -> str:
    """上传图片，返回 display_url"""
    with open(image_path, "rb") as f:
        resp = requests.post(
            UPLOAD_URL,
            files={"source": f},
            headers={"X-API-Key": API_KEY},
            timeout=30
        )
    data = resp.json()
    if data.get("status") == "success":
        return data["image"]["display_url"]
    else:
        raise Exception(f"Upload failed: {data}")

def upload_and_print_markdown(image_path: str, product_name: str) -> None:
    url = upload_image(image_path)
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    print(f"### {product_name} — Uploaded {timestamp}")
    print(f"![{product_name}]({url})")
    print(f"**URL**: {url}")
```

## n8n 自动化集成

在 n8n workflow 中使用 HTTP Request 节点：

```
Method: POST
URL: http://ph.smthelp.com/api/1/upload
Authentication: None (use Header)
Headers:
  X-API-Key: da4723b27ffac80ef3c8af30a8110838
Body: multipart-form-data
Body Fields:
  source: (file field — binary data from previous node)
  format: json
```

## 注意事项

1. **网络问题**: 如果 `http://ph.smthelp.com` 超时，可尝试 `https://ph.smthelp.com`
2. **文件格式**: 支持 JPG/PNG/GIF/WebP，最大 50MB（Chevereto 默认限制）
3. **文件名**: 建议用产品型号命名，如 `S70LD-hero-shot.jpg`
4. **URL 有效期**: Chevereto 托管的图片 URL 为永久 URL，无过期时间
5. **不要上传敏感信息**: 图床面向公众，确保图片不含机密数据

## 快速测试

```bash
# 测试连通性
curl -s --max-time 10 "http://ph.smthelp.com" | head -5

# 测试上传（创建空测试文件）
echo "test" > /tmp/test.txt
curl -s -X POST \
  -H "X-API-Key: da4723b27ffac80ef3c8af30a8110838" \
  -F "source=@/tmp/test.txt" \
  -F "format=json" \
  "http://ph.smthelp.com/api/1/upload"
```

## 常见错误

| 错误信息 | 原因 | 解决 |
|---------|------|------|
| `Request timeout` | 网络不通 / 防火墙拦截 | 尝试 https 或检查代理 |
| `{"status":"error","code":403}` | API Key 错误 | 确认 Key 未过期 |
| `{"status":"error","code":100}` | 缺少 source 字段 | 确保文件已正确读取 |
| `{"status":"error","code":421}` | 文件大小超限 | 压缩图片 < 50MB |
