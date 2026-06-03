# OUTPUT-DIFF-B1-LIFT-REPORTING-HARDENING-001 · Output Differentiation Reporting Hardening

## Purpose

Harden future `OUTPUT-DIFFERENTIATION-PHASE-001` evidence reporting so Batch B
and later Alpha-vs-plain runs preserve clearer score arithmetic, length context,
capture provenance, and blinding-integrity fields. This is a docs/test/schema
hardening lane only.

## Scope

This lane updates future-run templates, preservation guidance, and docs-integrity
tests. It also corrects stale implementation-evidence references for
`EVAL-ARTIFACT-PRESERVE-001` from PR #201 to PR #229 where that context is clear.

## Reporting fields

Future output-differentiation score tables should include or document these
fields:

- lift and polish subscores: `lift_subscore_plain`, `lift_subscore_alpha`,
  `polish_subscore_plain`, `polish_subscore_alpha`, alongside existing
  `lift_delta` and `polish_delta`;
- length context: `output_a_len_words`, `output_b_len_words`, `length_ratio`,
  `length_confound_flag`, optional `output_a_tokens`, and optional
  `output_b_tokens`;
- resolved decision surface: `winning_surface` plus `winning_surface_resolved`,
  with the polish-only guard capping resolved Alpha wins at `Tie` or
  `Inconclusive` when no material lift is qualified;
- capture provenance: `form_capture_level`, `capture_commit_sha`,
  `capture_started_at`, `capture_completed_at`, `capture_model_set`,
  `capture_surface_count`, and safe summary-level
  `capture_provider_execution_count` when available;
- blinding integrity: `scores_locked_before_unblinding`,
  `blinded_scoring_completed_at`, `unblinding_approved_by`, and
  `unblinding_applied_at`.

Token fields may be blank or `not-captured` when token counts are unavailable;
the schema should make the absence explicit rather than requiring live provider
or billing data.

## Non-claims and boundaries

This lane does not modify A3-1 historical scored artifacts, paired-output
captures, or evidence packets. It does not rerun capture, call live providers,
score outputs, unblind anything, execute Batch B, update Google Sheets, change
the 14 scoring rubric dimensions, or change runtime, provider, model, routing,
`/v1/solve`, dashboard, or deployment behavior.

This lane also:

- does not validate the MVP;
- does not prove Alpha Solver superiority;
- does not prove broad plain-provider superiority;
- does not prove answer-quality superiority;
- does not prove production readiness;
- does not prove broad runtime readiness;
- does not prove benchmark success;
- does not prove exact billing accuracy;
- does not prove provider reasoning orchestration.

## Validation expectations

```bash
git diff --check
rg -n <stale EVAL-ARTIFACT-PRESERVE-001 PR-201 reference patterns> .
python -m pytest tests/test_output_diff_measurement_hardening.py -q
```

Run broader tests only when practical and when they do not intentionally call live
providers.

## Backlog impact

`OUTPUT-DIFF-B1-LIFT-REPORTING-HARDENING-001` should be marked Done only after the
implementing PR is merged. Backlog spreadsheets are not edited from this repo
task.
