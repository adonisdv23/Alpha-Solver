# Policy & Governance (MVP)

Alpha Solver ships with a minimal governance layer that runs entirely in
stdlib-only mode and works offline.  The *policy engine* enforces simple
budget caps, a circuit breaker, optional data classification and emits an
audit log for every decision.

## Budget caps

Two optional limits protect a run from runaway executions:

- `max_steps` – maximum number of steps allowed.
- `max_seconds` – maximum wall clock seconds since the policy engine was
  created.

When a limit is exceeded the decision becomes **block** (or **warn** in
`--policy-dry-run` mode).

## Circuit breaker

`breaker_max_fails` counts consecutive step failures.  Once the threshold is
reached subsequent steps are blocked (or warned in dry-run).  A successful
step resets the counter.

## Dry-run mode

`--policy-dry-run` never blocks execution.  Any would-be block is recorded as a
`warn` decision in the audit log and the run continues.

## Audit JSONL

Decisions are appended to `artifacts/policy_audit.jsonl` with RFC3339Z
timestamps.  The first line contains deterministic run metadata.  Each
subsequent line includes the decision and policy state:

```json
{"run_id":"abc","step_index":1,"query":"demo","region":"US","tool_id":"t1","decision":"warn","reason":"max_steps exceeded","budget":{"steps":3,"max_steps":2,"elapsed_s":0.1,"max_seconds":0},"breaker":{"fails":0,"max_fails":0,"tripped":false},"data_class":{"family":"","tags":[],"status":"allow"}}
```

## Data policy JSON

A optional `data_policy.json` file can deny tools by family or tag:

```json
{
  "deny": { "families": ["x"], "tags": ["pii"] },
  "allow": { "families": [], "tags": [] }
}
```

A candidate tool matching a denied family or tag is blocked (or warned in
`--policy-dry-run` mode).

## Quickstart

```bash
python -m alpha.cli run --queries "demo" \
  --policy-dry-run --budget-max-steps 5 --breaker-max-fails 2
```
