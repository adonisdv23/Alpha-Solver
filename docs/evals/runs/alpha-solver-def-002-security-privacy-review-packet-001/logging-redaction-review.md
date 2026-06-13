# Logging and redaction review

Covers: structured logging, deterministic redaction, and provider telemetry
prompt-content risk.

## Structured request logging

- The service uses a JSON formatter (`JsonFormatter`, `service/app.py:76-89`) and
  configures `logging.basicConfig(level=logging.INFO, ...)`, routing
  `uvicorn.access` through the same handler.
- The per-request log record (`service/app.py:901-909`) emits **request metadata
  only** — `request_id`, `path`, `client` host, `duration_ms`, and `strategy`. It
  does **not** log the raw `query`/prompt or provider payloads.
- On error, `logger.exception("request error", extra={"request_id": req_id})`
  (`service/app.py:894`) records the request id without echoing user content,
  and the response path calls `record_safe_out(...)` so failures degrade to a
  SAFE-OUT rather than leaking internals.

**Observation:** Default request logging is metric-oriented and does not persist
prompt content. No raw-prompt logging gap was found on the request path.

## Deterministic redaction (Self Operator artifacts)

`alpha/self_operator/redaction.py` provides deterministic, **local** redaction:

- `SECRET_KEYWORDS` covers `api_key`, `apikey`, `token`, `secret`, `password`,
  `credential(s)` (line 9).
- `_SECRET_ASSIGNMENT_RE` redacts `key = value` style secret assignments; a
  `_BEARER_RE` redacts `Bearer <token>` (8+ chars); `_PLACEHOLDER_SECRET_RE`
  collapses `fake/placeholder/example` secret markers.
- `redact_value` recursively redacts mappings/lists/tuples, replacing values for
  secret-named keys with `REDACTION_TEXT = "[REDACTED_SELF_OPERATOR_SECRET]"`
  and redacting string values in place. `contains_secret_marker` lets callers
  detect secret-like content before emission.

**Observation:** Redaction is deterministic and offline (regex-based, no network,
no model). It is keyword/pattern driven, so novel secret formats not matching the
keyword/regex set could pass through — a known limitation of pattern redaction
(noted in `accepted-residual-risks.md`, RR-A1).

## Provider telemetry prompt-content risk

`alpha/providers/telemetry.py` is **allowlist-based** by construction:

- `_ALLOWED_FIELDS` (lines 23-44) is an explicit set of safe metadata:
  `event`, `provider`, `model`, `model_set`, `route`, `request_id`, `status`,
  `tenant`, `retry_count`, `latency_ms`, token counts, `estimated_cost_usd`,
  `cost_source`, `finish_reason`, `error_category`, `retryable`, `status_code`,
  `safe_message`, `provider_request_id`. **No prompt/response content field
  exists.**
- `build_provider_event` constructs an event from explicit safe keyword args
  only and drops `None` values; `emit_provider_event` re-filters through
  `_ALLOWED_FIELDS` before logging/sinking. The module docstring states it
  "never inspects provider request/response payloads, exception objects,
  dataclass `__dict__` values, or raw provider metadata."

**Observation:** Provider telemetry cannot carry prompt or completion content
because no content field is in the allowlist and the emitter re-filters. This is
a strong control against telemetry prompt-content leakage.

## Provider SAFE-OUT (failure path)

`alpha/providers/safeout.py` is similarly allowlist-built. The SAFE-OUT body is
constructed from **safe `ProviderError` fields only** — `provider`, `category`,
`retryable`, `request_id`, `retry_count`, `status_code`, and `safe_message`
(`build_provider_safe_out_body`, lines 37-52). Its docstring states it "never
inspects raw provider payloads, raw metadata, environment/config dumps, or
exception objects beyond the normalized `ProviderError` safe fields."

**Observation:** The provider failure path does not leak raw provider error
bodies, stack traces, or environment/config dumps to the client.

## Summary

Logging and redaction controls are a relative strength of the codebase:

- request logs carry metrics, not prompt content;
- provider telemetry and SAFE-OUT are allowlist-built and content-free;
- Self Operator artifacts get deterministic offline secret redaction.

The only residual is the inherent limitation of pattern-based redaction (RR-A1),
proposed for residual-risk acceptance rather than gap closure.
