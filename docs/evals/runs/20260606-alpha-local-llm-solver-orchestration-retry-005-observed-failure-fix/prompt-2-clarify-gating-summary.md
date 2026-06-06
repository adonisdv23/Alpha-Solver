# Local LLM Solver Orchestration Retry 005 Observed Failure Fix

- Lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-RETRY-005-OBSERVED-FAILURE-FIX-001`
- Source decision from PR #352: `MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_005_FAIL_REQUIRES_FIX`

Evidence boundary: this PR is a narrow implementation fix plus focused fake-transport tests for retry 005 observed failures. It is not manual smoke execution, runtime smoke evidence, local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, broad runtime readiness evidence, or billing evidence.

## Prompt 2 clarify gating summary

Prompt: `Make it faster.`

The gate now checks serious high-risk prompt text and Pass 1 fields first. If those are absent and the prompt is underspecified, the runner can return the existing clarify response without exposing model-produced considerations or assumptions and without calling Pass 2.

Unknown, non-allowlisted, or serious risk flags still block outside this narrow safe-clarify allowance. Serious risk flags in Prompt 2-style fields still block with empty normal output fields.
