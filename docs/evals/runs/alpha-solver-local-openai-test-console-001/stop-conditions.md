# Stop conditions

Stop and do not treat results as evidence beyond smoke-only output if:

- The console is not bound to loopback.
- A non-loopback Host header is accepted.
- OpenAI environment gates are missing.
- Local mode points at a non-loopback endpoint.
- Any API key, authorization header, bearer token, unsanitized provider payload, hosted account detail, or local machine identifier appears in rendered output or files.
- Any output is described as quality, readiness, benchmark, production, public, security/privacy completion, or superiority evidence.
