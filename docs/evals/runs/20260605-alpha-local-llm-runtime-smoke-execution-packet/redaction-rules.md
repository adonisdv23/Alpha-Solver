# Redaction Rules

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

Apply these rules before any sanitized artifact is imported in a future docs-only import lane.

## Must redact

- Provider keys, tokens, secrets, cookies, authorization headers, and credential-like values.
- Values of `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`, and `DEEPSEEK_API_KEY` if accidentally present.
- Full environment dumps.
- Private filesystem paths unless needed for artifact provenance and approved for disclosure.
- Nonpublic URLs and non-loopback endpoint details.
- User names, home directories, shell history, terminal metadata, machine names, and unrelated local service details.
- Prompt or output content that contains private, sensitive, or unrelated data.

## Must preserve

- `MODEL_PROVIDER=local_llm`.
- `ALPHA_LOCAL_LLM_ENABLED=true`.
- Endpoint locality summary: localhost or loopback only.
- Exact local model name, unless the operator marks the model name sensitive; if redacted, preserve a stable redacted label and raw artifact reference.
- Finite timeout value.
- Confirmation that hosted provider keys were absent and not required.
- Confirmation that hosted fallback was not used.
- Raw stdout, stderr, command, exit code, config summary, and sanitized result references.
- `behavior_evidence=false`.
- `status` and `reason` values.

## Endpoint redaction

The public sanitized artifact may show `http://127.0.0.1:11434/api/chat` or `http://localhost:<port>/<path>` only when the endpoint is loopback/local and the operator approves that disclosure. Otherwise summarize as `loopback http endpoint` and preserve the exact value only in raw artifacts.

## No provider keys for local mode

Do not add provider keys to make local mode pass. If a provider key is required or used, stop and classify as `provider key unexpectedly required` or `hosted fallback detected` as applicable.
