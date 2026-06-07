# Command Reference

## Stable local-only operator wrapper

The stable Level 2 operator-facing wrapper for the local LLM solver orchestration path is:

```bash
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt "List three bounded considerations for reducing local Python CLI startup latency." \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "qwen2.5:3b" \
  --timeout-seconds "60"
```

Command identity:

```text
python -m alpha.local_llm.operator_cli
```

This command is non-production, local-only, operator-only, and default-off. It delegates to
`alpha.local_llm.orchestration_runner.run_local_llm_solver_orchestration` and prints the
normalized result JSON to stdout. It is not smoke evidence, not model-quality evidence, not
benchmark evidence, not readiness evidence, and not evidence-model promotion.

Required local settings:

- `--enable-local-llm` is required for explicit local opt-in.
- Exactly one prompt source is required:
  - `--prompt TEXT`
  - `--prompt-file PATH`
  - `--prompt-stdin`
- `--endpoint-url` must be a loopback/local Ollama-style endpoint accepted by the existing local runtime config validation.
- `--model` must be the exact local model identifier.
- `--timeout-seconds` must be a finite positive timeout.

Required operator checks after the command:

- Confirm `behavior_evidence=false`.
- Confirm `no_hosted_fallback=true`.
- Confirm `no_provider_keys_required=true`.
- Confirm `metadata.gate_trace` contains only allowed diagnostic enum/boolean/numeric/list-of-enum values.
- Stop if hosted fallback, `/v1/solve` exposure, dashboard exposure, unsafe field exposure, raw diagnostic text, provider fallback, or evidence promotion appears.

The wrapper does not accept hosted-provider-key CLI flags or API-key CLI arguments. If hosted provider keys are present in the environment and the existing local runtime config path rejects them, the wrapper surfaces the normalized fail-closed local result and exits non-zero without printing provider-key values.

## Prompt-file form

Template only; run on the local developer machine where the intended local runtime is installed:

```bash
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt-file ./prompt.txt \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "qwen2.5:3b" \
  --timeout-seconds "60"
```

## Prompt-stdin form

Template only; stdin is read only when `--prompt-stdin` is explicitly supplied:

```bash
printf '%s\n' 'List three bounded local-only considerations.' | \
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt-stdin \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "qwen2.5:3b" \
  --timeout-seconds "60"
```

## Check Ollama model availability

Template only; run on the local developer machine where Ollama is installed:

```bash
ollama list
```

Confirm the intended model name, for example `qwen2.5:3b`, appears in the output before running local orchestration.

## Advanced module entry point

The lower-level Python/module entry point remains available for tests and advanced developer inspection:

```text
alpha.local_llm.orchestration_runner.run_local_llm_solver_orchestration
```

Prefer the stable wrapper above for operator command use. The module entry point is still non-production and local-only, and does not turn casual local usage into evidence claims.

## Run focused non-model tests only

These tests use fake transports/stubs and do not require a local model:

```bash
python -m pytest -q tests/test_local_llm_operator_cli.py tests/test_local_llm_solver_orchestration_runner.py
```

For broader local runtime configuration checks that still avoid local model execution:

```bash
python -m pytest -q tests/test_local_llm_runtime_integration.py tests/test_config_validation.py
```

## Inspect output JSON if artifacts already exist

Use this only for already-preserved artifacts; do not turn casual local usage into evidence claims:

```bash
jq '{status, mode, answer, final_answer, considerations, assumptions, confidence, metadata, behavior_evidence, no_hosted_fallback, no_provider_keys_required}' path/to/result.json
```

Inspect the gate trace specifically:

```bash
jq '.metadata.gate_trace' path/to/result.json
```
