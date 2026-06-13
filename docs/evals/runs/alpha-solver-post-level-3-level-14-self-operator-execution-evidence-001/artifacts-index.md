# Artifacts Index

This packet is markdown-only. Produced artifacts are embedded here (not committed as separate files),
because the release-gate CLI's JSON output path falls under the repository `.gitignore` rule `artifacts/`,
and PR #496's predecessor packet is likewise markdown-only.

## Artifact 1 — Self Operator suite result (JUnit XML, summarized)

- Producer: `python -m pytest tests/test_self_operator_*.py --junit-xml=…`
- Summary: `collected=213 passed=213 failed=0 errors=0 skipped=0 time=1.429s`
- Storage boundary: only aggregate counts and failing-test identifiers are recorded; no environment dump,
  no secrets, no provider payloads.

## Artifact 2 — Full-suite validation result (JUnit XML, summarized)

- Producer: `env -u MODEL_PROVIDER -u MODEL_SET -u OPENAI_API_KEY -u OPENAI_BASE_URL python -m pytest --junit-xml=…`
- Summary: `collected=1216 passed=1211 failed=2 errors=0 skipped=3 time=37.751s`
- Failing tests: `tests/test_smoke_quickstart.py::test_release_script`, `tests/test_tag_release.py::test_tag_release`
  (see `failure-analysis.md`).

## Artifact 3 — Release-gate JSON report (embedded verbatim)

- Producer: `python scripts/check_self_operator_release_gate.py --repo-root . --output <artifacts/…>`
- Schema: `self_operator.release_gate_report.v1`; size 4549 bytes; exit code `0`.
- Storage boundary: the report contains only in-repo evidence-directory paths and gate statuses; no
  secrets, credentials, provider payloads, or private data.

```json
{
    "earliest_missing_gate": null,
    "final_status": "eligible_for_release_closeout_review",
    "gates": [
        {"gate_id": "implementation_foundation_complete", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-10-self-operator-static-test-scaffold-implementation"},
        {"gate_id": "approval_identity_fix_complete", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-11-self-operator-approval-stopstate-gate-foundation"},
        {"gate_id": "dry_run_wrapper_complete", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-12-self-operator-local-harness-dry-run-wrapper"},
        {"gate_id": "manual_acceptance_packet_complete", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-manual-local-acceptance-packet"},
        {"gate_id": "operator_supervised_acceptance_executed", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution"},
        {"gate_id": "result_import_complete", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-local-acceptance-result-import-tooling"},
        {"gate_id": "acceptance_interpretation_complete", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-to-level-14-self-operator-acceptance-interpretation-engine"},
        {"gate_id": "p0_p1_defects_absent", "status": "pass", "reason": "No unresolved P0/P1 defect markers found in scanned release-gate evidence.", "evidence_path": "docs/evals/runs/self-operator-release-gate-packets"},
        {"gate_id": "mvp_runbook_finalized_or_updated", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization"},
        {"gate_id": "evidence_boundary_review_complete", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-evidence-boundary-review"},
        {"gate_id": "release_closeout_review_complete", "status": "pass", "reason": "Required evidence packet directory is present.", "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails"}
    ],
    "non_actions": [
        "does not claim MVP readiness",
        "does not update Google Sheets",
        "does not mutate source artifacts",
        "does not run providers, hosted models, local models, external APIs, browser automation, deployment, or billing"
    ],
    "ready": true,
    "schema_version": "self_operator.release_gate_report.v1",
    "summary": "11/11 gates pass; eligible for release closeout review, with no readiness claim."
}
```

The embedded report's own `non_actions` block and `summary` preserve the no-readiness-claim boundary;
this packet adopts the same boundary (see `evidence-boundary.md`, `forbidden-claims.md`).
