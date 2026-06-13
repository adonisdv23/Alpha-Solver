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
- Confirmation that the run is non-decisive and cannot support superiority, benchmark-validation, or product-readiness claims:

## Required stop statement

If any field above is absent or ambiguous, stop before provider calls and return `VALUE_EXPERIMENT_PILOT_BLOCKED_PRECONDITION_MISSING`.
