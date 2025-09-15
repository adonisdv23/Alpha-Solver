# API Key Management

The service supports API keys for authenticating requests. Keys are stored as
salted SHA256 hashes in `service/config/api_keys.yaml`:

```yaml
keys:
  - id: example
    hash: abc123$<sha256>
    tenant_id: tenant1
    scopes: [read, write]
    status: active
    created_at: 1700000000
```

Use `service.auth.api_keys.hash_key()` to generate the `salt$hash` value when
creating new keys. Raw keys are never stored on disk.

Each key is bound to a tenant and a list of scopes. The middleware attaches the
resolved principal to `request.state.principal` and enforces required scopes for
protected routes.

To rotate or revoke keys update the YAML file and reload the service. Changing a
key's `status` to `revoked` or `disabled` immediately prevents further use.

Example request:

```bash
curl -H "X-API-Key: <key>" https://example/api/protected
```

JWTs are also supported via the `Authorization: Bearer` header. If both headers
are present the JWT is preferred.
