# Health Endpoint

The service exposes `GET /health` to provide a quick status overview of core
runtime dependencies. The response is JSON with the following shape:

```json
{
  "app": "ok",
  "redis": "ok|down",
  "vectordb": "ok|down",
  "provider": "ok|down",
  "ts": 1697049600.0
}
```

Field meanings:

- **app** – always `"ok"` when the handler runs.
- **redis** – result of a lightweight `PING` against the configured Redis
  instance.
- **vectordb** – status of the vector database backend.
- **provider** – whether the model provider client can be imported and is
  available.
- **ts** – UNIX timestamp recorded when the check was executed.

Each dependency probe is designed to complete quickly so the endpoint responds
within ~50 ms on a warm cache.
