# Execution Authorization Template

STATUS: TEMPLATE ONLY - DO NOT EXECUTE FROM THIS FILE ALONE.

Lane ID: `ALPHA-SOLVER-VALUE-EXPERIMENT-EXECUTION-PILOT-001`

An operator must explicitly complete this authorization before any pilot execution.

## Required authorization fields

- Authorization statement: `I authorize ALPHA-SOLVER-VALUE-EXPERIMENT-EXECUTION-PILOT-001 as a NON-DECISIVE pilot.`
- Provider:
- Model:
- Cost cap, in USD:
- Token cap:
- Run count / number of paired tasks:
- Judge method:
- Judge provider/model or human reviewer:
- Confirmation that `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` completed without prompt echo:
- Confirmation that the Alpha path can produce substantive non-echo answers:
- Confirmation that canonical protocol preregistration is complete, frozen, and linked to `docs/evals/runs/alpha-solver-value-experiment-protocol-001/preregistration.md` before execution:
  - Task-bank size:
  - Task-bank freeze timestamp:
  - Baseline prompt hash:
  - Alpha configuration hash:
  - Scoring weights:
  - Tie band:
  - Task quotas / strata:
  - Exclusion rules:
  - Primary judge:
  - Human validation reviewer or plan:
  - Pass/fail criteria:
  - Cost/latency recording plan:
  - Provider/model/cost/token/run caps:
  - No-echo/substantive Alpha generation gate:
- Confirmation that the run is non-decisive and cannot support superiority, benchmark-validation, or product-readiness claims:

## Required stop statement

If any field above is absent or ambiguous, stop before provider calls and return `VALUE_EXPERIMENT_PILOT_BLOCKED_PRECONDITION_MISSING`. If preregistration is incomplete, ambiguous, not frozen, or not linked to the accepted protocol packet at `docs/evals/runs/alpha-solver-value-experiment-protocol-001/preregistration.md`, stop before provider calls and return `VALUE_EXPERIMENT_PILOT_BLOCKED_PRECONDITION_MISSING`.
