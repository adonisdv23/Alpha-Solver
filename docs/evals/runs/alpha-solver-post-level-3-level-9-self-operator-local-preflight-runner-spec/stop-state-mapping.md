# Stop-state mapping

Future preflight failures should map to explicit stop states:

- Missing approval: `SELF_OPERATOR_OPERATOR_CONFIRMATION_MISSING`
- Scope ambiguity: `SELF_OPERATOR_SCOPE_UNCLEAR`
- Provider risk: `SELF_OPERATOR_PROVIDER_CALL_BLOCKED`
- External API risk: `SELF_OPERATOR_EXTERNAL_API_BLOCKED`
- Credential risk: `SELF_OPERATOR_CREDENTIAL_RISK_BLOCKED`
- Browser risk: `SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED`
- Deployment risk: `SELF_OPERATOR_DEPLOYMENT_BLOCKED`
- Billing risk: `SELF_OPERATOR_BILLING_BLOCKED`
- Artifact boundary risk: `SELF_OPERATOR_ARTIFACT_BOUNDARY_BLOCKED`
