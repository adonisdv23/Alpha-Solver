# Credential-handling review

Covers: secrets-at-rest, `FileSecretsBackend`, API-key auth, JWT verification,
tenancy, audit, and evidence-API credential exposure.

## Secrets-at-rest: `FileSecretsBackend`

- `alpha/webapp/routes/settings.py:62` defines `FileSecretsBackend`, a
  "Simple file-based secrets backend storing JSON data."
- `set()` writes provider keys to disk via `_write()`
  (`settings.py:73-95`) using `json.dump(data, file, indent=2, sort_keys=True)`.
  Values are stored **in cleartext**; there is no encryption, no OS keyring, and
  no envelope/at-rest protection.
- The default storage path is `~/.alpha_solver/dashboard_api_keys.json`
  (`_resolve_path("ALPHA_DASHBOARD_SECRETS_PATH", "dashboard_api_keys.json")`,
  `settings.py:22-34`, `settings.py:170`). The directory is created with default
  permissions (`self.path.parent.mkdir(parents=True, exist_ok=True)`,
  `settings.py:93`) — no explicit `0600`/`0700` mode is set.

**Finding (SEC-1):** Provider API keys are persisted to disk in plaintext with no
at-rest encryption and no explicit restrictive file permissions. Tracked in
`risk-register.md` as RR-02.

### Mitigating controls observed

- The UI and audit log only ever render a masked form. `mask_secret`
  (`settings.py:115-122`) returns `****` for short/empty keys and `****<last4>`
  otherwise. `SettingsService.list_masked` (`settings.py:135-138`) yields only
  masked values, and `AuditLogger.log` records the masked key only
  (`settings.py:146-150`, `set_key` at `settings.py:140-149`).
- The persisted location defaults outside the repository / version control
  (under the user home), per the `_resolve_path` docstring (`settings.py:24-34`).

These reduce *display/log* leakage but do not address at-rest plaintext storage.

## API-key authentication

- `ServiceAuthConfig` (`alpha/core/config.py:17-26`) enables API-key auth by
  default (`SERVICE_AUTH_ENABLED` defaults `"true"`), reads the header name from
  `SERVICE_AUTH_HEADER` (default `X-API-Key`), and loads keys from
  `SERVICE_AUTH_KEYS` / `API_KEY`, **defaulting to `dev-secret`**.
- `service/middleware/auth_middleware.py` enforces JWT **or** API-key auth, with
  `exempt_paths`, optional `scope_map`, and an internal rate limiter.
- `service/auth/api_keys.py` provides the `APIKeyStore` used by the middleware.

**Finding (SEC-3):** The default API key is the well-known literal `dev-secret`.
If a deployment does not override `SERVICE_AUTH_KEYS`/`API_KEY`, the API is
effectively unauthenticated to anyone who knows the default. Tracked as RR-03.

## JWT verification

- `service/auth/jwt_utils.py` restricts algorithms to `ALLOWED_ALGS = {"RS256"}`
  (line 13) — asymmetric only, which avoids the classic `alg:none` and HS/RS
  confusion downgrade. It applies a bounded `LEWAY_SECONDS = 60` clock skew.
- Keys are loaded from a YAML keystore mapping `kid -> PEM public key`
  (`AuthKeyStore`, `jwt_utils.py:26-60`), with mtime/size-based reload and a
  forced-miss reload cooldown to bound key-rotation churn.

**Observation:** JWT handling is conservative (RS256-only, public-key keystore,
bounded leeway). No gap recorded here beyond ensuring the keystore file itself is
managed securely at deployment time (operational, noted in
`accepted-residual-risks.md`).

## Tenancy

- `service/tenancy/context.py`, `service/tenancy/limiter.py`, and
  `service/middleware/tenant_middleware.py` provide per-tenant context and
  limiting. Provider telemetry carries an explicit `tenant` field
  (`alpha/providers/telemetry.py`), enabling per-tenant attribution without
  embedding tenant secrets in logs.

## Audit and evidence APIs

- The audit log is **tamper-evident**: `service/audit/hash_chain.py` chains each
  entry with `SHA256(canonical_json(entry) + prev_hash)` and `verify_chain`
  returns the first corrupt index, providing integrity verification.
- The dashboard `AuditLogger` records only masked keys (`settings.py:146-150`), so
  the audit trail does not itself become a secret sink.
- The evidence API (`service/evidence/api.py`) accepts a `manifest`,
  `simulation_lines`, `metrics`, and `tags` and delegates to `store`. It does not
  itself handle credentials, but callers are responsible for not placing secret
  material into evidence payloads (operational note in
  `accepted-residual-risks.md`).

## Summary of credential gaps

| ID | Gap | Severity |
| --- | --- | --- |
| RR-02 | Plaintext provider secrets at rest (`FileSecretsBackend`), no explicit file mode | High |
| RR-03 | Default API key `dev-secret` ships as an insecure default | High |

Strong controls: RS256-only JWT, masked display/audit, tamper-evident audit
chain, per-tenant attribution.
