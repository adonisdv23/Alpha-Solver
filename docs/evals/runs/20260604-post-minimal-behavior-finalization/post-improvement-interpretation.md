# Post-Improvement Interpretation

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-INTERPRETATION-001`

Status: interpretation complete, docs-only, portable-surface only.

## Source scored artifacts used

- Canonical scored table: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/score-table.csv`
- Scored artifact summary: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/scored-artifact-summary.md`
- Score arithmetic check: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/score-arithmetic-check.md`
- Unblinding application log: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/unblinding-application-log.md`
- Post-improvement run summary: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/post-improvement-run-summary.md`
- Scored artifact preservation checklist: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/scored-artifact-preservation-checklist.md`
- Blind scorer result: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/blind-scorer-result.md`
- Blind scoring defects: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/blind-scoring-defects.md`
- Blind scoring completeness check: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/blind-scoring-completeness-check.md`
- Portable minimal behavior contract reference: `alpha_solver_portable.py`
- Rubric and preservation references: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`, `docs/evals/ARTIFACT_PRESERVATION.md`, `.specs/EVAL-ARTIFACT-PRESERVE-001.md`
- Prior limited evidence artifacts: `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/score-table.csv`, `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/run-summary.md`, `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/score-table.csv`, `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/interpretation-review.md`, `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/lift-vs-polish-diagnostic-matrix.csv`

Raw output content was not read or used for this interpretation.

## Artifact integrity status

Artifact integrity is preserved for this interpretation lane.

- PR #269 scored artifacts are present in the post-minimal-behavior portable-capture run directory.
- `score-table.csv` exists, contains exactly 8 comparison rows, and reports Alpha 314, plain 303, and Alpha-minus-plain +11.
- `score-arithmetic-check.md`, `scored-artifact-summary.md`, and `scored-artifact-preservation-checklist.md` are present.
- The prior scored-artifact lane explicitly preserved the locked blind score sheet, operator-only map, canonical score table, arithmetic check, run summary, and unblinding application log.
- The prior scored-artifact lane explicitly confirms no rescoring, no capture rerun, no raw-output modification, no sanitized-packet modification, no score edits, no Google Sheets update, no Batch C work, no runtime/provider/model/routing change, and no `/v1/solve` use or measurement.

## Locked blind result

- Output A aggregate blinded total: 306
- Output B aggregate blinded total: 311
- Aggregate blinded delta, Output A minus Output B: -5
- Blinded preference counts: Output A 3 / Output B 3 / Tie 2 / Inconclusive 0

## Unblinded scored result

- Alpha total: 314
- Plain total: 303
- Alpha minus plain delta: +11
- Alpha wins: 5
- Plain wins: 1
- Ties: 2

## Interpretation of delta

The +11 Alpha-minus-plain delta is a modest positive Alpha result on a limited 8-comparison portable-surface diagnostic. The aggregate is directionally favorable to Alpha and the win count is also favorable, but the margin is small relative to a roughly 300-point aggregate scale. It should not be treated as decisive and should not be generalized beyond the portable-surface diagnostic.

The row pattern supports a cautious positive reading rather than a strong one: Alpha won 5 comparisons, plain won 1, and 2 were ties; however, most Alpha wins were narrow, with only one larger per-row margin (+8). The current table records a small aggregate brevity-dimension deficit for Alpha (-1), and the preserved blind-scoring defects include format friction in one Alpha-mapped row and several narrow or materially comparable rows.

## Outcome family classification

Chosen family: **B. Mixed improvement with brevity/control concern**.

Rationale:

- The unblinded result is positive for Alpha: +11 aggregate, 5 Alpha wins, 1 plain win, and 2 ties.
- The artifact chain is clean enough for interpretation because the scored artifacts and preservation checklist explicitly preserve the mechanical unblinding chain and prohibit score or capture changes.
- The result remains mixed/modest because the aggregate margin is small and the blind-scoring defects preserve multiple caveats about narrow separation, comparable outputs, and format friction.
- The current scored table does not include the prior Batch B lift/polish cluster columns, so exact lift-versus-polish cluster classification for this run should not be asserted from this table alone. The table does expose the single brevity dimension, where Alpha is slightly behind in aggregate (-1), which keeps brevity/control refinement in scope.

## Comparison against prior evidence

A3-1 was a limited 4-comparison result where plain totaled 237, Alpha totaled 228, Alpha-minus-plain was -9, and plain won all 4 local comparisons. That result did not prove broad plain-provider advantage; it showed that the earlier Alpha surface could lose on a small set, especially where answer fit and claim discipline were insufficient.

Batch B was a limited 12-comparison pilot where plain totaled 405, Alpha totaled 455, Alpha-minus-plain was +50, Alpha won 8, plain won 4, and there were no ties. It favored Alpha in that pilot but did not generalize beyond the preserved prompt set. Batch B also showed the important diagnostic pattern: Alpha gained in the lift cluster (+21), was roughly flat in polish (-1), and lost on brevity (-10).

The current post-improvement result sits between those prior signals. It is more favorable to Alpha than A3-1 and directionally consistent with Batch B's conditional-positive view, but it is smaller than Batch B and still carries brevity/control caution. The combined evidence remains prompt-set-dependent and supports conditional usefulness, not a broad conclusion.

## PR #263 verdict

PR #263 likely helped the portable behavior surface modestly. The direction changed from the earlier A3-1 negative signal to a positive post-improvement portable-surface signal, and the minimal contract's answer-first, compact-caveat, no-invented-scaffolding, and safe-claim-wording rules align with the kinds of defects and prior Batch B patterns that needed control.

This should not be read as proof that PR #263 fixed the whole problem. It more likely improved wording and restraint in enough cases to create a modest positive portable-surface signal while leaving targeted brevity/control and low-headroom restraint work unresolved.

## What this proves

This proves only that, after mechanical unblinding of the locked PR #267 blind scores, the preserved 8-comparison portable-surface diagnostic scored Alpha modestly above plain: Alpha 314, plain 303, Alpha-minus-plain +11, with 5 Alpha wins, 1 plain win, and 2 ties.

It also proves that the current repo-preserved scored artifacts are sufficient to complete a conservative docs-only interpretation lane without rescoring, rerunning capture, changing runtime behavior, using raw output content, updating Google Sheets, or starting Batch C.

## What this does not prove

This does not prove:

- `/v1/solve` behavior
- runtime API behavior
- provider behavior
- model routing behavior
- production-readiness
- broad runtime-readiness
- MVP-validating evidence
- benchmark-level success
- billing-accuracy proof
- provider-orchestration behavior
- self healing behavior
- adaptive-learning behavior
- self-optimization behavior
- autonomous-optimization behavior
- broad Alpha-vs-plain generalization
- broad plain-provider weakness

## Recommended next lane

Recommended next lane: `ALPHA-BREVITY-CONTROL-REFINEMENT-001`.

## Blocked work

The following remain blocked by the portable-surface measurement boundary and by the modest/mixed result:

- Batch C execution
- runtime-readiness decision or runtime measurement
- `/v1/solve` measurement
- provider calls or provider-adapter changes
- model configuration or routing changes
- production-readiness documentation
- Google Sheets update from this repo task
- broad validation, readiness, or superiority claims
- exact lift/polish/brevity cluster claims for this run beyond the columns preserved in the current table
