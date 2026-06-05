# Prompt-Contract Simulation Mechanical Result Log

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-PROMPT-CONTRACT-SIMULATION-RESULTS-IMPORT-001`

Status: sanitized source evidence imported, mechanical result log created.

## Source evidence

This log uses only the two supplied completed evidence files represented in this folder:

- `source-evidence/sanitized-task-evidence.md`
- `source-evidence/alpha_solver_operator_feedback_filled.md`

## Boundary

This log is mechanical operator-feedback import only. It is not interpretation, rescoring, benchmarking, validation, production readiness, Batch C readiness, `/v1/solve` evidence, local LLM evidence, provider evidence, or Alpha-superiority evidence.

Stop-condition status is copied mechanically from Adonis' operator-provided statement that no task in LT-001 through LT-010 was marked as a blocking stop condition. This is operator feedback only, not expert technical adjudication.

The supplied files do not provide an overall 0-3 operator rating field, so that field remains `missing`.

## Core result log

| task_id | task_family | operator_name | test_date | test_surface | portable_surface_context | stop_condition_reached_yes_no | stop_condition_id_or_summary | overall_operator_rating_0_3 | mechanical_sum_of_10_operator_ratings_0_30 | keep_refine_reject | severity | primary_defect | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LT-001 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 29 | Keep | None | None material. | Directly blocked Batch C and named limited operator test as next action. |
| LT-002 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 19 | Refine | Minor to moderate | Visible process text and `standard:` artifact before usable reviewer comment. | Final comment was not useful, it just returned the comment back as is, and output violated “no memo / concise” expectation. |
| LT-003 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 27 | Keep | Minor | Some visible process text before answer. | Substance was strong and review-gate checks were correct. |
| LT-004 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 30 | Refine | Minor | `standard:` artifact and “Replacement:” label. | Replacement text itself was safe and evidence-bounded. |
| LT-005 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 28 | Keep | Minor | Visible process text before final answer. | Correctly made repo packet control over stale planning ledger. |
| LT-006 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 29 | Keep | Minor | Visible process text before final answer. | Correctly refused reconstruction and blocked readiness conclusion. |
| LT-007 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 26 | Refine | Minor to moderate | Visible process text and `standard:` artifact; prompt was compact request, output included extra wrapper. | Codex prompt content was strong and complete. |
| LT-008 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 26 | Refine | Minor | Named ALPHA-LIMITED-OPERATOR-TEST-EXECUTION-001, but current path later reframed as prompt-contract simulation. | Followed prepared-but-unexecuted packet logic at the time. |
| LT-009 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 29 | Keep | None | None material. | Clean two-sentence status update with sufficient caveat. |
| LT-010 | missing | Adonis | 2026-06-04 | portable Alpha behavior contract only | manual prompt-contract simulation only | no | none_marked_by_operator | missing | 27 | Refine | Minor | Visible process text and `standard:` artifact before checklist. | Checklist substance was correct and complete. |

## Rating detail log

| task_id | direct_usefulness | brevity | answer_first | no_overframe | claim_boundary | evidence_boundary | no_invention | stop_condition_handling | usable_next_action | usable_with_minor_edits | mechanical_sum_0_30 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LT-001 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 29 |
| LT-002 | 1 | 2 | 2 | 1 | 3 | 3 | 3 | 1 | 2 | 1 | 19 |
| LT-003 | 3 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 27 |
| LT-004 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 30 |
| LT-005 | 3 | 3 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 28 |
| LT-006 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 29 |
| LT-007 | 3 | 2 | 2 | 1 | 3 | 3 | 3 | 3 | 3 | 3 | 26 |
| LT-008 | 2 | 3 | 3 | 3 | 3 | 3 | 2 | 2 | 3 | 2 | 26 |
| LT-009 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 3 | 29 |
| LT-010 | 3 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 27 |
