# Stop-State Handling

## Stop-state purpose

A future local-only harness should stop predictably when a preflight, command, artifact, or boundary condition fails. Stop handling must favor safety, traceability, and human review over autonomous continuation.

## Required stop states

A future local harness should define at least these stop states:

- `STOP_MISSING_EVIDENCE` — required source evidence or lane context is missing.
- `STOP_UNCLEAR_TASK` — task scope, branch, or operator intent is unclear.
- `STOP_UNAPPROVED_ACTION` — requested command or task is not approved by the applicable later lane.
- `STOP_EXTERNAL_ACTION_REQUESTED` — requested action would cross the local-only boundary.
- `STOP_CREDENTIAL_OR_BILLING_RISK` — requested action would use credentials, secrets, billing, or provider configuration.
- `STOP_ARTIFACT_CAPTURE_FAILURE` — required local artifact capture cannot be completed.
- `STOP_COMMAND_FAILURE` — an authorized local command fails and the stop policy requires halt.
- `STOP_REPOSITORY_STATE_RISK` — repository state would make results ambiguous or unsafe.

## Required handling

When a stop state occurs, the future harness should:

1. Halt additional task execution.
2. Capture a local stop-state artifact.
3. Record the reason, triggering preflight or command, and local repository state.
4. Avoid retries that expand scope.
5. Return control to the human operator.

Stop-state handling must not invoke provider calls, hosted model calls, external API calls, fallback, credentials, billing, dashboards, `/v1/solve`, browser automation, deployment, or evidence promotion.
