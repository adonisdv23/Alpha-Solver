# Pilot protocol

## Task set to use

Use the 12 task cards from `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-packet-001/task-set.md`, preserving task ids `RVP-001` through `RVP-012` exactly.

## Output collection method

A future authorized lane may collect one plain baseline output and one routed Alpha output per task. This authorization packet itself collects no outputs. If no separate provider/local/tool/web execution authorization is granted later, the collector must use operator-provided outputs only.

## Execution permissions for later lanes

- Provider calls later: not authorized by this packet; require explicit later operator authorization.
- Hosted model calls later: not authorized by this packet; require explicit later operator authorization.
- Local model calls later: not authorized by this packet; require explicit later operator authorization.
- Tool execution later: not authorized by this packet; require explicit later operator authorization.
- Web/current research later: not authorized by this packet; require explicit later operator authorization.

## Route metadata capture

For each routed Alpha item, capture task id, task family, selected route family, model recommendation, tool recommendation, route reasons, fallback, warnings, evidence boundary, confidence or answerability note, next action, timestamp, collector identity, and artifact path. Do not place route metadata in scorer-facing blinded answer files unless a scoring protocol explicitly includes route-metadata scoring.

## Task ID preservation

Every filename, row, note, and capture record must preserve the exact task id. Do not renumber, merge, split, or rewrite task ids.

## Evidence boundaries

This authorization packet is docs-only. It does not execute pilot tasks, call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha-routed outputs, generate plain baseline outputs, score outputs, unblind outputs, inspect raw prior outputs, mutate Google Sheets, add dependencies, expose `/v1/solve`, or make readiness, benchmark-success, production/public-readiness, provider-quality, local-model-quality, tool-quality, or Alpha-superiority claims.