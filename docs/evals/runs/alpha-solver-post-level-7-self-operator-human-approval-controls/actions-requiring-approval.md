# Actions Requiring Approval

Self Operator must obtain explicit operator approval before performing any action in this file.

## Required approval categories

Approval is required for:

- PR creation, including opening a pull request, updating a pull request description with final claims, or requesting review.
- Merge instructions, including instructing a human or automation to merge, squash merge, rebase merge, fast-forward merge, close-and-reopen, or otherwise complete integration.
- External provider calls, including hosted model calls, hosted embedding calls, hosted search calls, hosted browser APIs, payment APIs, deployment APIs, observability APIs, issue-tracker APIs, or any third-party service that receives task data.
- File deletion, including deleting source files, docs, tests, artifacts, generated outputs, placeholders, legacy files, reference files, or evidence packets.
- Deployment, including production deployment, staging deployment, preview deployment, release publication, package publication, container publication, or infra mutation.
- Billing, including creating charges, changing subscription state, touching payment providers, changing metering, changing quotas, issuing credits, or modifying invoice-related records.
- Credential use, including reading, exporting, exchanging, rotating, validating, or submitting secrets, API keys, tokens, cookies, SSH keys, service account files, or browser session credentials.
- Browser automation, including logging into websites, clicking buttons, submitting forms, scraping authenticated pages, changing account settings, sending messages, purchasing, posting, or using a browser session to act outside local docs review.
- Evidence promotion, including upgrading local evidence to release evidence, benchmark evidence, production-readiness evidence, MVP-readiness evidence, public claims, marketing claims, provider-readiness claims, or release notes.

## Scope requirement

Approval must name the exact action category, target, intended result, constraints, and allowed time window. If any of these fields are missing or unclear, Self Operator must stop.
