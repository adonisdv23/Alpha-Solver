# Stop-State Handling

A future local-only harness must treat stop states as first-class outcomes rather than exceptions to bypass.

## Required stop states

- `PREFLIGHT_FAILED`: a required local preflight did not pass.
- `TASK_OUT_OF_SCOPE`: the requested task is not bounded or not local-only.
- `FORBIDDEN_EXTERNAL_ACTION_REQUESTED`: the task requested provider calls, hosted model calls, local model execution without later explicit local-only implementation authorization, external API calls, fallback, dashboard exposure, `/v1/solve` exposure, deployment, browser control, credential use, billing, or evidence promotion.
- `COMMAND_NOT_ALLOWLISTED`: the requested command is not approved for local execution.
- `TIMEOUT_EXCEEDED`: the local task exceeded the configured timeout.
- `OUTPUT_LIMIT_EXCEEDED`: stdout, stderr, or generated artifacts exceeded configured limits.
- `ARTIFACT_CAPTURE_FAILED`: the harness could not write required local artifacts.
- `REDACTION_REQUIRED`: secret-like material appeared in an output and requires local operator review before sharing.
- `TASK_FAILED`: the local command completed with a non-zero exit status.
- `TASK_PASSED`: the local command completed successfully within the approved boundary.

## Stop-state behavior

For every stop state, the future harness should:

1. Stop additional execution unless the state is `TASK_PASSED` and no post-run boundary issue exists.
2. Capture the stop state in the local artifact directory.
3. Record which requirement triggered the state.
4. Avoid automatic retries that could expand scope.
5. Avoid provider calls, hosted model calls, local model execution without later explicit local-only implementation authorization, external API calls, fallback, deployments, dashboard exposure, `/v1/solve` exposure, browser control, credential access, billing, and evidence promotion.
6. Tell the operator which separate authorized lane would be needed for remediation if remediation is outside the local-only boundary.

## Fail-closed requirement

Ambiguous states must resolve to stop, not continue. If the harness cannot determine whether an action is local-only and bounded, it must emit `TASK_OUT_OF_SCOPE` or `FORBIDDEN_EXTERNAL_ACTION_REQUESTED` and stop.
