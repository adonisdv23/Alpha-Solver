# Redaction Policy

## Must redact

Future execution artifacts must redact:

- hosted provider keys;
- API tokens and secrets;
- environment variables containing sensitive values;
- private local usernames when not needed for provenance;
- private hostnames when not needed for endpoint-locality proof;
- sensitive absolute local paths;
- private model identifiers if they expose confidential information;
- any accidental credential-like value in stdout, stderr, command captures, or operator notes.

## Must preserve

Future execution artifacts must preserve:

- exact repo HEAD;
- test-case ID;
- prompt source;
- prompt text;
- exact command shape, with only sensitive environment-specific values redacted;
- exit code;
- normalized JSON `status`;
- `behavior_evidence` value;
- `no_hosted_fallback` value;
- `no_provider_keys_required` value;
- endpoint locality classification sufficient to confirm loopback-only use;
- finite timeout value;
- redaction confirmation.

## Redaction confirmation

Each test-case artifact must include an explicit redaction confirmation that states whether redactions were applied and whether any hosted provider key, token, or secret was observed. Hosted provider key use or exposure is a stop condition.
