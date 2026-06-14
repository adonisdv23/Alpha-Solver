# Telemetry Inventory

## Sensitive or prompt-bearing field families

The following field families can contain user or provider-sensitive data and must be omitted, hashed, summarized, or redacted before default logging/evidence capture:

| Family | Examples | Boundary |
| --- | --- | --- |
| User prompt/input | `prompt`, `query`, `query_text`, `raw_prompt`, `user_input`, `input_text`, chat `messages` | Redact from default logs; provider transmission only after explicit provider opt-in. |
| Provider response/output | raw completion text, `provider_response`, provider response bodies, raw metadata dumps | Do not place in provider telemetry; redact from default structured logs. |
| Request/trace payloads | raw request body, raw headers, cookies, route trace payloads, replay payloads | Allowlist metadata only; redact sensitive keys and secret-like values. |
| Provider secrets | `OPENAI_API_KEY`, API keys, bearer tokens, authorization headers, provider credentials | Never log; redacted by key/value detectors. |
| Billing/account data | billing account labels, payment/card-like values, invoices, cost-account metadata | Keep numeric usage/cost fields only where intentionally allowlisted; redact billing-like free text. |
| User PII | email, phone, account identifiers, user-provided sensitive strings | Redact value patterns and prompt-like fields. |

## Allowlisted provider telemetry fields

`alpha/providers/telemetry.py` emits only explicit provider lifecycle metadata: event name, provider/model identifiers, model set, route, request id, status, tenant, retry count, latency, token counts, estimated cost, cost source, finish reason, coarse error category, retryability, HTTP status code, safe message, and provider request id. Prompt, response, headers, raw metadata, request bodies, and exception dumps are not allowlisted.

## Default logging boundary

`service/logging/redactor.py` now redacts sensitive field names for prompt-like content, raw payloads, provider secrets, billing-like data, and user-provided sensitive inputs. `service/observability/logger.py` applies that redactor to default JSONL payload and metadata fields, while keeping route explanation allowlisting intact.

## Opt-in verbose/debug boundary

Existing telemetry scrub behavior remains opt-in through `ALPHA_TELEMETRY_SCRUB=1` for the legacy telemetry tools. This lane does not enable verbose prompt capture, does not add debug prompt logging, and does not alter provider enablement gates. Operators must treat any future verbose/debug telemetry that includes prompt or provider payload text as a separate approval lane with retention, access, and disclosure controls.
