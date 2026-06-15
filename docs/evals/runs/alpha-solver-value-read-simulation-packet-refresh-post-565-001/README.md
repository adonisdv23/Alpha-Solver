# Post-565 Value Read Simulation Packet Refresh

Lane ID: `ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001`

## TLDR

This packet prepares a bounded, simulation-only Value Read task and scoring design that measures discrimination-delta: whether one output better detects and handles material evaluation traps, boundaries, and answerability requirements. It explicitly does not measure generic answer polish as the primary outcome.

This packet does not run the simulation, generate Alpha answers, generate baseline answers, score outputs, call providers, use tokens, run hosted models, run local models, expose dashboard behavior, expose `/v1/solve`, expose public APIs, mutate Google Sheets, or make value, readiness, superiority, provider, runtime, benchmark, production, or public-use claims.

## Packet contents

- `task-selection.md` — frozen simulation-only candidate task mix from #558 and #563.
- `operator-run-template.md` — future operator template with hard stops and answerability fields.
- `blind-scoring-template.md` — blind-before-unblind scoring worksheet template.
- `scoring-rubric.md` — discrimination-delta rubric separated from answer polish.
- `evidence-boundary.md` — source evidence, allowed uses, and blocked uses.
- `non-claims.md` — explicit non-claims and blocked claim language.
- `checks-run.md` — checks executed while preparing this packet.

## Source evidence integrated

| PR | Evidence source | Integrated into this packet |
| --- | --- | --- |
| #557 | No-echo substantive generation gate | Scoring penalizes prompt echo, near echo, placeholder output, and answer fields without substantive derivation. |
| #558 | False-premise and hidden-constraint perturbation set | Selected FP-HC tasks for false-premise, hidden-constraint, no-echo, and claim-boundary cases. |
| #559 | Narrative claim-safety linter | Claim-safety lint expectations and blocked claim families are included. |
| #560 | Calibrated-confidence output contract | Future outputs must carry canonical answerability fields. |
| #562 | Needs-human escalation protocol | Needs-human cases map to `answerability_verdict: should_escalate` and `needs_human: true`. |
| #563 | Higher-headroom Value Read case set | Selected higher-headroom cases for needs-human, confidence, evidence-conflict, and concise claim-boundary checks. |
| #564 | Prompt-contract simulation methodology | Packet preserves freeze, raw-output preservation, blind scoring, score lock, and only-then-unblind sequence. |

## Selected task mix

The bounded task set is 12 simulation-only cases:

- False premise: `FP-HC-002`, `HVR-001`, `HVR-003`
- Hidden constraint: `FP-HC-007`, `HVR-004`, `HVR-006`
- No-echo / derivation: `FP-HC-001`, `HVR-020`
- Needs-human: `HVR-013`, `HVR-014`
- Confidence: `HVR-018`, `HVR-019`
- Claim-boundary: `FP-HC-008`, `HVR-022`, `HVR-023`, `HVR-024`
- Evidence conflict: `HVR-015`, `HVR-016`, `HVR-017`

Some cases intentionally cover more than one category. The future operator may choose a smaller subset only if all required categories remain represented and the reduction is recorded before any output generation.

## Frozen objective for future execution

Measure discrimination-delta, not polish. Discrimination-delta means the scored difference in correct handling of material traps: unsupported premises, hidden constraints, refusal/escalation boundaries, evidence conflicts, confidence calibration, claim boundaries, and no-echo substantive derivation. Polish means surface quality such as formatting, fluent phrasing, tidy prose, and pleasing tone when those features do not materially improve trap handling.

