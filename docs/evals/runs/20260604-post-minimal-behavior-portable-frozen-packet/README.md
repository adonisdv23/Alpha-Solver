# Post-Minimal Behavior Portable Frozen Packet

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

Status: packet-only, pre-capture.

## Purpose

This directory freezes the docs-only prompt packet for a future portable-surface diagnostic after the minimal behavior contract was added to `alpha_solver_portable.py`.

The packet prepares, but does not execute, a future Alpha-vs-plain comparison where the Alpha condition explicitly loads the merged repository version of `alpha_solver_portable.py` as the portable behavior contract.

## Measurement boundary

This packet measures the portable contract surface only. It does not measure `/v1/solve` unless a later approved task proves that `/v1/solve` consumes `alpha_solver_portable.py` and explicitly authorizes that wired surface.

The current packet does not change runtime behavior, routing, provider adapters, model configuration, capture scripts, scored artifacts, Google Sheets integration, or Batch C materials.

## Source-of-truth files read

- `alpha_solver_portable.py`
- `docs/evals/runs/20260604-post-minimal-behavior-measurement-plan/measurement-surface-decision.md`
- `docs/evals/runs/20260604-post-minimal-behavior-measurement-plan/post-improvement-run-plan.md`
- `docs/evals/runs/20260604-post-minimal-behavior-measurement-plan/measurement-readiness-checklist.md`
- `docs/evals/runs/20260604-post-minimal-behavior-measurement-plan/measurement-surface-impact-matrix.csv`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/README.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/source-packet.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blind-scorer-result.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blinded-score-sheet.csv`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/score-table.csv`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/run-summary.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/interpretation-review.md`
- `docs/evals/ARTIFACT_PRESERVATION.md`
- `docs/evals/BLIND_SCORING_PROCEDURE.md`
- `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- `docs/evals/batch-b/execution-protocol.md`
- `docs/evals/batch-b/post-capture-scoring-workflow.md`
- `docs/evals/templates/blinding_map_template.csv`
- `docs/evals/templates/blinded_score_sheet_template.csv`

The optional PR #264 outline file was not present at `docs/evals/runs/20260604-post-minimal-behavior-measurement-plan/frozen-packet-next-pr-outline.md`.

## Artifact boundaries

This packet adds only frozen planning artifacts:

- frozen prompt list;
- condition instructions;
- future capture instructions;
- blinding plan;
- scorer-facing packet template;
- operator-only unblinding map template;
- artifact preservation checklist;
- packet readiness checklist;
- future task sequence.

It does not include captured outputs, A/B assignments, score sheets from a completed run, unblinded scored results, provider metadata, raw provider payloads, or Sheet updates.

## Non-claims

This packet does not claim MVP validation, general superiority by Alpha, broad inferiority of plain-provider output, answer-quality proof, readiness for production, broad runtime readiness, benchmark completion, billing precision, or live provider reasoning coordination.

Any future evidence generated from this packet must remain limited to the portable contract surface unless a separate approved task changes and proves the measured surface.

## Next allowed step after merge

After this packet is reviewed and merged, the next allowed step is to review and approve the frozen packet, then separately authorize capture. Capture, scoring, unblinding, Sheet updates, and Batch C remain out of scope for this packet PR.
