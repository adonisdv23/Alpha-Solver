# Data-sharing settings checklist

Operator must manually verify these items before any real OpenAI token smoke. Default status is `pending_operator_verification`.

| Item | Status | Evidence allowed in this packet |
|---|---|---|
| OpenAI API data-sharing settings are intentionally configured for the selected project. | `pending_operator_verification` | Redacted screenshot or explicit operator attestation. |
| The selected project is dedicated to Alpha Solver smoke/eval work. | `pending_operator_verification` | Redacted project identifier or operator attestation. |
| Inputs/outputs sharing scope is understood. | `pending_operator_verification` | Operator attestation. |
| Eval/fine-tuning data-sharing scope is understood. | `pending_operator_verification` | Operator attestation. |
| Model feedback sharing scope is understood. | `pending_operator_verification` | Operator attestation. |
| Operator understands no secrets or sensitive evidence may be sent. | `pending_operator_verification` | Operator attestation. |
| Operator understands only synthetic or sanitized prompts may be used. | `pending_operator_verification` | Operator attestation. |

This packet does not claim these settings are currently correct.
