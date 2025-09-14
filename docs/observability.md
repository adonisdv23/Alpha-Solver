# Observability

This guide covers how to **run**, **inspect**, and **evaluate** Alpha Solver’s observability: health/ready endpoints, Prometheus/Grafana, JSONL telemetry search, replay/benchmark utilities, accessibility checks, and leaderboards.

---

## Run (production compose)

```bash
docker compose -f infrastructure/docker-compose.prod.yml up
```

- API: http://localhost:8000  
- Prometheus metrics: http://localhost:9090/metrics  
- Grafana dashboards: http://localhost:3000 (provisioned from `infrastructure/grafana/provisioning`)

---

## Endpoints

- `GET /health` — basic process health; returns `{"status":"ok"}` when configuration is loaded.  
- `GET /ready` — readiness probe toggled by `app_state.ready`.  
- `GET /metrics` — Prometheus metrics (request counts, latency, rate-limit, SAFE-OUT events).

---

## JSONL Search (telemetry)

Filter run summaries from `telemetry/telemetry.jsonl`:

```bash
jq -r 'select(.event=="run_summary")' telemetry/telemetry.jsonl
```

---

## Replay Harness

Rehydrate a recorded session:

```bash
alpha-solver replay --session SESSION_ID
```

Artifacts (evidence packs) are written under `artifacts/replays/<SESSION_ID>.jsonl`.

---

## Benchmark

Quick sanity benchmark:

```bash
alpha-solver bench --quick
head bench_out/bench.csv
```

---

## Accessibility CLI

Run a11y checks on a replay and view the summary:

```bash
alpha-solver a11y-check --input artifacts/replays/SESSION_ID.jsonl
cat artifacts/a11y/summary.json
```

---

## Governance Flags (examples)

Budget and breaker examples for safe runs:

```bash
alpha-solver run --queries demo --budget-max-steps 5 --budget-max-seconds 1 --breaker-max-fails 2
```

*(Tune to your scenario; these flags gate cost and failure loops.)*

---

## Leaderboard & Overview

Generate per-query/top-k tables from telemetry:

```bash
python scripts/telemetry/leaderboard.py --paths telemetry/*.jsonl --format all
```

The overview lists run metadata and per-query leaderboards; links appear at the end.

---

## Notes

- The production compose stack wires Prometheus & Grafana for quick monitoring.  
- Evidence (replay/benchmark/a11y) plus metrics makes regressions easy to spot and reproduce.
