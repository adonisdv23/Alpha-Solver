# Failure Classification

## Classification

`mode-mismatch-after-complete-smoke-run`

## Reason

The retry 004 command completed, artifacts are present, result count is five, each wrapper status is `completed`, and each wrapper error is `null`. The failure is therefore not classified as artifact-incomplete, parse-error, prompt exception, or missing provenance.

The failure is classified as expected-behavior mismatch because:

1. Prompt 2 expected `clarify` but observed `block`.
2. Prompt 3 expected `answer_with_assumptions` but observed `clarify`.

## Decision impact

Under the lane decision rules, a complete executed artifact with one or more expected mode or boundary-behavior check failures selects:

`MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_004_FAIL_REQUIRES_FIX`
