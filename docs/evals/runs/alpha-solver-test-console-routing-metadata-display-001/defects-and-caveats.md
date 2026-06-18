# Defects and caveats

- The display depends on static catalog/router metadata and does not validate model or tool quality.
- Tool alternatives are rendered from existing tool-router candidates; richer fallback semantics require a future tool-router lane.
- Full manual UI review remains a selected next action, not completed by this implementation.

## Evidence boundary

This lane is a local-console product-foundation display lane only. It records route-preview UI behavior and tests for metadata rendering. It does not run Alpha runtime behavior, invoke `/v1/solve`, call providers, run hosted models, run local models or Ollama, execute tools, browse, use runtime GitHub calls, mutate Sheets, score, unblind, inspect A/B keys or source maps, deploy, or make readiness, value, benchmark, production/public, provider-quality, local-model-quality, tool-quality, security/privacy-completion, autonomous-readiness, or Alpha-superiority claims. Catalog inclusion is not model or tool quality evidence.

