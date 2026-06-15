# ALPHA-SOLVER-EVAL-HIGHER-HEADROOM-CASESET-001 · Higher-Headroom Value Read Case Set

## Status

Documentation/evaluation-design lane for a future Value Read iteration.

## Purpose

Create a harder synthetic case-set design for future Value Read evaluation when
prior Value Read tasks tie, saturate, or fail to separate Alpha behavior from a
baseline. The design raises headroom by combining false premises, hidden
constraints, clarification thresholds, refusal/escalation boundaries, conflicting
evidence, confidence calibration, low-headroom concision, and claim-boundary
preservation.

## Scope

In scope:

- Define case categories, quotas, and difficulty levels.
- Add 20 to 30 synthetic candidate task descriptions without private data.
- Mark ideal behavior and expected failure modes for each candidate.
- Define scoring dimensions and kill conditions for cases that do not separate
  behavior.
- State evidence boundaries and non-claims.

Out of scope:

- Executing the evaluation or scoring model outputs.
- Calling providers or creating live comparison artifacts.
- Claiming benchmark, product, MVP, production-readiness, or value evidence.
- Mutating existing scored packets or historical run artifacts.
- Using private data, secrets, account identifiers, raw provider payloads, or real
  user material.
- Runtime, routing, provider, SAFE-OUT, budget, replay, dashboard, or MCP
  behavior changes.

## Deliverables

- `docs/evals/HIGHER_HEADROOM_VALUE_READ_CASE_SET.md` contains the human-readable
  case-set design, taxonomy, candidate task table, scoring dimensions, kill
  conditions, and evidence boundary.
- `docs/evals/prompt_sets/higher_headroom_value_read_case_set_v1.md` contains a
  semi-structured manifest for copying candidates into future Value Read run
  artifacts.
- `docs/evals/prompt_sets/README.md` lists the new case-set manifest.
- `.specs/INDEX.md` includes this spec.

## Scoring contract

Future use must score conservatively and should report separation only within the
observed task families and run mode. Candidate design alone is not evidence of
Alpha Solver value. A case should be killed or revised if it is too easy, too
ambiguous to score, unsafe, biased toward either system, or fails to expose a
meaningful behavioral difference across systems.

## Readiness

The case set is ready for operator review and future simulation-only planning.
It is not an executed evaluation, not a scored packet, not benchmark evidence,
and not authorization to call providers.
