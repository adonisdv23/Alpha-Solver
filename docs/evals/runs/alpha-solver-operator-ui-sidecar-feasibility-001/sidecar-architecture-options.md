# Sidecar architecture options

## Preferred architecture

```text
UI sidecar
  -> Alpha Solver controlled endpoint
    -> Alpha Solver router / policy / evidence layer
      -> local or hosted model backend
```

This keeps model selection, policy enforcement, evidence handling, budget/determinism controls, and SolverEnvelope rendering in Alpha Solver rather than the UI.

## Disallowed architecture

```text
UI sidecar
  -> Ollama / OpenAI / hosted model directly
```

This bypasses Alpha Solver routing and can produce responses with no Alpha Solver envelope, route trace, safety boundary, or evidence provenance.

## Options reviewed

### Option A: Minimal local console first

- Implement later as a local-only operator shell against an already-approved Alpha Solver endpoint or CLI bridge.
- No document upload, RAG, external tools, model-provider settings, or direct backend credentials.
- Displays Alpha Solver response fields as first-class UI components.
- Recommended as the next implementation shape after security review.

### Option B: Open WebUI endpoint-only sidecar later

- Configure one provider: Alpha Solver controlled endpoint only.
- Disable or hide direct model endpoints, uploads, knowledge bases, web search, tools, code execution, pipelines, MCP, OpenAPI tool import, memory, and autonomous agents until individually approved.
- Treat Open WebUI as a shell, not as a policy or evidence engine.
- Candidate for later MVP if security gates prove configuration lockdown is reliable.

### Option C: LibreChat endpoint-only sidecar later

- Configure custom endpoint to Alpha Solver only.
- Lock down provider addition, credentials, plugins/tools, file upload/RAG, and user-level endpoint overrides.
- Consider only if Open WebUI is too broad or if LibreChat's ChatGPT-like UX is preferred.

### Option D: AnythingLLM document workspace sidecar

- Not recommended for early MVP.
- Document and workspace abstractions are useful for RAG products, but they add provenance, sharing, and embedding risks that conflict with this lane's boundary-preservation goal.
