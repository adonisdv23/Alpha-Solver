# Stop-state response plan

How stop states must be handled in any future supervised use, restating the
canonical runbook (sections 6, 13, 17, 18).

## Stop statuses

The only allowed gate status is `allowed_for_local_dry_run_wrapper`.
Everything else fails closed and produces a deterministic `StopStateRecord`
(`self_operator.stop_state_record.v1`) persisted as `stop-state.json` below
the output root:

- `blocked_by_missing_approval`
- `blocked_by_approval_identity_mismatch`
- `blocked_by_failed_preflight`
- `blocked_by_unsafe_artifact_path`
- `blocked_by_evidence_boundary_issue`
- `blocked_by_redaction_issue`
- `unclear_requires_operator_review`

Operator-level stop conditions in addition to gate statuses: missing
explicit operator confirmation, unclear scope, changed files or outputs
outside the allowed scope, an evidence boundary that cannot be preserved,
and unsafe or unredacted artifact paths.

## Required response to a stop state

1. The stop is terminal for the run. Do not retry by weakening inputs, and
   do not edit any prior evidence.
2. Preserve `stop-state.json` and all partial artifacts below the output
   root exactly as written.
3. Record the stop in the owning lane's packet, with the gate status, the
   findings, and the artifact paths.
4. Classify the defect with the runbook severity taxonomy (`P0` evidence
   boundary or source mutation; `P1` approval, identity, stop-state, or
   non-execution safety; `P2` artifact schema, import readiness,
   determinism, checksum, or redaction; `P3` docs, clarity, operator UX).
5. Route forward, never backward: a new lane with fresh approval and a fresh
   run ID; never rollback by rewriting committed evidence.

## When to route to blocker-fix instead of continuing

Route to the blocker-fix lane instead of continuing whenever any of these
holds:

- any stop status above is produced;
- any `P0` or `P1` class finding appears;
- a `P2` finding appears without an explicit recorded operator decision;
- any output or changed file falls outside the owning lane's allowed file
  list (`blocked_out_of_scope_change`);
- any forbidden action or forbidden claim is detected in any artifact;
- anything material is unclear — unclear means stop, enforced as
  `unclear_requires_operator_review`.

Routing for this prep stage is recorded in `blocker-fallback-lane.md`. A
future supervised-use lane defines its own fix lane in its charter and
routes there under the same rules.
