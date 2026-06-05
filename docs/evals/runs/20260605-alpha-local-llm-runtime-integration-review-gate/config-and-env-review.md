# Config and Environment Review

## Reviewed files

- `.env.example`
- `scripts/check_env.py`
- `service/config/validators.py`
- `tests/test_config_validation.py`
- `tests/config/test_loader.py`

## Findings

- `.env.example` defaults to `MODEL_PROVIDER=local`; the optional local LLM block is commented and marked default-off.
- The optional local LLM block requires `MODEL_PROVIDER=local_llm`, `ALPHA_LOCAL_LLM_ENABLED=true`, `ALPHA_LOCAL_LLM_ENDPOINT`, `ALPHA_LOCAL_LLM_MODEL`, and `ALPHA_LOCAL_LLM_TIMEOUT_SECONDS`.
- `.env.example` says local LLM mode requires localhost/loopback, exact local model name, finite timeout, and no provider keys.
- `scripts/check_env.py` includes `local_llm` as an allowed provider but performs local LLM-specific validation only when `MODEL_PROVIDER=local_llm` is selected.
- `scripts/check_env.py` requires explicit enablement and required local runtime fields for local LLM mode.
- `scripts/check_env.py` rejects hosted provider keys for local LLM mode, including OpenAI, Anthropic, Google/Gemini, and DeepSeek key variables.
- `scripts/check_env.py` delegates final local LLM validation to `LocalLLMRuntimeConfig.from_env()` and records fail-closed reason labels.
- `service/config/validators.py` accepts `local_llm` as a user-facing provider value for configuration shape validation only; this does not imply provider execution.

## Decision impact

Configuration and environment review found no blocker for bounded manual smoke. The next smoke lane must still record exact operator-selected endpoint, model, timeout, and provider-key absence before execution.
