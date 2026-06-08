# Blocker Matrix

## Status legend

- Clear: the current repository evidence is sufficient for docs-level planning.
- Blocked: work is not authorized until a future approved spec or gate closes the item.
- Risky: the item is not necessarily blocked forever, but it needs explicit controls before future implementation.

| Area | Current status | Blocker | Closure required before implementation |
| --- | --- | --- | --- |
| No provider calls | Blocked | Self Operator MVP readiness must not call hosted providers or infer provider readiness from local docs evidence. | Future spec must explicitly authorize any provider boundary and include no-secret, timeout, SAFE-OUT, accounting, and test isolation rules. |
| No browser automation | Blocked | No approved browser-control contract exists for Self Operator MVP readiness. | Future spec must define whether browser automation is out of scope or explicitly permitted, including sandbox, consent, target allowlist, and artifact capture limits. |
| No credentials | Blocked | This packet cannot introduce API keys, browser credentials, deployment credentials, billing credentials, or stored secrets. | Future spec must define credential-free local mode or an approved secrets model with redaction, storage, rotation, and test fixtures. |
| No fallback | Blocked | Hosted fallback, provider fallback, and implicit local fallback are not authorized. | Future spec must define exact fallback semantics or continue to hard-fail with explicit stop reasons. |
| No deployment | Blocked | No deployment target, environment, rollout plan, or production safety review is approved. | Future spec must define deployment as out of scope or supply approved deployment gates. |
| No billing | Blocked | No billing, spend guard, invoice, tenant budget, or live accounting path is authorized. | Future spec must define billing as out of scope or supply approved budget and accounting controls. |
| No autonomous merge | Blocked | Self Operator MVP must not autonomously merge branches or bypass human review. | Future spec must require human approval before merge and define merge prevention checks. |
| Local artifact persistence | Risky | Prior schema work is docs-only; no persistence implementation contract is approved. | Future spec must define artifact directory, retention, redaction, manifest shape, immutable run IDs, and cleanup policy. |
| Human approval controls | Risky | Approval fields exist only as candidate docs; no runtime approval enforcement exists. | Future spec must define confirmation prompts, blocking states, approver identity capture, and audit trail requirements. |
| Local run harness | Risky | Local wrappers exist for local orchestration, but Self Operator MVP harness behavior is not specified. | Future spec must define invocation command, inputs, outputs, timeout behavior, stop reasons, exit codes, and no-network expectations. |
| Acceptance test plan | Risky | No Self Operator MVP acceptance suite exists for this readiness matrix. | Future spec must define deterministic tests for local-only behavior, blocked external actions, approvals, artifacts, and stop conditions. |
| Branch pollution risks | Risky | Branch hygiene is procedural, not enforced by this docs packet. | Future spec must define clean-branch checks, allowed path checks, no unrelated changes, and rollback guidance. |
| Evidence-promotion risks | Blocked | Level 3 evidence remains non-promotional and must not be elevated to MVP readiness. | Future spec must define evidence labels, promotion criteria, and explicit non-claims before any readiness claim changes. |
