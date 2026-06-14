# Evidence boundary

## Evidence used

This packet used public documentation for Open WebUI, LibreChat, AnythingLLM, and Ollama to compare sidecar feasibility. It also used the repository's existing agent instructions and docs-only lane constraints.

Public documentation references:

- Open WebUI features: https://docs.openwebui.com/features/
- LibreChat Ollama endpoint configuration: https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints/ollama
- LibreChat custom endpoints: https://www.librechat.ai/docs/quick_start/custom_endpoints
- AnythingLLM document chat/RAG behavior: https://docs.anythingllm.com/chatting-with-documents/introduction
- AnythingLLM configuration index: https://docs.anythingllm.com/configuration
- Ollama OpenAI compatibility: https://ollama.com/blog/openai-compatibility

## Evidence not used

- No private Alpha Solver repo content was uploaded to any external UI, RAG system, or provider.
- No live UI instance was installed or tested.
- No credentials, API keys, or external provider accounts were used.
- No endpoint was exposed.
- No production or public readiness assessment was performed.

## Interpretation caveat

The candidate comparison is a feasibility snapshot, not a security certification. All third-party UI capabilities and defaults must be re-verified against pinned versions before implementation.
