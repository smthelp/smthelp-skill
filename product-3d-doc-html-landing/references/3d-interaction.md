# 3D 交互

## 适配器契约（模板 ↔ 3D 脚本）
| 全局 | 方向 | 说明 |
|---|---|---|
| `window.__mode3d(i)` | 模板→3D | 模式按钮 i（0 起）。程序化：重建机构；GLB：切相机预设/爆炸 |
| `window.__reset3d()` | 模板→3D | 复位视角 |
| `window.__rot` | 模板→3D | 自动旋转开关（布尔） |
| `window.__flow` | 模板→3D | 动画播放/暂停（布尔） |
| `window.__mat()` | 3D 定义 | 切下一种材质，返回 i18n 键（mat_*）；定义后模板显示"材质"按钮 |
| `window.__light()` | 3D 定义 | 切下一种光照，返回 i18n 键（light_*）；定义后显示"光照"按钮 |
| `window.__ctl3d()` | 模板定义 | 3D 脚本在定义 __mat/__light 后调用一次，绑定按钮 |
| `window.__fed(n, cycle)` | 3D→模板 | 可选：计数显示（如"已上板 n · 节拍 ≈ cycle s"） |
| `#fb` | 模板 | WebGL 或模型加载失败时显示的回退图 |

## viewer_glb.js（模型模式）
- GLTFLoader + DRACOLoader（gstatic 解码器）+ MeshoptDecoder；RoomEnvironment 环境光；ACES 色调映射；阴影地面。
- 自动按包围盒归一化：`views` 坐标单位 = 模型最大尺寸，`target` 相对包围盒中心。
- 材质：原始 / 金属 / 白模 / 透视（X-ray）/ 线框；光照：影棚 / 暖光车间 / 夜间产线（关环境贴图）。
- 爆炸视图：`explode` 0–1，网格沿各自中心方向外移。
- 模型自带动画（AnimationMixer）随 `__flow` 播放。
- 缺法线自动补算；不可见时停止渲染（IntersectionObserver）。

## 程序化模式
- 参考 `viewer_procedural_example.js`：每个模式一个参数对象（板尺寸、节拍、机构类型），`build(m)` 生成几何，`step(dt)` 按节拍相位插值（推板、电梯步进、吸盘升降平移、机器人取放），出板后沿下游输送带移动。
- 只用 Box/Cylinder 等基础几何，保持脚本 < 15 KB。
- 页面标注 "Concept illustration; not to scale"。

## 轻量化目标
| 项 | 目标 |
|---|---|
| 内嵌 GLB | ≤ 350 KB（`max_inline_kb`），超出则托管并填 `model.url` |
| 三角面 | ≤ 6 万（单产品）/ ≤ 15 万（整线） |
| 纹理 | ≤ 1024 px，webp |
| 压缩 | meshopt（解码器小、加载快）；draco 适合纯几何大模型 |
