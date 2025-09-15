# JWT Service-to-Service Authentication

Alpha Solver exposes optional JWT based authentication for service-to-service
calls. Requests must include an `Authorization: Bearer <token>` header where the
JWT is signed using an allowed algorithm (`RS256`). Tokens must contain a `kid`
header that maps to a public key in `service/config/auth_keys.yaml`.

## Validation Rules
- Only algorithms in the allowlist (`RS256`) are accepted.
- `exp` and `nbf` claims are enforced with a small clock skew (60s).
- Optional `aud` and `iss` claims are validated when provided to the middleware.
- `kid` is required and looked up in-memory; the underlying YAML file is
  reloaded automatically when it changes to support key rotation without
  downtime.

On success the middleware attaches `request.state.principal` with the `sub`,
`tenant_id`, and `roles` fields from the token payload.

## Error Codes
Failure responses return HTTP 401 with a JSON body:

| code             | meaning                    |
|------------------|----------------------------|
| missing_token    | Authorization header absent|
| invalid_header   | malformed token header     |
| invalid_alg      | unsupported signing alg    |
| missing_kid      | `kid` header missing       |
| unknown_kid      | key id not found           |
| token_expired    | `exp` claim has passed     |
| token_not_yet_valid | `nbf` claim in future  |
| invalid_token    | signature or claim error   |

The middleware never logs full tokens or secrets; only failure codes.

## Key Rotation
Update `service/config/auth_keys.yaml` with new `kid` entries. The middleware
reloads the file when it changes, allowing old and new keys to be used during
rotation.

## Sample Request
```
curl -H "Authorization: Bearer <JWT>" https://solver.example.com/protected
```
