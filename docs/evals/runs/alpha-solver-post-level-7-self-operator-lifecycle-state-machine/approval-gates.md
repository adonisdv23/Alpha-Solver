# Approval Gates

## Required operator approval

The operator must approve all externally visible actions before they occur. Externally visible actions include, but are not limited to:

- Calling hosted providers or external APIs.
- Deploying, releasing, or promoting artifacts.
- Updating dashboards, public documentation, tickets, spreadsheets, or customer-visible records.
- Sending notifications, comments, pull requests, issues, or messages outside the local evidence packet.
- Using credentials beyond an explicitly documented local boundary.
- Promoting docs-only evidence into runtime, benchmark, production, or readiness claims.

## Gate before `running_local_only`

Transition from `awaiting_operator_confirmation` to `running_local_only` requires an approval record that names:

- The requested action.
- The approved scope.
- The local-only boundary.
- The evidence being used.
- The credentials boundary.
- The fallback boundary.
- The non-claims and prohibited external actions.

## Re-approval triggers

A future implementation must return to `awaiting_operator_confirmation` or fail closed if any of these change:

- Scope.
- Evidence source.
- Credentials use.
- External visibility.
- Fallback path.
- Runtime target.
- Claims about readiness, quality, benchmark status, provider support, or deployment.
