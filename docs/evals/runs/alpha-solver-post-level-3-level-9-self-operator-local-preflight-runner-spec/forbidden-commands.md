# Forbidden commands

A future preflight runner must block commands involving:

- Network calls.
- Provider calls.
- Credentials or secret access.
- Browser automation.
- Deployment.
- Billing.
- Package installation.
- Remote fetch.
- Route exposure, including `/v1/solve` or dashboard exposure.
- Hosted fallback.
- Source-artifact mutation.
- Evidence promotion.
