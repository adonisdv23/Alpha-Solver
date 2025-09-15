# Dashboard Authentication & Session Management

The dashboard UI is protected by a lightweight password gate that issues
signed cookies and CSRF tokens when the user successfully authenticates.
This document explains how to configure the feature and integrate it with
custom FastAPI applications.

## Features

- Password-protected login screen at `/login`.
- Secure, signed session cookie (`alpha_dashboard_session`) marked as
  `HttpOnly`, `Secure`, and `SameSite=Strict`.
- Per-session CSRF token exposed via the `alpha_dashboard_csrf` cookie.
- Middleware that enforces authenticated access to dashboard routes and
  rejects state-changing requests without a valid CSRF token.
- Lockout after five consecutive failed password attempts (default lockout
  window is five minutes).

## Configuration

| Environment variable | Description | Default |
| -------------------- | ----------- | ------- |
| `ALPHA_DASHBOARD_PASSWORD` | Password required to sign in. | `alpha-dashboard` |
| `ALPHA_DASHBOARD_SECRET_KEY` | Secret used to sign session cookies. | Randomly generated at runtime |
| `ALPHA_DASHBOARD_SECRETS_PATH` | Storage path for provider credentials (used by the settings UI). | `~/.alpha_solver/dashboard_api_keys.json` |
| `ALPHA_DASHBOARD_AUDIT_LOG` | Path of the audit log file for settings changes. | `~/.alpha_solver/dashboard_audit.log` |

Set the password and secret key in the environment before starting the
application to ensure deterministic behaviour across restarts. The secret key
must remain private because it signs session cookies.

## Using the Router and Middleware

```python
from fastapi import FastAPI

from alpha.webapp.routes import auth, requests, settings

app = FastAPI()
auth.install_dashboard_security(app)
app.include_router(auth.router)
app.include_router(requests.router)
app.include_router(settings.router)
```

The middleware installed by `install_dashboard_security` intercepts all
requests whose path begins with `/requests`, `/settings`, or `/run`. Unauthenticated
clients receive a redirect to `/login`. POST/PUT/PATCH/DELETE requests to these
paths also require the `X-Alpha-CSRF` header to match the CSRF token stored in
the cookie.

## Obtaining the CSRF Token

The CSRF token for the current session is exposed via the
`alpha_dashboard_csrf` cookie. Browser-based clients should read this cookie and
send its value in the `X-Alpha-CSRF` header for all state-changing requests.

Example using Fetch:

```javascript
const csrfToken = getCookie('alpha_dashboard_csrf');
fetch('/settings/keys', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Alpha-CSRF': csrfToken,
  },
  body: JSON.stringify({ provider: 'openai', key: 'sk-demo' })
});
```

## Handling Logout

Calling `GET /logout` clears the session and CSRF cookies on the client and
invalidates the server-side session state. Subsequent dashboard requests will be
redirected back to `/login`.

## Lockout Behaviour

Failed password attempts are tracked per client address. After five incorrect
submissions, the login form returns HTTP 429 for five minutes to slow brute-force
attempts. A successful login immediately clears the failure counter.

## Testing Utilities

The `alpha.webapp.routes.auth.reset_state()` helper clears in-memory sessions and
failed login counters. Tests should call this function before interacting with
authentication-sensitive routes to keep suites hermetic.
