# Objective

Create a static pilot packet for a future routed-vs-plain comparison. The pilot is designed to assess route value, not answer value alone. A later operator may compare a plain single-model response against an Alpha-routed response that includes task classification, model recommendation, tool recommendation, route reasons, warnings, fallback, evidence boundary, confidence or answerability notes where appropriate, and next action.

This is a pilot scoring protocol and packet, not proof of superiority.

## Protocol boundaries

This packet does not execute the pilot. It does not call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha outputs, generate baseline outputs, score outputs, change scores, unblind, inspect raw Alpha outputs, inspect raw baseline outputs, perform source-map work, mutate Google Sheets, add dependencies, expose `/v1/solve`, or expose dashboard or public API behavior. It makes no readiness, benchmark, production, public, security/privacy, provider, local-model, tool-quality, or Alpha-superiority claims.
