# Test Results

Checks run in this implementation lane:

- `python -m pytest -q tests/test_local_llm_runtime_integration.py` — passed, including redirect fail-closed coverage for 301, 302, 303, 307, and 308.
- `python -m pytest -q tests/test_local_llm_runtime_integration.py tests/test_local_llm_provider_adapter.py` — passed.
- `python -m pytest -q tests/test_config_validation.py tests/config/test_loader.py` — passed.
- `python -m pytest -q tests/test_api_endpoints.py::test_solve_local_mode_ignores_provider_factory tests/test_api_endpoints.py::test_solve_expert_route_local_mode_preserves_local_response tests/ui/test_expert_preview.py::test_local_provider_expert_preview_ignores_route_context` — passed with upstream deprecation warnings.
- `python -m pytest -q tests/providers/test_openai_provider.py tests/providers/test_provider_contract.py tests/providers/test_provider_accounting.py tests/providers/test_provider_telemetry.py` — passed.
- `python -m ruff check alpha/local_llm/provider_adapter.py scripts/check_env.py service/config/validators.py tests/test_local_llm_runtime_integration.py tests/test_local_llm_provider_adapter.py tests/test_config_validation.py` — passed.
- `python -m py_compile alpha/local_llm/provider_adapter.py scripts/check_env.py service/config/validators.py` — passed.
- `python -m pytest -q` — failed in pre-existing unrelated areas after the focused checks passed: `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[...]` expected `gpt-5` but observed `gpt-5-mini`; `tests/test_cost_tracking.py::test_cost_tracking`; and `tests/test_security.py::test_a3_1_prompt_subset_passes_solve_input_validation`.

These checks use offline fakes and injected transports only. They do not call a hosted provider or a real local model.
