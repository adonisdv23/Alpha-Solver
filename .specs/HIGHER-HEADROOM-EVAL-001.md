# HIGHER-HEADROOM-EVAL-001 · Higher-Headroom Alpha-vs-Plain Prompt Set

## Status

Documentation/spec-first lane for `OUTPUT-DIFFERENTIATION-PHASE-001`.

This spec creates a curated higher-headroom prompt set for future Alpha-vs-plain
comparison runs. It does not change runtime behavior, provider behavior,
dashboard behavior, request metrics, Cloud Run configuration, OpenAI enablement,
or Google Sheets planning ledgers.

## Purpose

Alpha Solver supervised preview is operator-test-ready only. It is not
MVP-validated, production-ready, or proven superior to plain provider output.
Easy prompts can saturate both systems and make comparisons inconclusive, so the
project needs prompts that create room for visible differentiation.

This lane defines a prompt set that tests whether Alpha can preserve user intent,
identify hidden constraints, surface assumptions, diagnose risks and failure
modes, maintain claim boundaries, prioritize under uncertainty, and produce
execution-ready next actions better than plain provider output.

## Scope

In scope:

- Add a documentation prompt set for higher-headroom Alpha-vs-plain evaluation.
- Cover ambiguous planning, readiness judgment, hidden constraints,
  prioritization, artifact review, debugging, rollout decisions, evidence
  interpretation, adversarial/noisy context, research synthesis, backlog triage,
  and operator handoff.
- Define scoring and preservation expectations for future comparison runs.
- Provide a semi-structured prompt manifest under `docs/evals/prompt_sets/`.

Out of scope:

- Runtime behavior changes.
- Provider behavior changes.
- Request metric changes.
- Dashboard auth, session, or CSRF changes.
- Cloud Run deployment or configuration changes.
- Enabling OpenAI.
- Running live provider comparisons in this PR.
- Updating Google Sheets or backlog workbooks.
- Claiming MVP validation, Alpha superiority, production readiness, broad
  runtime readiness, benchmark success, exact billing accuracy, or provider
  reasoning orchestration.

## Deliverables

- `docs/evals/HIGHER_HEADROOM_PROMPT_SET.md` is the human-readable prompt set and
  operator guidance.
- `docs/evals/prompt_sets/higher_headroom_prompt_set_v1.md` is the
  semi-structured manifest for copying prompt entries into future run artifacts.
- `.specs/INDEX.md` includes this spec.

## Prompt design requirements

The prompt set must include at least twelve prompts and should prefer concise,
well-structured entries when more prompts are useful. Each prompt entry must
include:

- Prompt ID.
- Prompt family.
- Prompt text.
- What this tests.
- Hidden constraints or traps.
- Expected Alpha advantages if Alpha performs well.
- Plain provider likely failure modes.
- Rubric dimensions emphasized.
- Suggested scoring notes.
- Claim boundaries and non-claims.

Prompts must be relevant to Alpha Solver/operator work without requiring
secrets, private data, real API keys, account IDs, raw provider payloads,
cookies, session data, CSRF tokens, or sensitive personal data.

## Scoring contract

Future runs using this prompt set must score responses with
`docs/evals/RESPONSE_QUALITY_RUBRIC.md` and preserve sanitized artifacts using
`docs/evals/ARTIFACT_PRESERVATION.md`. Operators should record Alpha wins, plain
wins, ties, and inconclusive results honestly, including cases where plain output
is shorter or more useful.

Interpretation must be conservative. One prompt, one family, or one small run
must not be used to claim Alpha Solver superiority, MVP validation, production
readiness, broad runtime readiness, benchmark success, or provider reasoning
orchestration.

## Artifact preservation contract

Future comparison artifacts should summarize outputs instead of committing raw
provider payloads. They must redact or omit secrets, credentials, dashboard
passwords, cookies, CSRF tokens, session values, provider account identifiers,
private customer data, and sensitive runtime material.

Use the run artifact structure from `docs/evals/ARTIFACT_PRESERVATION.md`,
including side-by-side comparison fields, evidence strength, redactions
performed, conservative interpretation, defects or regressions, and non-claims.

## Relationship to future work

This prompt set supports:

- `DISC-MRG-068`.
- `DISC-MRG-069`.
- `EVAL-ARTIFACT-PRESERVE-001`.
- `ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001`.
- `EVAL-DIFFERENTIATION-RUN-001`.
- `ALPHA-VISIBLE-DIFFERENTIATOR-001`.
- `ALPHA-ANSWER-STRUCTURE-V2-001`.

`HIGHER-HEADROOM-EVAL-001` should be marked Done in external planning ledgers
only after the PR carrying this spec and prompt set is merged. This lane is P0
for `OUTPUT-DIFFERENTIATION-PHASE-001` because it supplies discriminating prompts
where Alpha can show, fail to show, or regress in visible added value.
