# Observability

The production compose stack wires the API with Prometheus and Grafana for quick monitoring.

## Running

```bash
docker compose -f infrastructure/docker-compose.prod.yml up
```

The API serves requests on `http://localhost:8000` and exposes metrics on `http://localhost:9000/metrics`.

## Endpoints

- `/healthz` – basic process health, returns `{"status": "ok"}` when configuration is loaded.
- `/readyz` – readiness probe that flips with `app.state.ready`.
- `/metrics` – Prometheus metrics including request counts, latency, rate-limit and SAFE-OUT events.

## Dashboards

Grafana is available at `http://localhost:3000` with a Prometheus data source pre-configured. Dashboards are provisioned from `infrastructure/grafana/provisioning` and mounted read-only.
