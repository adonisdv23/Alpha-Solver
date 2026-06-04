# Scored Artifact Summary

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-SCORED-ARTIFACTS-001`

Status: scored artifact produced by mechanical unblinding of locked blind scores.

## Source lanes

- Source blind-scoring lane: PR #267 / `OUTPUT-DIFF-POST-IMPROVEMENT-BLIND-SCORING-001`
- Source capture lane: PR #266 / `OUTPUT-DIFF-POST-IMPROVEMENT-PORTABLE-CAPTURE-001`
- Source frozen packet lane: PR #265 / `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

## Source files

- Locked blind score sheet: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/blinded-score-sheet.csv`
- Operator-only unblinding map: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/operator-only-unblinding-map.csv`
- Canonical score table: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/score-table.csv`

## Locked blinded totals from PR #267

- Output A: 306
- Output B: 311
- Output A minus Output B: -5
- Output A preferences: 3
- Output B preferences: 3
- Ties: 2
- Inconclusive: 0

## Mechanical unblinding result

- Unblinded Alpha total: 314
- Unblinded plain total: 303
- Alpha minus plain delta: 11
- Alpha win count: 5
- Plain win count: 1
- Tie count: 2

## Defect and caveat carry-forward

- The blind-scoring defect record remains the source for scorer-observed Output A / Output B caveats.
- This artifact only maps those already-locked Output A / Output B scores to Alpha/plain labels according to the operator-only map.
- Several prompts had limited need for assumption surfacing or risk analysis; middle scores on those dimensions are carried forward from the blind-scoring artifact and should not be read as new defects by themselves.
- This is portable-surface evidence only.
- Interpretation is deferred to `OUTPUT-DIFF-POST-IMPROVEMENT-INTERPRETATION-001`.

## Negative-scope confirmations

- No rescoring occurred.
- No capture rerun occurred.
- No raw outputs were read for scoring or interpretation.
- No raw outputs were modified.
- The sanitized scorer-facing packet was not modified.
- No Google Sheets update occurred.
- No Batch C work started.
- No runtime/provider/model/routing behavior changed.
- No `/v1/solve` measurement occurred.
- No validation, readiness, superiority, benchmark-success, runtime-readiness, or provider-orchestration claim is made here.
