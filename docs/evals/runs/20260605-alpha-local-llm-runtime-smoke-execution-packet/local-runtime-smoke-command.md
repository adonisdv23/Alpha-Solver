# Local Runtime Smoke Command

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

Do not run these commands in this packet-preparation PR. They are future-use templates only and remain blocked until `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-REVIEW-GATE-001` explicitly authorizes smoke.

## Environment precheck template

This precheck validates configuration shape and must be captured with stdout, stderr, and exit code in the future execution lane. It does not prove runtime smoke.

```bash
MODEL_PROVIDER=local_llm \
ALPHA_LOCAL_LLM_ENABLED=true \
ALPHA_LOCAL_LLM_ENDPOINT="<operator-confirmed-localhost-or-loopback-http-endpoint>" \
ALPHA_LOCAL_LLM_MODEL="<operator-confirmed-exact-local-model-name>" \
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS="<operator-confirmed-finite-positive-timeout>" \
env -u OPENAI_API_KEY \
    -u ANTHROPIC_API_KEY \
    -u GOOGLE_API_KEY \
    -u GEMINI_API_KEY \
    -u DEEPSEEK_API_KEY \
    python scripts/check_env.py
```

## Future runtime smoke command template

This command uses the merged implementation surface `run_configured_local_llm_runtime()` and the default local `urllib_ollama_json_transport()` path. Running it will call the operator-confirmed local loopback endpoint; therefore it must not be executed until smoke is explicitly authorized.

```bash
MODEL_PROVIDER=local_llm \
ALPHA_LOCAL_LLM_ENABLED=true \
ALPHA_LOCAL_LLM_ENDPOINT="<operator-confirmed-localhost-or-loopback-http-endpoint>" \
ALPHA_LOCAL_LLM_MODEL="<operator-confirmed-exact-local-model-name>" \
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS="<operator-confirmed-finite-positive-timeout>" \
env -u OPENAI_API_KEY \
    -u ANTHROPIC_API_KEY \
    -u GOOGLE_API_KEY \
    -u GEMINI_API_KEY \
    -u DEEPSEEK_API_KEY \
    python - <<'PY'
import json
import os
import sys

from alpha.local_llm.provider_adapter import run_configured_local_llm_runtime

PROMPT = "Local runtime smoke: respond with one concise sentence that does not echo this prompt."

result = run_configured_local_llm_runtime(PROMPT, env=os.environ)
record = {
    "status": result.status,
    "reason": result.reason,
    "behavior_evidence": result.behavior_evidence,
    "output_text": result.output_text,
    "metadata": dict(result.metadata),
}
print(json.dumps(record, sort_keys=True, indent=2))
if result.status == "failed_closed":
    sys.exit(2)
sys.exit(0)
PY
```

## Historical example values only

The following values were prior operator-local examples only. The future operator must confirm actual values at execution time.

```dotenv
ALPHA_LOCAL_LLM_ENDPOINT=http://127.0.0.1:11434/api/chat
ALPHA_LOCAL_LLM_MODEL=gemma3:4b
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=120
```

## Command constraints

- Use `MODEL_PROVIDER=local_llm`.
- Use `ALPHA_LOCAL_LLM_ENABLED=true`.
- Use only a localhost or loopback `http` endpoint.
- Use the exact local model name.
- Use a finite positive timeout.
- Unset hosted provider keys for local mode.
- Do not enable hosted fallback.
- Preserve raw stdout, raw stderr, command, exit code, config summary, and sanitized result.
