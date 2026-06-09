# Gate Contract

Required gates:

1. `implementation_foundation_complete`
2. `approval_identity_fix_complete`
3. `dry_run_wrapper_complete`
4. `manual_acceptance_packet_complete`
5. `operator_supervised_acceptance_executed`
6. `result_import_complete`
7. `acceptance_interpretation_complete`
8. `p0_p1_defects_absent`
9. `mvp_runbook_finalized_or_updated`
10. `evidence_boundary_review_complete`
11. `release_closeout_review_complete`

Final statuses:

- `blocked_missing_execution`
- `blocked_missing_import`
- `blocked_missing_interpretation`
- `blocked_missing_runbook_finalization`
- `blocked_missing_boundary_review`
- `blocked_release_closeout_not_reviewed`
- `eligible_for_release_closeout_review`

`eligible_for_release_closeout_review` means the checker found all required synthetic gate evidence. It is not an MVP readiness claim, production readiness claim, provider readiness claim, or release readiness claim.
