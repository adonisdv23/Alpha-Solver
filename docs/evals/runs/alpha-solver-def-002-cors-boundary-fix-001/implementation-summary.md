# Implementation summary

Verdict: `DEF_002_RR_01_CORS_BOUNDARY_HARDENED`

Implemented changes:

- Changed `ServiceCorsConfig` default origins from wildcard to a local-only
  allowlist for `localhost` and `127.0.0.1` development origins.
- Added `SERVICE_CORS_ALLOW_CREDENTIALS`, defaulting to `true` to preserve
  credential semantics while making wildcard origins invalid under that mode.
  The value is loaded through a per-instance default factory so environment
  changes made after module import are honored when constructing `APISettings()`.
- Added config validation that raises on `SERVICE_CORS_ORIGINS=*` with
  credentials enabled.
- Wired `service.app` CORS middleware to `cfg.cors.allow_credentials` instead of
  hard-coding credential support.
- Added tests for default local-only behavior, explicit external allowlists,
  per-instance `SERVICE_CORS_ALLOW_CREDENTIALS=false` opt-out loading,
  wildcard origins with credentials disabled, invalid wildcard-plus-credentials
  config, common truthy credential values, and real app CORS behavior for
  allowed/denied origins.
- Updated `.env.example` with non-wildcard CORS guidance.

No public exposure, provider call, token use, credential access, or deployment
was performed.
