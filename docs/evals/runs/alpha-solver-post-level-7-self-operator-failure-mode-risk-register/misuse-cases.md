# Misuse Cases

## Foreseeable misuse cases

1. A Self Operator opens a PR with both authorized docs and unrelated runtime edits, creating a polluted branch that reviewers do not fully inspect.
2. A Self Operator updates a stale PR after the base branch changed and presents old checks as current.
3. A Self Operator overclaims that a docs-only packet proves Self Operator readiness, product readiness, API readiness, dashboard readiness, provider readiness, benchmark readiness, quality readiness, MVP readiness, or production readiness.
4. A Self Operator cites vague source evidence such as entire directories, historical context, or unverified memory instead of exact files and commands.
5. A Self Operator invokes local or hosted providers implicitly through a smoke command, fallback path, dashboard preview, API route, model wrapper, or helper script.
6. A Self Operator exposes credentials by reading environment files, printing tokens, committing redacted artifacts incorrectly, screenshotting secret-bearing dashboards, or copying private URLs.
7. A Self Operator enables auto-merge, merges its own PR, force-pushes over reviewer changes, or modifies branch protections.
8. A Self Operator exposes a dashboard, API, health endpoint, metrics endpoint, or preview URL without security review.
9. A Self Operator promotes raw artifacts into decision ledgers without provenance, redaction, or reviewer acceptance.
10. A Self Operator treats absence of failing checks as permission to proceed with sensitive implementation.

## Abuse actors

- Over-eager automation that optimizes for task completion rather than safety boundaries.
- A malicious or compromised operator prompt that asks for provider calls, credential access, or branch-protection changes.
- A confused human requester who asks for readiness claims from insufficient evidence.
- External users or bots who discover accidentally exposed dashboards or APIs.

## Required response pattern

Any future Self Operator design must treat these misuse cases as blocked by default. It may only unblock a case through an explicit spec, scoped authorization, deterministic checks, and human review gates.
