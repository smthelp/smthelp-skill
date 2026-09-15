---
name: md-to-styled-html
description: >
  把 Markdown 文件渲染成自包含的、可直接双击打开的精美 HTML 单页
  （深色/浅色主题、左侧自动目录、代码块一键复制、表格卡片化）。
  当需要把报告、作战手册、SOP、案例集、方案书等 Markdown 变成"给客户/老板看的成品网页"时使用。
  触发词：渲染成网页、转成 HTML、做成网页、Markdown 转 HTML、美化文档、出个可浏览版、生成报告页。
agent_created: true
---

# md-to-styled-html

把 Markdown 变成**能直接发给别人看的单页 HTML**——不是裸转换，是带设计的成品。

## 什么时候用

- 用户要"可浏览版""网页版""能发出去的成品"
- 交付物是长文：报告、作战手册、SOP、案例集、方案书、调研
- 需要把 Markdown 里的**行动指令/代码块**做成可一键复制的形式

**不要用**：只是想把 md 转 html 给程序消费（那就直接 `markdown` 库转换）。
**不要用**：需要多页站点/路由（那要用真正的静态站点生成器）。

## 用法

```bash
PY=/Users/mac/.workbuddy-ai/binaries/python/envs/default/bin/python
# 首次需要: $PY -m pip install -q markdown

$PY ~/.workbuddy-ai/skills/md-to-styled-html/scripts/render.py \
    "输入.md" "输出.html" --accent amber
```

参数：
| 参数 | 说明 |
|---|---|
| `--accent amber\|teal\|violet\|blue` | 主色调，默认 `amber`（暖橙，适合工业/制造） |
| `--light` | 浅色主题。**默认深色**；IDE 是浅色主题时用这个 |
| `--lang auto\|zh\|en` | 界面文案语言（复制按钮 / 目录标题 / `<html lang>`），默认 `auto` |

**★ `--lang` 是给英文交付物的**：界面文案（Copy / Contents）和正文语言是两回事。
`auto` 按正文中文占比判断（<1% 判为英文）。**渲染英文客户文档时务必核对生成的 HTML 里没有
「复制 / 目录」这类中文按钮** —— 交付给海外客户的页面上出现中文界面文案是硬伤。
改过 `--lang` 相关逻辑后，用 `grep -o 'nav-title">[^<]*' 输出.html` 抽查一下。

## 设计规范（脚本已内置，改前先读）

- **字体**：`-apple-system / PingFang SC / Hiragino Sans GB / Microsoft YaHei`，中文优先
- **正文字号 15px / 行高 1.78** —— 中文长文可读性最佳区间
- **侧栏 264px 固定 + 主栏最大 900px** —— 超过 900px 中文行长会太长
- **`<h2>` 自动进侧栏目录**；标题形如 `案例 1｜xxx`、`步骤 2：xxx`、`Case 3 - xxx` 会**自动卡片化**（圆角头部 + 内容区包裹）并把序号提取成侧栏徽章
- **`<pre>` 自动加复制按钮**（hover 显现，复制后变绿）
- **表格**：圆角边框 + 表头底色 + 行 hover
- **响应式**：≤900px 隐藏侧栏；`@media print` 隐藏导航和复制按钮

## 让标题触发卡片化的写法

```markdown
## 案例 1｜沉睡客户唤醒          ← 卡片 + 侧栏徽章「1」
## 步骤 2：配置参数              ← 卡片 + 徽章「2」
## 附录：常见问题                ← 普通标题，不进徽章样式
```

序号支持半角/全角数字与 `｜ | : ：` 分隔符。**必须用 `##`（h2）**，h3 不触发。

## 常见坑

1. **代码块里的反引号/尖括号** —— 交给 markdown 库处理，不要手工 escape 两遍。
2. **`markdown` 库没装** —— 先 `pip install markdown`，用上面那个 venv 的 python。
3. **中文表格太宽** —— 表头会 `white-space:nowrap`，列多时靠容器横向滚动，别硬塞。
4. **浅色主题忘记加 `--light`** —— 深色页面在浅色 IDE 里会刺眼。
5. **英文交付物忘了 `--lang en`** —— 默认界面文案是中文，给海外客户的页面上会出现「复制 / 目录」。`auto` 一般能判对，但**判完要抽查**。
6. **写完不打开看** —— 生成后必须 `present_files` 给用户看，HTML 会自动开预览面板。

## 完整流程

1. 先写好 Markdown 源文件（**它是唯一真相源**，HTML 是派生产物，改内容改 md 再重渲染）
2. 按目标读者的主题偏好选 `--accent` / `--light`
3. 运行脚本
4. `present_files` 打开 HTML 预览
5. 如果同目录还有 md 源文件，**两个一起交付**（md 给 agent 复用，html 给人看）
