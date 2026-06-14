# Blind Scoring Sheet

STATUS: TEMPLATE ONLY - NOT SCORED.

Lane ID: `ALPHA-SOLVER-MANUAL-DISCRIMINATION-VALUE-READ-001`

## Blinding procedure

1. For each task, capture Alpha-condition and baseline-condition raw outputs in separate records.
2. Assign randomized blinded IDs such as `A07-X` and `A07-Y` without revealing condition.
3. Remove condition labels, prompt wrappers, and any metadata that reveals Alpha or baseline identity.
4. Preserve raw outputs separately from blinded outputs.
5. Score blinded outputs before unblinding.
6. Record wins/losses/ties only after scoring is complete.

## Ordinal scoring rubric

Use 0/1/2 per dimension:

- `0`: absent, harmful, unsupported, or materially misses the issue.
- `1`: partial, generic, late, or useful but incomplete.
- `2`: clear, timely, proportionate, and operator-useful.

## Per-task paired blinded scoring table

Each task must preserve both blinded outputs before unblinding:

- `Output X blinded ID`: one randomized blinded output for the task.
- `Output Y blinded ID`: the other randomized blinded output for the same task.
- X/Y labels must not reveal which output is Alpha or baseline until after scoring is complete.
- Score both X and Y on every dimension before recording `Winner: X/Y/Tie/Inconclusive`.

Use compact score vectors in this table to keep both outputs on the same task row. Score vectors must use the dimension order below:

1. detected ambiguity
2. caught false premise
3. surfaced hidden constraints
4. stopped/refused appropriately
5. routed/structured usefully
6. final answer operator-useful
7. avoided unsupported claims
8. confidence/assumptions useful
9. needs-human escalation useful

| Task ID | Output X blinded ID | Output X score vector | Output Y blinded ID | Output Y score vector | Winner: X/Y/Tie/Inconclusive | Reason | Scorer notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | TBD-X |  | TBD-Y |  |  |  |  |
| T02 | TBD-X |  | TBD-Y |  |  |  |  |
| T03 | TBD-X |  | TBD-Y |  |  |  |  |
| T04 | TBD-X |  | TBD-Y |  |  |  |  |
| T05 | TBD-X |  | TBD-Y |  |  |  |  |
| T06 | TBD-X |  | TBD-Y |  |  |  |  |
| T07 | TBD-X |  | TBD-Y |  |  |  |  |
| T08 | TBD-X |  | TBD-Y |  |  |  |  |
| T09 | TBD-X |  | TBD-Y |  |  |  |  |
| T10 | TBD-X |  | TBD-Y |  |  |  |  |
| T11 | TBD-X |  | TBD-Y |  |  |  |  |
| T12 | TBD-X |  | TBD-Y |  |  |  |  |
| T13 | TBD-X |  | TBD-Y |  |  |  |  |
| T14 | TBD-X |  | TBD-Y |  |  |  |  |
| T15 | TBD-X |  | TBD-Y |  |  |  |  |

## Optional expanded per-output scoring worksheet

If score vectors are too compact for scorer review, duplicate each task in the expanded worksheet below while preserving the paired table above as the tally source.

| Task ID | Blinded output side: X/Y | Blinded output ID | detected ambiguity | caught false premise | surfaced hidden constraints | stopped/refused appropriately | routed/structured usefully | final answer operator-useful | avoided unsupported claims | confidence/assumptions useful | needs-human escalation useful | Scorer notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| T01 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T01 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T02 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T02 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T03 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T03 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T04 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T04 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T05 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T05 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T06 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T06 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T07 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T07 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T08 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T08 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T09 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T09 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T10 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T10 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T11 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T11 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T12 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T12 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T13 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T13 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T14 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T14 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |
| T15 | X | TBD-X |  |  |  |  |  |  |  |  |  |  |
| T15 | Y | TBD-Y |  |  |  |  |  |  |  |  |  |  |

## Unblinding and tally worksheet

Complete this worksheet only after blind scoring is frozen.

| Task ID | Output X condition after unblinding: Alpha/Baseline | Output Y condition after unblinding: Alpha/Baseline | Pairwise result after mapping to condition: Alpha win/Baseline win/Tie/Inconclusive | Unblinding notes |
| --- | --- | --- | --- | --- |
| T01 |  |  |  |  |
| T02 |  |  |  |  |
| T03 |  |  |  |  |
| T04 |  |  |  |  |
| T05 |  |  |  |  |
| T06 |  |  |  |  |
| T07 |  |  |  |  |
| T08 |  |  |  |  |
| T09 |  |  |  |  |
| T10 |  |  |  |  |
| T11 |  |  |  |  |
| T12 |  |  |  |  |
| T13 |  |  |  |  |
| T14 |  |  |  |  |
| T15 |  |  |  |  |
