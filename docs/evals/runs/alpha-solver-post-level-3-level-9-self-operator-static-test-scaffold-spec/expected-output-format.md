# Expected output format

Future static tests should produce deterministic, reviewable failures. A finding should include:

- `finding_id`: one registry identifier.
- `path`: repo-relative path under review.
- `reason`: concise blocked-surface explanation.
- `required_action`: stop, narrow scope, or request separate authorization.

Output must not include secrets, provider outputs, external API responses, billing data, browser data, deployment output, or evidence-promotion labels.
