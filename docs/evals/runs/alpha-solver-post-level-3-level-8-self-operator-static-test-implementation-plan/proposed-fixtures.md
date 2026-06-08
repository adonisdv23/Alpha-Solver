# Proposed Fixtures

## Fixture principles

Fixtures should be inert text files or data files. They must not contain real credentials, executable deployment targets, real endpoints, or commands intended to be run.

## Proposed fixture layout

| Fixture path | Purpose | Expected result |
|---|---|---|
| `fixtures/self_operator/safe/minimal_plan.py.txt` | Allowed local-only plan with no side effects. | No findings. |
| `fixtures/self_operator/safe/approval_required_adapter.py.txt` | Allowed adapter shape that requires approval before action. | No findings. |
| `fixtures/self_operator/blocked/provider_openai_call.py.txt` | Contains hosted provider SDK import and client call. | Provider-call finding. |
| `fixtures/self_operator/blocked/external_requests_call.py.txt` | Contains outbound HTTP request to an external URL. | External-API finding. |
| `fixtures/self_operator/blocked/credential_env_read.py.txt` | Reads token-like environment variables. | Credential finding. |
| `fixtures/self_operator/blocked/browser_playwright.py.txt` | Imports browser automation and launches a browser. | Browser automation finding. |
| `fixtures/self_operator/blocked/deploy_command.py.txt` | Contains deployment command construction. | Deployment finding. |
| `fixtures/self_operator/blocked/billing_api.py.txt` | Contains billing or account-management API call pattern. | Billing finding. |
| `fixtures/self_operator/blocked/route_registration.py.txt` | Registers a public route for Self Operator behavior. | Route exposure finding. |
| `fixtures/self_operator/blocked/missing_approval.py.txt` | Performs a side-effect operation without approval metadata. | Approval-gate finding. |
| `fixtures/self_operator/blocked/missing_artifact_persistence.py.txt` | Emits output without persisting required artifacts. | Artifact persistence finding. |
| `fixtures/self_operator/blocked/non_terminal_stop_state.py.txt` | Continues after a stop state. | Stop-state finding. |

## Fixture safety requirements

- Use `.txt` suffixes for code-like fixtures unless a future test harness proves fixture imports cannot execute.
- Replace secrets with dummy markers such as `DUMMY_TOKEN_DO_NOT_USE`.
- Replace external domains with reserved examples such as `https://example.invalid`.
- Include line-specific patterns so expected findings can assert stable line numbers.
