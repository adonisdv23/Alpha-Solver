# Candidate UI comparison

## Evidence consulted

- Open WebUI feature docs state support for Ollama, OpenAI-compatible providers, model switching, file upload, RAG/knowledge bases, tools, pipelines, MCP, RBAC, SSO/OIDC/LDAP, API keys, Docker/Kubernetes/pip deployment, and observability-style deployment options.
- LibreChat docs describe custom OpenAI-compatible endpoints, Ollama via Ollama OpenAI compatibility, Docker-mounted configuration, `.env` API-key storage, and many AI endpoint integrations.
- AnythingLLM docs describe local and cloud LLM provider setup including Ollama and generic OpenAI, chat logs, document attachment, embedding/RAG, workspace-scoped document sharing, native tool-calling settings, and automatic tool approval controls.
- Ollama documents OpenAI Chat Completions compatibility, making UI tools that can target OpenAI-compatible endpoints technically relevant to local model backends.

## Comparison matrix

| Criterion | Open WebUI | LibreChat | AnythingLLM | Custom minimal console |
|---|---|---|---|---|
| Local Ollama support | Strong native fit; commonly Ollama-first and supports Ollama from UI. | Supported through custom endpoint using Ollama OpenAI compatibility. | Supported as local LLM and embedding provider. | Only if Alpha Solver endpoint exposes a safe abstraction; console should not call Ollama directly. |
| OpenAI-compatible endpoint support | Strong; can connect to OpenAI-compatible providers. | Strong; custom endpoints support OpenAI-compatible services. | Present through OpenAI generic provider. | Alpha Solver can define exactly one controlled endpoint contract. |
| Multi-model switching | Strong UI-level switching and side-by-side model use. | Strong multi-endpoint/multi-model potential. | Has provider/model/router concepts, but RAG/workspace focus may dominate. | Deliberately limited; model choice should remain Alpha Solver policy/router output. |
| Conversation history | Strong built-in history and organization. | Strong ChatGPT-like conversation history. | Strong chat logs/workspaces. | Minimal durable logs only if explicitly designed for SolverEnvelope/audit needs. |
| RAG/document upload risk | High by default because upload, knowledge, web search, code execution, and agentic retrieval are feature-rich. | Medium/high where file upload, RAG API, tools, and plugins are enabled. | High because document chat, embedding, workspace sharing, and RAG are core features. | Low if uploads are absent and transcript retention is explicit. |
| Auth and user management | Strong RBAC/SSO/OIDC/LDAP/user groups, but adds admin surface. | Configurable auth/social login/user controls; requires app stack. | Supports security/access settings and multi-user/workspace behavior. | Initially local-only; auth must be added before any shared use. |
| Plugins/tools/pipelines | Very high; tools, functions, pipelines, MCP, OpenAPI servers. | High; tools/MCP/toolkit ecosystem. | High; agents, skills, native tool calling, automatic approvals. | None until Alpha Solver explicitly exposes safe operations. |
| Deployment complexity | Medium/high: full web app, storage, users, optional vector stores. | High: Docker stack/config/env/database concerns. | Medium/high: self-hosted app with documents/vector storage/workspaces. | Low: repo-owned docs/CLI or local web shell, no external app stack. |
| Preserve SolverEnvelope/evidence boundaries | Possible only if configured as UI-to-Alpha endpoint with RAG/tools disabled. | Possible only if every endpoint points at Alpha Solver and direct providers are removed. | Difficult because workspace/RAG semantics can blur evidence provenance. | Strongest because UI can be shaped around envelopes and citations. |
| Risk of bypassing Alpha Solver routing | High if direct Ollama/OpenAI connections remain available. | High if users can add alternate endpoints or direct providers. | High if users select direct providers, agents, or workspace RAG. | Low if no direct backend configuration exists. |
| Early MVP suitability | Best off-the-shelf candidate after security gates, but too capable to enable casually. | Viable later for ChatGPT-like operator UX, but heavier configuration and provider sprawl. | Not preferred for early MVP because document/RAG-first UX conflicts with evidence-boundary discipline. | Best early MVP pattern for boundary preservation and scope control. |

## Candidate notes

### Open WebUI

Open WebUI is the most attractive existing UI candidate because it combines local Ollama, OpenAI-compatible providers, conversation management, auth, and extensibility. That strength is also the primary risk: RAG, file upload, web search, code execution, tools, pipelines, MCP, OpenAPI tools, and model switching can all create paths that bypass Alpha Solver evidence and routing if not locked down.

### LibreChat

LibreChat is a plausible chat-operator UI when the desired experience is closer to ChatGPT with configurable providers. Its custom endpoint support is useful for pointing at Alpha Solver, but its provider configuration and plugin/tool ecosystem need strong administrative lockdown before use.

### AnythingLLM

AnythingLLM is strongest when the product goal is document-centric RAG and workspace knowledge. That is not the Alpha Solver sidecar objective for this lane. Its upload/embed/workspace behavior creates avoidable ambiguity about evidence provenance and access boundaries.

### Custom minimal console

A minimal console has fewer conveniences, but it best preserves Alpha Solver envelopes, SAFE-OUT behavior, routing decisions, evidence boundaries, and audit trail requirements. It is the safest early MVP lane because it can be limited to prompt submission, envelope display, route trace display, evidence/citation display, and stop-state surfacing.
