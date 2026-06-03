# SOLVE-PROVIDER-FINAL-ANSWER-EMPTY-GUARD-001 · Provider Final Answer Empty Output Guard

## Purpose

Prevent `/v1/solve` provider final-answer success envelopes from returning HTTP
200 with an empty or whitespace-only `final_answer` when the provider call itself
returns successfully but yields no usable answer text.

## Context

During the clean A3-1 operator-supervised capture attempt for
`OUTPUT-DIFF-A3-FIRST-SCORED-RUN-ARTIFACT-001`, the run stopped after six of the
eight required outputs because the HHE-009 plain `/v1/solve` surface returned
HTTP 200 with `final_answer=""` while the OpenAI Responses API result was marked
`finish_reason="incomplete"`.

PR #237 fixed the HHE-009 sanitizer false-positive blocker. PR #238 guarded the
complex expert route against an empty Step 2 primary answer. The plain provider
success path still accepted a successful `ProviderResult` with empty or
whitespace text and serialized that text directly into the final answer envelope.

## Scope

In scope:

- Guard final HTTP 200 provider answer envelopes against empty or whitespace-only
  answer text.
- Use the existing typed provider SAFE-OUT response path for empty final-answer
  output.
- Preserve existing provider error SAFE-OUT responses.
- Preserve non-empty provider success responses.
- Preserve the PR #238 complex expert-route empty Step 2 guard.
- Preserve the PR #237 sanitizer behavior for benign `IMPORTANT` / import
  substrings and risky import statements.
- Add no-network regression coverage for plain provider empty output,
  whitespace-only output, redaction safety, non-empty success preservation, and
  related expert-route preservation.

Out of scope:

- A3-1 capture, scoring, unblinding, or artifact population.
- Batch B execution.
- Google Sheets or backlog workbook updates.
- Provider prompt refactors or broad routing changes.
- SAFE-OUT taxonomy refactors beyond the existing normalized provider error
  response fields.
- Dashboard, budget, replay, observability, MCP, or eval artifact changes.
- Claims of MVP validation, Alpha Solver superiority, answer-quality
  superiority, production readiness, broad runtime readiness, benchmark success,
  exact billing accuracy, or provider reasoning orchestration.

## Requirements

1. A provider final-answer success path must not return HTTP 200 when the final
   answer text is empty or whitespace-only.
2. Empty provider final-answer output must return a typed provider SAFE-OUT-style
   response with a non-empty `final_answer`, `safe_out=true`, and no `answer`
   field.
3. The empty-output response must not leak API keys, authorization headers,
   bearer tokens, raw provider payloads, raw prompts, raw metadata, tracebacks,
   environment dumps, config dumps, or unsafe internal metadata.
4. The guard should validate final response assembly rather than every provider
   execution call, because the expert route uses provider calls for Step 1
   preview parsing and Step 2 answer assembly.
5. The plain OpenAI provider path and the trivial expert direct final-answer path
   must be guarded.
6. Existing non-empty plain provider success behavior must be preserved.
7. Existing complex expert empty-answer guard behavior from PR #238 must be
   preserved.
8. Existing sanitizer behavior from PR #237 must be preserved.
9. No live provider calls are required for validation.

## Acceptance criteria

- A fake-provider plain `/v1/solve` request returning `ProviderResult(text="",
  finish_reason="incomplete")` returns a provider SAFE-OUT-style failure instead
  of HTTP 200 with an empty `final_answer`.
- A fake-provider plain `/v1/solve` request returning whitespace-only text
  returns the same safe failure shape.
- The empty-output SAFE-OUT body is allowlist-built and does not include secrets,
  raw prompt text, raw provider payloads, raw metadata, tracebacks, or unsafe
  internal metadata.
- Non-empty plain provider success still returns HTTP 200 with the expected
  `final_answer` and no `answer` field.
- Focused PR #238 expert empty-answer and expert route preservation tests still
  pass.
- Focused PR #237 sanitizer tests still pass.

## Backlog impact

`OUTPUT-DIFF-A3-FIRST-SCORED-RUN-ARTIFACT-001` remains blocked until this fix is
merged and any applicable operator bookkeeping is complete. A3-1 capture must not
be retried from this PR, and previous partial failed-capture outputs must not be
reused.
