# Alpha Solver API

The API service exposes the existing `_tree_of_thought` pipeline over HTTP.

## Running locally

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

Once started the service is available at `http://localhost:8000`.

## Authentication

Requests must include an API key header:

```
X-API-Key: changeme
```

Set `API_KEY` environment variable to change the expected key.

## Rate limiting

Each key is limited to **60 requests per minute**.

## Example

```bash
curl -H "X-API-Key: changeme" \
     -H "Content-Type: application/json" \
     -d '{"query": "hello"}' \
     http://localhost:8000/v1/solve
```

## Docs & Metrics

* Interactive docs: `http://localhost:8000/docs`
* OpenAPI JSON: `http://localhost:8000/openapi.json`
* Prometheus metrics: `http://localhost:8000/metrics`
