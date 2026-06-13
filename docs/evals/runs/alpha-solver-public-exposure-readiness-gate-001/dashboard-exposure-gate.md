# Dashboard exposure gate

## Required pass criteria

- Dashboard is disabled by default for public deployments unless explicit non-default credentials and signing secret are configured.
- Passwords/secrets are never default-usable in public exposure mode.
- Sessions are signed, finite-lived, secure-cookie-compatible, and backed by a rotation/custody plan.
- CSRF protection is enforced for state-changing routes.
- Route inventory states exactly which dashboard routes are mounted and which are forbidden.
- Provider-key settings routes are not public unless protected by role/CSRF/session/storage controls.
- Role boundaries separate operator/admin settings from preview/run access.

## Current classification

| Item | Status | Notes |
| --- | --- | --- |
| Service-app dashboard mounting guard | Pass now for current service app only | `service/app.py` mounts login + expert preview only when a non-default password and explicit secret key are set. |
| Shared auth/session machinery | Pass now for implementation existence only | Sessions, CSRF token, lockout, and protected prefixes exist in `alpha/webapp/routes/auth.py`. |
| Default password public safety | Fail now as broader product gate | The shared dashboard auth module still defines a known fallback password, and DEF-002 RR-03 requires hardening. |
| Settings/provider-key route exposure | Fail now | Settings routes manage provider keys and require explicit exposure decision, role boundary, CSRF proof, and hardened secret storage. |
| Role boundary | Unknown / requires implementation | No exposure-grade role model is captured by this packet. |
| Route inventory tests | Unknown / requires implementation | Need tests proving only intended routes are mounted in public mode. |

## Gate result

Dashboard public exposure is not allowed. Current service-app fail-closed mounting is useful but not sufficient for broad dashboard readiness.
