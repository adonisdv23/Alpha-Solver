# Local Orchestration Envelope Expected Fields

## Non-Execution Notice

This scaffold is blocked until a future implementation PR creates a local solver orchestration runner. It is scaffold-only and is not runtime evidence. It does not execute a local LLM, does not call hosted providers, does not import results, and does not close any track.

## Expected Fields for Future Smoke Output

Future smoke output should expose or preserve the following fields for inspection:

| Field | Expected future value or constraint |
| --- | --- |
| `provider_mode` | `local_llm` |
| `orchestration_mode` | Future implementation-defined local orchestration mode. |
| `strategy` | Future implementation-defined strategy. |
| `pass_count` | Number of local expert passes completed. |
| `mode` | One of `direct`, `clarify`, `answer_with_assumptions`, or `block`. |
| `considerations` | Structured or inspectable reasoning considerations suitable for artifact review without exposing secrets. |
| `assumptions` | Explicit assumptions, especially for `answer_with_assumptions`. |
| `confidence` | Available confidence value or confidence descriptor. |
| `final_answer` | Final user-facing answer. |
| `behavior_evidence` | `false` for this scaffold; future runtime evidence must be captured separately. |
| `no_hosted_fallback` | `true`. |
| `no_provider_keys_required` | `true`. |
| `local_endpoint_summary` | Redacted local endpoint summary only, not a private URL. |
| `model` | Local model identifier used by the future runner. |
| `timeout` | Timeout configured for the future run. |

## Field Boundary

These fields define expected future smoke observations. Their presence in this document is not evidence that any runner exists, that any local model was called, or that any behavior was validated.
