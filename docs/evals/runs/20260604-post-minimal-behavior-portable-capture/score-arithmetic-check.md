# Score Arithmetic Check

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-SCORED-ARTIFACTS-001`

## Method used

A Python CSV check read the locked blind score sheet and the operator-only unblinding map, verified row alignment, verified integer dimension scores, recomputed row totals, applied the condition assignment mechanically, and wrote `unblinded-score-table.csv`. No scoring rubric semantics were changed.

## Row count check

- Blind score rows: 8
- Operator-only map rows: 8
- Unblinded score table rows: 8
- Comparison IDs aligned: yes
- Prompt IDs aligned: yes

## Locked blinded total reconstruction

- Locked Output A total reconstruction: 306
- Locked Output B total reconstruction: 311
- Locked blinded delta reconstruction, Output A minus Output B: -5
- Expected locked Output A total: 306
- Expected locked Output B total: 311
- Expected locked blinded delta: -5

## Unblinded Alpha/plain total calculation

- Alpha total calculation: 314
- Plain total calculation: 303
- Alpha minus plain delta: 11

## Alpha/plain win/loss/tie counts

- Alpha wins: 5
- Plain wins: 1
- Ties: 2

## Preservation confirmations

- No dimension scores changed; Alpha/plain dimension scores were copied from the locked Output A/B dimension scores according to the map.
- No row totals changed; Alpha/plain row totals are the locked Output A/B row totals assigned to the mapped condition.
- No blind scores were altered.
- No scorer rationale was used to change any score.
