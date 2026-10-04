---
name: smthelp-remotion-animation-workflow
description: "Southern Machinery 产品动画制作工作流 — 从源码编写到渲染输出的完整流程。包含 Remotion 项目搭建、常见错误修复、邮件发送方案。"
whenToUse: "remotion 动画，产品视频 渲染，remotion render failed，SMTP blocked email send"
metadata:
  source: hermes
  origin: "media/smthelp-remotion-animation-workflow"
---
# Southern Machinery Remotion 动画制作工作流

## 已知问题与修复

### 1. index.ts 文件换行符问题（Critical）
**问题**：`execute_code` 写 Python 字符串时，`\n` 变成字面量而非真实换行符，导致 esbuild 报 `Syntax error "n"`  
**错误**：`import { registerRoot } from "remotion";\nimport { ... }`（字面 `\n` 字符串）  
**修复**：必须用 `write_file` 工具直接写 TypeScript 文件

```python
# ❌ 错误 — execute_code 中的 \n 是字面量
content = 'import { registerRoot } from "remotion";\nimport { X } from "./MyComp";'

# ✅ 正确 — 用 write_file 工具
write_file(path="/tmp/project/src/index.ts", content='import { registerRoot } from "remotion";\nimport { X } from "./MyComp";\n')
```

### 2. Remotion npm 包版本不存在
**问题**：`@remotion/bundler@4.0.283` 在 npm registry 不存在  
**修复**：所有 remotion 包用 `"latest"` 版本号

```json
"dependencies": {
  "@remotion/cli": "latest",
  "@remotion/bundler": "latest",
  "@remotion/media": "latest",
  "remotion": "latest"
}
```

### 3. Peer Dependency 冲突
**修复**：安装时加 `--legacy-peer-deps`
```bash
cd /tmp/remotion-project && npm install --legacy-peer-deps
```

### 4. 组件名未定义（ReferenceError）
**问题**：代码中引用了 `<MachineSVG>` 但未定义  
**修复**：确保组件名与引用完全一致；推荐在写代码前先列出所有组件名

### 5. SMTP 服务器全部被墙
**现象**：smtp.viwolf.cn、smtp.gmail.com 等连接全部被防火墙阻断（connection closed / timeout）  
**备用方案 A**：上传到 tmpfiles.org 获取下载链接
```bash
curl -F "file=@/path/to/video.mp4" https://tmpfiles.org/api/v1/upload
# 返回 {"status":"success","data":{"url":"http://tmpfiles.org/xxx/file.mp4"}}
```

**备用方案 B**：系统有 `/usr/sbin/sendmail`，但邮件发到本地 mailbox，不适合对外发送

**推荐方案**：将视频复制到用户本地 `~/Downloads/`，让用户手动发送
```bash
cp /tmp/remotion-project/out/Video.mp4 ~/Downloads/
```

---

## 完整制作流程

### Step 1：创建项目目录结构
```python
import os
for path in ["/tmp/remotion-product"]:
    os.makedirs(f"{path}/src", exist_ok=True)
```

### Step 2：写 package.json（用 latest 版本）
```json
{
  "dependencies": {
    "@remotion/cli": "latest",
    "@remotion/bundler": "latest",
    "@remotion/media": "latest",
    "remotion": "latest",
    "react": "18.2.0",
    "react-dom": "18.2.0"
  }
}
```

### Step 3：写 tsconfig.json + remotion.config.ts
```json
{ "compilerOptions": { "jsx": "react-jsx", "strict": true } }
```

### Step 4：写动画源码（MyComp.tsx）用 write_file
- 用 `useCurrentFrame()` + `interpolate()` 控制动画
- 用 `Sequence` 控制分镜
- 颜色常量放顶部便于统一修改

### Step 5：写入口文件（index.ts）用 write_file
```typescript
import { registerRoot } from "remotion";
import { MyComp } from "./MyComp";
registerRoot(MyComp);
```

### Step 6：安装依赖
```bash
cd /tmp/remotion-product && npm install --legacy-peer-deps
```

### Step 7：渲染
```bash
cd /tmp/remotion-product && npx remotion render MyComposition out/MyVideo.mp4 --quality=0
```

---

## 标准动画结构模板

```typescript
const DURATION = 15 * 60; // 900 frames @ 60fps = 15 seconds

export const MyProduct: React.FC = () => (
  <Composition
    id="MyProduct"
    component={MainScene}
    durationInFrames={DURATION}
    fps={60}
    width={1920}
    height={1080}
  />
);

const MainScene: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#0a0e1a" }}>
    <Sequence from={0} durationInFrames={90}><TitleScene /></Sequence>
    <Sequence from={90} durationInFrames={210}><SpecsScene /></Sequence>
    <Sequence from={300} durationInFrames={330}><PrincipleScene /></Sequence>
    <Sequence from={630} durationInFrames={180}><ROIScene /></Sequence>
    <Sequence from={810} durationInFrames={90}><CTAScene /></Sequence>
  </AbsoluteFill>
);
```

## 常用动画公式

```typescript
// 淡入+上移
const opacity = interpolate(f, [0, 30], [0, 1], { extrapolateRight: "clamp" });
const y = interpolate(f, [0, 30], [20, 0], { extrapolateRight: "clamp" });

// 缩放弹出
const scale = interpolate(f, [0, 25], [0.85, 1], { 
  extrapolateRight: "clamp", easing: Easing.out(Easing.back(1.5)) 
});

// 数字滚动
const count = Math.min(
  Math.floor(interpolate(f, [20, 120], [0, targetValue])),
  targetValue
);

// 循环动画
const cycleF = f % cycleDuration;
```
