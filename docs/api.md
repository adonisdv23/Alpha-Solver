# Alpha Solver API

The API service exposes the existing `_tree_of_thought` pipeline over HTTP.

- **POST only:** `/v1/solve` accepts JSON `{ "query": "...", "strategy": "react|cot|tot", "context": {...} }`. The old GET usage is deprecated.
- **SAFE-OUT policy (minimal):** for simple arithmetic prompts (e.g., `17 + 28`), the service will either include the computed result in the final answer or return `SAFE-OUT: ...`. This prevents confidently wrong results from being emitted.
- **Metrics:** exposed at `GET /metrics` in Prometheus text format. No separate Prometheus HTTP server is started.

## Running locally

Install dependencies with:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

```bash
docker compose -f infrastructure/docker-compose.yml up --build
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

### POST /v1/solve

- Header: `X-API-Key: dev-secret`
- Body:

```json
{
  "query": "What is 17 + 28? Show steps.",
  "strategy": "react"
}
```

curl

```bash
curl -sS http://localhost:8000/v1/solve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret" \
  -d '{"query":"What is 17 + 28? Show steps.","strategy":"react"}'
```

`strategy` selects the reasoning mode: `cot`, `react`, or `tot` (default).
`cot` returns a deterministic chain-of-thought with simple steps, `react`
executes a minimal ReAct loop, and omitting the field (or using `tot`)
invokes the full tree-of-thought solver. Responses using `react` include a
`trace` and `meta` block:

```json
{
  "final_answer": "...",
  "trace": [{"thought": "t1:...", "action": "self-check", "observation": "deterministic reflection"}],
  "confidence": 0.9,
  "meta": {"strategy": "react", "seed": 42}
}
```

Responses using `cot` include the generated steps:

```json
{
  "final_answer": "To proceed, consider: hello",
  "steps": ["step_1: hello"],
  "confidence": 0.5,
  "meta": {"strategy": "cot", "seed": 0}
}
```

## Docs & Metrics

* Interactive docs: `http://localhost:8000/docs`
* OpenAPI JSON: `http://localhost:8000/openapi.json`
* Prometheus metrics: `http://localhost:8000/metrics`

OpenAPI is available via:

```bash
curl -s http://localhost:8000/openapi.json | jq .
```

Note: GET examples for `/v1/solve` are deprecated; use POST with a JSON body.

## Local dev & CI gates

To exactly match CI: pip install -r requirements-dev.txt -c constraints.txt

```bash
pip install -r requirements-dev.txt
pre-commit run --all-files
pytest -q
python -m alpha.eval.harness --dataset datasets/mvp_golden.jsonl --seed 42 --compare-baseline
make smoke
```
