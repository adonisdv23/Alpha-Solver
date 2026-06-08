# Secret Boundary Overview

## Boundary statement

Future provider orchestration work must treat API keys, bearer tokens, refresh tokens, service account material, hosted-provider credentials, environment variable values, secret manager payloads, and any derived authorization artifacts as secrets unless a later Level 7-approved spec explicitly classifies a value as non-secret.

## Secret references versus secret values

- Secret references may identify where a credential lives, such as a local environment variable name or a managed-secret identifier.
- Secret values are the credential payloads themselves and must not be committed, logged, rendered in dashboards, embedded in docs, echoed in command output, or copied into evidence packets.
- A future implementation may use references only after Level 7 authorizes the storage, retrieval, validation, logging, and operator-confirmation behavior.

## Trust-boundary themes

- Local development settings are not automatically safe for hosted execution.
- Hosted-provider credentials are not automatically safe for local tooling, screenshots, packet evidence, or benchmark artifacts.
- Provider orchestration code must not infer permission to call providers merely because a credential reference is present.
- Evidence packets must not include credentials or unredacted secrets.

## Non-implementation status

This packet defines boundary rules only. It does not create credentials, does not configure credentials, does not call providers, and does not modify provider orchestration behavior.
