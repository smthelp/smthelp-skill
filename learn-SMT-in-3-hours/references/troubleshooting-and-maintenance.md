# Troubleshooting And Maintenance Learning Framework

Use this framework to teach reasoning and records. It does not replace the current manufacturer manual, site safety procedure, training authorization, or qualified service work.

## Safe Diagnostic Sequence

1. State the observed symptom without guessing its cause: location, time, product/program revision, alert wording where available, and the affected process state.
2. Place the equipment and board in the required safe condition under the site procedure. Do not bypass guards, interlocks, warnings, or prescribed isolation steps.
3. Check the current manual, approved setup/process record, and the available alarm, trend, or quality evidence.
4. Perform only the first inspection or corrective action explicitly permitted by the source and the person's authorization.
5. Verify the result through the approved method, record the evidence, and escalate when the cause or authorization is incomplete.

## Symptom-To-Question Matrix

| Symptom family | First learning question | Evidence to inspect | Boundary |
| --- | --- | --- | --- |
| Board-transfer interruption | Is the board/support/handoff state documented and physically understood? | Current transfer setup, recorded status/alarm, board condition | Do not force a board or alter an interface without authorization. |
| Printing-result concern | Is the approved material, alignment, or first-article evidence available? | Approved process record, inspection evidence, stencil/material status where authorized | Do not alter process settings based on a generic chart. |
| Placement-result concern | Are the component supply, approved program revision, and first-article evidence consistent? | Feeder/component identification, program record, inspection result | Do not make unapproved program or hardware changes. |
| Thermal-process concern | Is the authorized thermal process and its verification record available? | Current profile/process record, relevant quality evidence | Do not estimate a profile or change heating controls from a generic lesson. |
| Inspection/reject trend | Does the approved inspection program and disposition path explain the result? | Program revision, result image/data where available, quality procedure | Do not accept, reject, or reclassify product outside the approved rule. |

## Maintenance Card Pattern

```markdown
### Maintenance card: [equipment class or verified model]
- Evidence label: [已验证资料 / 待确认]
- Object and purpose: [what is being checked and why]
- Authorized task: [inspection, cleaning, replacement, calibration check, or other manual-backed action]
- Preconditions: [safe condition and required authorization]
- Source: [current manual page / approved site procedure]
- Record: [date, asset ID, person, observed condition, action, verification]
- Escalate when: [missing source, abnormal condition, safety issue, or task exceeds authorization]
```

Only populate a maintenance frequency, consumable, torque, calibration limit, lubrication instruction, replacement method, or safety isolation detail from a current source. Otherwise leave it `待确认`.

## Common Reasoning Errors

| Weak conclusion | Why it fails | Correct learning response |
| --- | --- | --- |
| An alarm name proves one root cause. | A symptom can have multiple process, setup, material, or equipment causes. | Treat the alarm as an observation and follow the source-backed check path. |
| A generic setting applies to every board. | Board design, materials, components, process approvals, and equipment configuration vary. | Use the approved record or mark the setting `待确认`. |
| A photo proves internal mechanism or capability. | A photo only confirms visible appearance and sometimes process position. | Use it as a labelled visual; seek the manual for internal or performance claims. |
| Restarting is a repair. | It can erase useful state and does not establish the cause. | Preserve required evidence and follow the approved recovery path. |

## Close The Learning Loop

After a fault or maintenance lesson, ask the learner to identify: the safe state, the evidence source, the first authorized check, the confirmation method, and the escalation owner. This demonstrates controlled reasoning without presenting unverified troubleshooting as a field instruction.
