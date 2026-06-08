# Dependency Matrix

| Dependency | Depends on | Unlocks only after closure | Current disposition |
| --- | --- | --- | --- |
| Local-only execution boundary | Approved future implementation spec and explicit no-provider/no-browser/no-credential rules. | Local Self Operator run harness design. | Not closed. |
| Provider-call prohibition | Static guardrails, tests, and documentation that hosted providers are out of scope. | Confidence that local runs cannot silently become hosted runs. | Must remain blocked. |
| Browser-automation prohibition | Explicit browser automation non-goals or a separately approved automation spec. | Confidence that Self Operator MVP cannot control external sites. | Must remain blocked. |
| Credential-free operation | Redaction policy, environment validation, and no-secret fixtures. | Safe local runs without API keys or browser/deployment credentials. | Not closed. |
| Fallback prohibition | SAFE-OUT/failure semantics and stop reasons. | Deterministic failure handling without hidden hosted/provider/local fallback. | Must remain blocked unless separately specified. |
| Deployment prohibition | Release target decision and production-readiness review. | Any deployment planning. | Must remain blocked. |
| Billing prohibition | Billing/spend guard spec and no-live-accounting test plan. | Any billing or tenant accounting work. | Must remain blocked. |
| Human approval controls | Approval schema, prompt contract, stop-state rules, and audit logging. | Any operator-mediated action flow. | Not closed. |
| Local artifact persistence | Artifact schema, retention, redaction, path policy, and integrity checks. | Durable run records and reviewable outputs. | Not closed. |
| Local run harness | Command contract, no-network expectation, finite timeout, exit codes, and fixture data. | Acceptance tests and operator dry runs. | Not closed. |
| Acceptance test plan | Harness contract, blocked-action tests, artifact checks, approval checks, and changed-file scope checks. | Implementation readiness claim for local-only MVP. | Not closed. |
| Branch pollution controls | Git status policy, path allowlist, unrelated-change detection, and manual review. | Safe implementation branch preparation. | Not closed. |
| Evidence-promotion controls | Evidence labels, non-claims, source-artifact rules, and acceptance thresholds. | Any future readiness or promotion decision. | Not closed. |

## Ordering constraints

1. Evidence-promotion controls must be closed before any readiness label can change.
2. Local-only execution, credential-free operation, fallback prohibition, and external-action prohibitions must be closed before the local run harness can be implemented.
3. The local run harness and artifact persistence contracts must be closed before acceptance tests can be meaningful.
4. Human approval controls must be closed before any operator-mediated action can run.
5. Branch pollution controls must be closed before an implementation lane can safely begin.
