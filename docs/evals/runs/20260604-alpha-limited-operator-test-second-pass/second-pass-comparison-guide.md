# Second-Pass Comparison Guide

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SECOND-PASS-001`

Status: packet prepared, second-pass test not yet executed

## Purpose

This guide describes how a later, separately authorized review may compare second-pass operator feedback to the imported first-pass operator feedback. It does not perform that comparison and does not state any outcome.

## Permitted comparison source

Compare only against the imported first-pass operator feedback and related interpretation files:

- `docs/evals/runs/20260604-alpha-limited-operator-test-prompt-contract-simulation-results-import-clean/source-evidence/alpha_solver_operator_feedback_filled.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test-prompt-contract-simulation-results-import-clean/mechanical-result-log.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test-prompt-contract-simulation-results-import-clean/mechanical-rating-totals.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test-interpretation/defect-patterns.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test-interpretation/task-family-observations.md`

Do not compare to product/runtime metrics, `/v1/solve` output, provider runs, local-model runs, benchmarks, or external anecdotes.

## Comparison dimensions

Preserve the same fixed higher-is-better 0-3 scale and task-level rating dimensions. Do not compare second-pass ratings to first-pass feedback if a later execution used a different scale.

Fixed scale:

- `0`: not useful / absent / unsafe / failed for this dimension
- `1`: weak, materially incomplete, or needs major edits
- `2`: mostly usable with minor to moderate edits
- `3`: strong, directly usable, and satisfies this dimension

Dimensions:

- direct usefulness
- brevity
- answer-first
- no over-frame
- claim boundary
- evidence boundary
- no invention
- stop-condition handling
- usable next action
- usable with minor edits

For inverse-seeming or boundary dimensions, treat higher scores as better: less over-framing for `no_overframe`, less invention for `no_invention`, correct stop-condition handling for `stop_condition_handling`, and stronger boundary preservation for `claim_boundary` and `evidence_boundary`.

Also compare qualitative contamination observations for:

- visible process-style lead-ins;
- wrapper labels;
- `standard:` artifacts;
- unnecessary `Replacement:` labels;
- memo framing when concise output was requested;
- unsupported readiness or comparative claims;
- missing-results reconstruction;
- Batch C blocking under limited evidence.

## Comparison method

A later comparison should:

1. Preserve raw second-pass artifacts before reviewing feedback.
2. Confirm each second-pass task has stop-condition fields filled.
3. Compare second-pass tasks to the closest first-pass task family, not as one-to-one proof.
4. Report differences as operator-feedback observations only.
5. Separate mechanical rating arithmetic from qualitative notes.
6. Avoid changing first-pass ratings, notes, totals, or interpretations.
7. Avoid claiming validation, readiness, superiority, benchmark status, production status, or broad provider conclusions.

## Suggested task-family mapping

| second-pass task | closest first-pass family | comparison focus |
| --- | --- | --- |
| LT2-001 | reviewer comment / concise response | lead-ins, memo framing, answer-first shape |
| LT2-002 | replacement wording | `standard:` artifact, unnecessary replacement label |
| LT2-003 | checklist | checklist starts directly, no wrapper |
| LT2-004 | status update | exact concise shape, no extra frame |
| LT2-005 | compact template | template-only response, no `standard:` prefix |
| LT2-006 | missing-results refusal | stop condition, no invented result or ratings |
| LT2-007 | Batch C blocking | limited-evidence block, no readiness claim |
| LT2-008 | evidence-boundary rewrite | evidence-boundary discipline in one sentence |
| LT2-009 | claim-boundary reviewer note | no broad comparative claim adoption |
| LT2-010 | preservation comment | compact PR-review comment and prior-packet preservation |

## Required comparison boundary language

Any later comparison summary should state that it compares second-pass results only to imported first-pass operator feedback and that the comparison remains manual prompt-contract simulation evidence only.
