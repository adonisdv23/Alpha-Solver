# Next Lane Recommendation

Exact recommended next lane: `ALPHA-BREVITY-CONTROL-REFINEMENT-001`.

## Trigger condition

Trigger this lane only after the docs-only finalization PR for `OUTPUT-DIFF-POST-IMPROVEMENT-INTERPRETATION-001` and `ALPHA-MINIMAL-CONTRACT-REFINEMENT-DECISION-001` has merged.

## Objective

Refine the current minimal portable behavior contract so Alpha preserves the modest positive portable-surface signal while reducing unnecessary expansion in concise, reviewer-facing, low-headroom, or answer-first prompts.

## Allowed scope

- Docs/spec planning for targeted brevity and control refinements.
- Proposed wording changes to the minimal portable behavior contract, if separately authorized.
- Focused offline tests for answer-first and compact-caveat behavior, if separately authorized.
- Preservation of narrow eval artifacts under `docs/evals/runs/`.

## Forbidden scope

- Rescoring or changing existing scored artifacts.
- Capture reruns.
- Raw output content inspection for reinterpretation.
- Sanitized scorer-facing packet modification.
- Operator-map assignment changes.
- Google Sheets updates from the repo task.
- Batch C execution.
- Runtime/provider/model/routing changes.
- `/v1/solve` measurement.
- Validation, readiness, or superiority claims.

## Why this lane follows from the decision

The final decision is to refine the current contract rather than keep it unchanged, simplify it, defer all contract work, or expand it. The interpretation found a modest positive Alpha result but retained a brevity/control concern, including narrow wins/ties and a small aggregate brevity-dimension deficit in the current table. A targeted brevity-control lane addresses that remaining weakness without broadening the evidence boundary.

## What remains blocked

- Batch C execution
- runtime-readiness work
- `/v1/solve` measurement
- provider calls and provider-adapter changes
- model routing changes
- production-readiness documentation
- Google Sheets updates from this repo task
- broad validation/readiness/superiority claims
