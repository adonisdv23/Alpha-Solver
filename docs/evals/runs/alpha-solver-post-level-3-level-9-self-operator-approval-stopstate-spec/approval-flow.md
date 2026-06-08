# Approval flow

Future Self Operator work must require explicit operator confirmation before any allowed local action proceeds. The flow should be:

1. Confirm selected lane and allowed scope.
2. Confirm current branch and changed-file scope.
3. Present hard stops and forbidden surfaces.
4. Require operator confirmation.
5. Stop if confirmation is missing or scope changes.

Approval must not authorize providers, external APIs, credentials, browsers, deployment, billing, route exposure, fallback, source-artifact mutation, or evidence promotion.
