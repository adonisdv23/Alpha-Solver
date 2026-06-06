# Local LLM Solver Orchestration Retry 005 Observed Failure Fix

- Lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-RETRY-005-OBSERVED-FAILURE-FIX-001`
- Source decision from PR #352: `MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_005_FAIL_REQUIRES_FIX`

Evidence boundary: this PR is a narrow implementation fix plus focused fake-transport tests for retry 005 observed failures. It is not manual smoke execution, runtime smoke evidence, local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, broad runtime readiness evidence, or billing evidence.

## Implementation summary

The implementation is intentionally narrow:

- Added a safe underspecified-clarify allowance that runs only after explicit serious-risk text/field checks and only when risk flags remain allowlisted benign local ambiguity/context labels.
- Added the benign `insufficient` and `planning` risk-flag tokens needed for retry 005 Prompt 2 and Prompt 3 local Python CLI startup planning shapes.
- Hardened boundary phrase detection for positive readiness/evidence-adjacent phrasings such as dashboard readiness, benchmark evidence validation, and evidence-model promotion.
- Added an `expose_gate_fields` control to failed-closed adapter result construction and disabled gate-field exposure for Pass 2 boundary claim failures.

No `/v1/solve`, dashboard, provider fallback, hosted provider path, local model call path, hosted model call path, or evidence-model semantic path was changed.
