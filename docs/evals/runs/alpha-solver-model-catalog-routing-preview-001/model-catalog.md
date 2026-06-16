# Model catalog

The backend catalog is loaded from `configs/model_catalog.json` through `alpha/model_catalog.py`.

## Included local/Ollama defaults

- `qwen2.5:3b`
- `gemma3:4b`
- `llama3.2:1b`
- `llama3.2:latest`

## Included OpenAI defaults

- `gpt-4.1-mini`
- `gpt-4.1`
- `gpt-4o-mini`

## Metadata fields

Each entry records provider, mode, model id, display name, enabled default status, smoke eligibility, notes, and `quality_claim: false`.

Catalog inclusion is not a claim that a provider currently offers a model to every account or that any model is validated for Alpha Solver quality.
