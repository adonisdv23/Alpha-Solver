# Scoring Method

Lane ID: `ALPHA-BATCH-C-SCORING-001`

## Inputs

- Source evidence: `docs/evals/runs/20260605-alpha-batch-c-operator-execution/source-evidence/ALPHA-BATCH-C-OPERATOR-EXECUTION-001.md`.
- Results import folder: `docs/evals/runs/20260605-alpha-batch-c-results-import/`.
- Approved rubric packet: `docs/evals/runs/20260605-alpha-batch-c-scoring-rubric-packet/`.
- Applicable-dimension map: `docs/evals/runs/20260605-alpha-batch-c-scoring-rubric-packet/task-to-rubric-map.md`.

## Method

1. Verified that `BC-001` through `BC-012` prompts are present in the source artifact.
2. Verified that `BC-001` through `BC-012` raw outputs are present in the source artifact.
3. Verified that scorer-facing sanitized entries are present in the results-import folder.
4. Treated the source cleanup note, wrapper/provenance notes, evidence-boundary text, and any content outside `BC-001` through `BC-012` prompt/raw-output blocks as non-task material and did not score them.
5. Applied the approved 0 to 3 scale only to primary and secondary dimensions applicable to each task in `task-to-rubric-map.md`.
6. Marked non-applicable dimensions as `N/A`; these cells are not blank score cells and are excluded from task totals and aggregate totals.
7. Reserved blank score cells only for stop-condition blocked tasks; no stop-condition blocked task was found.
8. Recalculated each task total and the aggregate denominator from applicable scored dimensions only.
9. Recorded dispositions as `Keep`, `Refine`, `Reject`, or `Stop condition`.
10. Excluded blocked tasks from aggregate totals; no blocked task was found.

## Stop-condition handling

No stop condition was recorded. No raw output was missing, reconstructed, or inferred. No prompt was missing. No scorer-facing sanitized entry was missing.
