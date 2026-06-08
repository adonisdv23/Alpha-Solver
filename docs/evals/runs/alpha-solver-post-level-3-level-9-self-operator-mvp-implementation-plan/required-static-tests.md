# Required static tests

Before any future runtime wrapper or CLI behavior, the next code lane must provide static tests that detect prohibited behavior including:

- provider calls and hosted model calls;
- external API calls;
- credential or secret access;
- browser automation;
- deployment and billing behavior;
- `/v1/solve` or dashboard route exposure;
- fallback and hosted fallback;
- evidence promotion and source-artifact mutation;
- missing operator approval, raw artifact, reviewer-note, or stop-state records.

The tests must be deterministic, local-only, offline, and incapable of starting models or services.
