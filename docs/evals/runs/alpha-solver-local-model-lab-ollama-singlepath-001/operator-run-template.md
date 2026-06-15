# Operator-run template

Do not run this template unless a real local Ollama run is explicitly authorized by the operator.

## Confirm exact local model without pulling

```bash
ollama list | awk 'NR > 1 {print $1}' | grep -Fx 'gemma3:4b'
```

The first `ollama list` column must equal `gemma3:4b` exactly. Suffix variants such as `gemma3:4b-it-qat` do not satisfy the approved model boundary. If the exact tag is absent, stop and record a blocked result. This lane does not authorize `ollama pull`, model installation, tag substitution, registry sweeps, or fallback models.

## Synthetic fixture

Use a synthetic prompt such as:

```text
Synthetic local-only fixture: summarize this toy note in one sentence. Note: Ada put two blue blocks and one red block in a box.
```

## Singlepath local command

```bash
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --endpoint-url http://127.0.0.1:11434/api/chat \
  --model gemma3:4b \
  --timeout-seconds 30 \
  --prompt "Synthetic local-only fixture: summarize this toy note in one sentence. Note: Ada put two blue blocks and one red block in a box."
```

## Required stop conditions

Stop and record a blocked local smoke result if any of the following are true:

- The first `ollama list` column does not equal `gemma3:4b` exactly, including when only suffix variants such as `gemma3:4b-it-qat` are present.
- The endpoint differs from `http://127.0.0.1:11434/api/chat`.
- Any hosted provider credential or token would be needed.
- The prompt is not synthetic.
- The intended surface is `/v1/solve`, dashboard, public API, routing, council, or multi-model harness.
