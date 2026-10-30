# 版本与迭代机制

## 版本号（SemVer）
- **MAJOR**：目录结构、配置格式或输出规范不兼容变化（如 v2.0.0 引入 product.json + pipeline.sh）。
- **MINOR**：新能力或新产品类型经验沉淀，向后兼容（如 v1.1.0 大装配体与分片渲染）。
- **PATCH**：脚本修复、文案、参数默认值调整。

## 每次升级必做（Definition of Done）
1. 改 `VERSION`、`SKILL.md` 头部 `version`、`README.md` 标题版本。
2. 在 `CHANGELOG.md` 顶部加条目：日期、版本、来源项目、Added / Changed / Fixed、对旧项目的影响。
3. 新产品的产品相关代码放入 `examples/<code>/`，机构分析放入 `references/`。
4. 同步 4 处：Agent skill（`cad3d-animation-video-landing`）、工作区 `/workspace/skills/cad3d-animation-video-landing/`、
   GitHub `smthelp/smthelp-skill/cad3d-animation-video-landing/`（含 README 技能条目）、Google Drive 技能仓库文件夹。
5. 用最近一个产品做回归：`preview` 两种比例 + `landing` 截图通过即可（不必重渲染 4K）。

## 反馈 → 迭代
- 每个交付项目结束时记录：用户修改意见、耗时最长的阶段、出过的错误 → 写入 CHANGELOG 的 "Lessons"。
- 重复出现 2 次以上的手工改动 → 提升为配置参数或通用脚本（这是 v2.x 抽离 product.json 的依据）。

## 路线图
- ✅ v2.1.0（2026-10-22）：慢动作/字幕映射/版式工具、实例化几何、调试与测速脚本、按比例 R3D。
- v2.2：engine/video/landing 产品参数并入 product.json（groups、motion、explode、anchors、scenes、tour）。
- v2.3：STEP/GLB 输入（occt-import-js / trimesh）。
- v2.4：1440p 预览片供客户确认后再出 4K；可选 GPU/云渲染。
- v2.5：多语言配音与字幕（es/pt/ru/ar）复用同一时间线。
