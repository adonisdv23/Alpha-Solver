# Validation Results

Final validation results are recorded for the committed change.

## Passing required static checkers

- `python scripts/check_local_llm_doc_paths.py` passed: `Local LLM/post-Level/OpenAI doc path/link check passed (1605 files scanned).`
- `python scripts/check_local_llm_evidence_boundaries.py` passed: `Local LLM evidence-boundary static check passed (2006 files scanned).`
- `python scripts/check_local_llm_packet_consistency.py` passed: `Local LLM packet consistency check passed (155 packet directories scanned).`

## Focused tests

- `python -m pytest tests/test_local_llm_doc_paths.py tests/test_local_llm_evidence_boundaries.py tests/test_local_llm_packet_consistency.py -q` passed: `31 passed`.

## Full pytest

- `python -m pytest -q` was run and failed in unrelated runtime/provider tests outside this docs/static-checker lane.
- Observed failures:
  - `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[timeout-504]`
  - `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[rate_limit-429]`
  - `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[network-503]`
  - `tests/test_cost_tracking.py::test_cost_tracking`
  - `tests/test_security.py::test_a3_1_prompt_subset_passes_solve_input_validation`
- The full-suite output included live OpenAI HTTP logging from pre-existing test environment/provider configuration. This lane did not intentionally add provider calls or modify runtime/provider/model behavior.
