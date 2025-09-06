# Plan Spine Architecture

The *plan spine* records how Alpha-Solver answers a query.  Each run produces
an ordered list of steps and a minimal JSON artifact describing the run.

## Data Model

```python
from alpha.core.plan import Plan, PlanStep
```

`PlanStep` captures:

* `step_id` – identifier
* `description` – human readable summary
* `contract` – expectations for a successful run
* `result` – output from execution
* `status` – `ok` or `failed`

`Plan` tracks the overall run:

* `run_id`, `query`, `region`
* list of `steps`
* `retries` – maximum retries per step
* `created_at`

`plan.to_json()` emits a dictionary with `schema_version="v1"` suitable for
serialization.

## Contracts and Retries

`validate_contract(step, result)` checks a step's contract against its result
and returns `(ok, critique)`.  `bounded_retry(step, fn, max_retries)` executes a
callable until the contract passes or retries are exhausted.  Critiques from
failed attempts are logged on the step's result.

## CLI Usage

```bash
python -m alpha.core.runner --plan-only --query "demo"
python -m alpha.core.runner --explain --query "demo"
python -m alpha.core.runner --execute --query "demo"
```

The `--plan-only` flag writes `artifacts/last_plan.json` and exits.  `--explain`
adds a short human‑readable explanation.  `--execute` (the default) also runs
steps with retry logic and updates the artifact with results.

## Example `last_plan.json`

```json
{
  "schema_version": "v1",
  "run_id": "1234",
  "query": "demo",
  "region": "US",
  "retries": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "steps": [
    {
      "step_id": "step-1",
      "description": "demo step for demo",
      "contract": {"ok": true},
      "result": {"ok": true},
      "status": "ok"
    }
  ]
}
```
