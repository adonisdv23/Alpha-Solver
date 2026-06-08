# Preflight Requirements

## Required local preflights

A future local-only harness should stop before execution unless all required local preflights pass:

- Confirm the operator-selected task is local-only, bounded, and tied to an approved later lane.
- Confirm the current branch and working tree are acceptable for the declared local task.
- Confirm required source evidence packets and specs are present.
- Confirm the local command allowlist contains only docs/checker commands or explicitly authorized local-only task commands.
- Confirm no credential files, secret variables, provider configuration, billing configuration, dashboard exposure, or `/v1/solve` exposure are required.
- Confirm artifact paths are local, deterministic, and scoped to the run.
- Confirm stop-state handling is enabled before any local command starts.

## Stop-before-start conditions

The future harness must stop before start if any of these conditions are present:

- Missing required source evidence.
- Unclear operator intent or task boundary.
- Dirty or unexpected repository state that would confuse artifact capture.
- Any request for provider calls, hosted model calls, external API calls, local model runs, fallback, credentials, billing, deployment, browser automation, dashboard exposure, `/v1/solve` exposure, or evidence promotion.
- Missing local artifact destination.
- Missing human approval where a future lane requires approval.
- A command that is outside the local-only allowlist.

## Preflight outputs

Preflight results should be captured as local artifacts only. They should record the check name, command if applicable, pass/fail state, timestamp, repository branch, and stop reason if the run stops.
