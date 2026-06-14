# Blocker register

## Top blockers

| Rank | Blocker | Current evidence | Unblock evidence required | Blocks |
| --- | --- | --- | --- | --- |
| 1 | Provider smoke authorization missing | `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` blocked before any call because explicit operator authorization fields were missing. | Authorization-refresh packet with explicit model, project boundary, cost cap, token cap, max run count, and exact synthetic fixture; then a successful tiny synthetic smoke if authorized. | Provider smoke, no-echo gate, value experiment execution. |
| 2 | No substantive/no-echo output | No provider response and no generated answer evidence exists in the current chain. | Controlled output artifact showing Alpha produces substantive non-echo content under approved constraints. | Value evidence, demo narrative, operator preference scoring. |
| 3 | Value experiment not executed | `ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001` is protocol-only and not a result. | Frozen task bank, paired Alpha/plain-baseline generations, scoring rubric, blinded or disciplined review, cost/latency capture. | Core product value claim and discrimination-value signal. |
| 4 | DEF-002 security/privacy not claimably closed | Security/privacy review captured open gaps and follow-on decisions, but public/security completion is not claimable from the current central state. | Gap closure or explicit operator risk acceptance with exposure-specific controls documented. | Public exposure, production readiness, external demo with live surface. |
| 5 | Public exposure gate blocked | Runtime/public maps identify product-shaped surfaces and unsafe-to-expose conditions. | Auth/CORS/secrets/provider disclosure/tenancy/operator controls resolved for the exact surface to expose. | Public MVP, dashboard readiness, `/v1/solve` readiness. |
| 6 | Runtime entrypoints not canonicalized for exposure | Entrypoint map shows overlapping service, dashboard, provider, portable, and legacy/reference surfaces. | Operator-selected canonical path and docs/code alignment before any external surface. | Public or production narrative clarity. |
| 7 | Test/CI health not globally clean | Local Self Operator evidence exists; full-suite health has known ambient failures in prior packet evidence. | Controlled focused/full test run with failures resolved or explicitly registered. | Release readiness and broad confidence claims. |

## Blocker interpretation

The blockers do not mean the project has no useful work. They mean the current evidence supports internal governance and local/offline discipline, not MVP readiness. The highest-leverage next step remains removing the narrow smoke authorization blocker before attempting value evidence.
