# Expected UI behavior

The console shows:

- Mode selection for `local` and `openai`.
- Model input with local default `qwen2.5:3b` and OpenAI default `gpt-4.1-mini`.
- Prompt textarea with the default prompt: `Reply with one concise sentence that does not echo this prompt.`
- Sanitized JSON result.
- Status, provider, model, latency, usage when available, and estimated cost only when present in runner output.
- Evidence flags with `smoke_evidence_only: true`, `behavior_evidence: false`, `quality_evidence: false`, and `readiness_evidence: false`.
- A visible notice that passing smoke does not prove quality, readiness, benchmark success, provider superiority, local-model superiority, production readiness, public readiness, security/privacy completion, or Alpha superiority.

The console does not expose `/v1/solve`.
