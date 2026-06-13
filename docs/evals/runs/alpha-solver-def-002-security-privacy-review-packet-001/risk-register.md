# Risk register (open gaps)

Severity scale: High / Medium / Low. Disposition: **Gap-closure** (requires a code
or config change, owned by the gap-closure lane) or **Residual** (candidate for
operator risk acceptance, see `accepted-residual-risks.md`).

All findings are derived from committed source read read-only. This packet records
them; it does not remediate them (docs-only).

| ID | Area | Finding | Evidence | Severity | Disposition |
| --- | --- | --- | --- | --- | --- |
| RR-01 | CORS | Default origin `*` combined with `allow_credentials=True`, wildcard methods/headers. Permissive default ("lock down in production"). | `alpha/core/config.py:45-48`; `service/app.py:161-166` | Medium | Gap-closure |
| RR-02 | Secrets-at-rest | `FileSecretsBackend` persists provider API keys as plaintext JSON; no at-rest encryption; no explicit restrictive file mode. | `alpha/webapp/routes/settings.py:62-95`, `:170` | High | Gap-closure |
| RR-03 | Default credentials | Default API key `dev-secret`; default dashboard password `alpha-dashboard` present in source. | `alpha/core/config.py:22-26`; `alpha/webapp/routes/auth.py:42` | High | Gap-closure |
| RR-04 | Provider data-sharing | With a provider enabled, user prompt text is transmitted to a third party; no committed end-user data-sharing/retention disclosure identified in scope. | `service/app.py:266`, `:987`, `:1002` | Medium | Residual (operator) |
| RR-05 | Data classification | Two divergent `data_classification.yaml` registries with conflicting rules; no documented precedence/authoritative policy. | `config/data_classification.yaml`; `registries/data_classification.yaml` | Medium | Gap-closure |
| RR-06 | Dependencies | Dependency declarations duplicated and potentially drifting between `requirements.txt` and `pyproject.toml`. | `requirements.txt`; `pyproject.toml:17-26` | Low | Gap-closure |
| RR-07 | Supply chain | No lockfile and no hash pinning; range-only runtime dependencies. | `requirements.txt`; `pyproject.toml` | Medium | Gap-closure |
| RR-08 | Supply chain | In-tree vendored/shimmed third-party libs with untracked provenance/patch status. | repo root: `slowapi/`, `prometheus_client/`, `prometheus_fastapi_instrumentator/`, `jsonschema/`, `jsonlines_compat.py` | Medium | Gap-closure |
| RR-09 | `/v1/solve` exposure auth model | Bundled `/v1/solve` relies on API-key auth + rate limiting; JWT and tenant middleware exist in-repo but are not mounted on the bundled app. Intended auth/tenancy model for `/v1/solve` must be explicitly confirmed or wired before public/runtime exposure. | `service/app.py:149-166`, `:884`, `:927`, `:943`; `service/security.py:19-27`; unmounted: `service/middleware/jwt_middleware.py`, `service/middleware/auth_middleware.py`, `service/middleware/tenant_middleware.py` | Medium | Gap-closure |

## Strong controls observed (not gaps — recorded for balance)

| Control | Evidence |
| --- | --- |
| Offline-first default; provider gated behind opt-in | `.env.example`; `service/app.py:950` |
| Local-LLM path default-off, loopback-only, not exposed via `/v1/solve`/dashboard | `.env.example` |
| Provider telemetry is allowlist-built, content-free | `alpha/providers/telemetry.py:23-44`, `:104-115` |
| Provider SAFE-OUT built from safe fields only | `alpha/providers/safeout.py:37-52` |
| Request logging carries metrics, not prompt content | `service/app.py:901-909` |
| Deterministic offline secret redaction for Self Operator artifacts | `alpha/self_operator/redaction.py` |
| Dashboard fail-closed mount (non-default password + secret key required) | `service/app.py:183-207` |
| RS256-only JWT with bounded leeway | `service/auth/jwt_utils.py:13`, `:14` |
| Tamper-evident audit hash chain | `service/audit/hash_chain.py` |
| Masked secret display + masked audit entries | `alpha/webapp/routes/settings.py:115-150` |

## Disposition summary

- **Gap-closure required:** RR-01, RR-02, RR-03, RR-05, RR-06, RR-07, RR-08, RR-09.
- **Operator residual-risk candidates:** RR-04 (and the inherent redaction-coverage
  limitation RR-A1 in `accepted-residual-risks.md`).

Because gap-closure items remain open, DEF-002 is **not** closed by this packet.
