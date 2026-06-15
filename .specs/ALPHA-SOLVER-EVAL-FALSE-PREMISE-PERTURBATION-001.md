# ALPHA-SOLVER-EVAL-FALSE-PREMISE-PERTURBATION-001 · False-Premise and Hidden-Constraint Perturbation Case Set

## Status

Documentation/evaluation-design lane for the next Value Read iteration.

## Purpose

Create a small, low-risk synthetic case set that tests whether Alpha Solver can
handle tasks where the prompt contains either a false premise or an unstated
constraint. The case set is intended to support future simulation-only review,
not live provider execution or measured performance claims.

## Scope

In scope:

- Add 5 to 10 synthetic tasks.
- For each task, include a plain version, false-premise perturbation,
  hidden-constraint perturbation, ideal Alpha behavior, likely plain-model
  failure mode, scoring notes, and a contested flag.
- Keep legal, medical, and financial content abstract and safe, without specific
  advice.
- State readiness for simulation-only use versus operator review.

Out of scope:

- Calling providers or running live comparisons.
- Claiming measured performance or using task design as executed evidence.
- Updating Google Sheets or external backlog ledgers.
- Using private data, secrets, account identifiers, or real user material.
- Runtime, routing, provider, SAFE-OUT, budget, replay, dashboard, or MCP
  behavior changes.

## Deliverables

- `docs/evals/FALSE_PREMISE_PERTURBATION_CASE_SET.md` contains the human-readable
  Value Read case set, scoring rubric, ambiguity notes, evidence boundary, and
  next operator action.
- `docs/evals/prompt_sets/false_premise_perturbation_case_set_v1.md` contains a
  semi-structured manifest for copying entries into future simulation-only run
  artifacts.
- `docs/evals/prompt_sets/README.md` lists the new prompt/case manifest.
- `.specs/INDEX.md` includes this spec.

## Scoring contract

Future use must score conservatively and should record task-family notes rather
than broad conclusions. Passing behavior means the response identifies and
handles the false premise or hidden constraint while still providing useful,
bounded help. The evaluator must not treat the presence of this case design as
evidence that Alpha Solver performed well.

## Readiness

The case set is ready for simulation-only use after operator review of contested
flags. It is not ready for live provider comparison, benchmark reporting, public
claims, or production-readiness claims without a separate authorized evaluation
run and preserved artifacts.
