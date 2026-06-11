# Operator-decision interpretation apply (MLA-006 / MLA-007 consumption)

- Lane ID: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-TO-LEVEL-14-SELF-OPERATOR-OPERATOR-DECISION-INTERPRETATION-APPLY-001`
- Date: 2026-06-10
- Scope: teach the acceptance interpretation engine to consume the explicit
  #469 operator-decision artifact, then apply interpretation with the
  unchanged #465 accepted import summary plus that decision. This lane never
  pretends the decision is machine-readable artifact confirmation, never
  mutates source evidence or prior packets, never runs the release gate, and
  never claims readiness.

## Prerequisites verified on current `main` (commit `fd568aa`)

- PR #469 merged into `main` (`fd568aa` "docs(self-operator): record expected
  safety-block operator acceptance (#469)"); working branch baseline identical
  to `origin/main`.
- #469 operator-review packet present:
  `docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-expected-safety-block-operator-review/`
  containing `operator-decision.json` with exactly
  `operator_decision = ACCEPT_LEDGER_LEVEL_CONFIRMATION`,
  `accepted_tasks = ["MLA-006", "MLA-007"]`,
  `confirmation_type = operator_ledger_level_acceptance`,
  `machine_readable_artifact_confirmation = false`,
  `source_artifacts_mutated = false`, `readiness_claimed = false`.
- #465 accepted import summary present and unchanged:
  `docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json`
  (sha256 `a54ebd46e8533b17738b302e6177b282348f811d7f6b694f75bea7ba2cf8285c`,
  identical before and after this lane).

## What this lane changed (code)

- `alpha/self_operator/acceptance_interpretation.py`: optional, explicit
  `operator_decision` input; strict validation of schema, lane ID, decision
  value, accepted tasks, confirmation type, and safety flags
  (`validate_operator_decision`); a validated decision closes only the
  MLA-006/MLA-007 `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` blockers; the result
  carries a deterministic `operator_decision_consumption` record and per-task
  `expected_block_confirmation` labels that keep operator ledger-level
  acceptance distinct from machine-readable artifact confirmation.
- `scripts/interpret_self_operator_acceptance.py`: narrow `--operator-decision`
  CLI input; CLI line reports `operator_decision=consumed|invalid|not_provided`,
  the confirmation type, and `machine_readable_artifact_confirmation=false`.
- `tests/test_self_operator_acceptance_interpretation.py`: 12 focused tests for
  valid consumption, the operator/machine confirmation distinction, invalid
  schema, wrong accepted tasks, `machine_readable_artifact_confirmation=true`
  rejection, safety-flag rejection, only-MLA-006/007 effect, allowed-defect
  non-clearing, missing-decision behavior, determinism, and CLI paths.

No other code changed. `alpha/self_operator/result_import.py`,
`scripts/import_self_operator_acceptance_results.py`, runtime solve behavior,
and provider/model/API/dashboard/deployment/billing/credential/secret files
were not touched (`changed-file-scope-proof.md`).

## Interpretation applied (this lane's output)

With the unchanged accepted import summary plus the #469 decision artifact
(`interpretation-result.json`, sha256 of two consecutive runs identical:
`dd3385e97239ddbd3b8829b409faaf73895ea28ccc1d646fe0d69a4e0e3c7dd6`):

```text
readiness_implication = eligible_for_later_release_review
defect_count = 0 (p0=0, p1=0, p2=0, p3=0)
operator_decision_consumption.consumed = true
operator_decision_consumption.applied_task_ids = ["MLA-006", "MLA-007"]
operator_decision_consumption.confirmation_type = operator_ledger_level_acceptance
operator_decision_consumption.machine_readable_artifact_confirmation = false
```

Both prior P1 `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` defects are closed by
explicit operator-decision consumption; MLA-006/MLA-007 remain
`observed_outcome = "unconfirmed"` in the machine-readable record with their
confirmation of record labeled `operator_ledger_level_acceptance`, never
machine-readable artifact confirmation. `eligible_for_later_release_review`
is the engine's bounded vocabulary and is not a readiness claim
(`non_claims` recorded in the result).

## File index

- `source-evidence-reviewed.md` — read-only prerequisite verification
- `changed-file-scope-proof.md` — allowed-scope proof for every changed file
- `interpretation-input.md` — the accepted import summary input
- `operator-decision-input.md` — the operator-decision artifact input
- `operator-decision-consumption.md` — required consumption record
- `interpretation-result.md` / `interpretation-result.json` — applied result
- `defect-register.md` — defect counts and closures
- `p0-p1-review.md` — P0/P1 review
- `checks-run.md` — commands and outputs
- `evidence-boundary.md`, `non-actions.md` — boundary and non-actions
- `selected-next-lane.md`, `blocker-fallback-lane.md` — lane continuity
