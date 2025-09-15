# Secrets Redaction

Alpha Solver automatically redacts sensitive data from logs and tracing spans.
The redactor masks common secrets before they are emitted or exported.

## Patterns & Masks

| Type | Pattern | Mask |
|------|---------|------|
| Authorization headers | `Authorization: Bearer <token>` | `Bearer ***REDACTED***` |
| API keys / tokens | `sk-…`, `xoxb-…`, 32-64 char base64/hex strings | `***REDACTED***` |
| Emails | user@host.tld | `u***@h***.tld` |
| Phones | E.164 / US formats | `+*-***-***-1234` |

Inputs may be raw strings or nested dictionaries. The redactor returns a
copy, leaving original objects untouched.

## Performance

Regular expressions are compiled and a fast path avoids scanning strings that
clearly contain no secrets. Benchmarks show an average overhead of less than
1 ms per call across 1,000 mixed events.

## Extending

Patterns and toggles live in `service/config/redaction.yaml`. Add new detectors
carefully – keep regexes fast and ensure masks preserve token shape for
debugging.
