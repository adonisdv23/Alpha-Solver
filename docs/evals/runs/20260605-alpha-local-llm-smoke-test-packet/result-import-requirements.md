# Result Import Requirements

If a later approved lane executes smoke after endpoint-locality hardening, result import into repository docs must be sanitized and bounded.

## Required imports

- Future lane ID and approval reference.
- Endpoint-locality hardening review reference.
- Exact command as executed, with operator-supplied fields documented.
- Exit code and pass/fail/error classification.
- Sanitized endpoint pattern limited to localhost loopback.
- Operator-supplied model name only if approved for repository disclosure.
- Timeout value.
- Evidence label for the future smoke lane.
- Raw artifact preservation locations or hashes, if approved for disclosure.
- Redaction log.

## Import prohibitions

- No access material.
- No private endpoint URLs.
- No nonpublic network endpoints.
- No provider access material.
- No raw sensitive environment dumps.
- No claim upgrades beyond the approved future smoke evidence boundary.
