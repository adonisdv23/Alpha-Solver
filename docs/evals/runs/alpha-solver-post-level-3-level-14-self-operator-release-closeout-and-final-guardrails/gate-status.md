# Gate status

| Gate | Evidence | Status |
| --- | --- | --- |
| `accepted_result_import_exists` | `docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-local-acceptance-result-import-tooling/` | pass |
| `acceptance_interpretation_complete` | `docs/evals/runs/alpha-solver-post-level-3-to-level-14-self-operator-acceptance-interpretation-engine/` | pass |
| `release gate application` | `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-gate-apply/` | pass |
| `mvp_runbook_finalized_or_updated` | `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md` | pass |
| `evidence_boundary_review_complete` | `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-evidence-boundary-review/` and #472 combined review packet | pass |
| `release_closeout_review_complete` | this closeout packet | pass |
| `p0_p1_defects_absent` | `defect-status.md` and prerequisite registers | pass |
| `p2_p3_resolved_or_deferred` | `defect-status.md` | pass |
| `non_execution_proof_present` | acceptance execution packet and import/interpretation checks | pass |
| `approved_claim_wording_only` | `approved-claims.md`, `final-status.md`, and tests | pass |
| `forbidden_claim_scan_passed` | `forbidden-claim-scan-results.md` | pass |
| `runbook_approval_identity_wording_corrected` | `runbook-approval-identity-correction.md` | pass |

Closeout eligibility is recorded only after all listed gates pass.

## Deterministic full-root gate proof (recorded after the path repair)

When PR #474 merged this packet, the deterministic checker in
`alpha/self_operator/release_gate.py` still pointed `CLOSEOUT_PACKET` at the
old `...-release-closeout/` path, so the full-root checker reported
`release_closeout_review_complete` as `missing` and the table above was not
yet backed by a deterministic full-root gate run. The repair lane
`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-MERGED-CLOSEOUT-GATE-PATH-REPAIR-001`
aligned the gate path to this packet and recorded the proof:

- `post-closeout-release-gate-report.json` — full-root checker output, exit `0`.
- `post-closeout-release-gate-report.md` — command, result, and bounds.
- Result: all eleven gates `pass`, `release_closeout_review_complete: pass`,
  final gate status `eligible_for_release_closeout_review`.

The `release_closeout_review_complete` row above is now proven by that
recorded full-root run, not asserted independently of it.
