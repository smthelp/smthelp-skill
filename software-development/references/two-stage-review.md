# Two-Stage Code Review

Systematic review process for implementation tasks.

## The Two Stages

### Stage 1: Spec Compliance Review
Verify the implementation matches the original specification.

**Reviewer questions:**
- [ ] All requirements from spec implemented?
- [ ] File paths match spec?
- [ ] Function signatures match spec?
- [ ] Behavior matches expected?
- [ ] Nothing extra added (scope creep)?
- [ ] Nothing missing?

**Output:** `PASS` or list of specific gaps to fix.

### Stage 2: Code Quality Review
Verify the implementation is well-built.

**Reviewer dimensions:**
- Style and conventions
- Error handling completeness
- Naming clarity
- Test coverage and quality
- Security (no hardcoded secrets, input validation, etc.)
- Performance concerns

**Output:** `APPROVED` or `REQUEST_CHANGES` with specific issues.

## Why Two Stages

Spec compliance and code quality are orthogonal concerns:
- A PR can be spec-compliant but poorly written
- A PR can be well-written but not match the spec

Reviewing both prevents shipping the wrong thing or shipping the right thing badly.

## Gate Integration

The spec compliance gate is a **Pre-flight Gate** — it must pass before code quality review begins.

The code quality gate is a **Revision Gate** — it may loop multiple times before approval.

If quality issues persist after 2 cycles, escalate to human review.

## Common Mistakes

- **Reviewing quality before spec** — fixing style on code that's doing the wrong thing wastes cycles
- **Reviewing both at once** — mixed feedback is harder to prioritize and track
- **Skipping spec review for "obvious" tasks** — even simple tasks can have subtle spec mismatches
