# Credential, browser, deployment, and billing gates

The future static scaffold must block:

- Credential or secret access.
- Browser automation, browser profiles, cookies, or session data.
- Deployment commands or hosted exposure.
- Billing, usage purchase, or payment workflows.

Expected finding IDs include `SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED`, `SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED`, `SELF_OPERATOR_DEPLOYMENT_BLOCKED`, and `SELF_OPERATOR_BILLING_BLOCKED`.
