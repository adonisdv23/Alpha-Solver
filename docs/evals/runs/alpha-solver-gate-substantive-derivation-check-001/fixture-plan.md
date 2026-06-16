# Fixture Plan

## Purpose

Define fixture categories for a future static derivation/no-echo check without running providers, local models, runtime endpoints, or external services.

## Fixture shape

Each fixture should include:

- stable fixture ID;
- frozen prompt text;
- frozen source text if distinct from the prompt;
- candidate output text;
- expected classification label;
- short rationale;
- allowed source-copy notes, if any;
- forbidden copying notes, if any.

## Fixture categories

1. `exact_echo`: output equals normalized prompt or source text.
2. `near_echo`: output adds small framing while copying most source content.
3. `paraphrase_only_response`: output restates the source without adding a reviewable inference.
4. `unsupported_copying`: output copies source claims that should have been bounded or rejected.
5. `substantive_derivation`: output transforms source text into supported criteria, implications, or next steps.
6. `acceptable_source_use`: output preserves short required identifiers, labels, or requested quotes while adding reasoning.
7. `non_answer_safe_out`: output refuses, blocks, or asks for clarification without echoing the prompt and without pretending to answer.

## Positive fixtures for substantive derived output

Positive fixtures should require the candidate output to:

- identify a constraint or risk from the source;
- state a bounded implication;
- name an allowed or blocked next action;
- avoid unsupported facts;
- avoid large copied spans;
- preserve required IDs or statuses only where needed.

Expected labels:

- `substantive_derivation`
- `acceptable_source_use`
- `non_answer_safe_out`

## Negative fixtures

Negative fixtures should cover:

- exact prompt echo;
- exact source echo;
- near echo with a generic preface;
- near echo wrapped in a safe-out marker;
- paraphrase-only restatement;
- unsupported copying of readiness, value, provider, benchmark, public API, production, security/privacy, or superiority claims.

Expected labels:

- `exact_echo`
- `near_echo`
- `paraphrase_only_response`
- `unsupported_copying`

## Frozen prompt and source text

Prompts and source text should be frozen in fixture files once accepted. Later wording changes should create a new fixture revision rather than mutating an existing fixture. Current-fact prompts should include an as-of date and source snapshot or should be excluded from execution and scoring lanes.

## Expected classification labels

The minimum label set for this lane is:

- `exact_echo`
- `near_echo`
- `paraphrase_only_response`
- `substantive_derivation`
- `acceptable_source_use`
- `unsupported_copying`
- `non_answer_safe_out`

## Boundary

This plan does not add fixtures in this PR because the selected lane is docs-first and review-only. Future fixture additions should use only synthetic or approved committed text and must not inspect raw Alpha or baseline outputs.
