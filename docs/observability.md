# Observability

Run the production stack with Docker Compose:

```bash
docker compose -f infrastructure/docker-compose.prod.yml up --build
```

The API exposes health, readiness and Prometheus metrics:

- `curl localhost:9000/healthz`
- `curl localhost:9000/readyz`
- `curl localhost:9000/metrics`

Prometheus scrapes the API automatically. Grafana boots with a pre-provisioned
Prometheus data source and example dashboard. Access them at:

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default credentials `admin`/`admin`)
