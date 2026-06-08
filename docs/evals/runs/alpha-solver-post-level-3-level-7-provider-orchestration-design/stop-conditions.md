# Stop Conditions

Future work must stop and use the blocker fallback lane or a separately approved fix lane if any of the following occur:

- accepted Level 6 product-surface design is missing or contradicted;
- this Level 7 packet is not accepted before Level 8 review is attempted;
- runtime code changes are proposed without a narrow implementation lane;
- provider routing would be enabled implicitly;
- fallback or hosted fallback would be enabled implicitly;
- credentials, tokens, secrets, or environment values would be exposed;
- provider calls, local model inference, hosted model inference, Ollama runs, or benchmarks are required to complete a docs-only lane;
- timeout, retry, circuit-breaker, budget, quota, or fail-closed requirements are undefined;
- provenance or observability would include raw prompts, raw provider payloads, raw exception dumps, or secrets;
- safety gates are missing, bypassed, or ambiguous;
- evidence from Level 2, Level 3, Level 4, Level 5, Level 6, or this packet would be promoted beyond its accepted boundary.
