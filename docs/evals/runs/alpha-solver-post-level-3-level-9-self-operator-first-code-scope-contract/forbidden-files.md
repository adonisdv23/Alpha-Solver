# Forbidden files

The future first-code lane must never add or change any file in the categories below. Presence of any such change is a hard stop.

## Forbidden file categories

- **Runtime code** modules that implement Self Operator behavior (any importable runtime package or module under the application source tree).
- **Provider code** modules, provider adapters, or provider-routing modules.
- **API route exposure**: files that add or expose service API routes, including `/v1/solve` or any new service endpoint.
- **Dashboard route exposure**: files that add or expose dashboard routes or dashboard surfaces.
- **CLI behavior changes**: files that change CLI entrypoint behavior.
- **Credentials**: `.env` files, secret files, token files, or any file carrying authentication material.
- **Browser automation**: browser-driver or headless-automation modules.
- **Deployment**: deployment, release, hosting, container, or infrastructure files.
- **Billing**: billing, metering, or payment files.
- **Fallback**: provider fallback or hosted fallback logic files.
- **Provider calls**: any module wired to make provider calls.
- **External API calls**: any module wired to make external API calls.
- **Evidence promotion**: files that promote prior evidence to a stronger accepted state.
- **Source-artifact mutation**: any `source-artifact` directory or preserved payload file.

These categories restate the forbidden scope in file terms; see `forbidden-code-behavior.md` for the behavior-level statement.
