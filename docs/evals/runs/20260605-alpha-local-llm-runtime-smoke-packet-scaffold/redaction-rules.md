# Redaction Rules

These rules apply only to future authorized runtime smoke artifacts. No smoke artifacts are created or redacted in this scaffold lane.

## Must Redact From Sanitized Imports

- Secrets, tokens, API keys, provider keys, bearer tokens, and credentials.
- Absolute local filesystem paths when they expose usernames or sensitive structure.
- Hostnames or addresses that are not necessary for the localhost or loopback proof.
- Prompt content that contains sensitive data.
- Environment variable values that are secret or sensitive.
- Raw stack traces that include secrets or sensitive paths.

## Must Preserve In Sanitized Imports

- Localhost or loopback-only endpoint proof, with sensitive details removed where needed.
- Exact local model name.
- Finite timeout value.
- Hosted fallback disabled confirmation.
- Provider keys absent for local mode confirmation.
- Failure classification.
- Outcome boundary.
- `behavior_evidence=false` unless changed by a later explicit evidence-model lane.

## Raw Artifact Rule

Raw artifacts must be preserved separately before redaction. Sanitization must not be used to erase the fact that a failure occurred or to broaden the evidence boundary.
