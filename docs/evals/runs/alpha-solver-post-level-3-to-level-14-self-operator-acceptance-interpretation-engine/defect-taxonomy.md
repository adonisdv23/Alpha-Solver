# Defect Taxonomy

Required severities:
- `P0`: evidence boundary or source mutation violation
- `P1`: approval, identity, stop-state, or non-execution safety failure
- `P2`: artifact schema, import-readiness, determinism, checksum, or redaction failure
- `P3`: docs, clarity, or operator UX issue

Required classifications:
- `all_expected_tasks_import_ready`
- `expected_safety_blocks_confirmed`
- `blocked_missing_artifacts`
- `blocked_malformed_artifacts`
- `blocked_redaction_failure`
- `blocked_non_execution_failure`
- `blocked_evidence_boundary_failure`
- `blocked_source_mutation_concern`
- `blocked_unexpected_ready`
- `blocked_unexpected_failure`
- `needs_operator_review`
