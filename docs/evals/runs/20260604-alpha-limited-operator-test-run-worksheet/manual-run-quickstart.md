# Manual-Run Quickstart

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-RUN-WORKSHEET-001`

This is a convenience worksheet for manually running the existing limited operator-test packet. Do not use it to invent, prefill, import, score, rescore, unblind, or interpret results.

## Source packet links

Open these source packet files before starting:

- [Operator test task set](https://github.com/adonisdv23/Alpha-Solver/blob/main/docs/evals/runs/20260604-alpha-limited-operator-test/operator-test-task-set.md)
- [Operator feedback form](https://github.com/adonisdv23/Alpha-Solver/blob/main/docs/evals/runs/20260604-alpha-limited-operator-test/operator-feedback-form.md)
- [Operator result log template](https://github.com/adonisdv23/Alpha-Solver/blob/main/docs/evals/runs/20260604-alpha-limited-operator-test/operator-result-log-template.md)
- [Operator defect log](https://github.com/adonisdv23/Alpha-Solver/blob/main/docs/evals/runs/20260604-alpha-limited-operator-test/operator-defect-log.md)
- [Operator test stop conditions](https://github.com/adonisdv23/Alpha-Solver/blob/main/docs/evals/runs/20260604-alpha-limited-operator-test/operator-test-stop-conditions.md)
- [Operator test claim boundaries](https://github.com/adonisdv23/Alpha-Solver/blob/main/docs/evals/runs/20260604-alpha-limited-operator-test/operator-test-claim-boundaries.md)

## Quickstart instructions for Adonis

1. Open the original [operator test task set](https://github.com/adonisdv23/Alpha-Solver/blob/main/docs/evals/runs/20260604-alpha-limited-operator-test/operator-test-task-set.md).
2. Run `LT-001` through `LT-006` first as the smoke test.
3. If time allows, run `LT-007` through `LT-010` after the smoke test.
4. For each task, paste only the task prompt from the source task set into the manual test surface.
5. Capture a short response snippet sufficient to support your feedback or defect note.
6. Fill ratings only after you have actually observed the response.
7. Mark `keep`, `refine`, or `reject` only after reviewing the observed response for that task family.
8. Log defects in the defect log format if you see one or more defect signals.
9. Stop immediately if a stop condition is reached, then record the task ID, stop condition, and smallest safe evidence snippet.
10. Do not invent results, ratings, snippets, defects, status, readiness conclusions, or validation claims.

## Fast run order

- Smoke test first: `LT-001`, `LT-002`, `LT-003`, `LT-004`, `LT-005`, `LT-006`.
- Optional if time allows: `LT-007`, `LT-008`, `LT-009`, `LT-010`.

## Claim boundary reminder

Safe framing: limited operator-test materials exist and may be manually run. This worksheet does not prove production readiness, Alpha superiority, `/v1/solve` behavior, provider orchestration, benchmark passage, or Batch C readiness.
