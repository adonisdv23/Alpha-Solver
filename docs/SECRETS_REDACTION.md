# Secrets Redaction

Alpha Solver masks common secrets before they reach logs or telemetry. The
`service.logging.redactor` module scans strings and mapping values for several
patterns and replaces sensitive data with minimal shapes.

## Patterns and Masks

| Pattern                | Example Input                              | Redacted Output                       |
|------------------------|--------------------------------------------|---------------------------------------|
| Authorization header   | `Authorization: Bearer abc123`             | `Authorization: Bearer ***REDACTED***`|
| API keys               | `sk-ABC...`, `xoxb-123...`                 | `***REDACTED***`                      |
| Generic tokens         | `A1B2...` (32-64 chars)                    | `***REDACTED***`                      |
| Emails                 | `alice@example.com`                        | `a***@e***.com`                       |
| Phone numbers          | `+1-415-555-2671`                          | `+*-***-***-2671`                     |

Configuration lives in `service/config/redaction.yaml` where detectors can be
enabled/disabled and keys allow‑listed.

## Logging and Spans

A logging `Filter` applies redaction to both message strings and structured
`extra` payloads before emitting. The OpenTelemetry helper cleans span attributes
and drops obviously sensitive keys such as `prompt`, `token` or `password`.

Redaction happens on copies, so caller objects are never mutated. Any errors are
counted via `alpha_redaction_errors_total` while successful masks increment
`alpha_redaction_applied_total{type}`.

## Performance

All patterns are compiled and a fast pre‑check avoids regex work when no secrets
are present. The test suite exercises 1,000 mixed events and observes an average
redaction overhead below 1 ms per log call.

## Extending

To add new patterns, update `service/logging/redactor.py` and consider tests to
prove the behaviour. Keep regexes simple and anchored to avoid excessive
backtracking.
