# Approval, preflight, and gate integration summary

The dry-run wrapper runs or accepts local preflight, then evaluates the existing corrected execution gate. The gate result is the source of truth for readiness.

Corrected approval identity matching is required before dry-run readiness. A proposed task cannot reach `ready_for_operator_supervised_local_dry_run` unless approval is present, approval is true, explicit operator confirmation is present, approval identity matches proposed task identity, preflight allows the task, artifact paths are safe, redaction is safe, and the evidence boundary is present.

Identity mismatches remain blocked with `blocked_by_approval_identity_mismatch`, reason code `approval_identity_mismatch`, and finding `SELF_OPERATOR_APPROVAL_IDENTITY_MISMATCH`.
