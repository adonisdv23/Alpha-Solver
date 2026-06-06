# Local LLM Solver Orchestration Retry 005 Observed Failure Fix

- Lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-RETRY-005-OBSERVED-FAILURE-FIX-001`
- Source decision from PR #352: `MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_005_FAIL_REQUIRES_FIX`

Evidence boundary: this PR is a narrow implementation fix plus focused fake-transport tests for retry 005 observed failures. It is not manual smoke execution, runtime smoke evidence, local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, broad runtime readiness evidence, or billing evidence.

## Risk flag preservation summary

Preserved risk behavior:

- Explicit high-risk prompt text still blocks.
- Serious Pass 1 risk flags and serious Pass 1 field text still block.
- Unknown and non-allowlisted risk flags still block for normal answer paths.
- The safe underspecified clarify route is limited to benign low-risk labels and does not expose model normal fields or call Pass 2.

The only benign additions are `insufficient` and `planning`, both scoped to local ambiguity/context and Python CLI startup/performance/profiling planning shapes covered by fake-transport tests.
