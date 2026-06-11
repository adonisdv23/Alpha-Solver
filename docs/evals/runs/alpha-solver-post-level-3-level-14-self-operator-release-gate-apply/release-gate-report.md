# Release-gate report (human-readable)

## First run (pre-fix, defective tooling output)

The first checker run returned:

```
final_status: blocked_release_closeout_not_reviewed
earliest_missing_gate: p0_p1_defects_absent
exit code: 1
```

The `p0_p1_defects_absent` gate reported three hits:

```
docs/evals/runs/alpha-solver-post-level-3-to-level-14-self-operator-acceptance-interpretation-engine/defect-taxonomy.md:4
docs/evals/runs/alpha-solver-post-level-3-to-level-14-self-operator-acceptance-interpretation-engine/defect-taxonomy.md:5
docs/evals/runs/alpha-solver-post-level-3-to-level-14-self-operator-acceptance-interpretation-engine/readiness-implication-contract.md:8
```

All three lines are backtick-quoted severity-vocabulary definitions
(e.g. "- `P0`: evidence boundary or source mutation violation"), not
unresolved defect markers. The authoritative defect registers — the #470
applied interpretation result and the engine packet's own outputs — record
zero defects at every severity. This was a release-gate tooling false
positive, fixed narrowly (see `changed-file-scope-proof.md`). The defective
first-run JSON was not preserved as evidence; it was superseded by the
post-fix deterministic output below.

## Final run (post-fix)

Command:

```bash
python scripts/check_self_operator_release_gate.py \
  --repo-root . \
  --output docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-gate-apply/release-gate-report.json
```

Output:

```
final_status: blocked_missing_runbook_finalization
ready: false (does not claim MVP readiness)
earliest_missing_gate: mvp_runbook_finalized_or_updated
exit code: 1
```

Gate-by-gate (deterministic order):

| # | Gate | Status |
| --- | --- | --- |
| 1 | `implementation_foundation_complete` | pass |
| 2 | `approval_identity_fix_complete` | pass |
| 3 | `dry_run_wrapper_complete` | pass |
| 4 | `manual_acceptance_packet_complete` | pass |
| 5 | `operator_supervised_acceptance_executed` | pass |
| 6 | `result_import_complete` | pass |
| 7 | `acceptance_interpretation_complete` | pass |
| 8 | `p0_p1_defects_absent` | pass |
| 9 | `mvp_runbook_finalized_or_updated` | missing |
| 10 | `evidence_boundary_review_complete` | missing |
| 11 | `release_closeout_review_complete` | missing |

Summary line from the report: "8/11 gates pass; final status is
blocked_missing_runbook_finalization. This is not a readiness claim."

Determinism: the checker was run twice with identical output;
`release-gate-report.json` sha256 =
`69674953f6c4ac776b6ec85431c64644adad3a535b27b0f56e040c3179e85242`.

## Claim boundary

The checker's only success vocabulary is
`eligible_for_release_closeout_review`, which was not returned. No release
readiness is claimed, and `eligible_for_release_closeout_review` itself would
not be a readiness claim. No MVP readiness is claimed.
