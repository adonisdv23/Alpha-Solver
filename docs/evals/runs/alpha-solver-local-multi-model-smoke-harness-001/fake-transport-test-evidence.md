# Fake Transport Test Evidence

CI tests use fake transports only and do not require Ollama.

Targeted test command:

```bash
python -m pytest -q tests/test_local_llm_multi_model_smoke_harness.py tests/test_local_llm_provider_adapter.py
```

Coverage assertions:

1. Multiple model names are iterated safely.
2. Hosted provider keys in env fail closed before transport.
3. Non-loopback endpoints fail closed before transport.
4. Empty output fails closed.
5. Prompt echo is detected.
6. Per-model result records do not claim behavior evidence.
7. No hosted fallback exists on local connection failure.

Verdict: `LOCAL_MULTI_MODEL_SMOKE_HARNESS_CAPTURED_FAKE_TRANSPORT_ONLY`.
