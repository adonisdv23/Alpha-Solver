# Dry-run wrapper summary

The wrapper entrypoint is `run_local_dry_run_wrapper`. It accepts a proposed task mapping/object, an approval record mapping/object or missing approval, a caller-provided `output_root`, an optional deterministic timestamp provider, optional preflight input, deterministic artifact names, and no-overwrite behavior.

Outputs are a `DryRunResult` object plus deterministic JSON artifacts. The result includes schema version, lane ID, run ID, dry-run status, allowed boolean, reason code, proposed task summary, approval summary, preflight summary, execution gate summary, optional stop-state summary, artifact paths, output-root summary without raw unsafe path leakage, evidence boundary, redaction status, non-execution confirmation, and metadata.

Statuses include `ready_for_operator_supervised_local_dry_run`, `blocked_by_missing_approval`, `blocked_by_approval_identity_mismatch`, `blocked_by_failed_preflight`, `blocked_by_artifact_path`, `blocked_by_evidence_boundary`, `blocked_by_redaction`, and `blocked_requires_operator_review`.

The wrapper fails closed. Any missing approval, false approval, missing operator confirmation, approval/proposed-task identity mismatch, unsafe preflight, unsafe artifact path, missing evidence boundary, redaction issue, or review-required state remains blocked.
