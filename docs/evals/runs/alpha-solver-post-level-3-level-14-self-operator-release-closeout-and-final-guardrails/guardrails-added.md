# Guardrails added

New focused tests were added in `tests/test_self_operator_closeout_guardrails.py`.

## Guardrails

- Prevent unapproved final status vocabulary.
- Prevent the approved claim surface from carrying forbidden status phrases.
- Prevent release closeout from ignoring the accepted import to interpretation order.
- Prevent release gate application from being treated as complete before accepted interpretation.
- Prevent closeout when the canonical runbook is missing.
- Prevent closeout when the evidence-boundary review is missing.
- Prevent closeout when non-execution proof is missing from the evidence chain.
- Prevent closeout if the forbidden-claim scan does not pass.
- Prevent approval identity enforcement overstatement in the canonical runbook.
- Verify the current gate implementation still compares proposed scope identity only from proposed metadata `task_identity`, `scope_identity`, and `scope_summary`.

No production code was changed by these guardrails.
