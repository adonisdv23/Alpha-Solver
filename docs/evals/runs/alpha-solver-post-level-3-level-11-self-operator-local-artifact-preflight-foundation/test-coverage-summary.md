# Test coverage summary

New deterministic tests cover:

- valid artifact validation;
- missing confirmation;
- missing stop state;
- unsupported schema version;
- redaction/rejection of secret-like markers using fake placeholders only;
- stable JSON roundtrip;
- safe artifact writes/reads;
- path traversal and outside-root rejection;
- default no-overwrite behavior;
- allowed local read/check command classification;
- blocked provider/network/browser/deployment/billing/credential/Google Sheets/source-artifact mutation/evidence-promotion commands;
- unclear command review classification;
- preflight blocks for missing confirmation, unclear scope, forbidden command, out-of-scope changed files, unsafe artifact paths, and missing evidence boundary;
- JSON-serializable preflight result;
- inert command strings only.
