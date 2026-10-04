---
name: doc-library-inventory
description: 只读盘点混杂格式的文档/手册库（PDF + OLE2 老 Office + OOXML + 图纸 + 媒体），识别云端占位符与重复副本，提取关键参数，输出项目级 AGENTS.md（目录结构/技术栈/模块职责/命名规范/数据治理铁律/术语表）。触发词：盘点文档库、生成 AGENTS.md、手册库盘点、文档资产盘点、product manuals inventory、AGENTS.md 生成。
agent_created: true
---

# 文档/手册库盘点 → AGENTS.md 生成

**适用场景：** 一个装满产品手册、说明书、图纸、演示稿的目录（通常同步自网盘），需要 Agent 快速建立认知并产出可长期复用的项目级契约文件。

**核心原则：只读。** 本流程**不修改、不重命名、不删除**任何原始文件。所有产出写入新文件。

---

## 环境

```bash
PY=/Users/mac/.workbuddy-ai/binaries/python/envs/default/bin/python
# 已装：pypdf / olefile / openpyxl
# 缺则：$PY -m pip install pypdf olefile openpyxl
```

---

## 第一步：结构盘点（只读）

```bash
cd "<LIB_ROOT>"

# 1. 目录骨架（注意空目录也是信息——它们是分类占位符）
find . -maxdepth 3 -type d | sort

# 2. 总文件数 + 格式分布
find . -type f | wc -l
find . -type f | sed 's/.*\.//' | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn

# 3. ⚠️ 关键：识别云端占位符（0 字节）
find . -type f -size 0 ! -name ".DS_Store" | wc -l
# 网盘同步盘的"仅云端"文件是 0 字节，不是空文档。必须区分，否则会误判。
```

**同时统计：** 本地实体文件（`-size +0`）与占位符各多少、每目录文件数（找内容密度区）。

**排除清单（永远忽略）：** `.DS_Store`、`~$*`（Office 锁文件）、`.sync-conflict-*`、`-副本*`、`*.tmp`。

---

## 第二步：重复与版本识别

| 后缀模式 | 含义 | 处理 |
|---|---|---|
| `(1)` `(2)` `(2)(1)` | 下载/同步重复副本 | 比对后建议保留较新，**需用户确认才动** |
| `_V1` `_V2` `2022` `YYYYMMDD` | 真实版本 | **全部保留**，最新版为对外口径 |
| `.sync-conflict-YYYYMMDD-HHMMSS-XXXXXXX` | 网盘同步冲突残留 | 垃圾，建议清理（需确认） |
| `-副本YYYYMMDDHHMMSS` | 手动副本 | 同上 |
| `~$` 开头 | Word/Excel 锁文件 | 忽略，不读取 |

---

## 第三步：内容抽样提取（按格式选工具）

```bash
# ① .doc / .docx（macOS 原生，最稳）
textutil -convert txt -output /tmp/out.txt "path/to/file.doc"

# ② .docx / .xlsx / .pptx（OOXML = ZIP+XML，纯标准库）
$PY -c "
import zipfile, re
z = zipfile.ZipFile('file.docx')
x = z.read('word/document.xml').decode('utf-8','ignore')
x = re.sub(r'</w:p>', '\n', x)
print(re.sub(r'<[^>]+>', '', x))"

# ③ PDF
$PY -c "
import pypdf
r = pypdf.PdfReader('file.pdf')
print('\n'.join(p.extract_text() or '' for p in r.pages[:5]))"

# ④ .xls / .ppt（OLE2 二进制，textutil 与 zipfile 都会失败）→ strings 兜底
strings "file.xls" | grep -vE "^(Microsoft|MS|Root|Workbook|Arial|Calibri|General)" | awk 'length($2)>2'
# 精细解析再上 olefile

# ⑤ 扫描件 PDF（extract_text 返回空）→ 需 OCR
```

**抽样策略：** 每个设备族/分类抽 1–2 个最有代表性的文档读全，其余读首页。目的是**搞清分类逻辑与术语体系**，不是穷举内容。

---

## 第四步：产出 AGENTS.md

固定章节骨架：

```markdown
# AGENTS.md — <仓库名>
## 0. 快速索引            ← 表格：我想…… → 去看 §N
## 1. 项目定位            ← 谁是消费者，核心矛盾是什么
## 2. 目录结构与实测清单   ← 实测统计 + 目录树 + 空目录清单
## 3. 技术栈              ← 内容格式栈 / 解析工具链 / 生成输出栈
## 4. 模块职责            ← 按业务族列表：模块 | 代表型号 | 目录锚点 | 价值主张
## 5. 命名规范            ← 推荐格式 + 正例 + 反例（贴真实文件名）+ 版本控制约定
## 6. 开发约定与数据治理铁律  ← 10 条以内，可执行
## 7. 已知问题与技术债     ← 严重度 | 问题 | 影响 | 建议动作
## 8. 业务语境速查         ← 公司/渠道/市场/行业（从公司档案取）
## 9. 术语表（中英）       ← 对外输出唯一口径
## 10. Agent 工作流约定    ← 标准闭环 + 记忆与技能位置 + 输出规范
```

**必写的三件事（决定文档价值）：**

1. **实测统计要带日期** — 「88 文件 / 35 占位符 / 30 空目录」比「包含多个手册」有用一万倍
2. **反例要贴真实文件名** — 直接引用库里实际存在的乱名，比抽象规范有效
3. **参数必须标注来源文件** — 任何数字都要能溯源，拿不准写 `[待确认]`

---

## 铁律

- **只读。** 不移动、不重命名、不删除、不覆盖原始文件。
- **0 字节 ≠ 空文件。** 是网盘占位符，不得删除、不得判定为空文档，要明确告知用户需先下载。
- **第三方文档要隔离。** 手册库里常混着竞品/对标厂商的资料，必须在 AGENTS.md 里显式声明「不得当作自有产品资料发布」。
- **不编参数。** 提不到就写 `[待确认]`，并列出需要什么信息才能确认。
- **不碰政治。** 涉及地区表述按中国官方口径。

---

## 常见坑

| 坑 | 症状 | 解法 |
|---|---|---|
| `textutil` 对 `.xls`/`.ppt` 静默失败 | 输出 0 字节且报 "no such file or directory" | 换 `strings` 或 `olefile` |
| 中文/空格路径导致 shell 报错 | `no such file or directory` | 所有路径加双引号；或用 `find -exec` |
| `zipfile` 报 "File is not a zip file" | 那是 OLE2 老格式 | 判断扩展名后走 `strings`/`olefile` 分支 |
| PDF `extract_text()` 返回空 | 扫描件无文本层 | 需 OCR，或改用 Read 工具视觉读取 |
| 把占位符当空文档写进报告 | 误判"库内容缺失" | 第一步就统计 0 字节文件数 |
