# Alpha boundary preservation

## Must preserve

- Alpha Solver controls routing and model selection.
- Alpha Solver emits and stores the authoritative SolverEnvelope.
- Evidence and citations are Alpha Solver artifacts, not UI-inferred artifacts.
- SAFE-OUT, policy, determinism, budget, replay, and observability gates remain upstream of any model backend.
- UI conversation history cannot become an alternate source of truth for eval or production claims.

## Required controls before any UI trial

1. **Endpoint allowlist:** the sidecar may call only the Alpha Solver controlled endpoint.
2. **Provider lockdown:** users cannot add direct Ollama/OpenAI/OpenRouter/Anthropic/etc. endpoints for Alpha Solver workflows.
3. **Upload/RAG off by default:** document upload, embedding, knowledge bases, workspace sync, and file injection remain disabled unless a separate evidence-ingestion lane approves them.
4. **Tooling off by default:** plugins, code execution, terminal access, web search, MCP, OpenAPI tools, auto-approved tools, and pipelines remain disabled.
5. **Envelope-first display:** UI renders Alpha Solver answer, route, safety state, evidence references, and stop conditions without rewriting them as free-form chat metadata.
6. **Retention decision:** conversation storage, deletion, export, and audit retention must be explicitly specified before shared use.
7. **Auth decision:** local-only usage can defer multi-user auth; shared usage requires authn/authz and per-user audit identity.

## Boundary test questions for any future implementation

- Can a user make the UI call a model directly without Alpha Solver?
- Can a user upload a private repo file into UI RAG or memory?
- Can the UI summarize or transform evidence in a way that looks authoritative but is not in the SolverEnvelope?
- Can a plugin/tool/pipeline invoke external services with prompt or repo data?
- Can a conversation be replayed from Alpha Solver artifacts alone, without trusting sidecar state?

If any answer is unsafe or unknown, the lane remains blocked.
