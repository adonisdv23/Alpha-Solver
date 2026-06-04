# Minimal Contract Decision

Lane ID: `ALPHA-MINIMAL-CONTRACT-REFINEMENT-DECISION-001`

Status: final contract decision for the current update plan.

## Source interpretation artifact

- `docs/evals/runs/20260604-post-minimal-behavior-finalization/post-improvement-interpretation.md`

## Decision

Decision: **Refine current contract**.

## Recommended next lane

Recommended next lane: `ALPHA-BREVITY-CONTROL-REFINEMENT-001`.

## Rationale tied to interpretation

The post-improvement interpretation classifies the result as **B. Mixed improvement with brevity/control concern**. The unblinded scored result is directionally positive for Alpha: Alpha 314, plain 303, Alpha-minus-plain +11, Alpha wins 5, plain wins 1, and 2 ties. That supports keeping the minimal portable behavior contract as the base rather than reverting it.

The same interpretation does not support freezing the contract unchanged. The aggregate margin is modest, several row-level outcomes are narrow or tied, the preserved blind-scoring defects include format-friction and comparable-output caveats, and the current scored table shows a small aggregate brevity-dimension deficit for Alpha. The prior Batch B diagnostic also identified brevity/control as a recurring weakness even where Alpha produced lift.

The appropriate decision is therefore to refine the current contract, with a narrow focus on concise, answer-first restraint and low-headroom control. The refinement should preserve the beneficial claim-boundary, evidence-hygiene, hidden-constraint, artifact-discipline, and risk-framing behavior while reducing unnecessary expansion.

## What remains blocked

- Batch C execution
- runtime-readiness decision or runtime measurement
- `/v1/solve` measurement
- provider calls, provider-adapter changes, model configuration changes, or routing changes
- Google Sheets update from this repo task
- production-readiness documentation
- broad validation or superiority claims
- scored-artifact edits, rescoring, capture reruns, or alternate unblinding-map application

## Non-claims

This decision does not claim:

- `/v1/solve` behavior changed or improved
- runtime API behavior changed or improved
- provider behavior changed or improved
- model routing behavior changed or improved
- production-readiness
- broad runtime-readiness
- MVP-validating evidence
- benchmark-level success
- billing-accuracy proof
- provider-orchestration behavior
- self healing behavior
- adaptive-learning behavior
- autonomous-optimization behavior
- broad Alpha-vs-plain generalization
- broad plain-provider weakness
