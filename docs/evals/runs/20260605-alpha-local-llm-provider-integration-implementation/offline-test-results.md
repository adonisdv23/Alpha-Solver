# Offline Test Results

Commands run for this lane:

```text
python -m pytest -q tests/test_local_llm_provider_adapter.py
python -m pytest -q tests/test_local_llm_contract_consumption_proof.py
```

Results:

- Local LLM provider adapter tests passed offline.
- Contract consumption proof tests passed offline.
- The contract proof command emitted third-party deprecation warnings from
  FastAPI routing under Python 3.14; the tests still passed.

No network, provider, model, runtime route, dashboard, or operator run was
started by these tests.
