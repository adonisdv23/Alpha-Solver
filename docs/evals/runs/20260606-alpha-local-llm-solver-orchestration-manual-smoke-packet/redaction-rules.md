# Redaction Rules

Apply these rules before preserving future manual smoke artifacts.

## Never preserve

- provider keys;
- raw credentials;
- private URLs;
- private local paths except `<REPO_ROOT>`;
- full environment dumps;
- shell history;
- tokens, cookies, or authorization headers.

## Required replacements

- Replace repo-local absolute paths with `<REPO_ROOT>`.
- Replace local loopback endpoint with a summary such as `http://127.0.0.1:<PORT>/<PATH>` when raw port/path should not be disclosed.
- Replace private local model cache paths with `<LOCAL_MODEL_CACHE_PATH_REDACTED>`.
- Replace any private hostname, LAN address, VPN address, or non-loopback endpoint with `<PRIVATE_OR_NON_LOOPBACK_ENDPOINT_REDACTED>`.

## Allowed local runtime metadata

- loopback confirmation;
- endpoint summary;
- local model identifier when non-sensitive;
- finite timeout value;
- provider mode `local_llm`;
- `behavior_evidence=false`;
- `no_hosted_fallback=true`;
- `no_provider_keys_required=true`.

## Provider key handling

The command template records only provider-key presence booleans for known provider key environment variable names. It must not print provider key values.
