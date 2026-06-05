# Implementation File Boundary

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Boundary purpose

This document records the docs/evals supporting view of the minimal file-change boundary for the future implementation lane. The canonical implementation contract is `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`. This document does not authorize changes in this docs-only lane.

## Minimal future implementation boundary

Future implementation lanes must reference `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md` as the canonical contract and should prefer the smallest file set needed to wire explicit local LLM mode while preserving default-off behavior. Expected candidate files are:

- `alpha/local_llm/provider_adapter.py` for endpoint, timeout, transport, parser, fail-closed, and provenance refinements;
- the narrow runtime configuration module or entrypoint code that selects provider mode, if needed after inspection;
- the narrow runtime call site that invokes LLM-backed behavior, if needed after inspection;
- focused tests covering the local LLM mode contract.

## Files and surfaces that must remain blocked unless separately authorized

The future implementation lane must not expose local LLM mode through the following surfaces unless that lane explicitly keeps them blocked or a later lane authorizes exposure:

- `/v1/solve` behavior;
- dashboard preview behavior;
- provider orchestration code;
- billing or hosted-provider credential paths;
- broad MCP, routing, SAFE-OUT, budget guard, determinism, observability, replay, or SolverEnvelope behavior.

## Implementation style constraints

A future implementation should:

- avoid broad refactors;
- preserve existing portable contract semantics;
- preserve `behavior_evidence=false`;
- keep hosted provider behavior separate from local LLM behavior;
- add only focused tests tied to this contract.
