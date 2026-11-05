# 升级路径

## 版本规则
- `VERSION` 与 SKILL.md front matter 的 `version` 同步；语义化版本：
  - PATCH：修 bug、文案规则、验证项微调
  - MINOR：新增语言、新 3D 适配器、新章节、新配置项（默认值保持旧行为）
  - MAJOR：模板结构或 i18n 键改名（旧页面需迁移）
- 每次变更写 `CHANGELOG.md`；推送到 smthelp/smthelp-skill 同名目录，并打 zip 备份。

## 新增语言（MINOR）
1. `config.languages` 追加 `[de, Deutsch]`；RTL 语言（如 he、fa、ur）同时加入 `rtl_languages`，模板 `apply()` 已按该列表设置 `dir=rtl`。
2. `i18n_tools.py add-lang <work> de` → `todo_de.json` → 翻译子代理 → `out_de.json` → `merge`。
3. 需要时补 `font-family`（如泰文、印地文字体）。
4. build → validate（languages、i18n keys、hreflang 会自动覆盖新语言）→ render_test 加 `?lang=de`。

## 新模板 / 配色（MINOR）
- 仅换色：项目 `config.theme`。
- 新版式：复制 `templates/template.html` 为 `template_<name>.html`，保留所有 `%%占位符%%` 与 `data-i18n` 键名，在 config 增加 `page.template` 并在 build.py 读取；validate 对两套模板通用。

## 新 3D 交互能力（MINOR）
- 例如热点标注、剖切、测量、AR（model-viewer）、滚动驱动动画：
  1. 在 viewer 中实现并暴露 `window.__<能力>()`；
  2. 模板 `.ctl` 加按钮（默认 `hidden`），参照 `__ctl3d` 绑定；
  3. i18n 加按钮与状态键；
  4. `config.model.interactions` 登记；`references/3d-interaction.md` 补契约；
  5. render_test 加点击与截图。

## 迁移旧页面
- 旧页面源码（work/*-src）只需：把数据段移入 `page.py`、配置移入 `config.yaml`、`rack3d.js`/`loader3d.js` 设为 `model.procedural_js`，即可用新 build.py 重建。
