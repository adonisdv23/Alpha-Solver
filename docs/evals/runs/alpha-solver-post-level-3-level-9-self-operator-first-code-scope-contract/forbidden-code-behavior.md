# Forbidden code behavior

The future first-code lane must never introduce any of the following behavior. Each item is a hard stop.

## Forbidden behavior

- **Runtime code**: implementing runtime Self Operator behavior.
- **Provider code**: implementing provider adapters or provider-routing behavior.
- **API route exposure**: exposing or modifying service API routes, including `/v1/solve`.
- **Dashboard route exposure**: exposing or modifying dashboard routes.
- **CLI behavior changes**: changing CLI entrypoint behavior.
- **Credentials**: handling credentials, secrets, tokens, or authentication material.
- **Browser automation**: driving a browser or headless automation.
- **Deployment**: performing deployment, release, hosting, or infrastructure changes.
- **Billing**: performing billing, metering, or payment work.
- **Fallback**: implementing provider fallback or hosted fallback.
- **Provider calls**: making provider calls.
- **External API calls**: making external API calls.
- **Evidence promotion**: promoting evidence beyond the accepted boundary.
- **Source-artifact mutation**: modifying source artifacts or preserved payloads.

The future first-code lane must stop rather than partially implement any forbidden behavior.
