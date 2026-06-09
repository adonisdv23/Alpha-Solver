# Checks run

| Check | Result | Notes |
| --- | --- | --- |
| `git status --short` | Passed | Showed only approved-scope changed files before commit. |
| `git diff --name-only` | Passed | Tracked diff showed `alpha/self_operator/__init__.py`; untracked approved files were visible in status. |
| `git diff --check` | Passed | No whitespace errors. |
| `python -m ruff check alpha/self_operator tests/test_self_operator_approval.py tests/test_self_operator_stop_state.py tests/test_self_operator_execution_gate.py tests/test_self_operator_dry_run.py` | Passed | Focused self-operator lint passed. |
| `python -m pytest -q tests/test_self_operator_dry_run.py` | Passed | 21 tests passed. |
| `python -m pytest -q tests/test_self_operator_approval.py tests/test_self_operator_stop_state.py tests/test_self_operator_execution_gate.py` | Passed | 32 tests passed. |
| `python -m pytest -q tests/test_self_operator_artifact_schema.py tests/test_self_operator_artifact_store.py tests/test_self_operator_preflight.py tests/test_self_operator_command_classification.py` | Passed | 38 tests passed. |
| `python -m pytest -q tests/test_self_operator_static_guardrails.py tests/test_self_operator_approval_stopstate_static.py tests/test_self_operator_artifact_schema_static.py tests/test_self_operator_forbidden_behavior_static.py` | Passed | 16 tests passed. |
| `make check-local-llm-orchestration-guardrails` | Passed | Evidence-boundary, doc path/link, and packet consistency checks passed. |
| `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-12-self-operator-local-harness-dry-run-wrapper` | Passed | One packet directory scanned. |
| `rg -n "stop if explicit operator confirmation is missing|blocked_by_approval_identity_mismatch|approval_identity_mismatch|SELF_OPERATOR_APPROVAL_IDENTITY_MISMATCH|local-only|operator-supervised|does not execute proposed commands|does not run acceptance|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-MANUAL-LOCAL-ACCEPTANCE-PACKET-001" alpha/self_operator tests docs/evals/runs/alpha-solver-post-level-3-level-12-self-operator-local-harness-dry-run-wrapper` | Passed | Required tokens found. |
| `python -m pytest -q` | Failed, unrelated/out-of-scope | Existing provider/API/security/cost tests failed outside this lane: three `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[...]` failures expected `gpt-5` but observed `gpt-5-mini`; `tests/test_cost_tracking.py::test_cost_tracking` did not create `artifacts/costs.csv`; `tests/test_security.py::test_a3_1_prompt_subset_passes_solve_input_validation` returned a non-`ok` answer. |
