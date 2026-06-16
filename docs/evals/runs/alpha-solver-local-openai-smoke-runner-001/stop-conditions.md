# Stop conditions

Stop and do not continue the smoke run if any condition occurs:

- A command would reveal a secret value.
- Local mode endpoint is not localhost or loopback.
- Local mode has hosted provider key variables present.
- Local model name is unknown or not explicitly configured.
- OpenAI mode lacks `MODEL_PROVIDER=openai`.
- OpenAI mode lacks explicit `ALPHA_LIVE_OPENAI=1` opt-in.
- OpenAI mode lacks a configured key variable.
- Output includes unexpected raw request or provider metadata.
- The runner returns `failed_closed` and the reason is not understood.
- The Operator is not ready to redact output before sharing.
