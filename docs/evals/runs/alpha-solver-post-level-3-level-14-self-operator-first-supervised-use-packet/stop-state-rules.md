# Stop-state rules

Stop-state rules binding the first supervised use, applying the prep
packet's `stop-state-response-plan.md` (and the canonical runbook) to this
lane's target.

## Stop statuses

The only allowed gate status is `allowed_for_local_dry_run_wrapper`.
Everything else fails closed and produces a deterministic
`StopStateRecord` (`self_operator.stop_state_record.v1`) persisted as
`stop-state.json` below the output root:

- `blocked_by_missing_approval`
- `blocked_by_approval_identity_mismatch`
- `blocked_by_failed_preflight`
- `blocked_by_unsafe_artifact_path`
- `blocked_by_evidence_boundary_issue`
- `blocked_by_redaction_issue`
- `unclear_requires_operator_review`

Operator-level stop conditions in addition to gate statuses: missing
explicit operator confirmation, unclear scope, a non-zero checker exit
code, any file changed inside the repository checkout during the run, any
output outside the output root, an evidence boundary that cannot be
preserved, and unsafe or unredacted artifact paths.

## Required response to a stop state

1. The stop is terminal for the run. Do not retry by weakening inputs, and
   do not edit any prior evidence.
2. Preserve `stop-state.json` and all partial artifacts below the output
   root exactly as written.
3. Record the stop in the execution lane's packet, with the gate status,
   the findings, and the artifact paths.
4. Classify the defect with the runbook severity taxonomy (`P0` evidence
   boundary or source mutation; `P1` approval, identity, stop-state, or
   non-execution safety; `P2` artifact schema, import readiness,
   determinism, checksum, or redaction; `P3` docs, clarity, operator UX).
5. Route forward, never backward: continue only in the blocker-fix lane in
   `blocker-fallback-lane.md`, with a fresh approval and a fresh run ID;
   never rollback by rewriting committed evidence.

## Unclear means stop

Anything material that is unclear during the run is a stop
(`unclear_requires_operator_review`), not a judgment call to push through.
