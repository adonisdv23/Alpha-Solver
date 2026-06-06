# Orchestration Objective

## Objective

Define the canonical implementation contract for moving local LLM output from a prompt-contract local runtime runner into Alpha Solver orchestration.

## Shift in goal

The local runtime track established only a bounded local runtime smoke boundary. The next goal is not additional prompt engineering and not further standalone local runtime proof. The next goal is a non-production orchestration runner that can call the local LLM runtime backend, apply bounded Alpha-style orchestration steps, and return a normalized Alpha-style result without exposing the path to production `/v1/solve` or dashboard preview.

## Selected integration approach

The selected integration approach is a non-production local orchestration runner. The runner may be internal or CLI-callable. It is not a production route, not dashboard functionality, and not an MVP adoption path.
