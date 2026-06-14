# Operator Local Run Template

Only run on an operator machine after confirming all of the following:

- Ollama is installed and listening on a loopback endpoint.
- The named models are local Ollama model names.
- No private repo files, secrets, customer data, or credentials are included in the prompt.
- No hosted provider keys are present in the environment.
- The output will be treated as smoke evidence only.
- If local Ollama is unavailable, preserve that result as
  `connection_failed` / `LOCAL_MULTI_MODEL_SMOKE_BLOCKED_LOCAL_OLLAMA_UNAVAILABLE`
  and do not retry through hosted providers.

Template:

```bash
unset OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY GEMINI_API_KEY DEEPSEEK_API_KEY
python -m alpha.local_llm.multi_model_smoke_harness \
  --local-only \
  --models "llama3.2:1b,qwen2.5:0.5b" \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --timeout-seconds 10 \
  --prompt "Local smoke check only. Reply with one short sentence about a safe test object. Do not echo this prompt."
```

Allowed operator-run verdicts:

- `LOCAL_MULTI_MODEL_SMOKE_CAPTURED_OPERATOR_LOCAL_OLLAMA`
- `LOCAL_MULTI_MODEL_SMOKE_BLOCKED_LOCAL_OLLAMA_UNAVAILABLE`
- `STOP_INCONCLUSIVE`

Do not convert an operator local run into quality, benchmark, routing, production, or value evidence.
