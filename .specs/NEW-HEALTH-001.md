# NEW-HEALTH-001 · Health Check Endpoints

Expose `/health` with dependency checks and fast responses.

- JSON payload: `{ "app": "ok", "redis": "ok|down", "vectordb": "ok|down", "provider": "ok|down", "ts": ... }`
- Probes Redis, vector database and provider availability.
- Latency target: local p95 under 50 ms.
- Includes unit tests and documentation.
