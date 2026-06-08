# Privacy and Data Risks

## Sensitive data risks

- Future product surfaces may receive personal data, confidential business data, credentials, proprietary prompts, or regulated information.
- Logs, traces, dashboards, evidence packets, screenshots, and copied artifacts may retain sensitive data longer than intended.
- Provider metadata, account identifiers, request IDs, billing identifiers, cookies, tokens, session values, and CSRF values could leak through artifacts.

## Data handling risks

- Data-retention behavior may be unclear if local runs, hosted provider calls, fallback calls, and dashboard logging are not separated.
- Operators may confuse sanitized evidence summaries with raw provider payloads or full request/response traces.
- Redaction gaps may allow private user content to enter docs, tickets, dashboard screenshots, benchmark reports, or PR descriptions.
- Future deletion, export, or audit expectations may be unsupported if storage locations are not inventoried before route exposure.

## Privacy stop signals

- Stop if a future packet requires raw unredacted prompts, responses, traces, credentials, cookies, sessions, provider account identifiers, billing identifiers, or private user data in committed docs.
- Stop if future dashboard risks are reviewed without redaction, retention, access-control, and screenshot-handling rules.
- Stop if provider/fallback behavior is ambiguous enough that data residency, third-party processing, or billing exposure cannot be explained to an operator.

## Boundary

This packet does not collect, store, inspect, transmit, or process private user data. It does not implement privacy controls, dashboard controls, route controls, provider calls, fallback behavior, billing work, model inference, benchmark execution, or evidence promotion.
