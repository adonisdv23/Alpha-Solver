# Scoring authorization gate

Scoring is not authorized by this packet.

A later scoring lane must be explicitly authorized after output collection and must state:

- scorer identity or role,
- scorer-facing artifacts,
- whether route metadata is scored,
- rubric version,
- handling of contested scores,
- score-lock procedure,
- unblinding boundary,
- source-of-truth update boundaries, and
- non-claims.

Until that later gate exists, all scoring fields remain blank.

## Evidence boundaries

This authorization packet is docs-only. It does not execute pilot tasks, call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha-routed outputs, generate plain baseline outputs, score outputs, unblind outputs, inspect raw prior outputs, mutate Google Sheets, add dependencies, expose `/v1/solve`, or make readiness, benchmark-success, production/public-readiness, provider-quality, local-model-quality, tool-quality, or Alpha-superiority claims.
