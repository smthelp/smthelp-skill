---
name: product-3d-doc-html-landing
description: 产品 3D 图 + 介绍文档（PDF/PPTX/DOCX/视频）→ Southern Machinery 品牌单文件自包含 HTML 交互落地页。含 3D 交互（旋转/缩放/机构动画/材质与光照切换）、7 语言切换（含 RTL）、明暗模式、8 篇博客、ROI 回本计算、选型工具、披露表、SEO+GEO JSON-LD、Chatwoot。参数化配置（语言、博客篇数、配色、模型格式），带构建、轻量化、验证脚本。用于"把这些产品资料做成单 html 页面""产品落地页""3D 产品页"。
version: 1.0.0
author: Jason Wu / Southern Machinery (packaged by Hark)
---

# product-3d-doc-html-landing

把一个产品（或一个产品家族）的 3D 模型和介绍文档，做成**一个**自包含的 HTML 文件：离线可打开、≤1 MB、7 种语言、3D 可交互、可直接推到 GitHub 落地页仓库。

本 skill 固化自 2026-10 至 2026-11 已上线的 5 个页面（机器人插件线、SIS7200A、SIS5210A、LED T8 整线、PCB 上板机方案）。`examples/pcb-loader-solution/` 是最完整的参考实现，`python3 scripts/build.py examples/pcb-loader-solution` 可原样复现线上页面。

## 何时使用

- 用户给了产品资料（PDF / PPTX / DOCX / 图片 / 视频 / 3D 模型 / 报价单），要求"做成单 html 页面 / 落地页 / 产品页"。
- 需要升级已有页面（加语言、换配色、换 3D 交互、加章节）。

不适用：多页网站（用 WordPress/站点类 skill）、纯海报/PPT/视频（用 smt-brand-kit 等）。

## 1. 输入约定

| 输入 | 格式 | 来源 | 必需 |
|---|---|---|---|
| 介绍文档 | PDF、PPTX、DOCX、XLSX/CSV、MD/TXT | 用户上传；Southern Machinery 目录板 `file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html`（article `data-original` / `data-url`） | 是 |
| 产品 3D 图 | GLB/GLTF（首选）、STL、OBJ、PLY、STEP/STP、FBX；PPTX 内嵌的 `ppt/media/*.glb` | 用户上传、CAD 导出、PPT 内嵌 | 否（无模型时用程序化 Three.js 场景） |
| 图片 | 已托管：`ph.smthelp.com`（搜索 `https://ph.smthelp.com/search/images/?q=词`，取 `.md.png/.md.webp`）；未托管：从 PDF/PPTX 抽取后内嵌 | 图床优先 | 是 |
| 视频 | YouTube（视频板 `.../Southern-Machinery-YouTube-Video-Board.html`，article `data-title` / `data-embed`）；本地 MP4 → 上传到公开 Google Drive 文件夹后用 `drive.google.com/file/d/ID/preview` | 视频板、用户上传 | 否 |
| 报价单 | PDF | 用户 | 否；**规则：隐去单价、总价、客户名、报价号；ROI 投资 = 报价总额 × 1.25** |

资料不足时，从 Southern Machinery 产品知识库（目录板、视频板、图床）补充，并在披露表中注明来源。

## 2. 处理流程

```
资料 ──► ① 抽取 ──► ② 看图 ──► ③ 3D 准备 ──► ④ 文案结构化（EN） ──► ⑤ 翻译（6 路并行）──► ⑥ 构建 ──► ⑦ 验证 ──► ⑧ 发布
```

1. **抽取**：`python3 scripts/extract_sources.py <work> <资料文件或目录...>` → `sources/<文件>/text.md`、`media/`、`inventory.json`（含 mp4 时长分辨率、是否含 3D 模型）。
2. **看图**：`python3 scripts/contact_sheet.py <work>/sources sheet.jpg`，**必须打开看**，再选图。海报式信息图不放 hero；hero 用去白边的 2×2 产品图（`inline_images.py --hero`）。
3. **3D 准备**（二选一，写入 `config.model.mode`）
   - `glb`：`python3 scripts/model_prep.py <模型或pptx> <work> --ratio 0.06 --max-tri 60000` → 合并顶点 → 减面 → `gltf-transform optimize`（meshopt/draco、纹理 ≤1024）→ `model.glb` + `model_report.json`。实测：PPT 内嵌 48.9 MB / 72 万面 → 214 KB / 4.3 万面。≤ `max_inline_kb` 内嵌，否则托管并填 `model.url`。
   - `procedural`：没有模型或要演示机构动作（推板、吸板、换料框、机器人取放）时，按 `templates/viewer_procedural_example.js` 写程序化场景（9 种上板机构的参考实现）。
4. **文案结构化**：按 `references/content-model.md` 写 `en_ui.py`（EN 字典）+ `en_blog.py`（`blog_count` 篇，每篇 t/c/m/x + h1..h6/p1..p6 六步结构）+ `page.py`（型号表、规格卡、披露表、图库、视频、下载、JSON-LD Product、选型工具）。每个数字标来源；文档互相矛盾的写进披露表，不自己挑。`python3 scripts/i18n_tools.py mk-en <work>`。
5. **翻译**：`i18n_tools.py reuse <work> <旧页面 i18n 目录...>` 复用相同英文的旧译文，只把 `todo_<lang>.json` 分给 6 个并行翻译子代理（提示词见 `references/i18n.md`），产出 `out_<lang>.json`，再 `i18n_tools.py merge <work>`。
6. **构建**：`python3 scripts/build.py <work>`（读 `config/default.yaml` 深合并 `<work>/config.yaml`）。内嵌图片自动去重进 `window.EMB`。
7. **验证**：`python3 scripts/validate.py <work>`（硬性检查，失败退出码 1）+ `python3 scripts/render_test.py <page.html>`（浏览器：各模式、材质/光照、zh、ar RTL、390 px 手机无横向溢出、无 JS 报错）。**截图必须看**。清单见 `references/validation-checklist.md`。
8. **发布**：复制到 `files/output/`；`GITHUB_TOKEN=… python3 scripts/publish_github.py smthelping/smt-product-landing-html main "msg" <file>=<folder>/<file> README.md=README.md`（一次提交；Hark 沙箱内也可用 `ghput.py`）。README 先重新拉取再打补丁（页数、表格行、段落），不要覆盖。

## 3. 输出规范

- **一个 HTML 文件**，文件名 = 原文件名的 SEO 化（小写连字符），≤ `page.size_budget_kb`（默认 1024 KB）。
- 外部依赖仅：Three.js（jsdelivr importmap）、Font Awesome、Google Fonts、YouTube/Drive iframe、Chatwoot、图床图片。断网时 3D 降级为 hero 图。
- **章节**（模板固定顺序）：顶栏（logo 左上、导航、语言、明暗）→ Hero（4 指标）→ 3D 交互 + 模式按钮 + 选型/工具卡 → How it works（`station_count` 步）→ 型号/BOM 表 → 规格卡（带证据标签与来源）→ 披露表 → 图库（灯箱）→ YouTube + Drive 片段 → 下载 → ROI 计算 → 博客（`blog_count` 篇，弹窗阅读）→ FAQ（`faq_count`）→ 询盘 → 页脚（LinkedIn 公司/个人、Twitter @smtspecialist、Facebook、YouTube、目录站、图床、info@smthelp.com、WhatsApp）→ Chatwoot 右下角。
- **3D 交互**：拖拽旋转、滚轮/双指缩放、自动旋转、复位、模式切换（程序化：机构动画；GLB：相机预设 + 爆炸视图 + 自带动画）、**材质切换**（原始/金属/白模/透视/线框）、**光照切换**（影棚/暖光车间/夜间产线），标注"概念示意"。
- **多语言**：默认 en、es、pt、fr、ar（RTL）、ru、zh；`?lang=` 覆盖；每页独立 localStorage 键（`page.ls_prefix`）；只用 textContent 写入。
- **ROI**：默认字段为空（营销页不预填）；报价类页面用 `roi.investment_multiplier: 1.25` 并在页面说明这 25% 的含义需用户确认。
- **SEO + GEO**：title/description/keywords/canonical/hreflang(+x-default)/OG/Twitter；JSON-LD `@graph` = Organization、WebPage（speakable）、Product/ProductGroup、FAQPage、HowTo、BreadcrumbList、BlogPosting×N、VideoObject×N。
- **证据标签**：Verified material / Concept illustration / To be confirmed。
- **禁用词**（可见文本与 class 名）：Dan Koe、hook、diagnosis、framework、vehicle、loop、CTA（及中文钩子/诊断/框架/载体/闭环）。

## 4. 参数化配置

全部在 `config/default.yaml`，项目只写差异到 `<work>/config.yaml`。关键项：

| 配置 | 作用 | 默认 |
|---|---|---|
| `languages` / `rtl_languages` | 语言清单与顺序（首个为默认） | 7 种 / `[ar]` |
| `content.blog_count` / `blog_steps` / `faq_count` / `station_count` | 区块数量 | 8 / 6 / 8 / 6 |
| `content.banned_words*` / `privacy_terms` | 禁用词、隐私词（客户名、报价号…） | 见文件 |
| `theme.primary/primary_dark/accent/warn` | 主题配色（CSS 变量） | 品牌青绿 |
| `model.mode` | `procedural` 或 `glb` | procedural |
| `model.formats_accepted` / `max_inline_kb` / `decimate_ratio` / `max_triangles` / `compress` / `texture_max_px` | 模型格式与轻量化参数 | glb…fbx / 350 / 0.25 / 150000 / meshopt / 1024 |
| `model.views` | GLB 模式的相机预设（每个 = 一个模式按钮，可带 `explode`） | 1 个 |
| `model.interactions` | 交互能力清单 | rotate…light |
| `roi.*` | ROI 字段、预填、投资倍数 | 空、1.0 |
| `chatwoot.token/host` | 客服 | 品牌值 |
| `page.*` | 文件名、目录、关键词、OG、mailto 主题、日期、体积预算 | — |

## 5. 调用示例

```bash
SK=~/.skills/product-3d-doc-html-landing; W=~/work/sl600a
mkdir -p $W && cp $SK/examples/pcb-loader-solution/config.yaml $W/   # 改 page.* 与 model.*
python3 $SK/scripts/extract_sources.py $W ~/uploads/SL600A*.pdf ~/uploads/*.pptx
python3 $SK/scripts/contact_sheet.py $W/sources $W/sheet.jpg
python3 $SK/scripts/model_prep.py ~/uploads/SL600A.step $W --ratio 0.1      # 可选
python3 $SK/scripts/inline_images.py $W --hero hero a.png b.png c.png d.png
#  写 $W/en_ui.py  $W/en_blog.py  $W/page.py（照 examples/pcb-loader-solution）
python3 $SK/scripts/i18n_tools.py mk-en $W
python3 $SK/scripts/i18n_tools.py reuse $W ~/old-pages/*/i18n
#  6 个并行子代理：todo_<l>.json -> out_<l>.json
python3 $SK/scripts/i18n_tools.py merge $W
python3 $SK/scripts/build.py $W && python3 $SK/scripts/validate.py $W && python3 $SK/scripts/render_test.py $W/*.html
```

对话式调用：「用 product-3d-doc-html-landing 把附件的 SL600A 资料做成单 html 页，放 board-handling/，模型用 PPT 里的 3D」。

## 6. 扩展点

见 `references/extension-points.md`：新章节（模板占位符 + build.py 生成函数）、工具卡（`page.py` 的 `TOOL_HTML` / `TOOL_JS`，`window.__toolRefresh`）、3D 适配器契约（`__mode3d / __reset3d / __rot / __flow / __mat / __light / __fed`）、新模型格式（`model_prep.py` 转换分支）、新验证项（`validate.py` 的 `chk()`）。

## 7. 升级路径

见 `references/upgrade-path.md`：新增语言（`i18n_tools.py add-lang`）、新模板/配色、新 3D 交互能力、版本号与 CHANGELOG 规则。

## 8. 已知坑（来自实际交付）

- 阿语页 `.skip` 链接放 `left:-999px` 会横向滚动；模板已改为 `top:-60px`。
- CAD 导出的 GLB 顶点按面分裂，不先 `merge_vertices` 减面会停在原面数。
- 减面后缺法线会全黑；viewer 自动 `computeVertexNormals`。
- 同一型号名在不同文档里指不同机器（如 SLD250L），只能进披露表并提醒用户确认。
- 沙箱里 Python 包与 `~/.cache` 每轮可能清空：Playwright 需重装；外部资源 407 是代理问题，不是页面错误。
- 翻译子代理会把法/葡语小数点改成逗号，属正常本地化。
