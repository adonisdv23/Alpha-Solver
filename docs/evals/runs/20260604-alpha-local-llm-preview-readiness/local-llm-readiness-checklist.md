# Local LLM Readiness Checklist

Lane ID: `ALPHA-LOCAL-LLM-PREVIEW-READINESS-001`

Status: checklist for future approval; not an approval.

## Future implementation approval checklist

- [ ] A specific implementation lane is approved before code changes begin.
- [ ] Portable contract consumption is proven from `alpha_solver_portable.py` or an approved transformed equivalent.
- [ ] Prompt source path and hash are preserved in safe metadata.
- [ ] Local provider is isolated from smoke-only `MODEL_PROVIDER=local`.
- [ ] A distinct provider value such as `MODEL_PROVIDER=local_llm` or `MODEL_PROVIDER=ollama` is used.
- [ ] Model/backend labels include backend, model name, model tag/version, endpoint class, timeout, and local-only setting.
- [ ] Tests use fake clients/transports by default and do not require Ollama, OpenAI, Anthropic, or other provider calls.
- [ ] No provider calls occur unless a later explicit lane authorizes a real local backend run.
- [ ] No operator tests are executed.
- [ ] No Batch C work is started.
- [ ] No Google Sheets files or external planning ledgers are updated.
- [ ] No scored artifacts, raw outputs, scorer-facing packets, or operator-only maps are modified.
- [ ] No unsupported claims are made.

## Stop conditions for future implementation

- [ ] Stop if the path cannot prove portable-contract consumption.
- [ ] Stop if `MODEL_PROVIDER=local` must be overloaded or smoke behavior breaks.
- [ ] Stop if local LLM execution can silently fall back to `_tree_of_thought` or v91.
- [ ] Stop if endpoint config can call non-local endpoints in local-only mode.
- [ ] Stop if prompt echoes or empty outputs would be accepted as behavior evidence.
- [ ] Stop if tests require real provider credentials or cloud calls.
- [ ] Stop if artifacts would blur local LLM preview evidence with operator-test, Batch C, validation, or production-readiness evidence.

## Tests required before behavior evidence

- [ ] Contract loader test.
- [ ] Request injection test.
- [ ] No-v91/no-`_tree_of_thought` fallback test for local LLM mode.
- [ ] Smoke isolation test for `MODEL_PROVIDER=local`.
- [ ] Safe metadata test.
- [ ] Missing backend/model/contract failure tests.
- [ ] Empty answer and prompt-echo failure or non-evidence-label tests.
- [ ] Surface-specific tests for `/dashboard/expert-preview`, `/v1/solve`, or dev-only route if one is included.
