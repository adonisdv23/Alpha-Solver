# Limited Alpha Operator Test Packet

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-001`

Status: packet prepared, test not yet executed.

This PR prepares the limited operator-test packet only. It does not run the test or report results.

## Purpose

Prepare a controlled internal manual operator test packet for the portable Alpha behavior contract after the brevity/control refinement in PR #272. The packet gives Adonis the task prompts, feedback form, defect log, result-log template, stop conditions, claim boundaries, and preservation checklist needed to run the test later.

## Source evidence

This packet is based only on repo-preserved portable-surface source evidence:

- `alpha_solver_portable.py`
- `tests/test_alpha_minimal_behavior_contract.py`
- `docs/evals/runs/20260604-alpha-brevity-control-refinement/README.md`
- `docs/evals/runs/20260604-post-minimal-behavior-finalization/post-improvement-interpretation.md`
- `docs/evals/runs/20260604-post-minimal-behavior-finalization/minimal-contract-decision.md`
- `docs/evals/runs/20260604-post-minimal-behavior-finalization/next-lane-recommendation.md`
- `docs/evals/runs/20260604-post-minimal-behavior-finalization/finalization-preservation-checklist.md`
- `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- `docs/evals/ARTIFACT_PRESERVATION.md`

The known post-improvement scored result remains limited portable-surface evidence: Alpha total 314, Plain total 303, Alpha-minus-plain delta +11, Alpha wins 5, Plain wins 1, ties 2, outcome family `B. Mixed improvement with brevity/control concern`, final decision `Refine current contract`.

## Required preconditions

- PR #272 for `ALPHA-BREVITY-CONTROL-REFINEMENT-001` must be squashed, merged, and closed on `main` before this packet proceeds.
- The operator test must be run manually after this packet merges.
- The first operator is Adonis unless a later approved packet names another operator.
- The test surface is the portable Alpha behavior contract only.
- The operator must not use raw outputs, operator-only maps, Google Sheets, live providers, `/v1/solve`, runtime APIs, Batch C, scoring, rescoring, capture, or unblinding.

## Files in this packet

- `README.md`
- `operator-test-packet.md`
- `operator-test-task-set.md`
- `operator-feedback-form.md`
- `operator-defect-log.md`
- `operator-result-log-template.md`
- `operator-test-stop-conditions.md`
- `operator-test-claim-boundaries.md`
- `operator-test-preservation-checklist.md`

## What this packet enables

- A limited manual internal operator test of the portable Alpha behavior contract.
- Operator feedback about direct usefulness, brevity, answer-first behavior, claim boundaries, evidence boundaries, stop-condition handling, and next-action quality.
- Defect capture for usability refinement decisions after Adonis runs the packet.

## What this packet does not prove

This packet does not prove:

- `/v1/solve` behavior
- runtime API behavior
- provider behavior
- model routing behavior
- production readiness
- broad runtime readiness
- MVP validation
- benchmark success
- exact billing accuracy
- provider orchestration
- self-healing
- adaptive learning
- self-optimization
- autonomous optimization
- broad Alpha-vs-plain generalization
- broad plain-provider weakness

## Non-claims

- No operator test results are reported here.
- No feedback has been filled in as if Adonis completed it.
- No capture, scoring, rescoring, unblinding, Google Sheets update, Batch C work, provider call, runtime work, or `/v1/solve` measurement occurred.
- No scored artifacts, raw outputs, sanitized scorer-facing packets, or operator maps were modified.

## Next step after packet merge

After this packet merges, Adonis should manually run the limited operator test using `operator-test-packet.md`, paste each task from `operator-test-task-set.md` into the portable Alpha behavior-contract surface, and record feedback and defects in copies of the templates without making benchmark, validation, readiness, or superiority claims.
