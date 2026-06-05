# Scoring Sheet

Lane ID: `ALPHA-BATCH-C-SCORING-001`

Source evidence: `docs/evals/runs/20260605-alpha-batch-c-operator-execution/source-evidence/ALPHA-BATCH-C-OPERATOR-EXECUTION-001.md`

Rubric packet: `docs/evals/runs/20260605-alpha-batch-c-scoring-rubric-packet/`

## Dimension key

| Column | Dimension |
| --- | --- |
| D1 | direct answer first |
| D2 | low-headroom restraint |
| D3 | requested output shape |
| D4 | no process-style lead-in |
| D5 | no unnecessary wrapper label |
| D6 | no accidental literal-label artifact |
| D7 | claim-boundary discipline |
| D8 | evidence-boundary discipline |
| D9 | stop-condition handling |
| D10 | no unsupported reconstruction |
| D11 | redaction/sensitive-data handling |
| D12 | concise next-action quality |

## Scores

All `BC-001` through `BC-012` prompts and raw outputs were present, so no stop-condition task was excluded. Scores use the approved 0 to 3 scale only for dimensions applicable to each task under `docs/evals/runs/20260605-alpha-batch-c-scoring-rubric-packet/task-to-rubric-map.md`. Non-applicable dimensions are marked `N/A`, are not blank score cells, and are excluded from task totals and aggregate totals.

| Task | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | Total | Disposition | Defect codes | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BC-001 | 3 | 3 | 3 | 3 | N/A | N/A | 3 | N/A | N/A | N/A | N/A | N/A | 15 / 15 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-002 | 3 | 3 | 3 | N/A | 3 | N/A | 3 | N/A | N/A | N/A | N/A | N/A | 15 / 15 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-003 | 3 | N/A | 3 | 3 | N/A | N/A | N/A | 3 | N/A | N/A | N/A | 3 | 15 / 15 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-004 | N/A | 3 | 3 | N/A | N/A | N/A | 3 | 3 | N/A | N/A | N/A | N/A | 12 / 12 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-005 | 3 | 3 | 3 | 3 | N/A | 3 | N/A | N/A | N/A | N/A | N/A | N/A | 15 / 15 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-006 | 3 | N/A | N/A | N/A | N/A | N/A | N/A | 3 | 3 | 3 | N/A | 3 | 15 / 15 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-007 | 3 | 3 | N/A | N/A | N/A | N/A | 3 | 3 | N/A | N/A | N/A | 2 | 14 / 15 | Refine | D-WORDING-DRIFT | Minor refinement: the next action is safe overall, but the phrase about an explicitly recreated artifact is slightly broader than the most conservative preservation wording for the applicable concise next-action dimension. |
| BC-008 | N/A | 3 | 3 | N/A | 3 | N/A | N/A | N/A | N/A | 3 | 3 | N/A | 15 / 15 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-009 | N/A | 3 | 3 | N/A | N/A | N/A | 3 | 3 | N/A | N/A | N/A | N/A | 12 / 12 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-010 | N/A | N/A | 3 | N/A | N/A | N/A | N/A | 3 | 3 | 3 | N/A | 3 | 15 / 15 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-011 | N/A | N/A | 3 | N/A | N/A | N/A | N/A | 3 | 3 | 3 | N/A | 3 | 15 / 15 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |
| BC-012 | N/A | 3 | 3 | N/A | N/A | N/A | 3 | 3 | N/A | N/A | N/A | 3 | 15 / 15 | Keep | None | Clean output matched the applicable prompt-contract dimensions and stayed within the evidence boundary. |

## Aggregate

- Evaluable tasks: 12.
- Blocked tasks: 0.
- Applicable scored cells: 58.
- Non-applicable cells marked `N/A`: 86.
- Aggregate total: 173 / 174.
- Blocked tasks excluded from aggregate totals: not applicable because no stop condition was recorded.
- Blank score cells: none.
