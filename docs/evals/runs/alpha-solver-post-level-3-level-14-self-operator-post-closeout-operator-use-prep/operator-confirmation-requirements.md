# Operator confirmation requirements

Required before any future supervised use of the Self Operator path. These
restate the canonical runbook (sections 3-5) and the enforced behavior of
`alpha/self_operator/approval.py` and
`alpha/self_operator/execution_gate.py`. Nothing here was executed in this
prep lane.

## Required confirmation

1. Explicit operator confirmation is required before any Self Operator
   activity. The enforced guard text is:

   ```
   stop if explicit operator confirmation is missing
   ```

2. The approval record's `operator_confirmation` field must be non-empty and
   must contain that guard text verbatim; validation fails closed otherwise
   (`SELF_OPERATOR_OPERATOR_CONFIRMATION_MISSING`,
   `SELF_OPERATOR_APPROVAL_HARD_STOP_TEXT_REQUIRED`).

3. The accepted #461 execution recorded this confirmation form, which future
   supervised use should follow (adapted to the new lane and run):

   ```text
   OPERATOR CONFIRMATION: I explicitly authorize this local-only
   operator-supervised acceptance execution. No providers, hosted/local
   models, external APIs, credentials, browser automation, deployment,
   billing, Google Sheets, source-artifact mutation, evidence promotion,
   readiness claims, autonomous approval, or autonomous merge are authorized.
   ```

## Required approval record

An `ApprovalRecord` (`self_operator.approval_record.v1`) validated fail
closed, with all of:

- `schema_version` supported; `lane_id` and `run_id` non-empty;
  `approved: true`;
- `operator_confirmation` containing the guard text;
- `approval_text`, `approved_by`, `approved_at`, `scope_summary`, and
  `evidence_boundary` non-empty;
- `redaction_status` equal to `redacted`.

## Required identity comparability

So the execution gate can compare every identity dimension, the operator
must provide on the proposed task:

- a `lane_id` matching the approval;
- explicit `metadata.run_id` matching the approval `run_id`;
- explicit metadata scope identity (`task_identity`, `scope_identity`, or
  `scope_summary`) consistent with the approval scope.

A comparable mismatch produces `SELF_OPERATOR_APPROVAL_IDENTITY_MISMATCH`
and a terminal stop state; there is no override.

## Scope of a confirmation

Confirmation is per lane and per run. A new lane, a new run ID, or a changed
scope requires a fresh confirmation and a fresh approval record. Reuse is an
identity mismatch and a stop condition.
