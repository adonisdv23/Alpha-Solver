# Offline Test Results

Lane: `ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-IMPLEMENTATION-001`

## Commands run

- `python -m pytest -q tests/test_local_llm_provider_adapter.py`
- `python -m pytest -q tests/test_local_llm_contract_consumption_proof.py`

## Result summary

The focused adapter tests passed with offline fixtures and injected transports.
The contract-consumption proof tests passed and continued to use fake-client-only
paths.

## Network/provider boundary

The default-off backend test monkeypatched the URL opener to fail if a socket was
opened, then confirmed the disabled backend fails closed before transport. No
live provider, local model, hosted service, `/v1/solve`, or dashboard path was
called by these tests.

## Evidence label

The test outputs are non-evidence or offline fixture evidence only.
`behavior_evidence` remains `False`.
