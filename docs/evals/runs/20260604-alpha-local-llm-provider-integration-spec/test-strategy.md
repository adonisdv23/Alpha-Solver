# Test Strategy

## Required order

Future tests must be developed in this order:

1. offline unit tests using injected fakes or pure functions;
2. fixture parser tests using static Ollama-style payloads;
3. opt-in local smoke tests only after separate authorization;
4. no provider or network dependency in default test runs.

## Default-skip smoke behavior

Any future smoke test must be skipped by default. It must require an explicit
operator-controlled flag, an approved localhost endpoint, and a bounded timeout.
It must not run as part of the default `python -m pytest -q` command.

## Failure cases to cover

Offline and fixture tests should cover timeout normalization, connection failure,
malformed response, empty output, prompt echo, missing contract, empty contract,
fingerprint mismatch, and backend errors. Each failure must produce a
failed-closed result with non-upgraded evidence labels.
