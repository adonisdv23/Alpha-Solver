# Health & Readiness Endpoints

Alpha Solver exposes lightweight liveness and readiness probes for use by
orchestrators and load balancers.

## `/health`

* **Method:** `GET`
* **Purpose:** Liveness check. Returns the operational status of the service and
  critical dependencies.
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

Both endpoints complete in under 100 ms and never expose secrets or PII.
