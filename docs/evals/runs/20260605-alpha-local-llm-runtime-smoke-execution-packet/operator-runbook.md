# Operator Runbook

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

This runbook is for a future execution lane only. Do not execute it in this packet-preparation PR.

## Step 0 — Confirm authorization

Stop unless `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-REVIEW-GATE-001` explicitly authorizes smoke.

## Step 1 — Confirm local-only configuration

Record actual operator-confirmed values at execution time. Historical examples are provided only for context and must not be copied blindly.

Required local setup fields:

```dotenv
MODEL_PROVIDER=local_llm
ALPHA_LOCAL_LLM_ENABLED=true
ALPHA_LOCAL_LLM_ENDPOINT=<localhost-or-loopback-http-endpoint>
ALPHA_LOCAL_LLM_MODEL=<exact-local-model-name>
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=<finite-positive-number>
```

Historical examples only:

```dotenv
ALPHA_LOCAL_LLM_ENDPOINT=http://127.0.0.1:11434/api/chat
ALPHA_LOCAL_LLM_MODEL=gemma3:4b
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=120
```

## Step 2 — Enforce local endpoint constraints

The endpoint must satisfy all constraints:

- scheme is `http`;
- host is `localhost`, `127.0.0.1`, `::1`, or another deterministic loopback address accepted by the merged implementation;
- no userinfo is present;
- port parses as valid if provided;
- endpoint does not redirect;
- endpoint is not hosted, LAN, private-network, ambiguous, malformed, or unsupported-scheme.

## Step 3 — Confirm credentials are absent

Local mode requires no hosted provider keys. Confirm the following are absent or empty before execution:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`
- `GEMINI_API_KEY`
- `DEEPSEEK_API_KEY`

If any key is present or unexpectedly required, stop and classify as `provider key unexpectedly required`.

## Step 4 — Confirm local service and exact model

Confirm the local service is intentionally started by the operator, reachable only on localhost or loopback, and has the exact model name available. Do not substitute a different model name after artifact capture starts; if the model is unavailable, stop and classify as `model unavailable`.

## Step 5 — Capture raw command and config summary before execution

Before executing the future command, capture:

- full command;
- working directory;
- start timestamp;
- redacted config summary;
- exact endpoint host label (`localhost` or `loopback` only);
- exact local model name;
- finite timeout;
- provider key absence confirmation;
- no hosted fallback confirmation.

## Step 6 — Execute exactly one bounded smoke command

Use `local-runtime-smoke-command.md`. Execute one bounded smoke only after authorization. Preserve stdout, stderr, exit code, and the raw result object or failure object.

## Step 7 — Classify and preserve

Classify success or failure without making readiness, validation, superiority, benchmark, production, MVP, billing, provider-orchestration, hosted-provider, local-model-quality, `/v1/solve`, or dashboard-preview claims.

## Step 8 — Import later, not here

Results must be imported in a future docs-only import lane. Do not import smoke results in the execution-packet preparation lane.
