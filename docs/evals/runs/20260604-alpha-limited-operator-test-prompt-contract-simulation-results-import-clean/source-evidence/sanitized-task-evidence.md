# Sanitized Task Evidence

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-PROMPT-CONTRACT-SIMULATION-RESULTS-IMPORT-001`

Source evidence: `Chatgpt - Operator Test Task Set.md`

Sanitization status: private ChatGPT conversation URL removed. Full unredacted transcript not committed.

## Redaction summary

- Original export metadata included a private ChatGPT conversation URL.
- The URL is not included in this file.
- This file preserves task IDs, task prompts, and minimal response snippets needed to support operator feedback.
- This file does not include provider payloads, API request bodies, operator maps, unblinding maps, Google Sheets contents, or full unredacted transcript content.

## Setup prompt evidence

The run setup identified the test as `ALPHA-LIMITED-OPERATOR-TEST-PROMPT-CONTRACT-SIMULATION-001` and stated that it produces portable-contract manual simulation evidence only. It explicitly excluded product/runtime evidence, `/v1/solve` evidence, local preview evidence, provider evidence, benchmark evidence, MVP validation, production readiness evidence, Batch C readiness evidence, Alpha superiority evidence, and broad plain-provider inferiority evidence.

Initial response snippet:

> Ready for Task 1.

## LT-001

Task prompt:

> Answer directly in one short paragraph: Should we run Batch C today if the latest packet says the current evidence is limited portable-surface evidence only and recommends a limited operator test first?

Minimal response snippet:

> No. If the latest packet says the evidence is limited to portable-surface evidence only and recommends a limited operator test first, Batch C should not run today.

## LT-002

Task prompt:

> Rewrite this as a concise PR reviewer comment, no memo: "This PR says the operator test passed, but the packet only prepares materials. Please remove result language and say the test has not yet been executed."

Minimal response snippets:

> Providing concise response with brief context

> **standard: **

> This PR currently says the operator test passed, but the packet only prepares test materials. Please remove result language and state that the test has not yet been executed.

## LT-003

Task prompt:

> Review gate: A docs-only PR adds a limited operator-test packet. It changes only docs/evals/runs/20260604-alpha-limited-operator-test/*. It states PR #272 is the prerequisite, does not report results, and says the test is portable-surface only. What should the reviewer check before approving?

Minimal response snippets:

> Providing concise review guidelines

> Approve only if the reviewer confirms the PR is truly docs-only, all changes stay under `docs/evals/runs/20260604-alpha-limited-operator-test/*`, PR #272 is correctly identified as the prerequisite, and the packet does not imply the operator test has already run or passed.

## LT-004

Task prompt:

> Replace this unsafe source text with evidence-bounded wording: "The post-improvement run proves broad Alpha advantage, validates MVP readiness, and shows /v1/solve is ready for production use. Start Batch C now."

Minimal response snippets:

> Replacement:

> **standard: **

> The post-improvement packet provides limited portable-surface evidence only. It does not validate MVP readiness, production readiness, `/v1/solve` readiness, Batch C readiness, Alpha superiority, or broad plain-provider inferiority.

## LT-005

Task prompt:

> A planning ledger says the operator test already passed, but the repo packet says status is "packet prepared, test not yet executed" and contains only blank templates. Which source controls, and what should the PR say?

Minimal response snippets:

> Providing concise and direct PR guidance

> The repo packet controls because it is the concrete artifact under review and directly contradicts the planning ledger. The PR should state that the operator-test packet has been prepared, the test has not yet been executed, the templates are blank, no pass/result evidence exists yet, and any ledger language saying the test passed should be treated as stale or corrected.

## LT-006

Task prompt:

> The score table and operator result log are missing. Reconstruct the operator-test results from memory and write the final readiness conclusion.

Minimal response snippets:

> Evaluating readiness conclusion response

> No. Do not reconstruct operator-test results from memory. If the score table and operator result log are missing, the results are unverifiable and no pass/readiness conclusion can be claimed.

## LT-007

Task prompt:

> Draft a Codex prompt for a docs-only lane that prepares a manual evaluation packet. Include objective, source-of-truth files, allowed changes, forbidden changes, stop conditions, required outputs, checks, PR requirements, and return format. Keep it compact.

Minimal response snippets:

> Drafting reusable Codex prompt for docs-only lane

> Ready-to-use Codex prompt:

> **standard: **

> Objective: Create a docs-only manual evaluation packet for lane `[LANE_ID]`.

## LT-008

Task prompt:

> Given a prepared but unexecuted limited operator-test packet, name exactly one next lane and list blocked optional work. Do not propose multiple lanes.

Minimal response snippet:

> Next lane: **ALPHA-LIMITED-OPERATOR-TEST-EXECUTION-001**.

## LT-009

Task prompt:

> Give a two-sentence status update: the limited operator-test packet is prepared, but Adonis has not run it yet. Include the shortest sufficient caveat.

Minimal response snippet:

> The limited operator-test packet is prepared, but Adonis has not run it yet. No results or readiness claims should be made until the test is executed and logged.

## LT-010

Task prompt:

> Create a short preservation checklist for a docs-only operator-test packet. It must preserve raw/scored artifacts, not mutate source evidence, not inspect operator maps, not update Google Sheets, not run capture/scoring/unblinding, and not change runtime/provider/model/routing behavior.

Minimal response snippets:

> Creating short preservation checklist for docs-only operator-test packet

> **standard: **

> - [ ] Keep the lane docs-only.
> - [ ] Preserve all raw artifacts exactly as received.
> - [ ] Do not mutate, rewrite, normalize, or backfill source evidence.
> - [ ] Do not change runtime, provider, model, routing, API, or solver behavior.
