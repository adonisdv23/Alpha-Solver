# Operator confirmation required

Exact confirmation required before the execution lane may run anything.
This binds the prep packet's `operator-confirmation-requirements.md` to this
lane's specific target. Nothing here was recorded or executed by this
packet lane.

## Required confirmation text

The approval record's `operator_confirmation` field must be non-empty and
must contain the enforced guard text verbatim:

```
stop if explicit operator confirmation is missing
```

The recorded confirmation for this first use must take the following form
(the lane and run identifiers must match the actual run):

```text
OPERATOR CONFIRMATION: I explicitly authorize this local-only
operator-supervised first supervised use, limited to the existing evidence
packet consistency review defined in the first-supervised-use packet, for
lane ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-EXECUTION-001
and this run ID only. No providers, hosted/local models, external APIs,
credentials, secrets, browser automation, deployment, billing, Google
Sheets, /v1/solve or dashboard exposure, production use, source-artifact
mutation, evidence promotion, readiness claims, autonomous operation,
autonomous approval, or autonomous merge are authorized.
stop if explicit operator confirmation is missing
```

## Required approval record

An `ApprovalRecord` (`self_operator.approval_record.v1`) validated fail
closed, with all of:

- `schema_version` supported;
- `lane_id` equal to
  `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-EXECUTION-001`;
- a non-empty, fresh `run_id` minted for this run only (see below);
- `approved: true`;
- `operator_confirmation` containing the guard text verbatim;
- `approval_text`, `approved_by`, `approved_at`, `scope_summary`, and
  `evidence_boundary` non-empty, with `scope_summary` matching
  `use-scope.md`;
- `redaction_status` equal to `redacted`.

## Required run ID

The execution lane mints one fresh run ID for this run only, of the form:

```
self-operator-first-supervised-use-execution-001-run-<YYYYMMDD>
```

Reusing any prior run ID (including the accepted #461 run) is an identity
mismatch and a stop condition.

## Required identity comparability

The proposed task must carry, explicitly:

- `lane_id` matching the approval;
- `metadata.run_id` matching the approval `run_id`;
- metadata scope identity (`task_identity`, `scope_identity`, or
  `scope_summary`) consistent with `use-scope.md`.

A comparable mismatch produces
`SELF_OPERATOR_APPROVAL_IDENTITY_MISMATCH` and a terminal stop state; there
is no override.

## Scope of this confirmation

Confirmation is per lane and per run. It authorizes exactly one execution
of the plan in `execution-command-plan.md`. A second attempt, a new lane, a
new run ID, or a changed scope requires a fresh confirmation and a fresh
approval record. Missing or partial confirmation is a hard stop: do not
run.
