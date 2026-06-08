# Output artifacts

Future preflight output should be local-only and unpromoted. It may include:

- Preflight summary.
- Passed and failed local checks.
- Stop-state code when blocked.
- Changed-file scope proof.
- Redacted command records.

It must not include secrets, provider outputs, external API responses, billing data, browser data, deployment output, source-artifact payloads, or evidence-promotion labels.
