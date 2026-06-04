# Post-Improvement Run Summary

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-SCORED-ARTIFACTS-001`

## Lane sequence

1. PR #265 frozen packet: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`
2. PR #266 capture: `OUTPUT-DIFF-POST-IMPROVEMENT-PORTABLE-CAPTURE-001`
3. PR #267 blind scoring: `OUTPUT-DIFF-POST-IMPROVEMENT-BLIND-SCORING-001`
4. Current scored-artifacts lane: `OUTPUT-DIFF-POST-IMPROVEMENT-SCORED-ARTIFACTS-001`

## Locked blinded result

- Output A aggregate blinded total: 306
- Output B aggregate blinded total: 311
- Aggregate blinded delta, Output A minus Output B: -5
- Blinded preference counts: Output A 3, Output B 3, Tie 2, Inconclusive 0

## Mapped Alpha/plain result

Canonical score table: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/score-table.csv`

- Alpha total: 314
- Plain total: 303
- Alpha minus plain delta: 11
- Alpha win count: 5
- Plain win count: 1
- Tie count: 2

## Defect/caveat summary

- The blind-scoring defect artifact recorded no unscoreable comparisons and no scorer-facing artifact problem that blocked scoring.
- The blind-scoring caveats noted materially comparable outputs for some comparisons and prompt-limited need for certain rubric dimensions.
- These caveats are carried forward only as artifact-preservation context; this run summary does not reinterpret the scorer result.

## Evidence boundary

This evidence is portable-surface only. It does not measure `/v1/solve`, runtime routing, provider adapters, model configuration, production behavior, or Batch C behavior.

## Next lane

Next lane: `OUTPUT-DIFF-POST-IMPROVEMENT-INTERPRETATION-001`.
