# Runtime Configuration Summary

Local LLM runtime mode is default-off.

Required explicit opt-in configuration:

- `MODEL_PROVIDER=local_llm`
- `ALPHA_LOCAL_LLM_ENABLED=true`
- `ALPHA_LOCAL_LLM_ENDPOINT=http://127.0.0.1:11434/api/chat` or another accepted localhost / loopback `http` endpoint
- `ALPHA_LOCAL_LLM_MODEL=<exact-local-model-name>`
- `ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=<finite-positive-number>`

Forbidden for local LLM runtime mode:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`
- `GEMINI_API_KEY`
- `DEEPSEEK_API_KEY`

`MODEL_PROVIDER=local` remains the existing offline/local solver default and is not treated as local LLM runtime opt-in.
