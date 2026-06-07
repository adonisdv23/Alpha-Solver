# Command Reference

## Current command-reference status

The repository currently provides a Python/module entry point, `alpha.local_llm.orchestration_runner.run_local_llm_solver_orchestration`, rather than a stable operator-facing CLI wrapper. Do not invent a CLI name for this path. A future CLI-wrapper decision lane is selected in [selected-next-lane.md](selected-next-lane.md).

## Check Ollama model availability

Template only; run on the local developer machine where Ollama is installed:

```bash
ollama list
```

Confirm the intended model name, for example `qwen2.5:3b`, appears in the output before running local orchestration.

## Run the current local-only orchestration entry point

Template only; this performs local model execution and must be run only by an operator who intends a local-only Level 2 run:

```bash
ALPHA_LOCAL_LLM_ENABLED="true" \
ALPHA_LOCAL_LLM_ENDPOINT="http://127.0.0.1:11434/api/chat" \
ALPHA_LOCAL_LLM_MODEL="qwen2.5:3b" \
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS="60" \
python - <<'PY'
import json
from alpha.local_llm.orchestration_runner import run_local_llm_solver_orchestration

result = run_local_llm_solver_orchestration(
    "List three bounded considerations for reducing local Python CLI startup latency."
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Required operator checks after the command:

- Confirm `behavior_evidence=false`.
- Confirm `no_hosted_fallback=true`.
- Confirm `no_provider_keys_required=true`.
- Confirm `metadata.gate_trace` contains only allowed diagnostic enum/boolean/numeric/list-of-enum values.
- Stop if hosted fallback, `/v1/solve` exposure, dashboard exposure, unsafe field exposure, or raw diagnostic text appears.

## Run focused non-model tests only

These tests use fake transports/stubs and do not require a local model:

```bash
python -m pytest -q tests/test_local_llm_solver_orchestration_runner.py
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
