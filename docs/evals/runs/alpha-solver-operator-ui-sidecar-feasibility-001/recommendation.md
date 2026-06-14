# Recommendation

## Verdict

**UI_SIDECAR_FEASIBILITY_CAPTURED**

## Recommended sidecar pattern

The next lane is **not direct sidecar deployment**. Start with a security/API-shape decision gate before any endpoint-only sidecar trial.

The selected next lane is `ALPHA-SOLVER-OPERATOR-UI-SIDECAR-API-SHAPE-SECURITY-GATE-001`. It should decide whether to use a minimal Alpha-native local console, an OpenAI-compatible shim, a sidecar native request mapper, or no sidecar integration yet.

## Ranking for early MVP

1. **Security/API-shape decision gate** — decide whether a minimal Alpha-native local console, OpenAI-compatible shim, sidecar native request mapper, or no integration is appropriate.
2. **Custom minimal console** — best boundary preservation and lowest bypass risk if the gate selects Alpha-native UX.
3. **Open WebUI endpoint-only sidecar** — blocked until lockdown decisions and API-shape compatibility are proven.
4. **LibreChat endpoint-only sidecar** — blocked until lockdown decisions and API-shape compatibility are proven.
5. **AnythingLLM** — defer; document/RAG/workspace orientation is not aligned with this safety-first lane.

## Do-not-integrate-yet warnings

- Do not connect any UI directly to Ollama, OpenAI, or other model backends for Alpha Solver workflows.
- Do not point Open WebUI, LibreChat, or a custom endpoint shell directly at `/v1/solve` unless the API-shape compatibility gate confirms an OpenAI-compatible shim/adapter, confirmed native request mapping, or approved bridge lane.
- Do not enable document upload, RAG, memory, knowledge bases, workspace sync, web search, tools, code execution, MCP, OpenAPI tools, pipelines, or auto-approved agents.
- Do not expose Alpha Solver endpoints to a browser or network until auth, CORS, CSRF, rate limiting, audit identity, and retention are specified.
- Do not treat UI chat history as authoritative evidence.
- Do not claim public, product, or production readiness.
