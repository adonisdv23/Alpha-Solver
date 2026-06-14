# Recommendation

## Verdict

**UI_SIDECAR_FEASIBILITY_CAPTURED**

## Recommended sidecar pattern

Start with a **minimal local Alpha Solver operator console**. Use it to prove the envelope-first UX before introducing a full external UI.

A later Open WebUI experiment can be considered only as an **endpoint-only sidecar** after security/exposure gates decide how to lock down direct providers, upload/RAG, tools, memory, web search, code execution, auth, and retention.

## Ranking for early MVP

1. **Custom minimal console** — best boundary preservation and lowest bypass risk.
2. **Open WebUI endpoint-only sidecar** — best off-the-shelf candidate after lockdown decisions.
3. **LibreChat endpoint-only sidecar** — plausible fallback if ChatGPT-like UX is favored and provider sprawl is controlled.
4. **AnythingLLM** — defer; document/RAG/workspace orientation is not aligned with this safety-first lane.

## Do-not-integrate-yet warnings

- Do not connect any UI directly to Ollama, OpenAI, or other model backends for Alpha Solver workflows.
- Do not enable document upload, RAG, memory, knowledge bases, workspace sync, web search, tools, code execution, MCP, OpenAPI tools, pipelines, or auto-approved agents.
- Do not expose Alpha Solver endpoints to a browser or network until auth, CORS, CSRF, rate limiting, audit identity, and retention are specified.
- Do not treat UI chat history as authoritative evidence.
- Do not claim public, product, or production readiness.
