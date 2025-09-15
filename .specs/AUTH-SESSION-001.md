# AUTH-SESSION-001 · Dashboard Login + Session

## Summary
- Adds a password-protected login flow for the dashboard UI.
- Issues signed, secure cookies and CSRF tokens upon successful login.
- Provides middleware enforcing authentication, CSRF validation, and lockout.
- Documents integration steps and covers behaviour with automated tests.

## Acceptance Criteria
- Password gate for dashboard.
- Secure cookie session handling.
- Lockout after five bad attempts (lockout window: five minutes).
- CSRF enforcement on POST routes.
- Test coverage validating success, failure, CSRF enforcement, cookie presence, and logging hygiene.
