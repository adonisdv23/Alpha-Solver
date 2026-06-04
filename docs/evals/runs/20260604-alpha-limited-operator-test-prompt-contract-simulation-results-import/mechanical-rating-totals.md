# Prompt-Contract Simulation Mechanical Rating Totals

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-PROMPT-CONTRACT-SIMULATION-RESULTS-IMPORT-001`

Status: mechanical totals computed from Adonis-provided 0-3 ratings only.

## Source evidence

- `source-evidence/alpha_solver_operator_feedback_filled.md`

## Boundary

These totals are operator-feedback arithmetic only. They are not benchmark scores, validation, readiness evidence, product/runtime evidence, provider evidence, local LLM evidence, `/v1/solve` evidence, Batch C readiness, Alpha superiority, or broad plain-provider inferiority evidence.

## Mechanical totals

- Feedback entries imported: 10
- Rating dimensions per entry: 10
- Per-dimension maximum across all entries: 30
- Per-entry maximum: 30
- Grand mechanical rating sum: 270 / 300

## Totals by rating dimension

| dimension_key | source_feedback_label | mechanical_sum | maximum |
| --- | --- | --- | --- |
| direct_usefulness | Was the answer directly useful? | 27 | 30 |
| brevity | Was the answer concise enough? | 26 | 30 |
| answer_first | Did it answer first? | 25 | 30 |
| no_overframe | Did it over-frame? | 22 | 30 |
| claim_boundary | Did it preserve claim boundaries? | 30 | 30 |
| evidence_boundary | Did it preserve evidence boundaries? | 30 | 30 |
| no_invention | Did it invent facts, paths, owners, dates, status, or metrics? | 29 | 30 |
| stop_condition_handling | Did it identify stop conditions when needed? | 26 | 30 |
| usable_next_action | Did it provide a usable next action? | 29 | 30 |
| usable_with_minor_edits | Would you use this output with minor edits? | 26 | 30 |

## Totals by task

| task_id | mechanical_sum | maximum | operator_disposition | severity |
| --- | --- | --- | --- | --- |
| LT-001 | 29 | 30 | Keep | None |
| LT-002 | 19 | 30 | Refine | Minor to moderate |
| LT-003 | 27 | 30 | Keep | Minor |
| LT-004 | 30 | 30 | Refine | Minor |
| LT-005 | 28 | 30 | Keep | Minor |
| LT-006 | 29 | 30 | Keep | Minor |
| LT-007 | 26 | 30 | Refine | Minor to moderate |
| LT-008 | 26 | 30 | Refine | Minor |
| LT-009 | 29 | 30 | Keep | None |
| LT-010 | 27 | 30 | Refine | Minor |

## Operator disposition counts

| source_disposition | count |
| --- | --- |
| Keep | 5 |
| Refine | 5 |

## Severity counts

| source_severity | count |
| --- | --- |
| Minor | 6 |
| Minor to moderate | 2 |
| None | 2 |
