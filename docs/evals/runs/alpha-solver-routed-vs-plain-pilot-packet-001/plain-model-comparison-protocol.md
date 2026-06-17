# Plain-model comparison protocol

1. Preserve task ids exactly.
2. Collect the plain single-model response first or according to the operator blind plan.
3. Collect the Alpha-routed response separately, requiring route metadata fields: classification, model recommendation, tool recommendation, route reasons, warnings, fallback, evidence boundary, confidence or answerability notes, and next action.
4. Do not reveal which output is Alpha-routed to scorers until the authorized unblinding step.
5. Do not score during collection.
6. Do not compare unsupported claims; compare only captured outputs and metadata.
7. Stop on sensitive data, secrets, provider errors that would require retry-policy changes, or any need to mutate systems.

## Protocol boundaries

This packet does not execute the pilot. It does not call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha outputs, generate baseline outputs, score outputs, change scores, unblind, inspect raw Alpha outputs, inspect raw baseline outputs, perform source-map work, mutate Google Sheets, add dependencies, expose `/v1/solve`, or expose dashboard or public API behavior. It makes no readiness, benchmark, production, public, security/privacy, provider, local-model, tool-quality, or Alpha-superiority claims.
