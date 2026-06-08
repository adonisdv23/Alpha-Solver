# Proposed Test Files

## Proposed directory

Future implementation should add tests under a dedicated static-test location such as `tests/static/self_operator/` or an equivalent repo-approved test directory.

This packet does not create those files.

## Proposed files

| Proposed file | Purpose | Primary expected output |
|---|---|---|
| `test_self_operator_no_provider_calls_static.py` | Detect hosted provider SDK imports, provider endpoint strings, and provider client construction. | Fails with `SELF_OPERATOR_PROVIDER_CALL_BLOCKED` for any provider call surface. |
| `test_self_operator_no_external_api_static.py` | Detect generic outbound HTTP clients, webhooks, sockets, and service URLs outside approved local-only boundaries. | Fails with `SELF_OPERATOR_EXTERNAL_API_BLOCKED`. |
| `test_self_operator_no_credentials_static.py` | Detect secrets, token reads, credential env var access, and credential persistence. | Fails with `SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED`. |
| `test_self_operator_no_browser_automation_static.py` | Detect Playwright, Selenium, Puppeteer, browser driver, and CDP usage. | Fails with `SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED`. |
| `test_self_operator_no_deploy_billing_routes_static.py` | Detect deployment commands, billing/account APIs, and public route registration. | Fails with deploy, billing, or route exposure finding IDs. |
| `test_self_operator_no_fallback_static.py` | Detect fallback configuration, fallback-enabling code, local-to-provider fallback paths, and hosted fallback paths. | Fails with `SELF_OPERATOR_FALLBACK_BLOCKED` or `SELF_OPERATOR_HOSTED_FALLBACK_BLOCKED`. |
| `test_self_operator_no_evidence_promotion_static.py` | Detect evidence-promotion, readiness-promotion, benchmark-promotion, and score-promotion labels. | Fails with `SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED`. |
| `test_self_operator_approval_gate_static.py` | Verify every planned side-effect operation requires explicit approval metadata before execution. | Fails with `SELF_OPERATOR_APPROVAL_GATE_REQUIRED`. |
| `test_self_operator_artifact_schema_static.py` | Verify required artifact fields, redaction fields, and persistence locations are defined. | Fails with `SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE`. |
| `test_self_operator_stop_state_static.py` | Verify stop states are explicit, persisted, terminal, and non-promotional. | Fails with `SELF_OPERATOR_STOP_STATE_REQUIRED`. |

## Shared helper files

| Proposed helper | Purpose |
|---|---|
| `static_scan.py` | Shared deterministic scanner for source text, AST nodes, configuration text, and fixture directories. |
| `finding_schema.py` | Shared finding schema with `id`, `path`, `line`, `severity`, `blocked_behavior`, and `message`. |
| `fixtures.py` | Fixture loader that never imports fixture files as executable modules. |

## Minimum test behavior

- Tests should inspect text or AST only.
- Tests should not import target runtime modules if import side effects could trigger providers, fallback paths, promotion labeling, routes, deployments, billing, or browser startup.
- Tests should report all findings in a stable order.
- Tests should include positive blocked fixtures and negative safe fixtures.
