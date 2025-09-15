# Budgeting

## Simulator (RES-08)

Estimate costs before running:

```bash
python -m service.budget.simulator --items eval/sample.jsonl
```

## CLI Guard (NEW-012)

```bash
python -m service.budget.cli --provider OPENAI --model gpt-5 \
  --items eval/sample.jsonl --max-cost 2.50 --max-tokens 200000 \
  --jsonl-out out/budget.jsonl
echo $?  # 0=ok, 2=over thresholds
```

Example `out/budget.jsonl`:

```json
{"item_id": "q1", "tokens": 400, "cost_usd": 0.02, "budget_verdict": "under"}
```

`budget_verdict` reports `under` or `over` against the thresholds.

