# Execution Results

## Summary

| Target | Command | Exit | Result |
| --- | --- | --- | --- |
| Self Operator suite | `pytest tests/test_self_operator_*.py` | `0` | **213/213 passed**, 0 failed, 0 skipped (1.43s) |
| Release-gate CLI | `check_self_operator_release_gate.py --repo-root .` | `0` | `eligible_for_release_closeout_review`, **11/11 gates pass** |
| Full suite (env unset) | `env -u … pytest -q` | `1` | 1211 passed, **2 pre-existing failures**, 3 skipped (1216 collected) |

The two selected Self Operator execution targets **succeeded**. The full-suite validation is recorded for
completeness; its only failures are pre-existing and unrelated (see `failure-analysis.md`).

## 1. Self Operator suite (authoritative counts via JUnit XML)

```
self_operator_suite: collected=213 passed=213 failed=0 errors=0 skipped=0 time=1.429s
```

This exercises the deterministic Self Operator modules end-to-end at the unit/component level: preflight
classification, the dry-run wrapper (which classifies proposed command text without executing it), the
execution gate, the release-gate evaluator, the artifact store, approval and stop-state records, command
classification, result import, acceptance interpretation, import-blocker triage, and the static
guardrail suites.

## 2. Release-gate CLI (verbatim stdout)

```
Self Operator release gate final_status: eligible_for_release_closeout_review
ready: true (does not claim MVP readiness)
earliest_missing_gate: none
- implementation_foundation_complete: pass (Required evidence packet directory is present.)
- approval_identity_fix_complete: pass (Required evidence packet directory is present.)
- dry_run_wrapper_complete: pass (Required evidence packet directory is present.)
- manual_acceptance_packet_complete: pass (Required evidence packet directory is present.)
- operator_supervised_acceptance_executed: pass (Required evidence packet directory is present.)
- result_import_complete: pass (Required evidence packet directory is present.)
- acceptance_interpretation_complete: pass (Required evidence packet directory is present.)
- p0_p1_defects_absent: pass (No unresolved P0/P1 defect markers found in scanned release-gate evidence.)
- mvp_runbook_finalized_or_updated: pass (Required evidence packet directory is present.)
- evidence_boundary_review_complete: pass (Required evidence packet directory is present.)
- release_closeout_review_complete: pass (Required evidence packet directory is present.)
```

The checker prints `ready: true` together with its own explicit disclaimer `(does not claim MVP
readiness)`. This packet repeats that disclaimer: a passing release-gate inspection is a static
file-presence check, **not** an MVP/release/runtime readiness claim. The full JSON report is embedded in
`artifacts-index.md`.

## 3. Full-suite validation (authoritative counts via JUnit XML)

```
full_suite_env_unset: collected=1216 passed=1211 failed=2 errors=0 skipped=3 time=37.751s
   FAILURE: tests.test_smoke_quickstart::test_release_script
   FAILURE: tests.test_tag_release::test_tag_release
   SKIPPED: tests/providers/test_openai_live_smoke.py (requires ALPHA_LIVE_OPENAI=1 and non-empty OPENAI_API_KEY)
   SKIPPED: tests/test_decks_smoke.py (web adapter disabled in test environment)
   SKIPPED: tests/test_packaging_build.py (build module missing or build failed)
```

These counts match the result recorded by PR #496 ("2 failed, 1211 passed, 3 skipped"). No product, test,
or CI code was modified.

## Validation (static guardrail checkers, run after packet creation)

All three deterministic offline checkers pass with this packet present (exit `0`):

- `python scripts/check_local_llm_doc_paths.py` → `Local LLM/post-Level doc path/link check passed (1461 files scanned).`
- `python scripts/check_local_llm_evidence_boundaries.py` → `Local LLM evidence-boundary static check passed (1862 files scanned).`
- `python scripts/check_local_llm_packet_consistency.py` → `Local LLM packet consistency check passed (145 packet directories scanned).`

The Self Operator release-gate checker was re-run after this packet was added and still reports
`final_status: eligible_for_release_closeout_review` (exit `0`), confirming the new packet introduces no
unresolved P0/P1 defect markers and no path/boundary regression.
