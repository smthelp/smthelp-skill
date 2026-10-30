# Three-Hour SMT Automation Curriculum

Use this route as a learning-time budget, not as a production standard. Rebalance minutes only when the learner has selected a documented focus. Total planned time is 180 minutes.

| Time | Module | Learner outcome | Required visual |
| --- | --- | --- | --- |
| 0-15 min | System orientation | Explain why an SMT line is a connected process rather than a collection of machines. | End-to-end process map |
| 15-35 min | Board handling and printing | Identify board movement, stencil-printing purpose, handoffs, and relevant checks. | Material-flow diagram |
| 35-55 min | Inspection before placement | Explain where solder-paste or incoming checks may sit and why a configured line may omit a station. | Optional-station map |
| 55-90 min | Placement system | Describe feeders, component supply, vision/alignment concept, motion system, and placement verification at a conceptual level. | Placement-system anatomy |
| 90-115 min | Reflow and thermal process | Connect profile validation, transport, heating/cooling zones, and solder-joint outcome without inventing recipe values. | Parameter-causality map |
| 115-135 min | Post-process inspection and handling | Distinguish inspection, buffering, routing, and downstream handoff. | Quality-loop diagram |
| 135-155 min | Parameters and operating checkpoints | Use parameter categories, pre-start checks, changeover controls, and first-article logic. | Checkpoint card |
| 155-172 min | Faults and preventive maintenance | Trace a symptom to a safe preliminary check, evidence, and escalation route. | Fault tree and maintenance card |
| 172-180 min | Line coordination recap | Locate a likely bottleneck, a handoff dependency, and the next source to verify. | Coordination swimlane |

## Lesson Pattern

For every module, use the same five-part pattern so learners can scan and compare.

1. **What moves or changes:** board, solder paste, component, heat, image, or production state.
2. **Why the station exists:** the process problem it controls.
3. **How it works:** a labelled conceptual mechanism, not a hidden machine-specific claim.
4. **What to watch:** parameter category, operation checkpoint, quality signal, and escalation boundary.
5. **What connects next:** upstream input, downstream expectation, and a possible effect on line flow.

## Completion Checks

The learner should be able to answer these questions without relying on an unverified number or model claim.

- Can I trace a board and its process state from loading to the configured downstream handoff?
- Can I explain the difference between a device function, a parameter category, and a validated setpoint?
- Can I name one upstream and one downstream dependency for printing, placement, reflow, and inspection?
- Can I choose a safe first check for a common symptom and state when to escalate?

## Adaptation Rules

- For a new learner, keep every module and prefer conceptual diagrams.
- For an operator refresher, retain the 180-minute total but emphasize source-backed operation and fault modules.
- For an engineer or buyer, retain the system map and replace general device cards with current source-backed comparison cards.
- A machine-specific module requires the current manual, specification, or engineering confirmation. Otherwise use `待确认` rather than an estimated setting.
