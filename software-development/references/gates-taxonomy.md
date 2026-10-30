# Gates Taxonomy

The four canonical gate types used in multi-stage review workflows.

## Gate Types

### 1. Pre-flight Gate
**Entry condition:** Task created or worker spawned.
**Failure behavior:** Task stays blocked, worker exits with error.
**Recovery:** Fix the prerequisite, re-trigger.

### 2. Revision Gate
**Entry condition:** Worker completes work, submits for review.
**Failure behavior:** Reviewer requests changes, worker re-spawned with feedback.
**Recovery:** Address feedback, re-submit.

### 3. Escalation Gate
**Entry condition:** Revision gate repeated N times without resolution.
**Failure behavior:** Task blocked for human review.
**Recovery:** Human resolves, unblocks, or archives.

### 4. Abort Gate
**Entry condition:** Unrecoverable error or hard constraint violated.
**Failure behavior:** Task archived, no retry.
**Recovery:** Human intervention required to restart.

## Behavior

Each gate has:
- **Entry condition** — what triggers it
- **Failure behavior** — what happens on failure
- **Recovery** — how to get unblocked

## Usage

Use explicit gate vocabulary in orchestrator prompts so each validation checkpoint has defined entry, failure behavior, and resumption rules. Example:

```
This task has 2 gates:
1. Pre-flight: validate credentials exist before starting
2. Revision: independent reviewer approves before proceeding
```

Adapted from gsd-build/get-shit-done (MIT © 2025 Lex Christopherson).
