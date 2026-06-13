# Data-flow review

Covers: request/data flow, local-vs-provider execution boundary, CORS at the
data-flow level, and the data-classification registries.

## Request entry and shape

- The primary product API is `POST /v1/solve` (`service/app.py:943`). The handler
  accepts a `SolveRequest` and immediately runs `query = sanitize_query(req.query)`
  (`service/app.py:945`) before any further processing.
- Optional `context` params and `strategy` flow through
  (`service/app.py:946-948`). `request.state.strategy` is set for telemetry.

## Local-vs-provider execution boundary

- Alpha Solver is **offline-first**. `.env.example` documents
  `MODEL_PROVIDER=local` as "the verified safe default for offline/local checks"
  that "does not require provider API keys."
- The provider branch in `/v1/solve` only runs when
  `_is_openai_provider_enabled()` is true (`service/app.py:950`, helper at
  `service/app.py:211`). When it is not
  enabled, the request is served locally and the prompt is not forwarded to any
  external provider.
- The optional local-LLM runtime path is **default-off** and constrained to
  loopback. `.env.example` documents it requires `localhost / loopback`, an exact
  local model name, a finite timeout, and **no provider keys**, and states it "is
  not exposed through `/v1/solve` or dashboard preview by this implementation."

This is a strong default-safe posture: by default no prompt content leaves the
host. See `provider-data-sharing-review.md` for the enabled-provider path.

## CORS at the data-flow boundary

- `ServiceCorsConfig.origins` defaults to `os.getenv("SERVICE_CORS_ORIGINS", "*")`
  (`alpha/core/config.py:47-48`). The default is wildcard `*`.
- `service/app.py:161-166` installs `CORSMiddleware` with
  `allow_origins=cfg.cors.origins`, `allow_credentials=True`,
  `allow_methods=["*"]`, and `allow_headers=["*"]`.
- The config class docstring itself flags this: "CORS configuration (lock down in
  production)." (`alpha/core/config.py:45`).

**Finding (CORS-1):** A wildcard origin combined with `allow_credentials=True` is
a permissive default. Browsers reject literal `*` when credentials are allowed,
but the combination is a misconfiguration smell and, depending on how origins are
later set, can broaden cross-origin credentialed access. Tracked in
`risk-register.md` as RR-01.

## Data classification registries

Two registries exist and **disagree**:

- `config/data_classification.yaml`:
  ```
  rules:
    - match: "pii|secret|token"
      action: "instructions_only"
  ```
- `registries/data_classification.yaml`:
  ```
  version: "0.1.0"
  rules:
    - { match: "phi", action: "mask" }
    - { match: "pii", action: "deny" }
  ```

The two files define different match sets and different actions for overlapping
categories (e.g. `pii` maps to `instructions_only` in one and `deny` in the
other). There is no single authoritative classification policy.

**Finding (CLASS-1):** Divergent / duplicated data-classification registries with
no documented precedence. A reviewer cannot determine which policy is
authoritative for runtime enforcement. Tracked in `risk-register.md` as RR-05.

## Summary

The default execution boundary is conservative and offline-first. The data-flow
gaps are (a) the permissive CORS default and (b) the inconsistent
data-classification registries.
