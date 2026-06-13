# Repo-state verification

## Branch and revision

- Working branch: `claude/def-002-security-privacy-review-wt6fja`.
- Review baseline commit (HEAD at review time): `f5711182a592c0a76bc556f8ec68e77228024112`
  (`docs(openai): add project billing boundary attestation retry packet (#512)`).
- Working tree was clean before this packet was authored.

## Read-only verification context

This lane is a documentation review. All findings below are derived from reading
committed source files. No runtime was started, no provider was contacted, no
secret or environment variable was read or printed, and no route was exercised.

## Validators (offline, documentation hardening)

The three offline doc-hardening validators were confirmed green at the review
baseline before authoring this packet, and are re-run after authoring:

- `python scripts/check_local_llm_doc_paths.py`
- `python scripts/check_local_llm_evidence_boundaries.py`
- `python scripts/check_local_llm_packet_consistency.py`

These validators are marker-scoped (they scan local-LLM / `alpha-solver-post-*`
/ OpenAI packet directories and the operator guide). This packet's directory
name is outside those scan markers, so the packet is not itself scanned; the
validators must nonetheless remain green, which is verified in
`def-002-verdict.md`.

## Primary evidence files inspected (read-only)

| Area | File(s) |
| --- | --- |
| CORS / auth / rate-limit config | `alpha/core/config.py` |
| Service app, middleware, `/v1/solve` | `service/app.py` |
| Secrets backend / dashboard settings | `alpha/webapp/routes/settings.py` |
| Dashboard auth / fail-closed mount | `alpha/webapp/routes/auth.py`, `service/app.py` |
| JWT verification | `service/auth/jwt_utils.py`, `service/middleware/jwt_middleware.py` |
| API-key / auth middleware | `service/middleware/auth_middleware.py`, `service/auth/api_keys.py` |
| Tenancy | `service/tenancy/context.py`, `service/tenancy/limiter.py`, `service/middleware/tenant_middleware.py` |
| Audit | `service/audit/audit_log.py`, `service/audit/hash_chain.py`, `service/audit/exporter.py` |
| Evidence API | `service/evidence/api.py`, `service/evidence/store.py`, `service/evidence/collector.py` |
| Redaction | `alpha/self_operator/redaction.py` |
| Provider telemetry / SAFE-OUT | `alpha/providers/telemetry.py`, `alpha/providers/safeout.py` |
| Data classification | `config/data_classification.yaml`, `registries/data_classification.yaml` |
| Dependency surface | `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`, `.env.example` |

## Prior DEF-002 context

The prior packet
`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-def-002-def-003-evidence-boundary-001/def-002-security-privacy-boundary.md`
recorded that DEF-002 remained **open** and enumerated the minimum future
evidence required (scope, data-flow, credential handling, logging/redaction,
provider data-sharing, dashboard and `/v1/solve` exposure, operator approval
boundary, threat model / risk register, accepted residual risks, forbidden
claims). This lane performs that review against committed evidence.
