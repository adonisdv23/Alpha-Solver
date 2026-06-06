# Failure Classification

## Non-Execution Notice

This scaffold is blocked until a future implementation PR creates a local solver orchestration runner. It is scaffold-only and is not runtime evidence. It does not execute a local LLM, does not call hosted providers, does not import results, and does not close any track.

## Future Failure Taxonomy

Use exactly these classifications unless a future spec explicitly updates the taxonomy:

| Classification | Meaning |
| --- | --- |
| `implementation missing` | The local solver orchestration runner does not exist. |
| `config missing` | Required future local-only configuration is absent. |
| `endpoint not local` | The endpoint is not local-only or cannot be summarized as local. |
| `model unavailable` | The configured local model cannot be loaded or reached. |
| `timeout` | The future smoke exceeds the configured timeout. |
| `malformed response` | The runner returns an unparsable or schema-incompatible response. |
| `empty output` | The runner returns no usable output. |
| `prompt echo` | The output repeats the user prompt in a way that violates the echo guard. |
| `system echo` | The output exposes hidden, system, developer, or orchestration instructions. |
| `pass-one parse failure` | The first local expert pass cannot produce a usable parse or mode selection. |
| `pass-two answer failure` | The second local expert pass cannot produce a usable final answer. |
| `confidence unavailable` | Confidence is missing or not inspectable. |
| `incorrect mode selection` | The selected mode does not match the expected prompt behavior. |
| `hosted fallback detected` | Any hosted provider fallback is observed. |
| `provider key unexpectedly required` | The runner requires a provider key despite local-only constraints. |
| `artifact capture incomplete` | Required redacted artifacts are missing or incomplete. |

## Boundary

A failure classification is not a readiness claim. It is only a future smoke observation label.
