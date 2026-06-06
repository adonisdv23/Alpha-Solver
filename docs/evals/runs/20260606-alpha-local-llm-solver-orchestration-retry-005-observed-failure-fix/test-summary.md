# Local LLM Solver Orchestration Retry 005 Observed Failure Fix

- Lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-RETRY-005-OBSERVED-FAILURE-FIX-001`
- Source decision from PR #352: `MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_005_FAIL_REQUIRES_FIX`

Evidence boundary: this PR is a narrow implementation fix plus focused fake-transport tests for retry 005 observed failures. It is not manual smoke execution, runtime smoke evidence, local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, broad runtime readiness evidence, or billing evidence.

## Test summary

Updated fake-transport tests cover:

- Retry 005 Prompt 2 safe underspecified clarify with no Pass 2 and no model field exposure.
- Retry 005 Prompt 2 serious-risk guard with no Pass 2 and no normal field exposure.
- Retry 005 Prompt 3 bounded Python CLI startup/performance/profiling assumption path.
- Retry 005 Prompt 3 guard cases for low or unparseable confidence, empty or unbounded assumptions, too much missing information, serious risk, boundary claims, and unknown risk flags.
- Retry 005 Prompt 5 Pass 1 boundary phrasings.
- Retry 005 Prompt 5 Pass 2 boundary failure suppression of gate considerations and assumptions.
- Existing direct, high-risk block, boundary, non-exposure, `/v1/solve`, dashboard, no-hosted-fallback, and non-evidence invariants.
