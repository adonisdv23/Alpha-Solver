# Checks run

All checks were local. No proposed task commands, providers, hosted/local models, browser automation, deployments, billing checks, credential access, Google Sheets updates, acceptance execution, source-artifact mutation, or evidence promotion were intentionally run.

- `git status --short` — passed; showed only this lane's scoped source, test, and docs changes after reverting test-created unrelated artifacts.
- `git diff --name-only` — passed; changed paths remained limited to `alpha/self_operator/`, focused tests, the #453 runbook packet marker follow-up, and this packet.
- `git diff --check` — passed; no whitespace errors reported.
- `python -m ruff check .` — failed on pre-existing unrelated lint findings under `service/` and `tools/`; no findings were reported for this lane's new files in the focused ruff check.
- `ruff check .` — expected to report the same pre-existing unrelated lint findings as `python -m ruff check .`.
- `python -m pytest -q tests/test_self_operator_approval.py tests/test_self_operator_stop_state.py tests/test_self_operator_execution_gate.py` — passed, 27 tests.
- `python -m pytest -q tests/test_self_operator_artifact_schema.py tests/test_self_operator_artifact_store.py tests/test_self_operator_preflight.py tests/test_self_operator_command_classification.py` — passed, 38 tests.
- `python -m pytest -q tests/test_self_operator_static_guardrails.py tests/test_self_operator_approval_stopstate_static.py tests/test_self_operator_artifact_schema_static.py tests/test_self_operator_forbidden_behavior_static.py` — passed, 16 tests.
- `make check-local-llm-orchestration-guardrails` — passed; evidence-boundary, doc path/link, and packet consistency checks passed.
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-11-self-operator-approval-stopstate-gate-foundation` — passed for this packet.
- Focused marker `rg` check — passed; the updated Level 10/11/12 marker and explanatory sentence were present, and the old Level 11/12-only marker was absent from the #453 packet.
- `python -m pytest -q` — failed on pre-existing unrelated product tests: `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[timeout-504]`, `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[rate_limit-429]`, `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[network-503]`, `tests/test_cost_tracking.py::test_cost_tracking`, and `tests/test_security.py::test_a3_1_prompt_subset_passes_solve_input_validation`.
