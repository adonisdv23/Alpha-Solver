# Stop-state review

| Task ID | Expected blocked behavior | Observed behavior | Status | Review note |
| --- | --- | --- | --- | --- |
| MLA-002 | Wrapper blocks with missing approval stop-state and writes dry-run, execution-gate, and stop-state artifacts. | dry_run_status=blocked_by_missing_approval; allowed=False; reason_code=missing_approval | PASS | stop-state.json produced and copied. |
| MLA-003 | Wrapper blocks with missing/invalid approval stop-state and writes dry-run, execution-gate, and stop-state artifacts. | dry_run_status=blocked_by_missing_approval; allowed=False; reason_code=approval_invalid | PASS | stop-state.json produced and copied. |
| MLA-004 | Wrapper blocks with approval identity mismatch stop-state and writes dry-run, execution-gate, and stop-state artifacts. | dry_run_status=blocked_by_approval_identity_mismatch; allowed=False; reason_code=approval_identity_mismatch | PASS | stop-state.json produced and copied. |
| MLA-005 | Wrapper blocks through preflight/execution gate and writes dry-run, execution-gate, and stop-state artifacts. | dry_run_status=blocked_by_failed_preflight; allowed=False; reason_code=failed_preflight | PASS | stop-state.json produced and copied. |
| MLA-006 | Wrapper rejects traversal before writing raw JSON artifacts and raises ArtifactStoreError. | exception=ArtifactStoreError: artifact path outside allowed output root: ../dry-run-result.json | PASS | Expected blocked cases remained blocked; MLA-006/MLA-007 rejected before producing new stop-state JSON where applicable. |
| MLA-007 | Second wrapper invocation rejects overwrite with ArtifactStoreError; proposed command is not executed. | initial dry_run_status=ready_for_operator_supervised_local_dry_run; second invocation blocked with ArtifactStoreError: artifact already exists and overwrite is false: execution-gate-result.json | PASS | Expected blocked cases remained blocked; MLA-006/MLA-007 rejected before producing new stop-state JSON where applicable. |
