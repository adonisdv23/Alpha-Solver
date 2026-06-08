# Local Versus Hosted Secret Boundaries

## Local-only settings

Local-only settings are scoped to developer or operator machines and must not be treated as approval for hosted-provider usage. A local secret reference must not be promoted into hosted execution, dashboards, shared evidence, CI, or benchmark runs without a Level 7-approved lane.

## Hosted-provider credentials

Hosted-provider credentials are sensitive production or managed-environment material. Future work must not copy hosted-provider credentials into local docs, local `.env` files, packet artifacts, screenshots, shell transcripts, source artifacts, or PR messages.

## Boundary transitions

Any transition between local-only settings and hosted-provider credentials must be explicitly authorized. Future work should require separate confirmation for:

- moving from local-only configuration to hosted-provider configuration;
- enabling provider calls from hosted infrastructure;
- adding or changing secret manager references;
- enabling billing-capable provider paths;
- allowing benchmark or evidence workflows to use provider credentials.

## Non-implementation status

This document does not configure local settings, does not configure hosted-provider credentials, does not call providers, and does not perform billing work.
