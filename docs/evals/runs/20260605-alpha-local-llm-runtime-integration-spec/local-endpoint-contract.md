# Local Endpoint Contract

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Allowed endpoint boundary

Local LLM mode may call only localhost or loopback endpoints. The acceptable host boundary must be limited to local machine targets such as:

- `localhost`
- `127.0.0.1`
- `::1`

A future implementation may include additional loopback addresses only if they are parsed deterministically as loopback by standard IP parsing.

## Required URL behavior

A future implementation must parse the endpoint before use and must reject endpoints that are malformed, ambiguous, remote, hosted, or non-local.

The implementation must fail closed for:

- missing scheme;
- unsupported scheme;
- missing host;
- malformed host;
- non-local host;
- userinfo-bearing URLs;
- values that cannot be parsed deterministically.

## Scheme requirement

The future implementation should require `http` for loopback local service calls unless a later lane explicitly authorizes additional local-only schemes. Hosted `https` endpoints must not be accepted as local LLM endpoints.

## No network expansion

The endpoint contract does not authorize calls to LAN, private-network, public-network, hosted-provider, or proxy endpoints.
