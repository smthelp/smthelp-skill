---
name: smt-product-poster
description: "Southern Machinery 产品海报流水线 — 从产品 PDF/PPT 一键生成 SP-830 品牌模板风格的 16:9 高保真营销海报（PNG），自动生成 SEO 文件名/标题/描述/标签，保存本地并把海报 + 元数据推送到 GitHub 仓库 smthelping 系 poster 库（可开 GitHub Pages 展示页）。"
whenToUse: "做产品海报，PPT转海报，PDF转海报，poster，营销海报生成，海报推仓库，poster SEO 元数据，smt-Machine-poster，Southern Machinery 产品宣传图"
version: 1.0.0
metadata:
  source: hermes
  origin: "marketing/smt-product-poster"
---

# SMT Product Poster Pipeline（产品 PDF → 品牌海报 → GitHub 交付）

> **定位**: 输入一个产品资料（PDF/PPT）+ 一张模板海报，输出品牌一致、文字经过校验、带完整 SEO 元数据的高保真营销海报，并完成本地保存 + GitHub 推送 +（可选）Pages 上线。
> **品牌规范**: 复用 `smt-machine-marketing-image-prompts` 的 Southern Machinery 视觉体系（绿色/青色主视觉、工业橙点缀、禁止竞品外观、禁止员工面孔）。
> **默认模板**: `https://file.autoinsertion.com/public/SMThelp%20Poster/SP-830%20Full-Auto%20Screen%20Printer.png`（16:9 · 2752×1536 · 版式见下文「模板版式契约」）

---

## 输入参数（有默认值，缺省不追问）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `PRODUCT_SRC` | 产品 PDF/PPT 绝对路径 | 用户指定；若用户给了文件夹，取本次点名的文件 |
| `TEMPLATE_URL` | 模板海报 URL | SP-830（见上） |
| `TARGET_REPO` | 推送目标 GitHub 仓库 | `smthelp111/smt-Machine-poster`（`smthelping/smt-Machine-poster` 对现有账号只读，见 Pitfalls #4） |
| `WORK_DIR` | 中间产物目录 | 产品文件夹下 `.poster-work/`（临时区，可直接删） |
| `LOCAL_OUT` | 本地交付目录 | 产品文件夹根 + 会话 outputs 目录各存一份 |
| `PAGES` | 是否开 GitHub Pages 展示页 | 用户要求才开 |

## 工作流

### Step 0 · 环境与素材

```bash
mkdir -p "$WORK_DIR" && cd "$WORK_DIR"
curl -sL --fail -o template.png "$TEMPLATE_URL"
file template.png   # 必须是 PNG/JPEG，记下宽高比（默认 16:9）
```

### Step 1 · 读产品资料，提炼海报文案槽位

用 **Read 工具直接读 PDF**（多模态，逐页看图），提炼：
- 型号（如 SLD350L / SUL350L）与产品全称
- 3 个量化卖点（大数字，如 `~30s Magazine Changeover`、`±0.025mm`）
- 3 个特性卖点（短语 + 一句解释）
- 参数表 4–5 行（Model / Max PCB / Dimensions / Rack / Power / Air）
- 服务承诺与联系方式（footer：www.smthelp.com info@smthelp.com）

**文案槽位固定为模板的 6+1 结构**（见「模板版式契约」），填不满就合并，不要留空占位。

### Step 2 · 从 PDF 裁真实产品照（生成参考图）

```bash
pdftoppm -png -r 150 -f 1 -l 4 "$PRODUCT_SRC" page     # 渲染前 4 页
python3 - <<'EOF'
from PIL import Image
# 按页面实际坐标裁产品照片（先 Read 渲染页确认坐标，150dpi 下 A4横版=1500×1125px 左右）
Image.open('page-1.png').crop((x0, y0, x1, y1)).save('ref-product.png')
EOF
```

⚠️ **必须目检裁切结果**（Read 查看），照片里出现可辨认的员工/人脸要重新裁切排除（品牌红线）。裁 1–2 张最能代表设备外观的即可，参考图不是越多越好。

### Step 3 · 生成 SEO 元数据（基于原文件名）

从原始文件名（如 `1.2M LED PCB Magazine loader unloader.pdf`）派生，**保留原文件名的核心词根**再补关键词：

- **filename**: `<核心词>-<型号>-<品类词>-<场景词>-<品牌>.png`，全连字符，例：
  `1.2M-LED-PCB-Magazine-Loader-Unloader-SLD350L-SUL350L-SMT-Automatic-PCB-Handling-EMS-Factory-Southern-Machinery.png`
- **title**（≤65 字符最佳）: `<产品词> <型号> | <品类/卖点> | Southern Machinery`
- **description**（≤160 字符）: 一句能力 + 2–3 个量化参数 + 目标客群（EMS factories）
- **keywords/tags**: 12–15 个（品类词、同义词、型号、场景词、品牌词）
- 写入 `poster-meta.json`（结构含 `source_pdf / product / seo / key_specs / contact`），随海报一起入库。

### Step 4 · 生成海报（图生图编辑模式）

用 `qwenwork_image_generate`：

```
mode = edit
model = open-image-2
images = [template.png, ref-product-1.png, ref-product-2.png]   # 模板在前 = 版式参考
prompt = 「模板复刻指令 + 设备外观描述（来自真实照片）+ 全部文字逐字给出」
```

Prompt 骨架（替换 `{...}` 槽位）：

```
Recreate the layout, style, color system and iconography of image 1 (a Southern
Machinery product poster template) as a NEW wide 16:9 landscape marketing poster
for the {设备外观一句话描述} shown in images 2 and 3. Keep the same visual language:
light background with subtle circuit-trace pattern, Southern Machinery logo top-left,
model number in green + rest of headline in bold black, section headers with teal
vertical accent bars, isometric teal/green line icons, central clean product cutout
photo, teal-accented spec table bottom-center, contact footer.

Render this text EXACTLY:
Headline: "{型号}: {英文产品名}"
Intro: "{一句话定位，含目标客群}"
Left column header: "{栏目A}" — Big stat "{数字}" + "{标题}" + "{解释}" ; 另 2 组同构
Right column header: "{栏目B}" — 3 组 {标题}+{解释}
Table title: "ESSENTIAL MACHINE PARAMETERS". Rows: "Model | ..."; "Max PCB Size | ..."; ...
Footer: "www.smthelp.com    info@smthelp.com".
No watermark, no human faces, crisp legible typography, professional commercial
catalog quality, 4K.
```

⚠️ **open-image-2 的 edit 模式不接受 `aspect_ratio` / `resolution` / `web_search` 参数**（传了报 400；传空字符串报 schema 校验错），必须整个字段省略。横版比例靠 prompt 里 "wide 16:9 landscape" 控制。

### Step 5 · 文字逐字校验（poster 规范，≤2 次重试）

`qwenwork_media_task action=wait output_name=<语义中文名>` 取回 PNG 后，**用 Read 目检**：
标题、型号、6 组卖点、参数表每一行数字、邮箱网址逐字对照。发现错字/漏字/数字错 → 微调 prompt（把出错短语加引号强调或缩短该短语）重新生成，最多 2 次。2 次仍不过 → 交付最接近版本并向用户标注瑕疵。

### Step 6 · 本地保存

```bash
cp "$GENERATED.png" "$PRODUCT_DIR/$SEO_FILENAME.png"     # 产品文件夹一份
cp "$GENERATED.png" "$OUTPUTS_DIR/$SEO_FILENAME.png"     # outputs 一份（用于 present）
```

### Step 7 · 推送 GitHub 仓库

```bash
# 克隆位置必须在 APFS 卷（如 ~/.qwenworkcn/workspace/...），不要在 exFAT/移动硬盘（见 Pitfalls #1）
gh repo clone "$TARGET_REPO" poster-repo || \
  gh repo create "$TARGET_REPO" --private --source=. --remote=origin --push   # 仓库不存在则创建
```

仓库内三件套：`{SEO_FILENAME}.png` + `{产品名}.meta.json` + README 追加条目：

```markdown
### {产品标题} ({型号})
- **File**: `{SEO_FILENAME}.png` (16:9, 2K)
- **Source**: `{原始 PDF 文件名}`
- **SEO Title**: ...
- **Meta Description**: ...
- **Tags**: ...
- **Full metadata**: `{产品名}.meta.json`
```

```bash
git add -A && git -c user.name="{账号}" -c user.email="{账号}@users.noreply.github.com" \
  commit -m "Add {产品} poster ({型号}) with SEO metadata" && git push origin main
gh api repos/"$TARGET_REPO"/contents --jq '.[].name'    # 远端验证
```

### Step 8 ·（可选）GitHub Pages 展示页

写一个自包含 `index.html`（品牌绿/青配色：海报大图 + Key Specs + SEO Tags + 下载按钮 + OG meta 含 `og:image`），push 后：

```bash
gh api -X POST repos/"$TARGET_REPO"/pages -f 'source[branch]=main' -f 'source[path]=/'
# 轮询 status（首次可能 errored，构建器就绪后会变 built），再 curl 验证 200
gh api repos/"$TARGET_REPO"/pages --jq .status
curl -sI "https://{user}.github.io/{repo}/" | head -1
```

Pages 站点即海报的永久分享直链（PNG raw URL 也可直接嵌邮件/社媒）。

---

## 模板版式契约（SP-830 系，升级模板时同步改这里）

1. 左上 Southern Machinery 绿色 logo
2. 标题行：`型号：` 绿色 + 副题黑色粗体（一行）
3. 标题下 2 行 intro（灰黑正文）
4. 左栏：teal 竖条 + 栏目名，下 3 组「等距图标 + 大标题 + 小解释」，第一组带超大数字
5. 中央：白底产品抠图（占版面 ~1/3 宽）
6. 右栏：同左栏结构（无大数字）
7. 底部中央：teal 描边参数表（表头浅绿底）
8. 页脚居中：网址 + 邮箱；全版面浅底 + 电路纹理装饰

## Pitfalls（血泪清单）

1. **exFAT/移动盘上的 git 仓库会坏**: `._*` AppleDouble 文件混进 `.git/objects/pack` → `non-monotonic index`。克隆/提交一律放 APFS 卷（`~/.qwenworkcn/workspace/...`）。
2. **open-image-2 edit 参数**: 见 Step 4，多余参数直接省略字段，不要传空串。
3. **PDF 照片带人脸**: 品牌红线，裁切后必须 Read 目检。
4. **目标仓库权限**: `smthelping/smt-Machine-poster` 属独立用户 `smthelping`，`smthelp`/`smthelp111` 只有读权限（403）。默认推 `smthelp111/smt-Machine-poster`；用户点名 smthelping 时先 `gh api repos/... --jq .permissions` 探测，缺权限就引导加协作者而不是硬试。
5. **gh 多账号**: 推送前 `gh auth switch --user {owner}`，推完切回；`gh api /user --jq .login` 确认当前身份。git remote 记住修正 `origin`（clone 后改地址）。
6. **文字校验不可跳过**: AI 直出海报最常见的错是参数表数字和型号字母。
7. **present 文件**: 最终用 `qwenwork_file_present_files` 展示 outputs 里的海报，不要只给路径。

## Verification（交付前逐项打勾）

- [ ] 海报标题/型号/参数表逐字正确（Step 5 通过）
- [ ] 无人脸、无竞品品牌、无水印
- [ ] 本地 2 份（产品文件夹 + outputs）均为 SEO 文件名
- [ ] `poster-meta.json` 五段齐全（source_pdf/product/seo/key_specs/contact）
- [ ] 远端仓库 `gh api .../contents` 能看到 PNG + JSON + README 更新
- [ ] （开了 Pages 时）站点 HTTP 200 且 PNG 直链 200

## 升级路径（v1.x → v2）

- **v1.1**: 模板注册表 `assets/templates.json`（多模板：SP-830 横版 / 9:16 竖版电商 / 1:1 社媒），一源多尺寸批量出图
- **v1.2**: 批量模式——给一个文件夹自动扫描全部 PDF 逐个出海报（增量：以 `.meta.json` 是否存在 + PDF mtime 判断）
- **v2.0**: 接入 `smthelp-image-hosting-workflow` 上传 ph.smthelp.com 图床，README 里同时写图床直链；Pages 升级为全站海报库（列表页自动生成）
- 修改本 skill 后：frontmatter `version` 按 semver 递增，并跑 `sync-skills.sh` 同步到 `~/.qwenworkcn/skills/`

## 关联 skill

- `smt-machine-marketing-image-prompts` — 品牌 prompt 结构与色值来源
- `poster`（产品设计套件）— 材质字体海报（不同风格线，勿混用模板契约）
- `smthelp-image-hosting-workflow` — 图床上传（v2 集成点）
- `smt-product-landing-page` — 同源 PDF 的落地页线，共享 SEO 命名规范
