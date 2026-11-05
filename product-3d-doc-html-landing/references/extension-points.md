# 扩展点

1. **新章节**：在 `templates/template.html` 加 `<section>` 与占位符 `%%NEW%%`；在 `scripts/build.py` 生成 HTML 并加入 `rep` 字典；数据放 `page.py`（`g('NEW_DATA', [])` 读取）；文字键进 `en_ui.py`。validate 的 placeholders 检查会发现遗漏。
2. **工具卡**（选型器、配置器、产能计算）：`page.py` 的 `TOOL_HTML` + `TOOL_JS`；JS 可用 `T(key)`、`num(id)`、`showStation(i)`；设置 `window.__toolRefresh = fn` 以便切语言时刷新。参考 `examples/pcb-loader-solution/page.py` 的上板机选型器。
3. **3D 适配器**：新建 `templates/viewer_<name>.js`，实现 3d-interaction.md 的契约，在 build.py 的 3D 分支按 `model.mode` 选择。
4. **新模型格式**：`scripts/model_prep.py` 第 1 步加转换分支，输出 `model_raw.glb`；不能转换时 `SystemExit` 说明缺什么工具，不生成假模型。
5. **新验证项**：`scripts/validate.py` 中加 `chk('名称', 条件, 说明)`；浏览器级检查加到 `render_test.py`。
6. **ROI 变体**：模板 ROI 的 `calc()` 读 `rOps/rFreed/rWage/rShifts/rPrice`；产能型 ROI（节省/件、件/时、电费、维护）见 LED T8 页做法：在模板中替换 ROI 区块并在 `config.roi.inputs` 记录字段。
7. **配色/品牌**：`theme.*` 写入 CSS 变量 `--teal/--teal2/--green/--amber`；暗色模式变量在模板 `[data-theme=dark]`。
