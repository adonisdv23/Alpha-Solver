# Budget Simulator CLI

This lightweight tool estimates token usage, latency and cost for a deck of
scenarios.  It lives entirely in the repository – no external services or
secrets are required – which makes it handy for quick "what if" experiments.

## Running

```bash
python -m cli.budget_sim --scenarios data/scenarios/decks/core_*.jsonl \
  --model-set default \
  --out-json artifacts/budget_report.json \
  --out-csv artifacts/budget_report.csv
```

### Caps

Optional flags let you enforce budgets:

* `--max-cost-usd` – warn at 90% and block over 100% of this amount
* `--max-tokens` – token budget
* `--latency-budget-ms` – p95 latency budget in milliseconds

The summary object contains a `budget_verdict` field with value `ok`, `warn` or
`block` depending on these caps.

### What‑if comparisons

Two YAML/JSON configs can be provided to compare different model sets or caps:

```bash
python -m cli.budget_sim --scenarios scen.jsonl \
  --before-config before.yaml --after-config after.yaml \
  --out-json diff.json
```

The resulting JSON will contain `before`, `after` and `delta` sections showing
total cost, token usage and latency differences.

### Summary only

Use `--summary-only` to print a concise one-line summary suitable for quick
checks in CI pipelines.
