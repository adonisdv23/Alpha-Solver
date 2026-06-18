# Operator UI contract

The console keeps prompt/task entry, local/OpenAI smoke-mode selection, model selection/override, preview-only route display, and smoke execution as separate controls. Preview submission targets `/preview`; bounded smoke execution remains on `/run` through the existing smoke-runner path. The panel states that preview is metadata-only and does not authorize execution.

## Evidence boundary

This lane is a local-console product-foundation display lane only. It records route-preview UI behavior and tests for metadata rendering. It does not run Alpha runtime behavior, invoke `/v1/solve`, call providers, run hosted models, run local models or Ollama, execute tools, browse, use runtime GitHub calls, mutate Sheets, score, unblind, inspect A/B keys or source maps, deploy, or make readiness, value, benchmark, production/public, provider-quality, local-model-quality, tool-quality, security/privacy-completion, autonomous-readiness, or Alpha-superiority claims. Catalog inclusion is not model or tool quality evidence.

