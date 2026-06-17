# Output collection rules

1. Preserve task ids exactly.
2. Capture plain baseline and routed Alpha outputs in separate artifacts.
3. Use neutral labels before scoring; do not expose which side is routed to scorers.
4. Capture route metadata in a separate metadata file keyed by task id and blind label.
5. If provider/local/model/tool/web execution is not separately authorized in the future lane, use operator-provided outputs only.
6. Do not summarize raw outputs into source-of-truth docs beyond approved, non-sensitive status summaries.
7. Stop before collection if prompts contain secrets, credentials, private data without operator-approved handling, or requests for direct financial/legal/medical decisions.

## Evidence boundaries

This authorization packet is docs-only. It does not execute pilot tasks, call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha-routed outputs, generate plain baseline outputs, score outputs, unblind outputs, inspect raw prior outputs, mutate Google Sheets, add dependencies, expose `/v1/solve`, or make readiness, benchmark-success, production/public-readiness, provider-quality, local-model-quality, tool-quality, or Alpha-superiority claims.
