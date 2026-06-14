# Selected next lane

`ALPHA-SOLVER-DEF-002-DATA-CLASSIFICATION-RUNTIME-MIGRATION-001`

## Purpose

Migrate runtime classification enforcement to the canonical registry decision
made in this packet, or generate runtime compatibility rules from the canonical
registry with explicit tests.

## Entry criteria

- Operator approves changing runtime classification behavior.
- Expected handling for `pii`, `phi`, `secret`, and `token` is explicitly stated.
- Replay, shortlist snapshot, JSONL logging, provider-call, and dashboard data
  surfaces have approved event/data schemas or redaction requirements.
- Validation commands for the lane have an explicit no-provider profile before any
  broad suite is attempted.

## Non-goals

- Do not call live providers.
- Do not expose `/v1/solve` or dashboard publicly.
- Do not claim DEF-002 closure unless all remaining DEF-002 gates are separately
  closed or accepted.
