# Offline Test Results

Lane ID: `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-HARDENING-001`

## Commands to run for this lane

```text
python -m pytest -q tests/test_local_llm_provider_adapter.py
python -m pytest -q tests/test_local_llm_contract_consumption_proof.py
python -m compileall -q alpha/local_llm
```

## Expected coverage

- Rejected hosted endpoints fail closed before injected transport invocation.
- Allowed loopback endpoints reach injected fake transport.
- Behavior evidence remains false.
- Existing local LLM adapter tests continue to pass.
- Contract-consumption proof tests continue to pass.

## Boundary

These are offline tests only. They do not run Ollama, a local model, a hosted provider, `/v1/solve`, dashboard preview, Batch C, benchmark, billing, or provider orchestration.
