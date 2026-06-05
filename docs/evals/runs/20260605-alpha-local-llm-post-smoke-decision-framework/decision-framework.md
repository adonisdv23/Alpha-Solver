# Decision Framework

Lane ID: `ALPHA-LOCAL-LLM-POST-SMOKE-DECISION-FRAMEWORK-001`

Status: framework only; no actual smoke result is imported or interpreted.

## Framework boundary

This document pre-commits the decision rules for a future lane that imports preserved local LLM smoke evidence. It does not execute smoke, call a local model, call Ollama, call a hosted provider, inspect private endpoints, import a result, or interpret an absent result.

The future decision must be evidence-bound: it may use only preserved raw artifacts and the corresponding sanitized import from the future smoke-results import lane.

## Required future decision behavior

The actual future decision must:

1. confirm that smoke execution evidence exists;
2. confirm that a sanitized import exists and references preserved raw artifacts;
3. classify the imported evidence into exactly one outcome branch;
4. select exactly one next lane from the branch mapping;
5. preserve non-claims and blocked-work boundaries; and
6. document why other branches were not selected.

## Branch selection priority

If multiple symptoms are present, the future decision should choose the immediate blocker that prevents reliable interpretation of smoke behavior:

1. skipped or blocked execution;
2. environment setup failure;
3. endpoint locality failure;
4. connection failure;
5. model unavailable;
6. timeout;
7. malformed response;
8. empty output;
9. prompt or system echo;
10. passed cleanly only when no `failed_closed` status or fail-closed label is present.

This priority order is not a result. It is only a tie-breaker for future imported evidence.

## Prohibited in this lane

This framework lane does not perform smoke execution, live Ollama calls, hosted provider calls, local model calls, network calls, provider-key handling, runtime routing changes, `/v1/solve` changes, dashboard preview changes, operator-test evidence changes, Batch C work, actual smoke result import, or interpretation of missing smoke results.
