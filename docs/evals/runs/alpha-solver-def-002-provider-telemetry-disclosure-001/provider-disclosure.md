# Provider Data-Sharing Disclosure

## Operator disclosure text

Alpha Solver is local/offline by default. If an operator explicitly enables a hosted provider path, Alpha Solver may send the user's prompt/query and derived provider prompts to the configured external provider for inference. The provider may receive the text necessary to answer the request, and that provider's own processing, retention, abuse-monitoring, and billing terms apply.

Default Alpha Solver telemetry is designed to record only operational metadata such as provider name, model name, route, request id, status, retry count, latency, token counts, estimated cost, cost source, finish reason, error category, retryability, HTTP status code, safe message, and provider request id. Default provider telemetry must not include raw prompts, raw provider responses, raw request bodies, raw headers, cookies, bearer tokens, API keys, raw provider metadata, exception dumps, environment dumps, or config dumps.

Verbose or debug telemetry that would capture prompt text, response text, raw provider payloads, or secret-bearing data is not enabled by this lane and requires separate explicit approval, access controls, retention limits, and disclosure.

## End-user disclosure seed

When hosted provider mode is enabled, your prompt and any necessary derived prompt context may be sent to the configured external AI provider to generate a response. Do not submit secrets or sensitive personal information unless your operator has approved that provider use and its data handling terms. Alpha Solver's default logs are intended to store operational metadata, not raw prompt or provider response text.
