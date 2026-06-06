# Selected Next Lane

## Required decision

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-IMPLEMENTATION-001`

## Decision count

Exactly one next lane is selected.

## Rationale

The highest-value next step is to implement local solver orchestration before API or dashboard exposure. The implementation lane should integrate local expert two-pass, local orchestration envelope, local confidence/clarify/block gates, and then bounded local ToT-lite while preserving the local-only, no-provider-fallback, `behavior_evidence=false` boundary until a later evidence lane explicitly changes it.
