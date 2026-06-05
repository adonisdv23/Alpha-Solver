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

All `BC-001` through `BC-012` prompts and raw outputs were present, so no stop-condition task was excluded. Scores use the approved 0 to 3 scale.

| Task | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | Total | Disposition | Defect codes | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BC-001 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-002 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-003 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-004 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-005 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-006 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-007 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 35 | Refine | D-WORDING-DRIFT | Minor refinement: the next action is safe overall, but the phrase about an explicitly recreated artifact is slightly broader than the most conservative preservation wording. |
| BC-008 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-009 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-010 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-011 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |
| BC-012 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 36 | Keep | None | Clean output matched the prompt contract and stayed within the evidence boundary. |

## Aggregate

- Evaluable tasks: 12.
- Blocked tasks: 0.
- Score cells: 144.
- Aggregate total: 431 / 432.
- Blocked tasks excluded from aggregate totals: not applicable because no stop condition was recorded.
- Blank score cells: none.
