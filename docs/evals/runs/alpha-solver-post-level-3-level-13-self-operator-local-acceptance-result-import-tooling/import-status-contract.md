# Import status contract

Allowed import statuses:

- `import_ready`
- `import_ready_with_expected_blocks`
- `blocked_missing_artifact`
- `blocked_malformed_artifact`
- `blocked_checksum_mismatch`
- `blocked_redaction_failure`
- `blocked_evidence_boundary_failure`
- `blocked_non_execution_missing`
- `blocked_source_mutation_concern`
- `blocked_unknown`

Expected safety blocks may remain import-ready when the expected stop-state artifact is present and validates. Source-artifact mutation markers remain a separate import block for operator review.

No status means MVP readiness, runtime readiness, production readiness, provider readiness, release readiness, or final acceptance readiness.
