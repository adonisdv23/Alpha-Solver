# Failure Classification

## Selected classification

`MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_003_FAIL_REQUIRES_FIX`

## Why this is not blocked or incomplete

The required artifact files are present, the primary JSON is parseable, provenance is recorded, the runner exit status is `0`, there are five results, every prompt-level outer status is `completed`, and every prompt-level `error` field is `null`.

## Why this is not a narrow pass

The expected smoke behavior did not fully pass:

- Prompt 2 expected `mode=clarify` but observed `mode=block`.
- Prompt 3 expected `mode=answer_with_assumptions` but observed `mode=block`.

Prompt 1, Prompt 4, and Prompt 5 satisfied their expected outcomes, but the decision rules require all expected smoke modes/outcomes to pass before selecting the narrow pass decision.

## Failure class

The failure is an observed behavior/mode mismatch in an otherwise complete and interpretable preserved artifact. It is not an artifact preservation failure, parse failure, provenance failure, prompt-level exception, local model quality claim, or hosted provider claim.
