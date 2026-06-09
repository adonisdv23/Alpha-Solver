# PR #456 approval identity/correlation follow-up

Lane: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-SELF-OPERATOR-APPROVAL-IDENTITY-MISMATCH-FIX-001`

PR #456 was merged with a blocking approval identity/correlation follow-up: a valid approval record for one lane could be evaluated with a proposed task for another lane because the execution gate validated approval completeness separately from proposed-task identity.

This follow-up fixes the issue by failing closed before any `allowed_for_local_dry_run_wrapper` readiness result when available approval and proposed-task identity fields mismatch. The added gate check compares lane identity, run identity when both sides expose it, and comparable scope/task identity when present.

Focused tests were added in `tests/test_self_operator_execution_gate.py` for lane mismatch, run mismatch, scope mismatch, deterministic blocked reason/finding output, stop-state creation, continued matching approval readiness, non-execution of proposed commands, deterministic JSON serialization, and temporary-output-root bounded artifact writes.

Checks run for this follow-up are recorded in this PR and include focused ruff, focused approval/stop-state/execution-gate tests, #454 foundation tests, static guardrail tests, packet consistency, and a full-suite attempt where practical.

Evidence boundary is unchanged: this is a local approval-boundary safety fix only. It does not run Self Operator, execute proposed commands, call providers, run hosted or local models, expose APIs or dashboards, change product CLI behavior, automate browsers, deploy, bill, touch credentials, update Google Sheets, mutate source artifacts, promote evidence, run acceptance, or claim MVP readiness.

The dry-run harness lane remains blocked until this fix is merged and GS done:

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-12-SELF-OPERATOR-LOCAL-HARNESS-DRY-RUN-WRAPPER-001`

## Checks run for this follow-up

- `git status --short` — passed; showed only the scoped execution-gate, focused test, and packet follow-up changes.
- `git diff --name-only` — passed; changed paths remained limited to `alpha/self_operator/execution_gate.py`, `tests/test_self_operator_execution_gate.py`, and this packet follow-up file.
- `git diff --check` — passed; no whitespace errors reported.
- `python -m ruff check alpha/self_operator tests/test_self_operator_approval.py tests/test_self_operator_stop_state.py tests/test_self_operator_execution_gate.py` — passed.
- `python -m pytest -q tests/test_self_operator_approval.py tests/test_self_operator_stop_state.py tests/test_self_operator_execution_gate.py` — passed, 32 tests.
- `python -m pytest -q tests/test_self_operator_artifact_schema.py tests/test_self_operator_artifact_store.py tests/test_self_operator_preflight.py tests/test_self_operator_command_classification.py` — passed, 38 tests.
- `python -m pytest -q tests/test_self_operator_static_guardrails.py tests/test_self_operator_approval_stopstate_static.py tests/test_self_operator_artifact_schema_static.py tests/test_self_operator_forbidden_behavior_static.py` — passed, 16 tests.
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-11-self-operator-approval-stopstate-gate-foundation` — passed.
- `python -m pytest -q` — failed on pre-existing unrelated product tests: `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[timeout-504]`, `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[rate_limit-429]`, `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[network-503]`, `tests/test_cost_tracking.py::test_cost_tracking`, and `tests/test_security.py::test_a3_1_prompt_subset_passes_solve_input_validation`.
