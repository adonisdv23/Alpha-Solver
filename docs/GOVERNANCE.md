# Governance v1

Alpha Solver includes lightweight governance primitives to enforce policy
limits during execution.

## Environment variables

- `ALPHA_BUDGET_STEPS` – maximum allowed steps per run (default: 100)
- `ALPHA_MAX_ERRORS` – number of errors allowed before the circuit breaker trips
- `ALPHA_POLICY_DRYRUN` – set to `1` to log governance violations without
  raising exceptions

## Audit trail

Governance events are appended to `logs/governance_audit.jsonl`. Each line is a
JSON object with:

- `timestamp` – ISO formatted UTC time
- `session_id` – unique identifier for the run
- `event` – event name such as `budget.exceeded` or `breaker.tripped`
- `data` – additional context

## Dry-run mode

When `ALPHA_POLICY_DRYRUN=1` the solver logs policy violations at the warning
level instead of stopping execution. This allows simulation of governance
effects without interrupting runs.
