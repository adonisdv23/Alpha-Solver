# Selected Next Lane

Lane ID: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-SPEC-001`

## Selection

Exactly one next lane is selected:

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-IMPLEMENTATION-001`

## Selected integration approach

The selected integration approach is a non-production local orchestration runner that can call the optional local LLM runtime backend, run bounded local expert-style passes, normalize the result into an Alpha-style envelope, preserve local runtime metadata, and preserve evidence boundaries.

## Non-selections

No other next lane is selected by this package. Production `/v1/solve`, dashboard exposure, provider fallback, evidence-model promotion, local ToT-lite implementation, and model-quality validation remain non-selections.
