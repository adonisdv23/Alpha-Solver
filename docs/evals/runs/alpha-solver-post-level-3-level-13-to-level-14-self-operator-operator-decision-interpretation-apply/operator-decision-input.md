# Operator-decision input

The operator-decision input is the #469 packet's machine-readable decision
artifact, read read-only:

```text
docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-expected-safety-block-operator-review/operator-decision.json
```

Verbatim content (sha256
`db074b7b15b7b8cf5bd9636cbede0ed37ec447e8397a9a8ef2af0729ebacb30e`, identical
before and after this lane):

```json
{
  "schema": "self_operator.expected_safety_block_operator_review.v1",
  "lane_id": "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-TO-LEVEL-14-SELF-OPERATOR-EXPECTED-SAFETY-BLOCK-OPERATOR-REVIEW-001",
  "operator_decision": "ACCEPT_LEDGER_LEVEL_CONFIRMATION",
  "accepted_tasks": ["MLA-006", "MLA-007"],
  "confirmation_type": "operator_ledger_level_acceptance",
  "machine_readable_artifact_confirmation": false,
  "source_artifacts_mutated": false,
  "readiness_claimed": false
}
```

## Validation applied before consumption

`validate_operator_decision` requires every field to match this recorded
artifact exactly before the decision may be consumed:

- `schema` must be `self_operator.expected_safety_block_operator_review.v1`;
- `lane_id` must be the #469 operator-review lane ID;
- `operator_decision` must be `ACCEPT_LEDGER_LEVEL_CONFIRMATION`;
- `accepted_tasks` must be exactly `["MLA-006", "MLA-007"]` (no subset,
  superset, substitution, or duplication);
- `confirmation_type` must be `operator_ledger_level_acceptance`;
- `machine_readable_artifact_confirmation` must be boolean `false` — a
  decision claiming machine-readable artifact confirmation on this path is
  rejected;
- `source_artifacts_mutated` must be boolean `false`;
- `readiness_claimed` must be boolean `false`.

Any validation failure means the decision is not consumed: the
MLA-006/MLA-007 P1 blockers remain open, interpretation stays `blocked`, and
the result reports the reasons in
`operator_decision_consumption.validation_errors` plus a P2
`OPERATOR_DECISION_INVALID` defect. The real artifact above passed
validation.
