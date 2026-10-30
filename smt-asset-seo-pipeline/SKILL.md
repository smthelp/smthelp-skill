---
name: smt-asset-seo-pipeline
description: Southern Machinery 素材库的两段式流水线——先用 asset_index.py 只读盘点任意产品目录（生成可检索 CSV + 缺口矩阵），再把 SMT Feeder 的图片 SEO 流水线（SEO 命名 + WebP + manifest）复制到新产品线并上传图床。触发词：素材盘点、资产索引、素材缺口、图片 SEO、WebP 批处理、manifest、上传图床、跑流水线、SEO_WebP。
agent_created: true
---

# SMT 素材库 SEO 流水线

素材库根目录：`/Volumes/wuj-data/baidunetdiskworkspace/My picture`（11GB / 9,540 文件 / 49 子目录，百度网盘同步目录）。

两段流程：**先盘点，再 SEO 化**。盘点能看清"哪些产品线没图可用"，避免对一堆备件图做无意义的 SEO 优化。

## 环境

```bash
PY=/Users/mac/.workbuddy-ai/binaries/python/envs/default/bin/python   # 已有 pillow / pandas / openpyxl / requests
ROOT="/Volumes/wuj-data/baidunetdiskworkspace/My picture"
```

路径含空格、子目录大量中文与 `(1)` `- 副本`，**所有命令必须双引号包裹**。

## 铁律

- **原始素材只读**：不重命名、不移动、不删除、不覆盖。产出一律进新的 `Output/`。
- **不覆盖已有批次**：输出目录用 `Output/SEO_WebP_<YYYYMMDD>/`，绝不复用旧日期目录。
- **凭据不落盘**：API key 只用环境变量传，这个目录会同步网盘。

---

## 第一段：盘点（asset_index.py）

```bash
cd "$ROOT"
$PY scripts/asset_index.py --root "Auto Insertion" --name AssetIndex_AutoInsertion_20260913
```

产出 `Output/AssetIndexes/<name>.csv` + `.md`。

脚本自动做：产品类别分类、机型编号正则提取（23 种：`S3010B` `S-4000` `SME-5300` `JS-GZ-01` 等）、场景标签、md5 查重、问题件标记、机型×场景缺口矩阵、行动建议。

### 判定标准（踩过的坑）

| 项 | 正确标准 | 错误做法 |
| --- | --- | --- |
| 低清 | **长边 < 1000px** | ~~短边 < 800px~~ —— 会把 1408×736 产线横幅误判，误报率 3 倍 |
| 超长拼接图 | 长宽比 ≥ 4，单独标 `panorama` | 不标 → 1920×16200 的图直接上站会炸版 |
| 超大未压 | > 3MB | — |

CSV 中 `flags` 为空 = 可直接使用。

### 改分类/机型规则

改 `scripts/asset_index.py` 顶部的 `CATEGORIES` / `SCENES` / `MODEL_RE` 三张表。**顺序敏感：先具体后一般**。

---

## 第二段：图片 SEO 流水线复制

### 1. 复制脚本

```bash
mkdir -p "$ROOT/<新产品线>/scripts"
cp "$ROOT/SMT Feeder/scripts/ph_upload_webp.py" "$ROOT/<新产品线>/scripts/"
```

`seo_webp_prepare.py` 不要直接 cp，要改写分类表（见下）。

### 2. 改写 CATALOG_CATEGORIES

用 Python **切片替换** `CATALOG_CATEGORIES = [` 到 `def slugify` 之间的整块，比整文件重写安全：

```python
text = SRC.read_text(encoding="utf-8")
start = text.index("CATALOG_CATEGORIES = [")
end = text.index("def slugify")
DST.write_text(text[:start] + NEW_BLOCK + text[end:], encoding="utf-8")
```

`NEW_BLOCK` 包含 `CATALOG_CATEGORIES` 与 `DEFAULT_CATEGORY`。每个类别字段：`category` / `product` / `keywords`（中英都要）/ `title` / `description` / `tags`。

**顺序敏感**：具体类别必须排在兜底类别前。例：`selective-soldering-machine`（关键词 `selective`）必须排在 `wave-soldering-machine`（关键词 `wave soldering`）之前，否则 `SL-300 Desktop Selective Wave Soldering Machine` 会被误归整机。

`title` 会被拼成 `f"Southern Machinery {title}"`，**不要再写 "Southern Machinery"**。

### 3. 先 dry-run 看分类分布，再真跑

```bash
cd "$ROOT/<新产品线>"
$PY scripts/seo_webp_prepare.py --root . --output "Output/SEO_WebP_<YYYYMMDD>" --dry-run
# 人工确认分类分布合理后再去掉 --dry-run
```

常用参数：`--max-side 1920`（默认）`--quality 82` `--limit N` `--dry-run`。

产物：`manifest.csv`（含 title/description/tags，可直接喂图床）、`manifest.json`、`webp/<类别>/`、`errors.csv`。

**注意**：`.psd` 不在支持的扩展名内（只处理 jpg/jpeg/png/webp/gif），PSD 图会被跳过，需提醒用户。

### 4. 生成待确认清单

产出 `Output/SEO_WebP_<YYYYMMDD>/REVIEW_<日期>.md`：概览 + 分类分布 + 前 20 条命名对照 + 需人工确认的疑点 + 下一步命令。让用户核对后再上传。

---

## 上传图床

图床 `ph.smthelp.com`（Chevereto）。**必须用 https**，http 入口会 301 且 curl 默认不跟随 → 表现为"上传无反应"。

```bash
PH_API_KEY=<key> python3 upload_standalone.py            # 零依赖，纯标准库，推荐
PH_API_KEY=<key> python3 upload_standalone.py --limit 5  # 先试跑
PH_API_KEY=<key> python3 upload_standalone.py --write-back  # 回写 URL 到 manifest
```

原脚本 `scripts/ph_upload_webp.py` 需要 `requests`，参数：`--manifest --output --api-url --mode api-v1 --limit`，key 读 `PH_API_KEY`。

`upload_standalone.py` 位于 `Wave soldering/Output/SEO_WebP_20260913/`，可直接复制到其他批次目录使用。支持断点续传（跳过已有 `uploaded_url` 的行）。

### ⚠️ 已知环境限制

本机（WorkBuddy 沙箱）**无法向 ph.smthelp.com 上传**：TCP 443 通、TLS 1.3 握手成功，但发送应用层数据后即 `SSL record layer failure`。已验证无效的手段：`--noproxy '*'`、`env -u https_proxy…`、curl `-k`、`--tlsv1.2`、`curl -L`、`dangerouslyDisableSandbox`。环境有 `https_proxy=http://127.0.0.1:55769`。

**不要反复重试浪费时间** —— 直接交付 `upload_standalone.py` + `UPLOAD_GUIDE.md`，让用户在其他机器/网络执行。

---

## 上传后

拿到 `upload_results.csv` 后，生成 **「图片 URL → 用途」对照表**：按类别分组，标注每张图适用页面（产品页首屏 / 规格表 / 博客插图 / LinkedIn / YouTube 封面），交付网站与社媒。
