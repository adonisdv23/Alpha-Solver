# Abuse Cases

The abuse cases below are for future product-surface threat modeling only. They do not describe implemented routes or currently authorized product behavior.

## Prompt and content abuse cases

- A user submits prompt-injection text intended to override solver policies, exfiltrate hidden context, or induce unsafe tool use.
- A user submits private third-party data and later expects deletion or non-retention guarantees that have not been implemented.
- A user uses generated output for high-impact decisions while believing the product has validated quality, benchmark, or safety claims.
- A user requests illegal, harmful, privacy-invasive, or deceptive content through a future public route.

## Access and route abuse cases

- An attacker enumerates route exposure for `/v1/solve`, dashboard endpoints, health endpoints, or debug endpoints.
- An unauthenticated actor submits high-volume requests to cause resource exhaustion or billing spend.
- A user tampers with request parameters to bypass route, provider, fallback, budget, or local-only constraints.
- A stale client calls a route after a future product-surface decision changes allowed behavior.

## Evidence and claim abuse cases

- A reviewer promotes local orchestration evidence as product readiness evidence.
- A dashboard screenshot or packet excerpt is reused as proof of quality, production readiness, or benchmark superiority.
- A future artifact omits caveats and creates unsupported claims about accuracy, latency, cost, reliability, privacy, or safety.

## Provider and fallback abuse cases

- An operator believes local-only execution is active while a hosted provider or fallback path is used.
- A fallback path silently changes model behavior, billing exposure, or data residency.
- A provider failure is hidden behind fallback output, making incident review and user disclosure difficult.
