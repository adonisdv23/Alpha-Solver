# DEF-002 Security / Privacy Inputs

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. These are **inputs for a future DEF-002
> review**, verified against committed files. **DEF-002 is NOT resolved**, and
> nothing here is a security/privacy completion claim. DEF-002 is best framed as
> **assessment + threat-model + gap closure of existing machinery**, not
> build-from-scratch.

## Inputs to review

| topic | finding | evidence path | status |
|-------|---------|---------------|--------|
| **CORS** | Default origins `"*"` with `allow_credentials=True`, `allow_methods=["*"]`; docstring says "lock down in production" | `alpha/core/config.py` (`ServiceCorsConfig.origins`), `service/app.py` (`CORSMiddleware`) | CONFIRMED — lock down before exposure (ISS-003) |
| **Secrets at rest** | `FileSecretsBackend` stores raw provider keys as plaintext JSON; masking only on display/audit | `alpha/webapp/routes/settings.py` | CONFIRMED — plaintext-at-rest (ISS-004). Path is gitignored / not committed |
| **Provider telemetry / prompt content** | Telemetry is **allowlist-based** and "never inspects provider request/response payloads"; no prompt-content field | `alpha/providers/telemetry.py` | PARTIALLY_CONFIRMED — **default path is safe**; verify no opt-in verbose/debug path logs prompts (ISS-005) |
| **Data sharing** | Operator data-sharing verification captured but all items `pending_operator_verification` | `docs/evals/runs/openai-data-sharing-operator-verification-001/` (PR #504) | OPEN — operator must verify before any call |
| **Credential handling** | No OpenAI/Anthropic SDK; httpx-style plumbing; `.env` gitignored; secrets file not committed | `requirements.txt`, `.gitignore`, `alpha/providers/` | CONFIRMED — no committed real secrets (not exhaustively re-scanned this lane) |
| **Logging / redaction** | Deterministic regex redaction exists but **no Unicode normalization** (homoglyph/escape evasion possible) | `alpha/self_operator/redaction.py` | CONFIRMED gap — harden before public (ISS-009) |
| **Dashboard exposure** | Dashboard/secrets settings surface exists; exposure out of scope | `alpha/webapp/routes/settings.py`, `service/` dashboards | OPEN — not exposed; review before any exposure |
| **/v1/solve exposure** | Service app exists; route exposure out of scope and not authorized | `service/app.py` | OPEN — not exposed; no exposure claim |
| **Dependency / supply-chain** | Small dependency set (9 runtime deps); pinned ranges | `requirements.txt`, `pyproject.toml` | INPUT — review pins/advisories during DEF-002 |
| **Existing auth/tenancy/audit machinery** | Auth, audit, tenancy, validation, classification modules already present | `service/auth/`, `service/audit/`, `service/tenancy/`, `service/validation/`, `alpha/self_operator/command_classification.py`, audit logger in `alpha/webapp/routes/settings.py` | CONFIRMED — DEF-002 should assess/close gaps in these, not rebuild |

## What would advance DEF-002 (future lane, not this one)

1. Threat-model the public/runtime surface (CORS, auth, tenancy, `/v1/solve`,
   dashboards).
2. Disposition each input above (accept / fix / defer) with recorded rationale.
3. Confirm no opt-in telemetry/logging path emits prompt content.
4. Harden redaction (Unicode normalization) and secrets-at-rest before exposure.
5. Review dependency pins/advisories.

## Boundaries

- **DEF-002 remains open.** No claim of security/privacy completion, runtime
  readiness, or safe public exposure is made.
- No security fix is implemented in this docs-only lane; inputs are recorded for
  the future DEF-002 review.
