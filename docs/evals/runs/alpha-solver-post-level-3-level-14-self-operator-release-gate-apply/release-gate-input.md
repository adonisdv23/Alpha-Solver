# Release-gate input

## Repo state

- Base: `main` at `40f3e654dc97f8ba56a97a3f22d70b406d08c48a` (#470 merged).
- Working branch: `claude/release-gate-checker-apply-p0uf7x`, containing only
  this packet plus the narrow checker fix recorded in
  `changed-file-scope-proof.md`.

## Exact command

```bash
python scripts/check_self_operator_release_gate.py \
  --repo-root . \
  --output docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-gate-apply/release-gate-report.json
```

The CLI interface documented in the lane (`--repo-root`, `--output`) is the
checker's actual interface; no alternative invocation was needed.

## Evidence the checker consumes (directory-presence gates, deterministic order)

1. `implementation_foundation_complete` — `docs/evals/runs/alpha-solver-post-level-3-level-10-self-operator-static-test-scaffold-implementation`
2. `approval_identity_fix_complete` — `docs/evals/runs/alpha-solver-post-level-3-level-11-self-operator-approval-stopstate-gate-foundation`
3. `dry_run_wrapper_complete` — `docs/evals/runs/alpha-solver-post-level-3-level-12-self-operator-local-harness-dry-run-wrapper`
4. `manual_acceptance_packet_complete` — `docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-manual-local-acceptance-packet`
5. `operator_supervised_acceptance_executed` — `docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution`
6. `result_import_complete` — `docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-local-acceptance-result-import-tooling`
7. `acceptance_interpretation_complete` — `docs/evals/runs/alpha-solver-post-level-3-to-level-14-self-operator-acceptance-interpretation-engine`
8. `p0_p1_defects_absent` — defect-marker scan over the checker's six scanned packets.
9. `mvp_runbook_finalized_or_updated` — `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization`
10. `evidence_boundary_review_complete` — `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-evidence-boundary-review`
11. `release_closeout_review_complete` — `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout`

## Accepted evidence reviewed alongside the checker (read-only)

- Accepted import evidence (#465):
  `docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json`
  — all ten MLA task artifact sets present, checksums matched, import-ready.
- Accepted interpretation evidence (#470):
  `docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-operator-decision-interpretation-apply/interpretation-result.json`
  — p0=0, p1=0, p2=0, p3=0;
  `readiness_implication = eligible_for_later_release_review`; the #469
  operator ledger-level acceptance consumed for MLA-006/MLA-007 only.

The checker's own interpretation gate keys on the engine packet directory
(item 7); the #470 applied-interpretation result above is the accepted defect
register this lane uses to validate that no P0, P1, or unresolved P2
interpretation defects remain.
