# Hermes Local Run Template

Use this template only on an operator-controlled machine with a locally installed Hermes-style Ollama model. Do not run against hosted providers.

## Preflight

```bash
unset OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY GEMINI_API_KEY DEEPSEEK_API_KEY
command -v ollama
ollama list
```

Confirm the exact local model name before running, for example `hermes3:latest` or another installed local Hermes-style name. Do not pull or install models as part of this packet unless a separate operator instruction authorizes it.

## Approved harness command pattern

Replace `<LOCAL_HERMES_MODEL_NAME>` and `<PROMPT_TEXT>` with a single synthetic fixture from `prompt-fixtures.md`.

```bash
unset OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY GEMINI_API_KEY DEEPSEEK_API_KEY
python -m alpha.local_llm.multi_model_smoke_harness \
  --local-only \
  --models "<LOCAL_HERMES_MODEL_NAME>" \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --timeout-seconds 30 \
  --prompt "<PROMPT_TEXT>"
```

## Capture template

For each prompt fixture, record the sanitized result in `observed-results.md`:

```text
Fixture ID:
Local model name:
Endpoint URL:
Run timestamp UTC:
Harness status:
Harness reason:
Sanitized output preview:
Persona adherence observation:
Instruction-following observation:
Refusal/SAFE-OUT observation:
Structured-output observation:
Council-role observation:
Final-synthesis observation:
Failure modes observed:
Non-claims retained:
Operator verdict:
```

## Stop conditions

Stop and preserve the blocked state if any of the following occur:

- Ollama is not installed or not listening on loopback.
- The Hermes-style model is not listed locally.
- Hosted-provider keys are present and cannot be removed from the environment.
- The endpoint is not loopback.
- The prompt would include private data, credentials, dashboards, `/v1/solve`, or production data.
- The harness reports blocked, timeout, connection failure, prompt echo, or empty output.
