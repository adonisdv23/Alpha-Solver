# Hermes Operator Local Run Template

Only run on an operator machine after confirming all preconditions:

- The operator authorizes a local-only Hermes characterization smoke.
- Ollama is installed and listening on `http://127.0.0.1:11434/api/chat`.
- The Hermes-style model name is installed locally, for example `hermes3` or `nous-hermes2`.
- Hosted-provider API keys are absent or unset for the shell session.
- Prompts are synthetic and contain no private data, secrets, customer data, or credentials.
- Results will be treated as local characterization notes only, not benchmark or production evidence.

## Install/status checks

```bash
command -v ollama
ollama list
```

## Safe shell setup

```bash
unset OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY GEMINI_API_KEY DEEPSEEK_API_KEY
```

## Harness command template

Replace `hermes3` with the exact local model name shown by `ollama list`.

```bash
python -m alpha.local_llm.multi_model_smoke_harness \
  --local-only \
  --models "hermes3" \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --timeout-seconds 30 \
  --prompt "You are Alpha Solver v2.3.0-P3, running in PORTABLE-SPEC mode. Use compact SolverEnvelope-shaped Markdown. In SOLUTION, say whether a docs-only local model characterization lane can claim production readiness. Keep other required labels minimal."
```

## Optional fixture runs

Run one fixture at a time by replacing `--prompt` with one fixture from `prompt-fixtures.md`. Preserve each command and result in `observed-results.md`.

## Allowed operator-run outcomes

- `HERMES_LOCAL_CHARACTERIZATION_CAPTURED`
- `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED`
- `STOP_INCONCLUSIVE`

Do not convert local runs into superiority, benchmark, routing, production-readiness, or paid-provider comparison claims.
