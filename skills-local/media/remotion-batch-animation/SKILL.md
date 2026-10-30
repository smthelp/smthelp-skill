---
name: remotion-batch-animation
description: How to create multiple Remotion product animations efficiently — batch project setup, template-based source writing, and quota-constrained rendering workflow.
metadata:
  tags: remotion, animation, batch, product-video, execute-code
---

# Remotion Batch Animation Workflow

## Problem

Creating 8+ product animation videos via `npx create-video@latest` is too slow (1-3 min per project × 8 = 25+ min of just scaffolding).

## Solution: Pre-created Directories + Direct Source Writing

### Step 1 — Create ONE reference project with `create-video`

```bash
npx create-video@latest
# Choose "Hello World" template
# Name it (e.g., remotion-sld-loader)
```

### Step 2 — Copy the directory structure for each new product

Do NOT run `create-video` again. Instead, copy the reference directory:

```bash
cp -r /tmp/remotion-sld-loader /tmp/remotion-svl-loader
cp -r /tmp/remotion-sld-loader /tmp/remotion-slvv-combo
cp -r /tmp/remotion-sld-loader /tmp/remotion-buffer-conveyor
# ... etc
```

This preserves `node_modules`, `package.json`, `tsconfig.json`, and `remotion.config.ts` — no need to reinstall.

### Step 3 — Write animation source code directly via Python

Use `execute_code` (Python) to write `src/MyComp.tsx` and `src/index.ts` directly. Do NOT use `npx create-video`.

```python
comp_code = '''import React from "react";
import { Composition, AbsoluteFill, Sequence, useCurrentFrame, interpolate } from "remotion";

const DURATION = 15 * 60; // 15-second loop at 60fps

export const MyComp: React.FC = () => (
  <Composition
    id="ProductAnimation"
    component={Scene}
    durationInFrames={DURATION}
    fps={60}
    width={1920}
    height={1080}
  />
);

const Scene: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#1a1a2e", fontFamily: "Arial" }}>
    <div style={{ position: "absolute", width: "100%", height: "100%",
      background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)" }} />
    <Sequence from={0} durationInFrames={DURATION}><Title /></Sequence>
    <Sequence from={30} durationInFrames={DURATION - 60}><Animation /></Sequence>
    <Sequence from={DURATION - 90} durationInFrames={90}>
      <Caption name="Product Name" cn="中文名" sub="key specs" />
    </Sequence>
  </AbsoluteFill>
);
'''

with open("/tmp/remotion-product/src/MyComp.tsx", "w") as f:
    f.write(comp_code)
with open("/tmp/remotion-product/src/index.ts", "w") as f:
    f.write('import { registerRoot } from "remotion";\nimport { MyComp } from "./MyComp";\nregisterRoot(MyComp);\n')
```

### Step 4 — Render when quota allows

Quota is often exhausted for `delegate_task` and Remotion CLI. Workaround:

1. Write ALL source files first via `execute_code` (may still work when quota exhausted)
2. Render later when quota is restored:

```bash
cd /tmp/remotion-product && npm run build 2>&1 | tail -5
```

Or locally on your machine using the project files in `/tmp/remotion-*/`.

---

## Animation Template Structure

```typescript
const DURATION = 15 * 60; // 900 frames @ 60fps = 15 seconds

const COLORS = {
  background: "#1a1a2e",
  accent: "#4ecca3",      // green
  highlight: "#e94560",   // red
  info: "#74b9ff",        // blue
  purple: "#a29bfe",
  yellow: "#fdcb6e",
};

// Standard title fade-in (frames 0-30)
const Title: React.FC = () => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const ty = interpolate(f, [0, 30], [20, 0], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", top: 60, left: 0, right: 0,
      textAlign: "center", opacity: o, transform: `translateY(${ty}px)` }}>
      <div style={{ color: "#e94560", fontSize: 28, fontWeight: "bold", letterSpacing: 4 }}>
        SMT PERIPHERAL EQUIPMENT
      </div>
      <div style={{ color: "#4ecca3", fontSize: 42, fontWeight: "bold", letterSpacing: 8, marginTop: 8 }}>
        PRODUCT NAME
      </div>
      <div style={{ color: "#74b9ff", fontSize: 24, marginTop: 8 }}>中文名</div>
    </div>
  );
};

// Caption at end (last 90 frames)
const Caption: React.FC<{ name: string; cn: string; sub: string }> = ({ name, cn, sub }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", bottom: 40, left: 0, right: 0, textAlign: "center", opacity: o }}>
      <div style={{ display: "inline-block", padding: "15px 50px",
        backgroundColor: "rgba(45,52,54,0.9)", borderRadius: 10, border: "2px solid #4ecca3" }}>
        <div style={{ color: "#4ecca3", fontSize: 32, fontWeight: "bold", letterSpacing: 4 }}>{name}</div>
        <div style={{ color: "#a29bfe", fontSize: 16, marginTop: 5 }}>{cn} — {sub}</div>
      </div>
    </div>
  );
};
```

---

## Key Remotion Hooks

```typescript
useCurrentFrame()                    // Current frame number
interpolate(value, [inputRange], [outputRange], { extrapolateLeft/Right: "clamp" | "extend" })
Sequence                             // <Sequence from={0} durationInFrames={30}>...</Sequence>
AbsoluteFill                         // Full canvas container
```

---

## Known Constraints

- **Quota exhaustion**: `delegate_task` and Remotion CLI require AI-tier quota.
  - Source files CAN be written via `execute_code` (uses code interpreter, may still work)
  - Rendering (`npm run build`) MUST wait for quota top-up
- **`npx create-video` is slow** — never use for batch. Copy directories instead.
- **90s timeout** for `terminal` commands using `notebooklm` CLI

---

## Southern Machinery Products (already created)

| Product | Directory | Status |
|---------|-----------|--------|
| SLD Standard Loader | `/tmp/remotion-sld-loader/` | ✅ Rendered (out.mp4 exists) |
| SVL Vacuum Loader | `/tmp/remotion-svl-loader/` | Source written |
| SLD-V Combo Loader | `/tmp/remotion-slvv-combo/` | Source written |
| Buffer Conveyor S-350C/460C | `/tmp/remotion-buffer-conveyor/` | Source written |
| NG/OK Sorter SBM/SBN | `/tmp/remotion-ng-ok-sorter/` | Source written |
| SUL Unloader | `/tmp/remotion-sul-unloader/` | Source written |
| SP Stencil Printer | `/tmp/remotion-sp-printer/` | Source written |
| SME5200 Pallet Cleaner | `/tmp/remotion-smt-cleaner/` | Source written |
| STF1003 Tube Feeder | `/tmp/remotion-stf-feeder/` | Source written |
