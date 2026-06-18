# Route preview display contract

When metadata is available, the route panel displays recommended mode, recommended model, model route status, selected backend type, selected cost tier, selected latency tier, selected context tier, selected privacy tier, smoke eligibility, no-call evidence flag, confidence label, catalog-not-quality-evidence caveat, grouped reasons/warnings, and fallback candidates with mode, model, backend type, and fallback eligibility. Failed-closed previews render the failure status and safe reason instead of silently selecting an ineligible route.

## Evidence boundary

This lane is a local-console product-foundation display lane only. It records route-preview UI behavior and tests for metadata rendering. It does not run Alpha runtime behavior, invoke `/v1/solve`, call providers, run hosted models, run local models or Ollama, execute tools, browse, use runtime GitHub calls, mutate Sheets, score, unblind, inspect A/B keys or source maps, deploy, or make readiness, value, benchmark, production/public, provider-quality, local-model-quality, tool-quality, security/privacy-completion, autonomous-readiness, or Alpha-superiority claims. Catalog inclusion is not model or tool quality evidence.

