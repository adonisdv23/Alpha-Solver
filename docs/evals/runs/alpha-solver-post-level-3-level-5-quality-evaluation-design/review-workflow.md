# Review Workflow

## Future workflow

A future quality evaluation execution lane must use a workflow at least as strict as this sequence:

1. Confirm lane authorization and evidence boundary.
2. Freeze tasks, prompts, scoring rubric, reviewer roster, execution commands, and artifact paths.
3. Generate outputs only after freeze confirmation.
4. Preserve raw outputs before review begins.
5. Score independently against the frozen rubric.
6. Reconcile disagreements using the predeclared procedure.
7. Log defects, invalid tasks, environment issues, and boundary concerns.
8. Apply stop conditions before summarizing results.
9. Interpret evidence only within the lane's allowed claim boundary.
10. Close the lane with selected next lane or blocker fallback.

## Future pass/fail criteria requirements

A future execution packet must define pass/fail criteria before execution, including:

- minimum artifact completeness;
- minimum valid task count by category;
- minimum reviewer coverage;
- maximum unresolved reviewer disagreement;
- invalidation rules for missing raw outputs or changed prompts;
- thresholds for any bounded quality evidence claim;
- language that remains blocked regardless of scores.

## Independence and auditability

Reviewers must score the preserved outputs rather than regenerated outputs. The review workflow must preserve enough metadata for a later audit to identify exactly which prompt, context, output, reviewer, score, and adjudication note produced each summarized result.
