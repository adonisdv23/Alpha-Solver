# Adapter Preservation Checklist

- [x] Loads `alpha_solver_portable.py` through the portable contract loader.
- [x] Preserves `prompt_source_path` as `alpha_solver_portable.py`.
- [x] Preserves the SHA-256 prompt-source fingerprint.
- [x] Uses the loaded portable contract as system/contract content.
- [x] Keeps the user prompt separate from the system/contract content.
- [x] Uses the distinct `local_llm` adapter mode label.
- [x] Rejects `provider_mode="local"` so `MODEL_PROVIDER=local` remains
  smoke-only.
- [x] Avoids v91 `_tree_of_thought` fallback.
- [x] Uses an injected stub backend in tests.
- [x] Performs no default Ollama, local model, OpenAI, Anthropic, or hosted
  provider calls.
- [x] Fails closed on empty output.
- [x] Fails closed on prompt echo.
- [x] Fails closed on injected-backend error.
- [x] Labels successful stub output as non-evidence wiring only.
