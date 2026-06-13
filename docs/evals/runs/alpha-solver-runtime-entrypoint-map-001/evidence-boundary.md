# Evidence Boundary

## Evidence inspected

- Runtime/service code: `service/app.py`, `service/security.py`, `service/middleware/*`, `service/auth/*`, `service/evidence/*`, `service/tenancy/*`.
- Dashboard code: `alpha/webapp/routes/*`, templates by path inventory only.
- Provider/settings code: `alpha/providers/*`, `alpha/local_llm/provider_adapter.py`, `alpha/core/config.py`, model-set/settings paths.
- Portable/reference entrypoints: `alpha_solver_portable.py`, `alpha_solver_entry.py`, `alpha-solver-v91-python.py`.
- Tests by static inventory and targeted path/name review for service, dashboard, provider, tenancy, rate-limit, and portable behavior.
- Docs: `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, and `docs/evals/runs/alpha-solver-def-002-security-privacy-review-packet-001/`.

## Evidence limits

- Static review only; no app was started for exposure validation.
- No providers were called.
- No tokens or credentials were accessed.
- No claims are made about production readiness, public MVP readiness, security closure, provider validation, value proof, dashboard readiness, `/v1/solve` readiness, or benchmark superiority.

## Verdict basis

`RUNTIME_ENTRYPOINT_MAP_CAPTURED` is selected because committed repository evidence is sufficient to map current entrypoints and boundaries at documentation level. It does not mean those entrypoints are safe to expose.
