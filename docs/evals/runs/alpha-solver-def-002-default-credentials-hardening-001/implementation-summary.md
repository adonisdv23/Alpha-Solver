# Implementation summary

## Default credential paths identified

- `alpha.core.config.ServiceAuthConfig` previously loaded `SERVICE_AUTH_KEYS`,
  then `API_KEY`, then a built-in API-key fallback. The fallback was removed so
  an absent key list remains empty while API auth is still enabled.
- `alpha.webapp.routes.auth` previously accepted the historical dashboard
  fallback password when `ALPHA_DASHBOARD_PASSWORD` was unset. The fallback is
  now retained only as a denied sentinel.
- `service.app` already guarded bundled dashboard mounting on non-default
  dashboard password plus explicit signing secret. It now delegates password
  validity to the shared dashboard auth helper.
- `service/config/api_keys.yaml` no longer contains an active placeholder key.

## Runtime behavior changed

- Missing service API keys fail closed for protected API auth.
- The known `dev-secret` API-key fallback is no longer configured implicitly.
- Missing or default dashboard password values cannot authenticate even if a
  caller manually mounts the shared dashboard router.
- The bundled API-key YAML contains only a revoked synthetic placeholder.
