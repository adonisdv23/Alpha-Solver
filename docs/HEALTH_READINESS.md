# Health & Readiness Endpoints

Alpha Solver exposes lightweight liveness and readiness probes for use by
orchestrators and load balancers. This page documents the current service-layer
runtime behavior in `service/health.py` and `service/app.py`, not the future
`NEW-HEALTH-001` placeholder target.

## `/health`

* **Method:** `GET`
* **Purpose:** Liveness check. Returns the operational status of the service and
  the current lightweight local probes. These probes check adapter-registry JSON
  loadability and model-provider import availability; they do not check Redis,
  VectorDB, or perform live provider pings.
* **Response:**

```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_s": 12.345,
  "deps": {
    "adapter_registry": true,
    "model_provider": true
  }
}
```

A non-OK status triggers a `503` response.

## `/ready`

* **Method:** `GET`
* **Purpose:** Readiness check. Ensures the service and its dependencies are
  ready to receive traffic. Fails closed (`503`) if any dependency probe fails or
  the application is not yet marked ready.
* **Response:** same schema as `/health`.

Both endpoints complete in under 100 ms and never expose secrets or PII. The
compatibility `/healthz` and `/readyz` endpoints in `service/app.py` remain
lighter service-state probes and do not use the richer `/health`/`/ready`
dependency payload.
