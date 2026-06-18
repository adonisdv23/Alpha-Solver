# Tool preview display contract

When the existing tool router returns a metadata-only recommendation, the route panel displays recommended tool route, tool category, execution authorization status, grouped tool reasons/caveats, and candidate alternatives as available. Tool recommendation remains preview-only and does not execute tools, browse, call GitHub runtime APIs, mutate files, or authorize later execution.

## Evidence boundary

This lane is a local-console product-foundation display lane only. It records route-preview UI behavior and tests for metadata rendering. It does not run Alpha runtime behavior, invoke `/v1/solve`, call providers, run hosted models, run local models or Ollama, execute tools, browse, use runtime GitHub calls, mutate Sheets, score, unblind, inspect A/B keys or source maps, deploy, or make readiness, value, benchmark, production/public, provider-quality, local-model-quality, tool-quality, security/privacy-completion, autonomous-readiness, or Alpha-superiority claims. Catalog inclusion is not model or tool quality evidence.

