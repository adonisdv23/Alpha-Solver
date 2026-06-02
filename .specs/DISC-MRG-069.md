# DISC-MRG-069 · Universal Response Quality Rubric

## Purpose

Define the universal reviewer rubric for side-by-side comparison of plain
provider output versus Alpha Solver expert-preview output during
`OUTPUT-DIFFERENTIATION-PHASE-001`.

The rubric defines what "better than plain output" means before additional
comparison runs begin. It is intended to calibrate human reviewers, preserve
claim boundaries, and make future evidence packets comparable across higher
headroom prompts.

## Scope

This is a documentation/spec-only task. It adds the review contract in
`docs/evals/RESPONSE_QUALITY_RUBRIC.md` and indexes this spec.

The rubric applies to side-by-side answer review where reviewers have the
original prompt, the plain provider answer, and the Alpha Solver expert-preview
answer. It does not change runtime behavior, provider behavior, request metrics,
auth/session/CSRF behavior, deployment configuration, or backlog spreadsheets.

## Required rubric dimensions

The canonical rubric must score each answer on a 0-to-3 scale for these
fourteen dimensions:

1. User intent preservation.
2. Direct answer usefulness.
3. Structure and format discipline.
4. Assumption surfacing.
5. Hidden constraint detection.
6. Risk and failure-mode detection.
7. Claim boundary discipline.
8. Evidence and uncertainty handling.
9. Decision usefulness.
10. Execution-ready next actions.
11. Specificity over generic filler.
12. Brevity versus necessary depth.
13. Safety and policy preservation.
14. Comparative added value over plain output.

The rubric document must define the dimensions, describe what earns 0, 1, 2,
and 3, list common failure examples, and state what reviewers should look for.

## Reviewer calibration contract

Reviewers must:

- score the answer, not the model brand;
- compare against the prompt's real user goal;
- avoid rewarding length by itself;
- avoid punishing useful caution when it improves decision quality;
- avoid rewarding unsupported confidence;
- treat "Alpha was safer but less useful" as mixed, not automatically better;
- treat "Alpha added assumptions but missed the requested deliverable" as a
  defect;
- mark cases where the plain output is better;
- mark ties honestly;
- use conservative interpretation.

## Summary scoring contract

Each comparison artifact should record:

- total score;
- Alpha score;
- plain score;
- delta;
- winning surface: Alpha, Plain, Tie, or Inconclusive;
- reason for winner;
- defects found;
- follow-up tickets.

Small deltas are not enough to claim superiority. A single prompt cannot prove
superiority. A narrow prompt family can show only local advantage. Broad claims
require repeated artifact-backed evidence across higher-headroom prompts.
Cost/latency may be noted but should not dominate this phase unless it prevents
usability.

## Strict non-claims

This rubric does not:

- validate the MVP;
- prove Alpha Solver superiority;
- prove production readiness;
- prove broad runtime readiness;
- prove benchmark success;
- prove exact billing accuracy;
- prove provider reasoning orchestration.

## Relationship to future work

This rubric supports and constrains future output-differentiation work,
including:

- `DISC-MRG-068`, prompt quality scoring and regression harness;
- `HIGHER-HEADROOM-EVAL-001`;
- `ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001`;
- `EVAL-DIFFERENTIATION-RUN-001`;
- `ALPHA-VISIBLE-DIFFERENTIATOR-001`;
- `ALPHA-ANSWER-STRUCTURE-V2-001`.

## Backlog impact

`DISC-MRG-069` should be marked Done only after the PR containing this spec and
rubric is merged. This is a P0 task for `OUTPUT-DIFFERENTIATION-PHASE-001` and
defines what "better than plain output" means for future comparison runs.
Backlog spreadsheets are not edited from this repo task.

## Validation expectations

For this docs/spec-only task, run:

```bash
git diff --check
python -m pytest -q
```

If full pytest is skipped because the final change remains docs/spec-only,
explain why and still run `git diff --check`.
