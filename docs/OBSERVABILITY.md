# Observability

## Record

```bash
alpha_solver_cli --record --events out/events.jsonl
```

## Replay

```bash
python -m service.observability.replay_cli --events out/events.jsonl
```

## Diff

```bash
python -m service.observability.replay_cli --compare out/a.jsonl --events out/b.jsonl
```

## Metrics

Expose Prometheus metrics at `/metrics`.

Metrics referenced by tests:

- `alpha_solver_route_decision_total{...}`
- `alpha_solver_budget_verdict_total{...}`
- `alpha_solver_latency_ms_bucket{...}`
- `alpha_solver_tokens_total`
- `alpha_solver_cost_usd_total`
- `alpha_solver_confidence`

## Dashboards

- `dashboards/alpha_observability.json`
- `dashboards/cost_budget.json`

Datasource placeholder: `${DS_PROMETHEUS}`.

## Sample `route_explain`

```json
{
  "route": "default",
  "decision": "allow",
  "confidence": 0.82,
  "scorers": {"tot": 0.82},
  "gates": ["budget_ok"]
}
```

