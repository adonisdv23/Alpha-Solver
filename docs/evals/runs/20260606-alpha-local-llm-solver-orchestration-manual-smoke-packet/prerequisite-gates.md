# Prerequisite Gates

Manual smoke remains blocked unless every prerequisite below is true.

## Required upstream records

- PR #327 is squashed, merged, closed, and recorded in GS.
- PR #328 is squashed, merged, closed, and recorded in GS.
- PR #329 is squashed, merged, closed, and recorded in GS.
- PR #330 is squashed, merged, closed, and recorded in GS.
- PR #331 is squashed, merged, closed, and recorded in GS.
- Local LLM runtime track is closed with terminal next action: `STOP-HERE-LOCAL-LLM-RUNTIME-TRACK-CLOSED`.
- Local LLM solver orchestration implementation lane is complete.
- `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-IMPLEMENTATION-REVIEW-GATE-001` authorizes smoke.

## Required authorization phrase

The implementation review gate must return exactly:

`AUTHORIZE_MANUAL_LOCAL_ORCHESTRATION_SMOKE`

If the phrase is absent, partial, superseded, contradicted, or ambiguous, classify the smoke attempt as `review gate not authorized` and do not execute it.

## Concurrent review gate note

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-IMPLEMENTATION-REVIEW-GATE-001` may be running concurrently with this packet. This packet does not presume the review-gate result.
