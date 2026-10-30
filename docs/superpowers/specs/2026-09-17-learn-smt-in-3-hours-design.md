# learn-SMT-in-3-hours Design

## Purpose

Create an independent Southern Machinery learning skill for beginners and practitioners who need a diagram-led, three-hour introduction to SMT automation equipment. The skill produces a learning package, not a fixed product brochure or an unattended machine-operation instruction.

## Architecture

The entry point contains selection, evidence, safety, and output rules. Four references hold the time-boxed curriculum, diagram grammar, process-and-operation concepts, and fault-and-maintenance framework. This keeps routine invocations short while allowing a focused deep read for a requested module.

```text
SKILL.md
  -> curriculum.md                  learning order and time budget
  -> visual-language.md             diagram selection and labels
  -> process-and-operations.md      equipment, principles, parameters, flow
  -> troubleshooting-and-maintenance.md  fault and maintenance boundaries
```

## Requirements

- Directory display name: `learn-SMT-in-3-hours`; YAML name is normalized to lowercase for Agent Skills validation.
- Cover board handling, printing, inspection where applicable, placement, soldering, final inspection, buffering/unloading, and adjacent peripherals as applicable to the documented line.
- Teach functions, structure/principles, parameter categories, operating checkpoints, maintenance/fault reasoning, and inter-equipment coordination in a 180-minute learning sequence.
- Use Markdown explanation plus diagrams. Diagrams can be Mermaid or source-grounded image briefs; each must say whether it is a conceptual schematic, verified-source representation, or pending confirmation.
- Do not present a model, numerical setting, capacity, compatibility, certification, commercial term, or maintenance interval as fact without current source support.
- Do not recommend bypassing guarding, interlocks, lockout procedures, or manufacturer maintenance instructions.

## Validation

- The official quick validator accepts `SKILL.md` frontmatter.
- Every reference linked from `SKILL.md` exists.
- Content checks confirm all requested knowledge areas, the 180-minute route, diagram requirements, evidence labels, and safety boundaries.
- The post-change inventory shows exactly one new skill entry and no modification to unrelated skills.
