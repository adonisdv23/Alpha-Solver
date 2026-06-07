# Local LLM solver orchestration retry 007 smoke expectation update

Lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-RETRY-007-SMOKE-EXPECTATION-UPDATE-001`

## Purpose

This packet updates the retry 007 Prompt 3 smoke expectation surface after the Prompt 3 spec expectation decision selected `KEEP_CURRENT_RULE`.

The update is documentation / expectation alignment only. It does not change runtime solver behavior, provider behavior, API exposure, dashboard exposure, fallback behavior, allowlists, safety gates, boundary fail-closed behavior, model field exposure, or evidence promotion.

## Source decision confirmed

The source decision packet records decision path `KEEP_CURRENT_RULE` and states that `missing_information_too_broad` blocks `answer_with_assumptions` for Prompt 3 and the bounded local Python CLI startup-plan shape.

## Updated expectation

Prompt 3 is now conditional:

- if the assumption gate passes, the expected success-path mode remains `answer_with_assumptions`;
- if `missing_information_too_broad` fires for `03-answer-with-assumptions` under `prompt_shape=bounded_local_python_cli_startup_plan`, `clarify` is acceptable and should not be treated as a smoke failure when the safety and boundary conditions listed in this packet are preserved.

## Packet index

1. [source-decision-summary.md](source-decision-summary.md)
2. [prompt-3-expectation-update.md](prompt-3-expectation-update.md)
3. [accepted-outcome-matrix.md](accepted-outcome-matrix.md)
4. [safety-boundary-preservation.md](safety-boundary-preservation.md)
5. [changed-files-ledger.md](changed-files-ledger.md)
6. [blocked-work.md](blocked-work.md)
7. [selected-next-lane.md](selected-next-lane.md)
8. [evidence-boundary.md](evidence-boundary.md)
9. [checks-run.md](checks-run.md)
