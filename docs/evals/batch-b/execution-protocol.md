# Batch B Execution Protocol

## Status

This is the Batch B execution protocol and operator runbook for future expanded
output-differentiation runs in `OUTPUT-DIFFERENTIATION-PHASE-001`.

This document is a planning and execution-control artifact only. It is not a
capture result, not an evaluation result, and not evidence that Batch B has run.
It does not execute Batch B, does not modify A3-1 artifacts, and does not change
runtime, provider, model, routing, `/v1/solve`, or scoring-rubric behavior.

## Purpose

Batch B must preserve a clean evidence chain while reducing operator friction.
This protocol is designed to prevent the workflow failures that can corrupt or
slow future output-differentiation runs, including:

- missing source packets;
- temporary scratch file loss;
- copy/paste placeholder errors;
- helper validators without the required inputs;
- unblinding before scoring;
- score arithmetic errors;
- overclaiming;
- excessive prompt size causing Codex task creation failures;
- unnecessary API token usage.

## Source hierarchy for Batch B

Use this evidence hierarchy when planning, capturing, scoring, reviewing, and
summarizing Batch B work:

1. Repo code, tests, and specs.
2. Preserved eval artifacts committed under `docs/evals/`.
3. Operator-approved source packets.
4. Blind scorer results.
5. Google Sheet rows as a planning ledger only.
6. AI helper outputs as advisory unless tied to repo evidence.

Google Sheet rows are not proof of implementation. AI summaries are not
canonical unless they are source-backed and traceable to repo evidence or an
operator-approved source packet. Raw provider output should not be preserved in
the repo unless it has been sanitized and approved under the artifact
preservation protocol.

## Standard Batch B lifecycle

### A. Planning gate

Before any capture begins:

- Select the Batch B prompt subset.
- Confirm the exact prompt IDs.
- Confirm the model set and surfaces.
- Confirm the capture cap, including any contingency cap.
- Confirm no pending runtime PR, provider PR, model-config PR, routing PR, or
  `/v1/solve` PR will contaminate the run.
- Create or confirm the source packet skeleton before live work starts.
- Confirm the preservation location for the blinded bundle and operator-only
  unblinding map.

Do not begin Batch B execution until the prompt subset, model set, cap, and
source packet skeleton are all approved.

### B. Capture gate

During capture:

- Use one capture task only.
- Do not run parallel captures.
- Send the same prompt text to both surfaces.
- Do not add extra instructions to one surface only.
- Enforce the approved capture cap.
- Record retry rules before using them.
- Treat retries as exceptions, not as a way to improve an answer.
- Stop if the capture is incomplete, ambiguous, or contaminated.

Partial failed-capture outputs must not be reused as official Batch B evidence.
If a capture cannot be completed cleanly, halt and preserve only a sanitized
failure note.

### C. Immediate preservation gate

Immediately after capture:

- Save the blinded bundle.
- Save the operator-only unblinding map separately.
- Save the blind scorer prompt.
- Save the capture metadata summary.
- Do not rely on `/tmp` scratch files.
- Do not rely on chat history alone.
- Do not leave required source material only in an assistant thread.

Preservation happens before scoring, review, artifact population, or Sheet
updates.

### D. Blinding gate

Before any blind scoring task:

- Verify the blinded bundle has no route labels.
- Verify there is no provider metadata.
- Verify there is no assignment table or unblinding map in scorer-facing input.
- Verify every prompt and paired output is complete.
- Verify synthetic prompt text cannot be confused with real credentials,
  headers, cookies, or provider metadata.

If any route leak or provider identifier appears in scorer-facing material, stop
and repair the blinded bundle before scoring.

### E. Blind scoring gate

Official Batch B scoring requires:

- One official blind scorer result.
- Scores for all 14 rubric dimensions for each side of each comparison.
- Scorer confirmations that the bundle was blinded and that no route identity was
  used.
- A complete scored sheet, not winner-only notes.
- Immediate preservation of the scorer result.

Winner-only scoring, informal impressions, and helper comments are not official
Batch B scores.

### F. Math verification gate

After blind scoring and before claims:

- Recompute totals from dimension scores.
- Record any mismatch between scorer-provided totals and recomputed totals.
- Apply the unblinding map only after scoring is complete.
- Compute aggregate totals from the corrected comparison totals.
- Preserve a conservative interpretation of margins, sample size, and defects.

Corrected computed totals are the reviewable arithmetic record. Any scorer-total
mismatch must be retained rather than silently overwritten.

### G. Artifact population gate

When populating repo artifacts:

- Use one Codex writer task only for the target artifact file set.
- Include complete source packets.
- Do not use placeholders when the operator has already supplied source data.
- Do not depend on helper-thread results unless all helper results are embedded
  in the writer prompt or committed source packet.
- Do not call live providers.
- Do not change runtime, provider, model, routing, `/v1/solve`, or scoring-rubric
  behavior.

Artifact population is a documentation and preservation task, not a runtime
implementation task.

### H. PR review gate

Before merge, review:

- score math and aggregate math;
- blinding integrity;
- redaction and secret hygiene;
- claim boundaries;
- scope boundaries;
- CI and focused check status;
- confirmation that no capture, scoring, unblinding, runtime change, provider
  change, model change, scoring-rubric change, or Sheet update occurred in any
  protocol-only PR.

### I. Sheet update gate

Google Sheet updates happen only after the relevant PR has merged:

- Mark items Done only from merged PR evidence.
- Treat Sheet rows as planning/status records, not implementation proof.
- Do not mutate uncertain legacy rows without operator approval.
- Do not add broad claims.
- Preserve links to merged repo artifacts when available.

## Source packet standard

No Batch B artifact-population task should run from summaries alone. The
operator or coordinator must provide a complete source packet before a writer
populates artifacts.

Canonical source packet template:

```text
SOURCE PACKET
1. Run ID:
2. Prompt IDs:
3. Capture status:
4. Blinded bundle:
5. Operator-only unblinding map:
6. Blind scorer result:
7. Scorer confirmations:
8. Corrected computed totals:
9. Redactions:
10. Non-claims:
11. Operator approval to unblind:
12. Operator approval to populate artifacts:
```

Rules:

- No artifact population task should run from summaries alone.
- No prompt should contain `[PASTE HERE]` placeholders when the operator has
  already supplied the data.
- If source data is too large, use staged chunks with an explicit completion
  marker.
- The writer must stop if required source-packet fields are missing.
- Helper outputs are advisory unless they are included in the source packet and
  traceable to source material.

## Prompt-size / Codex task length protocol

When source material is large:

- Keep the initial Codex task below the platform limit.
- Remove duplicate source data.
- Use staged source packets only when necessary.
- Label staged packets with clear markers such as:

```text
SOURCE PACKET CHUNK 1 OF N
SOURCE PACKET CHUNK 2 OF N
SOURCE PACKETS COMPLETE - BEGIN
```

Codex must not proceed until the `SOURCE PACKETS COMPLETE - BEGIN` marker is
received. Codex must never infer missing source material, silently fill gaps, or
convert partial failed captures into official artifacts.

## API/key usage protocol

Use API credentials only for tasks that actually require live access:

- Capture and live diagnostics may require `OPENAI_API_KEY` or equivalent
  provider credentials.
- Artifact population does not require an API key.
- PR review does not require an API key.
- Docs and hygiene tasks do not require an API key.
- Prompt-bank and protocol tasks do not require an API key.
- Remove, unset, or ignore API credentials for non-live tasks when possible.
- Live provider calls are forbidden in non-capture tasks.

Never include actual credential values, bearer tokens, cookies, headers, or
environment dumps in source packets, docs, prompts, artifacts, or PR bodies.

## Concurrency policy

Safe concurrency for Batch B is narrow:

- Use one writer task per target file set.
- Do not run multiple capture tasks.
- Do not run multiple artifact-population PRs for the same run.
- Use read-only validators only if they receive full inputs.
- Prompt-bank docs may run concurrently if they do not touch A3 artifacts.
- Protocol docs may run concurrently if they do not touch A3 artifacts.
- Batch B execution must wait for the approved run plan.

A helper thread without complete inputs should not be treated as a validator.
If a helper did not receive the source packet, its output is advisory at most.

## Stop conditions

Stop and escalate before writing or merging artifacts if any of these conditions
is true:

- The source packet is missing or incomplete.
- Any comparison is missing the required 14-dimension scores.
- The scorer did not confirm blinding.
- A route leak appears in the scorer-facing bundle.
- Unblinding happened before scoring.
- Partial failed-capture outputs are being used as official evidence.
- Totals cannot be recomputed from dimension scores.
- The artifact task would need runtime, provider, model, routing, `/v1/solve`,
  or scoring-rubric changes.
- A broad claim would be required to justify the write-up.
- A Sheet update is requested before merge.
- The prompt exceeds the task limit and the source packet is incomplete.

## Redaction and safety protocol

Batch B artifacts and source packets must exclude:

- raw provider payloads;
- response IDs;
- headers;
- cookies;
- auth tokens;
- environment dumps;
- secret-like strings;
- private user data or provider account identifiers.

Synthetic secret or cookie mentions are allowed only as prompt content and must
be clearly synthetic. Redactions must be recorded in the source packet and final
artifacts.

## Claim-boundary protocol

Strict non-claims for Batch B and protocol work:

- no MVP validation;
- no Alpha Solver superiority;
- no broad plain-provider superiority;
- no answer-quality superiority;
- no production readiness;
- no broad runtime readiness;
- no benchmark success;
- no exact billing accuracy;
- no provider reasoning orchestration.

Approved conservative language examples:

- "This limited run favored [surface] on the selected comparisons."
- "This does not establish broad superiority."
- "This is evidence for follow-up investigation, not a production-readiness
  claim."
- "Margins and sample size should be interpreted conservatively."

## Batch B deliverable checklist

Before any Batch B run, the operator should confirm:

- [ ] prompt subset approved;
- [ ] model set approved;
- [ ] capture cap approved;
- [ ] one capture task only;
- [ ] output preservation path ready;
- [ ] scorer prompt ready;
- [ ] source packet destination ready;
- [ ] unblinding map storage ready;
- [ ] artifact-population prompt under size limit;
- [ ] Sheet update prompt prepared but not run until after merge.

## Lessons learned from A3-1

A3-1 artifacts are present on `main` in the preserved run directory for
`20260602-eval-differentiation-run-001-alpha-vs-plain`. The Batch B protocol
uses those artifacts only as lessons-learned context and does not modify them.
Conservative lessons for future runs:

- The evidence chain depended on clear runtime/config preconditions before live
  capture; future Batch B planning should confirm no pending runtime or config
  PR will contaminate the run.
- Artifact population required a full source packet, not summaries.
- Official scores must be recomputed from dimension scores and mismatches must
  be recorded.
- Helper outputs without source data are not useful as official validators.
- Prompt-size limits must be considered before creating Codex tasks.
- Operator burden should be reduced by compiling complete prompts and source
  packets before assigning writer or reviewer tasks.

## Recommended next operator action

After PR #243 and the Batch B opener are merged, select an 8 to 12 prompt subset,
create one capture task, preserve the blinded bundle immediately, and use this
protocol to avoid repeating A3-1 friction.
