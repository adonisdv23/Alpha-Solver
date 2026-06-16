# Operator runbook

Review all command output before pasting results back. Redact any accidental secrets or local machine identifiers first.

## Local/Ollama preflight

Use placeholders and keep the endpoint loopback-only:

```bash
export ALPHA_LOCAL_LLM_ENABLED=1
export ALPHA_LOCAL_LLM_ENDPOINT="http://127.0.0.1:11434/api/chat"
export ALPHA_LOCAL_LLM_MODEL="<LOCAL_MODEL_NAME>"
export ALPHA_LOCAL_LLM_TIMEOUT_SECONDS="10"
python tools/operator_smoke_runner.py --mode local --prompt "Reply with one concise sentence that does not echo this prompt."
```

Do not set hosted provider key variables for local mode. Local mode fails closed when such keys are present.

## Local/Ollama smoke

```bash
python tools/operator_smoke_runner.py --mode local --prompt "Reply with one concise sentence that does not echo this prompt."
```

## OpenAI environment preflight

Set only the provider selector, explicit live opt-in, model placeholder, and key variable. Do not print the key value.

```bash
export MODEL_PROVIDER="openai"
export ALPHA_LIVE_OPENAI="1"
export OPENAI_MODEL="<OPENAI_MODEL_NAME>"
export OPENAI_API_KEY="<SET_IN_SHELL_OR_SECRET_MANAGER_WITHOUT_PRINTING>"
python - <<'PY'
import os
required = ["MODEL_PROVIDER", "ALPHA_LIVE_OPENAI", "OPENAI_MODEL", "OPENAI_API_KEY"]
print({name: ("set" if os.getenv(name) else "missing") for name in required})
PY
```

## OpenAI smoke

```bash
python tools/operator_smoke_runner.py --mode openai --prompt "Reply with one concise sentence that does not echo this prompt."
```

## Capture warning

Paste results back only after redaction review. Do not paste secret values, shell history with key values, provider dashboard details, raw request bodies, raw provider metadata, or local machine identifiers.
