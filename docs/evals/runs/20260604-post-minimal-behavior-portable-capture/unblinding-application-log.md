# Unblinding Application Log

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-SCORED-ARTIFACTS-001`

Date/time of unblinding application: 2026-06-04T07:55:12Z

## Authorization note

The operator request authorized this scored-artifacts lane to apply the operator-only Output A / Output B map mechanically to the already-locked PR #267 blind scores. This lane is not a scoring, capture, interpretation, Google Sheets, runtime, or Batch C lane.

## Source files

- Source locked blind score sheet path: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/blinded-score-sheet.csv`
- Source operator-only map path: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/operator-only-unblinding-map.csv`

## Preconditions checked

- PR #267 blind-scoring artifacts were present.
- `blinded-score-sheet.csv` was present.
- `operator-only-unblinding-map.csv` was present.
- The blind score sheet had exactly 8 comparison rows.
- The operator-only map had exactly 8 comparison rows.
- Comparison IDs and prompt IDs aligned between score sheet and map.
- Locked blind totals reconstructed to Output A 306, Output B 311, and Output A minus Output B -5.
- All dimension scores were integers from 0 to 3.
- Output A and Output B row totals equaled their 14-dimension sums.
- No instruction in this lane required rescoring, capture rerun, raw-output-content inspection, Google Sheets update, Batch C, runtime/provider/model/routing modification, `/v1/solve` use, or broad claims.

## Mechanical mapping method

For each comparison row, the locked Output A and Output B dimension scores and row totals were read from `blinded-score-sheet.csv`. The Output A and Output B condition assignments were read from `operator-only-unblinding-map.csv`. The Output A score vector and total were copied to Alpha or plain when the map assigned Output A to that condition; the Output B score vector and total were copied the same way. Row-level Alpha minus plain delta and mapped preference were then computed from the copied row totals.

## Negative-scope confirmations

- The map was applied only after blind scores were locked by PR #267.
- No rescoring occurred.
- No capture rerun occurred.
- No raw outputs were read for scoring or interpretation.
- No raw outputs were modified.
- No Google Sheets update occurred.
- No Batch C started.
- No runtime/provider/model/routing behavior changed.
- No `/v1/solve` measurement occurred.
