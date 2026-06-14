# Redaction Test Evidence

## Tests added or expanded

- `tests/test_secrets_redaction.py::test_prompt_provider_billing_and_user_sensitive_keys_are_redacted`
  - Covers prompt-like keys, chat messages, provider response-like keys, provider API key names, authorization-bearing structures, billing-like fields, and user-provided email/phone-sensitive strings.
- `tests/test_observability.py::test_jsonl_logger_redacts_prompt_provider_secret_and_billing_like_fields`
  - Covers default JSONL observability payload and metadata redaction for raw prompt markers, provider response markers, provider keys, authorization values, billing-like values, and preservation of safe numeric/correlation metadata.

## Expected proof

The tests prove the narrow lane that default redaction and JSONL logging do not preserve raw prompt markers, raw provider response markers, provider key values, bearer token values, billing-like card strings, or user-provided email markers when those values are submitted under sensitive field names.

## Non-proof

These tests do not prove full security/privacy completion, provider readiness, third-party retention behavior, public exposure readiness, or correctness of every possible future logging sink.
