# Credential, browser, deployment, and billing gates

Static tests must fail with:

- `SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED` for secret, token, key, auth, or environment credential access.
- `SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED` for Playwright, Selenium, browser-driving, or headless automation.
- `SELF_OPERATOR_DEPLOYMENT_BLOCKED` for deployment, release, hosting, infrastructure, or remote environment commands.
- `SELF_OPERATOR_BILLING_BLOCKED` for billing, metering, payment, invoice, cost-charging, or payment-provider behavior.
