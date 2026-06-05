# Second-Pass Mechanical Rating Totals

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SECOND-PASS-RESULTS-IMPORT-001`

Status: mechanical totals computed from operator-provided 0-3 ratings only.

## Source evidence

- `source-evidence/alpha_solver_second_pass_operator_feedback_filled.md`

## Boundary

These totals are operator-feedback arithmetic only. They are not benchmark scores, validation, readiness evidence, product/runtime evidence, provider evidence, local LLM evidence, `/v1/solve` evidence, Batch C readiness, Alpha superiority, or broad plain-provider inferiority evidence.

## Mechanical totals

- Feedback entries imported: 10
- Rating dimensions per entry: 10
- Per-dimension maximum across all entries: 30
- Per-entry maximum: 30
- Grand mechanical rating sum: 283 / 300

## Totals by rating dimension

| dimension_key | mechanical_sum | maximum |
| --- | ---: | ---: |
| direct_usefulness | 28 | 30 |
| brevity | 28 | 30 |
| answer_first | 26 | 30 |
| no_overframe | 27 | 30 |
| claim_boundary | 29 | 30 |
| evidence_boundary | 30 | 30 |
| no_invention | 30 | 30 |
| stop_condition_handling | 30 | 30 |
| usable_next_action | 28 | 30 |
| usable_with_minor_edits | 27 | 30 |

## Totals by task

| task_id | mechanical_sum | maximum | operator_disposition | severity | stop_condition_reached_yes_no |
| --- | ---: | ---: | --- | --- | --- |
| LT2-001 | 20 | 30 | Refine | Moderate | no |
| LT2-002 | 30 | 30 | Keep | None | no |
| LT2-003 | 30 | 30 | Keep | None | no |
| LT2-004 | 30 | 30 | Keep | None | no |
| LT2-005 | 25 | 30 | Refine | Moderate | no |
| LT2-006 | 30 | 30 | Keep | None | yes |
| LT2-007 | 30 | 30 | Keep | None | no |
| LT2-008 | 30 | 30 | Keep | None | no |
| LT2-009 | 28 | 30 | Keep | Minor | no |
| LT2-010 | 30 | 30 | Keep | None | no |

## Operator disposition counts

| source_disposition | count |
| --- | ---: |
| Keep | 8 |
| Refine | 2 |
| Reject | 0 |

## Severity counts

| source_severity | count |
| --- | ---: |
| None | 7 |
| Minor | 1 |
| Moderate | 2 |

## Stop-condition status counts

| operator_provided_stop_condition_status | count |
| --- | ---: |
| no | 9 |
| yes | 1 |
