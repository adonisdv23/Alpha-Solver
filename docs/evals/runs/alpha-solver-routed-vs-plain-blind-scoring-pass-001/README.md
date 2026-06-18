# Routed-vs-plain blind scoring pass 001

This packet records `ALPHA-SOLVER-ROUTED-VS-PLAIN-BLIND-SCORING-PASS-001`.

## Objective

Score the 12 blinded Response A / Response B task pairs from the approved scorer-facing packet before any unblinding or final interpretation.

## Evidence boundary

Only the approved scorer-facing packet and authorization/prep materials were used. This packet does not include or rely on source identities, source artifacts, route metadata, an A/B key, a source map, runtime execution, provider calls, local-model calls, tool execution, browsing, Sheets mutation, deployment, or external/current research.

## Outputs

- `score-output.md` contains all 12 locked blind task scores.
- `task-scores/` mirrors one task per file for readability.
- `score-lock-confirmation.md` records the pre-unblinding lock.
- `selected-next-state.md` records the review-only next state.
