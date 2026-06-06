# Packet Purpose

This packet prepares the manual local smoke materials for the non-production local LLM solver orchestration runner.

## Scope

The packet is documentation-only and exists so Adonis can later execute the manual smoke from repo root on his Mac after review-gate authorization.

## Blocked gate

This packet is blocked until the implementation review gate returns:

`AUTHORIZE_MANUAL_LOCAL_ORCHESTRATION_SMOKE`

No manual smoke should be run from this packet before that exact authorization is present.

## Non-actions

This packet does not run smoke, does not call a local model, does not call hosted providers, does not import results, and does not close the local LLM solver orchestration track.

## Intended future source artifact

The future local execution outputs should be written under:

`docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-source-artifact/`

That folder is not created as completed evidence by this packet. It is reserved for Adonis's local execution output and will require a later source artifact preservation PR or equivalent repo-source preservation step.
