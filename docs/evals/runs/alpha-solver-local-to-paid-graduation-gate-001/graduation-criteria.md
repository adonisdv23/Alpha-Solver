# Graduation criteria

A move from free local/fake-provider testing to a paid hosted-provider smoke is allowed only when every required category below is satisfied for the exact proposed run. Passing this gate authorizes at most a tiny smoke; it does not authorize value experiments, public exposure, production traffic, benchmark claims, or Alpha superiority claims.

## Gate categories

| Category | Required condition | Current state | Gate result |
| --- | --- | --- | --- |
| 1. Local model smoke state | A local/fake-provider smoke lane must identify the candidate path, fixture shape, artifact schema, and failure handling without claiming model quality. | Local model catalog is captured. Multi-model smoke harness is fake-transport only and explicitly not behavior/model-quality evidence. | Captured, not sufficient by itself. |
| 2. No-echo/substantive generation state | The Alpha path intended for paid testing must produce substantive non-echo output or the paid run must be scoped as provider-connectivity-only and not a value run. | The no-echo gate is blocked because the Alpha path echoed prompts in all four synthetic cases. | Blocker for value experiments; allows only a connectivity smoke if separately authorized. |
| 3. Routing matrix readiness | The route/model under test must be selected from documented routing opportunities with explicit misroute and fallback handling. | Routing opportunity map exists, but it is an opportunity map and not implemented routing evidence. | Not ready for routing claims. |
| 4. Provider billing/project authorization state | The operator must provide explicit per-run model, project boundary, cost cap, token cap, max run count, and exact synthetic fixture. | Prior project/billing boundary attestation exists, but retry-002 authorization is incomplete. | Blocked. |
| 5. Cost cap and token cap state | The paid run must have hard pre-run caps and a stop rule that prevents additional calls after cap ambiguity or cap exhaustion. | Provider cost-cap controls are partial and fake-provider only; local retry authorization omitted explicit caps. | Blocked until exact per-run caps are supplied. |
| 6. Data-sharing and redaction state | The operator must acknowledge provider data sharing for the exact fixture and confirm no secrets/sensitive data are included. | Prior data-sharing attestation exists; the exact retry-002 fixture was not supplied in the blocked run prompt. | Needs refresh for the exact run. |
| 7. Security no-go blockers | No public exposure, dashboard exposure, credential exposure, unsafe CORS/auth posture, or DEF-002 closure claim may be required for the run. | Public exposure gate is no-go; DEF-002 remains open. | Allows only non-public, local operator-supervised smoke if authorized. |
| 8. Value experiment preregistration state | Value experiment protocol must be frozen before value execution, and Alpha must pass the no-echo precondition. | Protocol exists but is unexecuted; no-echo precondition fails. | Blocks value experiment execution. |
| 9. Operator approval state | Operator must explicitly approve the exact next paid action after seeing this gate and its stop conditions. | Not captured in this packet. | Blocked. |
| 10. Stop conditions | Stop conditions must be explicit, checkable, and stronger than the planned action. | Captured in this packet. | Captured, but not sufficient without authorization. |

## Minimal ready state for a tiny paid smoke

`LOCAL_TO_PAID_GATE_CAPTURED_READY_FOR_TINY_SMOKE` is allowed only if all of the following are true:

1. The action is explicitly limited to a tiny synthetic connectivity/no-echo smoke.
2. The exact hosted provider, model, project/account boundary, fixture, max run count, max request count, max token count, and max estimated cost are documented.
3. The fixture contains no secrets, sensitive personal data, proprietary customer data, or live user payloads.
4. The operator signs off that provider terms, data-sharing, retention, and billing exposure are acceptable for that fixture.
5. Stop conditions are accepted before the call.
6. The result will be labeled smoke evidence only, not value, benchmark, production, or public-readiness evidence.

The current packet does not satisfy these conditions.
