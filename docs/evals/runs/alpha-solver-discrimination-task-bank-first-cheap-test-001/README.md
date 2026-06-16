# ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-FIRST-CHEAP-TEST-001

## Lane ID

`ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-FIRST-CHEAP-TEST-001`

## Objective

Prepare a first cheap-test packet that turns the existing discrimination task-bank feasibility work and the substantive derivation / no-echo gate into a small, repeatable, evidence-bounded test design.

This packet is preparation only. It does not execute the task bank, generate outputs, score outputs, call providers, run local models, call runtime endpoints, expose dashboard or public API behavior, expose `/v1/solve`, or mutate Google Sheets.

## Source evidence reviewed

- `docs/CURRENT_STATE.md`
- `docs/LANE_REGISTRY.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/README.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/derivation-vs-echo-criteria.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/fixture-plan.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/heuristic-spec.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/test-plan.md`
- `docs/evals/runs/alpha-solver-discrimination-task-bank-asset-001/README.md`
- `docs/evals/runs/alpha-solver-discrimination-task-bank-asset-001/repeatability-plan.md`
- Existing committed discrimination task-bank docs found under `docs/evals/runs/alpha-solver-discrimination-task-bank-asset-001/`
- Existing safe static checker docs and scripts referenced by `scripts/check_narrative_claim_safety.py`, `scripts/check_local_llm_evidence_boundaries.py`, and `scripts/check_local_llm_packet_consistency.py`

No raw Alpha outputs or raw baseline outputs were inspected.

## Relationship to the derivation / no-echo gate

This packet follows the substantive derivation / no-echo gate by using its review vocabulary for exact echo, near echo, paraphrase-only response, substantive derivation, acceptable source use, unsupported copying, and non-answer safe-out. The canonical copying failure label is `unsupported_copying`.

The packet does not change the gate, run the gate, or claim the gate passed on any model output.

## Relationship to the discrimination task-bank asset

The discrimination task-bank asset established that a guarded follow-up is feasible. This packet narrows that follow-up into an operator-review-only cheap-test design with a small candidate set, evidence-boundary markers, and fixture-schema expectations.

It does not execute the task bank or turn the asset into benchmark evidence.

## Evidence boundary

Evidence is limited to committed docs, synthetic design sketches, and approved committed text references. The packet excludes raw Alpha outputs, raw baseline outputs, source identity inference, unblinding, score changes, source-map work, provider behavior, local-model behavior, runtime behavior, dashboard behavior, public API behavior, `/v1/solve`, and Google Sheets behavior.

## Packet contents

1. `README.md`
2. `cheap-test-objective.md`
3. `case-selection-rules.md`
4. `fixture-schema.md`
5. `candidate-case-list.md`
6. `execution-plan.md`
7. `operator-review-checklist.md`
8. `stop-conditions.md`
9. `non-actions.md`
10. `non-claims.md`
11. `selected-next-state.md`
12. `checks-run.md`

## Selected-next state after merge

`OPERATOR_REVIEW_REQUIRED_AFTER_DISCRIMINATION_TASK_BANK_FIRST_CHEAP_TEST_001`

This is review-only. It authorizes no execution, scoring, providers, local models, runtime endpoints, dashboard or public API work, `/v1/solve`, Google Sheets mutation, source-map work, unblinding, dependencies, release behavior, or broad claims.

## Non-actions and non-claims summary

This lane performs docs-only packet preparation. It does not run systems, inspect raw outputs, score, unblind, add dependencies, release behavior, or support claims of Alpha superiority, benchmark success, value proof, readiness, provider validation, hosted-model validation, local-model validation, runtime validation, security/privacy completion, partnership readiness, Pi.dev integration, buyer validation, traction, or external-use approval.
