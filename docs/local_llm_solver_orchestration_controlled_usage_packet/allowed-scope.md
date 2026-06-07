# Allowed Scope

## Scope classification

This packet is limited to Level 2 local operator usability for the stable local LLM solver orchestration CLI wrapper.

Allowed work in this packet:

- define a future controlled usage process;
- define operator preflight checks;
- define run artifact capture requirements;
- define stop conditions;
- define future result review checks;
- record lane continuity.

## Future controlled usage run boundary

A future controlled usage operator-run lane may use only this command identity:

```text
python -m alpha.local_llm.operator_cli
```

A future run must remain local-only and explicitly configured:

```bash
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt-file ./controlled-usage-prompt.txt \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "<exact-local-model-name>" \
  --timeout-seconds "<finite-positive-timeout>"
```

The prompt source may use `--prompt`, `--prompt-file`, or `--prompt-stdin`, but exactly one prompt source must be selected.

## Local-only invariants

Any future controlled usage run must confirm all of the following before execution:

- explicit opt-in with `--enable-local-llm`;
- loopback endpoint only;
- finite positive timeout;
- exact local model name;
- no hosted provider keys required;
- no hosted provider keys accepted as wrapper inputs;
- no hosted fallback;
- no provider fallback;
- no `/v1/solve` exposure or call;
- no dashboard exposure or call;
- `behavior_evidence=false`;
- `no_hosted_fallback=true`;
- `no_provider_keys_required=true`.

## Out of scope

This packet does not authorize execution. It does not authorize local model inference, Ollama execution, smoke reruns, hosted provider calls, `/v1/solve` exposure, dashboard exposure, provider fallback, hosted fallback, Google Sheets updates, backlog workbook edits, or evidence-model promotion.
