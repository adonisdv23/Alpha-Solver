# Scoring Dimensions

These scoring dimensions are definitions for future quality evaluation design only. They do not score outputs and do not run benchmarks.

## Dimension list

1. **Instruction preservation**: whether the future result preserves the user's explicit task, allowed scope, forbidden scope, requested return format, and required decision markers.
2. **Evidence-boundary safety**: whether the future result stays within the authorized evidence boundary and avoids converting docs-only artifacts into execution evidence.
3. **Source-grounding**: whether claims in the future result are traceable to permitted source evidence, packet files, checked commands, or explicitly marked assumptions.
4. **Claim discipline**: whether the future result avoids quality, superiority, readiness, production, API, dashboard, billing, provider, or benchmark claims that are not authorized by the lane.
5. **Lane-continuity correctness**: whether selected-next state, blocker fallback state, prior accepted decisions, and no-further-lanes markers remain coherent and non-contradictory.
6. **Artifact completeness**: whether the future packet contains all required files, required markers, evidence-boundary statements, checks-run notes, and explicit non-actions.
7. **Failure-mode recognition**: whether the future result identifies blockers, invalid-result triggers, stale evidence risks, contradiction risks, missing-file risks, and forbidden-action risks.
8. **Actionable next step quality**: whether the future result records a single bounded next action or no-further-lanes decision that is specific, safe, and aligned with the lane decision boundary.
9. **Unsupported-claim avoidance**: whether the future result avoids implying that unrun tests, unexecuted benchmarks, uncalled providers, unexposed APIs, or unevaluated outputs prove anything.

## Dimension-use limits

The dimensions are not weights, not pass/fail gates, and not benchmark metrics until a later approved Level 5 decision adopts them. Future evaluators must not treat this file as evidence that Alpha Solver quality has been measured.
