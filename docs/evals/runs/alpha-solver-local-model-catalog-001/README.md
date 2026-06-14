# Alpha Solver Local Model Catalog 001

Lane ID: `ALPHA-SOLVER-LOCAL-MODEL-CATALOG-001`

Verdict: `LOCAL_MODEL_CATALOG_CAPTURED`

## TLDR

This packet inventories Ollama-hosted local model families that operators may consider for free local testing before any paid-provider testing. It is documentation only: no models were installed, no Ollama endpoint was called, no default urllib loopback transport was exercised, no hosted providers were called, and no routing behavior was exercised.

## Source context inspected

- `alpha/local_llm/provider_adapter.py`
- `alpha/local_llm/operator_cli.py`
- `alpha/local_llm/orchestration_runner.py`
- `docs/local_llm_solver_orchestration_operator_guide/`
- `docs/local_llm_solver_orchestration_guardrails/`
- `docs/evals/runs/20260604-alpha-local-llm-preview-readiness/`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/`

## Packet files

- `current-local-llm-adapter-map.md`
- `ollama-model-candidates.md`
- `model-role-matrix.md`
- `local-resource-notes.md`
- `routing-opportunity-map.md`
- `evidence-boundary.md`
- `selected-next-lane.md`
- `non-actions.md`
