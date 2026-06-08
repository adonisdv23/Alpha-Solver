# Run Metadata Schema

## Purpose

Future operator-only runs should preserve local run context without converting that context into a claim of runtime quality, deployment readiness, or external reproducibility.

## Required fields

A future `run_metadata.*` record should include:

- `schema_name`: `self_operator_artifact_persistence_schema`.
- `schema_packet_lane`: `ALPHA-SOLVER-POST-LEVEL-7-SELF-OPERATOR-ARTIFACT-PERSISTENCE-SCHEMA-PACKET-001`.
- `run_id`: stable local run identifier.
- `packet_path`: path where the run packet is preserved.
- `operator_role`: description of the human or agent operator role.
- `run_intent`: brief operator-only objective.
- `started_at_utc`: ISO-8601 timestamp or `UNKNOWN_NOT_RECORDED`.
- `ended_at_utc`: ISO-8601 timestamp or `UNKNOWN_NOT_RECORDED`.
- `timezone_context`: local timezone when relevant.
- `repo_branch`: branch name at capture time when available.
- `repo_commit`: commit SHA at capture time when available.
- `dirty_worktree_before_run`: `true`, `false`, or `UNKNOWN_NOT_RECORDED`.
- `dirty_worktree_after_run`: `true`, `false`, or `UNKNOWN_NOT_RECORDED`.
- `commands_executed`: list of exact commands, if any.
- `tools_used`: local tools used, if any.
- `provider_calls_made`: must be explicit; use `none` when no provider was called.
- `runtime_calls_made`: must be explicit; use `none` when runtime was not exercised.
- `artifact_inventory_path`: path to the inventory record.
- `redaction_ledger_path`: path to the redaction ledger, if any.
- `stop_reason_record_path`: path to the stop reason record.
- `confirmation_record_path`: path to the confirmation record, if any.

## Prohibited metadata inflation

Run metadata must not claim:

- production readiness;
- provider quality;
- model quality;
- benchmark success;
- deployment status;
- promoted eval evidence;
- user-facing reliability.

Those claims require separate approved evidence lanes.
