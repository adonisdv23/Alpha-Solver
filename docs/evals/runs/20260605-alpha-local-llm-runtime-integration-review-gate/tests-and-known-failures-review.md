# Tests and Known Failures Review

## Focused tests run

Command:

```bash
python -m pytest -q tests/test_local_llm_runtime_integration.py tests/test_local_llm_provider_adapter.py tests/test_config_validation.py tests/config/test_loader.py
```

Result: passed.

Observed output summary:

```text
........................................................................ [ 74%]
.........................                                                [100%]
```

## Full suite run

Command:

```bash
python -m pytest -q
```

Result: failed in unrelated pre-existing areas.

Known failures observed:

- `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[timeout-504]` expected model `gpt-5` and observed `gpt-5-mini`.
- `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[rate_limit-429]` expected model `gpt-5` and observed `gpt-5-mini`.
- `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[network-503]` expected model `gpt-5` and observed `gpt-5-mini`.
- `tests/test_cost_tracking.py::test_cost_tracking` failed in the existing cost-tracking area.
- `tests/test_security.py::test_a3_1_prompt_subset_passes_solve_input_validation` failed in the existing security/input-validation area.

These failures are not local LLM runtime integration failures and do not hide a local LLM blocker because the focused local LLM/config suite passed and the full-suite failures occur in OpenAI provider telemetry/model expectations, cost tracking, and input validation.

## Fake/injected-only confirmation

The reviewed local LLM tests use injected fake transports, stub backends, monkeypatched openers, and subprocess config checks. They do not call a real local model, do not call hosted providers, and do not require provider keys.

## Decision impact

Focused test evidence is clean enough for a bounded manual smoke lane. The full-suite failures should remain recorded as unrelated/pre-existing until repaired by separate lanes.
