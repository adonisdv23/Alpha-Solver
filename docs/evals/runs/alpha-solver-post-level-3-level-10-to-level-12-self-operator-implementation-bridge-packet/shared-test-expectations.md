# Shared test expectations

Future implementation lanes must use deterministic local tests and static safety regression checks. Expected categories include:

- artifact schema validation;
- redaction behavior;
- preflight blocked-command detection;
- operator confirmation missing stop;
- unclear scope stop;
- forbidden surface stop;
- changed-file scope stop;
- no provider/network/browser/deployment/billing access;
- dry-run writes local redacted review artifacts only.

Tests must be offline, deterministic, and incapable of starting hosted models, local models, browsers, services, deployment, billing, or external API workflows.
