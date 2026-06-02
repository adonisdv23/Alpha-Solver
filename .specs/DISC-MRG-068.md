# DISC-MRG-068 · Prompt Quality Scoring and Regression Harness

## Purpose

Define a documentation/spec-first prompt quality scoring and regression harness
for future Alpha-vs-plain comparison runs during
`OUTPUT-DIFFERENTIATION-PHASE-001`.

The harness exists to:

- make Alpha-vs-plain runs repeatable;
- score prompts and outputs consistently;
- detect regressions in Alpha Solver expert-preview behavior after behavior
  changes;
- preserve sanitized evidence through the evaluation artifact preservation lane;
- avoid unsupported superiority, readiness, benchmark, billing, or orchestration
  claims.

## Scope

This is a documentation/spec-only task. It adds the harness plan in
`docs/evals/PROMPT_QUALITY_SCORING_HARNESS.md`, adds lightweight copyable
human-readable templates under `docs/evals/templates/`, and indexes this spec.

This task does not change runtime behavior, provider behavior, request metrics,
dashboard auth/session/CSRF behavior, deployment configuration, environment
configuration, or backlog spreadsheets.

## Harness contract

Future comparison runs should use the harness to record, at minimum:

- stable prompt-level metadata before running either surface;
- the prompt family and higher-headroom capability being tested;
- sanitized summaries of plain provider and Alpha expert-preview outputs;
- per-dimension scores using `docs/evals/RESPONSE_QUALITY_RUBRIC.md`;
- Alpha-vs-plain score deltas;
- defects, regressions, expected changes, and follow-up tickets;
- conservative interpretations constrained by preserved artifacts;
- redactions performed and non-claims.

Prompt manifests and score tables must be sanitized before commit. They must not
store raw provider payloads, secrets, provider account identifiers, full
unredacted request/response traces, or private user data unless explicitly
sanitized and needed.

## Prompt metadata requirements

Each stable prompt in a future prompt set should define:

1. Prompt ID.
2. Prompt family.
3. Prompt text or sanitized prompt summary.
4. User intent.
5. Expected deliverable.
6. Required sections or format.
7. Hidden constraints being tested.
8. Failure modes being tested.
9. Rubric dimensions emphasized.
10. Difficulty/headroom level.
11. Safety or claim-boundary concerns.
12. Source or rationale.
13. Allowed assumptions.
14. Disallowed claims.
15. Expected evidence capture.

## Prompt family taxonomy

Higher-headroom prompt sets should classify prompts into one or more of these
families:

- ambiguous execution planning;
- claim-boundary / readiness judgment;
- hidden constraint detection;
- prioritization under uncertainty;
- artifact review / prompt review;
- debugging and failure-mode diagnosis;
- rollout / go/no-go decision;
- evidence interpretation;
- adversarial/noisy context;
- research synthesis / source hierarchy.

## Scoring workflow requirements

Future runs should:

1. select a stable prompt set and record its manifest;
2. run the plain provider output;
3. run the Alpha Solver expert-preview output;
4. preserve sanitized artifacts under `docs/evals/runs/` using
   `docs/evals/ARTIFACT_PRESERVATION.md`;
5. score both outputs with `docs/evals/RESPONSE_QUALITY_RUBRIC.md`;
6. calculate per-dimension scores;
7. calculate `Alpha score - Plain score` deltas;
8. identify defects;
9. identify follow-up tickets;
10. record a conservative interpretation.

## Regression workflow requirements

After behavior changes, future reviewers should rerun a stable prompt set and
compare against prior preserved run artifacts. Regression review should flag
material degradation in:

- direct answer usefulness;
- format preservation;
- assumptions;
- hidden constraints;
- risk/failure modes;
- claim boundaries;
- next actions;
- comparative added value.

Regression notes must distinguish expected behavior changes from regressions.
Expected changes are allowed only when they are tied to the relevant spec,
implementation change, or documented review rationale.

## Score interpretation contract

Future reports must preserve these interpretation rules:

- one prompt cannot prove superiority;
- small deltas are inconclusive;
- narrow prompt family wins only support local advantage;
- broad claims require repeated artifact-backed evidence;
- plain wins must be recorded honestly;
- ties must be recorded honestly;
- score tables are decision aids, not automatic proof of product readiness.

## Strict non-claims

This harness does not validate the MVP.

This harness does not prove Alpha Solver superiority.

This harness does not prove production readiness.

This harness does not prove broad runtime readiness.

This harness does not prove benchmark success.

This harness does not prove exact billing accuracy.

This harness does not prove provider reasoning orchestration.

## Relationship to related work

This spec complements:

- `DISC-MRG-069`, which defines the universal response quality rubric used by
  the scoring workflow;
- `EVAL-ARTIFACT-PRESERVE-001`, which defines where sanitized artifacts live and
  what must never be stored;
- `HIGHER-HEADROOM-EVAL-001`, which should use this taxonomy and manifest shape
  for higher-headroom prompt selection;
- `ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001`, which should use these score tables
  and conservative interpretation rules in side-by-side evidence packets;
- `EVAL-DIFFERENTIATION-RUN-001`, which should use this workflow for repeatable
  Alpha-vs-plain runs;
- `ALPHA-VISIBLE-DIFFERENTIATOR-001`, which should rely only on repeated,
  artifact-backed local advantages rather than unsupported broad claims;
- `ALPHA-ANSWER-STRUCTURE-V2-001`, which should use this regression workflow to
  detect whether answer-structure changes improve or degrade outputs.

## Backlog impact

`DISC-MRG-068` should be marked Done only if the PR containing this spec and
harness documentation is merged.

This is a P0 task for `OUTPUT-DIFFERENTIATION-PHASE-001`.

This enables repeatable Alpha-vs-plain comparison and regression detection.

This does not prove Alpha Solver superiority.

This does not validate the MVP.

This does not prove production readiness.

Backlog spreadsheets are not edited from this repo task.

## Validation expectations

For this docs/spec-only task, run:

```bash
git diff --check
python -m pytest -q
```

If full pytest is skipped because the final change remains docs/spec-only,
explain why and still run `git diff --check`.
