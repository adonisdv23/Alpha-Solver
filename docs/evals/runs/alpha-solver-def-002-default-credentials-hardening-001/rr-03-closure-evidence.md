# RR-03 closure evidence

RR-03 is materially reduced by removing known/default credential authentication
semantics from the service API and dashboard paths in this repo state.

## Evidence

- `ServiceAuthConfig` now loads only explicit `SERVICE_AUTH_KEYS` or `API_KEY`
  values and otherwise returns an empty accepted-key list.
- `validate_api_key` remains fail-closed when authentication is enabled and the
  accepted-key list is empty.
- The dashboard expected-password path returns no accepted password when
  `ALPHA_DASHBOARD_PASSWORD` is missing, empty, or equal to the historical
  default sentinel.
- Bundled dashboard mounting remains disabled unless a non-default password and
  explicit signing secret are configured.
- The bundled API-key config contains no active default key.

## Verdict

`DEF_002_RR_03_DEFAULT_CREDENTIALS_HARDENED`
