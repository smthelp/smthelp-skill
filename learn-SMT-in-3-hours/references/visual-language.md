# Visual Language For SMT Learning

Each visual must answer one operational question. Do not decorate pages with unlabeled machine silhouettes or imply that a conceptual schematic is a specific Southern Machinery model.

## Visual Selection Map

| Learner question | Preferred diagram | Minimum labels |
| --- | --- | --- |
| What is the route through the line? | Process flow | Station class, board direction, optional/required/`待确认` state |
| What is inside a station conceptually? | Structure or mechanism map | Input, actuator/process element, sensing/check, output |
| Which material or signal moves? | Material/control flow | Board, paste, component, recipe/state, inspection result |
| Why does a parameter matter? | Causality map | Parameter category, affected process, symptom/risk, verification |
| How do I respond to a symptom? | Fault tree | Safe state, observed symptom, first source-backed check, escalation |
| What should I maintain? | Maintenance card | Object, approved task type, record evidence, manual/qualified-person boundary |
| Where do stations depend on each other? | Coordination swimlane | Upstream condition, handoff, downstream condition, feedback loop |

## Diagram Rules

- Put the evidence label in the title: `概念示意`, `已验证资料`, or `待确认`.
- Use arrows only for a named flow: board movement, material, information, quality decision, or escalation.
- Mark any optional station as `可选`, and any unverified station as `待确认`; do not silently place it in the line.
- Limit a single teaching diagram to one central question. Split a dense diagram into a process map and a separate mechanism or causality map.
- Never label an unverified numerical value, model name, certification, or exact maintenance interval.

## Editable Process Template

```mermaid
flowchart LR
    A[上板与板件准备] --> B[印刷]
    B --> C{配置了印刷后检验?}
    C -->|是| D[检验]
    C -->|否| E[贴装]
    D --> E
    E --> F[回流焊]
    F --> G{配置了后段检验?}
    G -->|是| H[检验与结果反馈]
    G -->|否| I[缓存、下板或下游工序]
    H --> I
```

Use this as a `概念示意`. Replace labels only after confirming the actual configuration. A real line can add, remove, reorder, or bypass stations according to its documented process.

## Parameter-Causality Template

```mermaid
flowchart TD
    A[参数类别] --> B[受影响的工艺动作]
    B --> C[可观察的质量或节拍信号]
    C --> D[依据来源的验证方法]
    D --> E{结果符合已验证要求?}
    E -->|是| F[记录并继续监控]
    E -->|否| G[保持安全状态并按手册/工程路径处理]
```

## Fault-Tree Template

```mermaid
flowchart TD
    A[异常现象] --> B[先使设备处于规定安全状态]
    B --> C{有当前手册和报警/趋势记录?}
    C -->|有| D[执行手册允许的第一项检查]
    C -->|无| E[记录现象、批次和时间并升级]
    D --> F{原因已被证据确认?}
    F -->|是| G[执行已授权的纠正与验证]
    F -->|否| E
```

## Source-Grounded Image Brief

When a raster illustration is needed, write a brief before generating or selecting it:

```markdown
### Visual brief: [topic]
- Purpose: [the learner question this visual answers]
- Evidence label: [已验证资料 / 概念示意 / 待确认]
- Source: [current file path, page/slide, or `none - conceptual schematic`]
- Visible facts to retain: [only items plainly supported by the source]
- Required labels: [short, source-backed labels]
- Exclusions: [no model number, value, certification, or hidden configuration unless verified]
```

If the image cannot be made source-grounded, use an editable conceptual diagram instead.
