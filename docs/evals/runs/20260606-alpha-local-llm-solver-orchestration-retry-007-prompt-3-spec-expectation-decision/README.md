# Local LLM solver orchestration retry 007 Prompt 3 spec expectation decision

## Lane

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-RETRY-007-PROMPT-3-SPEC-EXPECTATION-DECISION-001`

## Purpose

This packet records the docs/spec decision after the retry 007 diagnostic classification selected `prompt expectation mismatch requiring spec review` for Prompt 3.

The decision is intentionally limited to the Prompt 3 contract. It does not change runtime behavior, test fixtures, provider behavior, smoke artifacts, Google Sheets, backlog workbooks, `/v1/solve`, dashboard exposure, billing, MCP, replay, observability, or unrelated solver behavior.

## Selected decision

Exactly one decision path is selected:

`KEEP_CURRENT_RULE`

`missing_information_too_broad` continues to block `answer_with_assumptions`. Prompt 3 `clarify` is acceptable when that reason code fires.

## Selected next lane

Exactly one selected next lane is recorded:

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-RETRY-007-SMOKE-EXPECTATION-UPDATE-001`

## Files in this packet

1. `README.md`
2. `source-classification-summary.md`
3. `prompt-3-contract-review.md`
4. `decision-options-reviewed.md`
5. `selected-decision.md`
6. `rationale.md`
7. `safety-invariant-preservation.md`
8. `implementation-authorization.md`
9. `smoke-expectation-impact.md`
10. `selected-next-lane.md`
11. `blocked-work.md`
12. `evidence-boundary.md`
13. `checks-run.md`
