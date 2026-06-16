# Operator runbook

## Start locally

```bash
uvicorn tools.operator_test_console:app --host 127.0.0.1 --port 8765
```

Then open `http://127.0.0.1:8765/` on the same machine.

## Local mode

1. Select `local`.
2. Keep the default model `qwen2.5:3b` or enter another local model name.
3. Confirm the local Ollama environment variables required by `tools/operator_smoke_runner.py` are already set.
4. Submit the prompt.

## OpenAI mode

1. Select `openai`.
2. Keep the default model `gpt-4.1-mini` or enter another OpenAI model name.
3. Set `MODEL_PROVIDER=openai`, `ALPHA_LIVE_OPENAI=1`, and `OPENAI_API_KEY` in the local shell before starting the console.
4. Submit the prompt.

The console has no API-key input field. It reads OpenAI credentials from the local environment only.
