# Forbidden scope stop

A future first code lane must stop when the requested work or observed diff enters forbidden scope.

## Forbidden scope for this stop packet

- Provider calls or provider-routing behavior.
- Credentials, secrets, tokens, or authentication material.
- Browser automation.
- Deployment, release, hosting, or infrastructure changes.
- Billing, metering, or payment changes.
- External API integration or invocation.
- `/v1/solve` exposure or dashboard exposure.
- Evidence promotion or claims beyond the accepted evidence boundary.
- Source artifact modification.
- Any file outside the future selected lane's allowed scope.

The operator must stop rather than partially implement forbidden scope.
