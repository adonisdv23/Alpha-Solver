# Score-Lock Preservation

## Locked score source

The locked blind score output is:

`docs/evals/runs/alpha-solver-value-read-blind-scoring-pass-post-581-001/score-output.md`

## Preservation rule

This authorization packet does not alter the locked score output. A future unblinding/final-interpretation pass must treat score values, scoring notes, contested-score flags, scorer identity/tool, scoring method, timestamp, and score-lock confirmation as fixed historical scoring artifacts.

## Future pass requirements

A future pass must:

1. Verify the score-output file before source identities are reviewed.
2. Preserve scores exactly.
3. Record any attempted or required score change as a stop condition.
4. Keep interpretation separate from scoring.
5. Avoid using unblinded identities to revise the scoring record.
