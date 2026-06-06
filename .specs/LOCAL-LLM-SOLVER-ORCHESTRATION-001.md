# LOCAL-LLM-SOLVER-ORCHESTRATION-001 · Local LLM Solver Orchestration Integration Contract

## Purpose

This spec is the canonical implementation contract for wiring the optional local LLM runtime backend into Alpha Solver orchestration. The supporting lane record lives under `docs/evals/runs/20260605-alpha-local-llm-solver-orchestration-spec/`.

The next goal is not more prompt engineering. The next goal is to connect bounded local LLM runtime output to an Alpha Solver orchestration surface while preserving the local-runtime safety boundary and while keeping production `/v1/solve` and dashboard exposure blocked.

## Source-of-truth context

This contract builds on `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md` and the current local runtime adapter seam in `alpha/local_llm/provider_adapter.py`.

The existing local LLM runtime path is closed and proven only as bounded local runtime smoke evidence. The runtime track ended with terminal next action `STOP-HERE-LOCAL-LLM-RUNTIME-TRACK-CLOSED`. That closeout does not prove model quality, orchestration quality, production readiness, `/v1/solve` readiness, dashboard readiness, MVP validation, benchmark standing, hosted-provider behavior, or evidence-model promotion.

## Safety invariants

Every future implementation under this contract must preserve all of the following local LLM invariants:

1. Local LLM use is optional and default-off.
2. Explicit operator opt-in is required.
3. Only localhost or loopback HTTP endpoints are allowed.
4. No provider keys are required or accepted for local LLM mode.
5. Every local runtime call uses a finite timeout.
6. There is no hosted fallback from local LLM failure.
7. `behavior_evidence=false` is preserved unless a separate approved evidence-model lane changes it.
8. Hosted output must never be labeled as local LLM output.
9. Local runtime errors fail closed and do not become successful answers.

## Blocked surfaces

This spec does not authorize any of the following:

- production `/v1/solve` exposure;
- dashboard exposure;
- hosted provider fallback;
- evidence-model promotion;
- model-quality claims;
- MVP adoption;
- production readiness claims;
- benchmark claims;
- Alpha superiority claims;
- provider orchestration claims;
- billing-path changes.

## First implementation target

The first implementation target is a non-production local orchestration runner, not `/v1/solve`.

The local orchestration runner must be an internal or CLI-callable path that can:

- call the approved local LLM runtime backend;
- wrap local output in an Alpha-style envelope;
- preserve local runtime metadata;
- run bounded expert-style passes;
- run local confidence, clarify, or block decisions where possible;
- fail closed on runtime errors;
- preserve evidence boundaries.

This runner is the selected integration approach. It is not a production route and must not be mounted into `/v1/solve` or dashboard preview by this lane.

## Required local expert two-pass contract

Local expert two-pass is the first quality-lift feature for implementation.

### Pass 1: considerations and gate inputs

Pass 1 asks the local LLM to extract:

- considerations;
- assumptions;
- confidence;
- uncertainty or missing-information notes when available.

### Deterministic parse

The implementation must deterministically parse Pass 1 output:

1. parse JSON when valid JSON is available;
2. fall back to conservative section parsing only where the section shape is safe and bounded;
3. fail closed or mark the result as needing clarification or blocking when parsing is unsafe, empty, echoed, or ambiguous.

### Gate

The local runner must choose exactly one gate mode from:

- `direct`;
- `clarify`;
- `answer_with_assumptions`;
- `block`.

The gate must be based on bounded local confidence and missing-information checks. If confidence or parse safety cannot be established, the runner must prefer fail-closed, `clarify`, or `block` over presenting unsupported output as successful behavior.

### Pass 2: answer with context

Pass 2 asks the local LLM to answer using the parsed considerations and assumptions from Pass 1. Pass 2 must preserve the same default-off, localhost-only, no-provider-key, finite-timeout, no-hosted-fallback runtime boundary.

### Normalized output

The local orchestration runner output must be normalized into an Alpha-style result containing at least:

- `answer`;
- `considerations`;
- `assumptions`;
- `confidence`;
- `mode`;
- `metadata`;
- `evidence_boundary`.

The result must preserve local runtime metadata, including provider mode, backend identifier, local model identifier, localhost or loopback confirmation, timeout, deterministic status or reason labels, no-provider-key status, no-hosted-fallback status, and `behavior_evidence=false`.

## Later local ToT-lite contract

Local ToT-lite is a later feature, not the first implementation target.

A later local ToT-lite lane may consider:

- a small branch count;
- a low token budget;
- no production exposure;
- no dashboard exposure;
- no model-quality claim;
- no benchmark or superiority claim.

Local ToT-lite remains blocked until a separate approved implementation lane selects it.

## Later deterministic strategy surfaces

`alpha/reasoning/react_lite.py`, `alpha/reasoning/cot.py`, and `alpha/reasoning/cot_self_validate.py` are existing deterministic strategy surfaces that can be considered in later integration. They are not required for the first implementation target and must not broaden this lane into unrelated reasoning refactors.

## Built-code versus approved integration surfaces

Existing code surfaces can contain local runtime seams, deterministic reasoning utilities, provider routes, preview routes, reference entrypoints, or legacy files. The presence of built code is not authorization to expose local LLM output through every available surface.

Approved runtime integration for the first implementation is limited to the non-production local orchestration runner described here and the minimum supporting call path needed to invoke the already-approved local LLM runtime backend. Production `/v1/solve`, dashboard preview, hosted provider fallback, broad routing, MCP, SAFE-OUT, budget guard, determinism, replay, and SolverEnvelope behavior remain unchanged unless a later spec explicitly authorizes changes.

`alpha_solver_v225_p2_experts.py` is not active unless separately approved as non-stub. It must not be treated as an approved non-stub orchestration target merely because it exists or is referenced.

## Implementation boundary

A future implementation lane may change only the narrow files needed to add the non-production runner and focused tests for this contract. It must not change production `/v1/solve`, dashboard routes, hosted provider behavior, provider credential behavior, evidence model semantics, or runtime smoke artifacts unless a separate lane authorizes those changes.

## Required future tests and checks

A future implementation must include focused tests or checks proving:

1. the runner is not exposed through `/v1/solve`;
2. the runner is not exposed through dashboard preview;
3. local LLM mode remains default-off;
4. explicit opt-in is required;
5. localhost and loopback endpoints are accepted;
6. non-local endpoints fail closed;
7. provider keys are not required and hosted fallback does not occur;
8. finite timeout is enforced;
9. runtime errors fail closed;
10. Pass 1 JSON parsing succeeds when valid JSON is returned;
11. safe section parsing works only for bounded section shapes;
12. unsafe, empty, echo, or malformed outputs do not become successful answers;
13. gate mode is one of `direct`, `clarify`, `answer_with_assumptions`, or `block`;
14. Pass 2 receives bounded considerations and assumptions;
15. the normalized result includes answer, considerations, assumptions, confidence, mode, metadata, and evidence boundary;
16. local runtime metadata and `behavior_evidence=false` are preserved.

## Selected next lane

Exactly one next lane is selected:

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-IMPLEMENTATION-001`

## Evidence boundary

This spec is a docs-only canonical specification and implementation contract.

It is not implementation, runtime smoke execution, local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, runtime-readiness evidence, billing evidence, output reconstruction, or local LLM quality validation.
