# Risks and non-goals

## Main risks

- **API-shape mismatch:** Open WebUI, LibreChat, or a custom endpoint shell may send an OpenAI-compatible request shape to `/v1/solve`, which currently requires Alpha Solver's `query` request shape, and fail before router, policy, SAFE-OUT, evidence, auth, tenancy, CORS, cost, and observability boundaries are reached.
- **Routing bypass:** UI connects directly to local or hosted models.
- **Evidence confusion:** UI RAG, memory, or notes become untracked evidence sources.
- **Credential exposure:** UI stores provider keys or permits users to add providers.
- **Tool overreach:** plugins, code execution, web search, MCP, OpenAPI tools, or auto-approved agents send data outside Alpha Solver controls.
- **Data retention drift:** conversation history persists sensitive prompts outside approved artifact storage.
- **False readiness:** a polished UI can imply product readiness despite unapproved security and exposure gates.
- **Admin surface expansion:** full web UIs add auth, user, database, file-storage, and deployment obligations.

## Non-goals

- No runtime implementation.
- No UI deployment.
- No endpoint exposure.
- No credentials or provider keys.
- No production mounting of an external UI.
- No RAG ingestion of private repo data.
- No endpoint, UI, runtime, provider, production, or public readiness claim.
- No replacement of Alpha Solver routing, policy, evidence, SAFE-OUT, determinism, replay, observability, or SolverEnvelope semantics.
