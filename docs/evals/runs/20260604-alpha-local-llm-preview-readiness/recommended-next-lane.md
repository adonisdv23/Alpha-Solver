# Recommended Next Lane

Lane ID: `ALPHA-LOCAL-LLM-PREVIEW-READINESS-001`

Status: recommendation only; evidence-bounded and not an implementation approval.

## Recommendation

Recommend exactly one next lane: **run a focused contract-consumption proof lane**.

Suggested lane name: `ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-001`.

## Why this lane

The main readiness gap is not merely absence of an Ollama adapter. The main gap is that current preview and runtime paths do not prove that `alpha_solver_portable.py` is consumed. A focused proof lane can establish the source-to-request binding and smoke isolation before the repo decides whether to build a full local LLM provider adapter, dashboard preview, `/v1/solve` integration, or dev-only tool.

This recommendation does not assume local LLM should be built. It says the next decision should be based on whether a minimal, fake-client-tested path can load the portable contract, inject it into a local LLM-style request, preserve safe metadata, and avoid v91/local-smoke fallback.

## Scope of the recommended proof lane

A focused proof lane should be limited to:

- contract loader or wrapper design;
- fake-client request construction;
- prompt source hash metadata;
- tests proving local LLM mode does not call `_tree_of_thought`;
- tests proving `MODEL_PROVIDER=local` remains smoke-only;
- no real Ollama execution;
- no cloud provider calls;
- no operator-test execution;
- no scoring or result import.

## Decision after proof lane

After that proof, the project can choose one of these later paths with better evidence:

- implement `ALPHA-LOCAL-LLM-PROVIDER-ADAPTER-001`;
- expose the path through `/dashboard/expert-preview`;
- expose the path through `/v1/solve` as part of a separate surface-fix lane;
- keep local LLM deferred if the proof exposes unacceptable drift or evidence risks.

## Non-claims

This recommendation does not claim Alpha validation, superiority, runtime readiness, production readiness, Batch C readiness, provider orchestration, exact billing, or OpenAI/Claude behavior.
