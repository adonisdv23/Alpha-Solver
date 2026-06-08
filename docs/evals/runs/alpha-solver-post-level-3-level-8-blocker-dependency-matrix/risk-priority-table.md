# Risk Priority Table

| Priority | Risk | Severity | Likelihood | Why it matters | Mitigation required |
| --- | --- | --- | --- | --- | --- |
| P0 | Evidence-promotion overclaim | High | Medium | Local, non-promotional evidence could be misread as Self Operator MVP readiness. | Preserve explicit non-claims and require future promotion criteria. |
| P0 | Unauthorized provider call | High | Medium | Hosted calls may expose secrets, incur cost, and invalidate local-only evidence. | Add no-provider guardrails and deterministic tests before implementation. |
| P0 | Autonomous merge or review bypass | High | Medium | Self Operator MVP could change repository state without human approval. | Require human approval gate and merge-prevention checks. |
| P0 | Credential capture or leakage | High | Medium | Browser/provider/deployment secrets could be stored in artifacts or logs. | Define credential-free operation or approved secret-handling policy. |
| P1 | Browser automation escape | High | Low-to-Medium | External browser automation could affect third-party systems. | Keep browser automation blocked unless explicitly specified with sandbox and consent. |
| P1 | Hidden fallback path | Medium-to-High | Medium | Fallback could mask failures and create unsupported readiness claims. | Require explicit no-fallback assertions and tests. |
| P1 | Local artifact persistence ambiguity | Medium | High | Missing path, retention, and redaction rules can create unreproducible or unsafe artifacts. | Define artifact manifest, retention, redaction, and integrity rules. |
| P1 | Acceptance test gap | Medium | High | Implementation could proceed without proving blocked external actions and approvals. | Define focused acceptance tests before implementation. |
| P2 | Branch pollution | Medium | Medium | Unrelated changes may be mixed into readiness work. | Enforce changed-file scope and clean-branch checks. |
| P2 | Billing boundary confusion | Medium | Low-to-Medium | Accounting or billing claims could be inferred without live billing controls. | Preserve no-billing non-action and require a future billing spec. |
| P2 | Deployment boundary confusion | Medium | Low-to-Medium | Docs could be mistaken for deployment readiness. | Preserve no-deployment non-action and require release gates. |
