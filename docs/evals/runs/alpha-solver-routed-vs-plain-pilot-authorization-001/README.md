# ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-AUTHORIZATION-001

Docs-only authorization packet for a future routed-vs-plain pilot. This lane authorizes a later operator-controlled output-collection lane under the protocol in this directory, but it does not execute the pilot and does not generate, score, unblind, or inspect outputs.

## Files

- `authorization-decision.md` - authorization verdict and denied actions.
- `pilot-protocol.md` - precise future pilot protocol.
- `task-scope.md` - authorized task set and task-id preservation rules.
- `output-collection-rules.md` - future collection method and identity rules.
- `blinding-rules.md` - blinding and unblinding boundaries.
- `scoring-authorization-gate.md` - scoring gate for a later lane.
- `stop-conditions.md` - stop rules.
- `non-actions.md` - actions not performed by this lane.
- `non-claims.md` - claims not supported by this lane.
- `checks-run.md` - validation record.
- `selected-next-state.md` - post-lane selected next state.
- `selected-next-action.md` - next operator action.

## Evidence boundaries

This authorization packet is docs-only. It does not execute pilot tasks, call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha-routed outputs, generate plain baseline outputs, score outputs, unblind outputs, inspect raw prior outputs, mutate Google Sheets, add dependencies, expose `/v1/solve`, or make readiness, benchmark-success, production/public-readiness, provider-quality, local-model-quality, tool-quality, or Alpha-superiority claims.
