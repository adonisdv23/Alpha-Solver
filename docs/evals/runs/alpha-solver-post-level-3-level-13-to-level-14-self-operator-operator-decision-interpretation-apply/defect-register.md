# Defect register

## This lane's applied interpretation (with operator decision)

```text
P0: 0
P1: 0
P2: 0
P3: 0
total: 0
```

## Defects closed by this lane (via explicit operator-decision consumption)

| Task | Defect | Severity | Prior state (#466/#467/#468 record) | Closure |
| --- | --- | --- | --- | --- |
| MLA-006 | `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` | P1 | open, blocked | closed by validated `ACCEPT_LEDGER_LEVEL_CONFIRMATION`; confirmation of record `operator_ledger_level_acceptance` |
| MLA-007 | `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` | P1 | open, blocked | closed by validated `ACCEPT_LEDGER_LEVEL_CONFIRMATION`; confirmation of record `operator_ledger_level_acceptance` |

The closures do not rewrite history: the prior packets that recorded these
defects are unchanged, and the machine-readable import summary still carries
`expected_safety_block_confirmed: false` for both tasks. The closure exists
only in this lane's interpretation output, attributed explicitly to the #469
operator decision (`operator_decision_consumption`), and it is not
machine-readable artifact confirmation.

## Defects deliberately not closeable by an operator decision (regression-proven)

- `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` for any task other than MLA-006/MLA-007
  (test: unconfirmed MLA-002 stays P1 with a valid decision).
- `EXPECTED_SAFETY_BLOCK_ALLOWED` (test: MLA-006 observed `ready` stays P1
  with a valid decision; the decision closes only the unconfirmed blocker).
- All P0/P1/P2/P3 behavior for every other task and field is preserved; the
  pre-existing suite passes unchanged.

## New defect class introduced by this lane

- `OPERATOR_DECISION_INVALID` (P2, `blocked_malformed_artifacts`): emitted
  only when a provided decision artifact fails validation (wrong schema, lane
  ID, decision value, accepted tasks, confirmation type, or safety flags —
  including `machine_readable_artifact_confirmation: true`). The blockers are
  then not cleared and interpretation remains `blocked` with the reasons
  reported in `operator_decision_consumption.validation_errors`.

## Remaining blockers

None in this lane's applied interpretation (p0=0, p1=0, p2=0, p3=0).
