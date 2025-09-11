# Alpha Solver API

The API service exposes the existing `_tree_of_thought` pipeline over HTTP.

## Local dev & CI gates

Run `docker compose -f infrastructure/docker-compose.yml up --build`.

To exactly match CI:

```bash
pip install -r requirements-dev.txt -c constraints.txt
```

Once started the service is available at `http://localhost:8000`.

## Authentication

Requests may include an API key header (default `X-API-Key`). When
authentication is enabled, only configured keys are accepted. Set
`SERVICE_AUTH_KEYS=key1,key2` to change the allowed keys or
`SERVICE_AUTH_ENABLED=false` to disable the check entirely.

```
X-API-Key: dev-secret
```

## Rate limiting

Each API key is limited to **120 requests per 60 seconds** by default. Set
`SERVICE_RATELIMIT_ENABLED=false` to disable or tune
`SERVICE_RATELIMIT_WINDOW_SECONDS` and `SERVICE_RATELIMIT_MAX_REQUESTS`. When
auth is disabled the limit applies per client IP.

## Example

```bash
curl -H "X-API-Key: dev-secret" \
     -H "Content-Type: application/json" \
     -d '{"query": "hello", "strategy": "react"}' \
     http://localhost:8000/v1/solve
```

`strategy` selects the reasoning mode: `cot` (default), `react`, or `tot`.
Responses using `react` include a `trace` and `meta` block:

```json
{
  "final_answer": "...",
  "trace": [{"thought": "t1:...", "action": "self-check", "observation": "deterministic reflection"}],
  "confidence": 0.9,
  "meta": {"strategy": "react", "seed": 42}
}
```

## Docs & Metrics

* Interactive docs: `http://localhost:8000/docs`
* OpenAPI JSON: `http://localhost:8000/openapi.json`
* Prometheus metrics: `http://localhost:8000/metrics`
