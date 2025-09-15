# OAuth & Secrets Scaffold

This document describes how the simulated OAuth token system and secret
store are configured for tests.  It is **not** a real authentication system.

## Configuration

Providers are declared in `service/config/oauth_providers.yaml` and include
allowed scopes, cache settings and prefetch jitter used for background
refresh.  Secrets for tenants live in `service/config/secrets.example.yaml`.
Each entry is versioned so rotation can occur without downtime.

## Rotation

To rotate a secret create a new version with `SecretStore.set` and deploy the
updated file.  The previous version is retained and can be restored with
`SecretStore.rollback` if needed.

## Safety

No secrets are logged by the token provider, OAuth client or middleware.
Tests scan logs to ensure that client secrets and refresh tokens are absent.

This scaffold is intentionally simple and intended for unit tests only.
