# Billing and cost boundary checklist

The operator must manually verify billing/cost readiness before any real OpenAI token smoke. Do not record private payment details.

| Requirement | Status | Recording boundary |
|---|---|---|
| Positive API balance. | `pending_operator_verification` | Record only yes/no or redacted attestation. |
| Billing method active if required. | `pending_operator_verification` | Do not record card, bank, invoice, address, tax, or account numbers. |
| Spending limits if available. | `pending_operator_verification` | Record only limit category or redacted cap. |
| Daily smoke budget selected. | `pending_operator_verification` | Record a non-sensitive cap such as maximum dollars/tokens. |
| Hard stop if any unexpected billing occurs. | `pending_operator_verification` | Operator attestation. |

If billing or cost scope is unclear, the next verdict must be `BLOCKED_PROJECT_OR_BILLING_SCOPE_UNCLEAR`, not a token-smoke lane.
