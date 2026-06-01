# Expert Pass Behavioral Demo Checklist

## Purpose

Use this one-screen checklist to review whether the opt-in expert provider pass shows the intended judgment behavior on representative prompts. It is a small behavioral review/demo aid only, not an answer-superiority benchmark.

## Scope

- Applies to `/v1/solve` only when OpenAI provider mode is explicitly enabled and `context.route` is `expert`.
- Uses no-network fake-provider tests or operator-supervised inspection; it must not require live OpenAI calls, credentials, or provider billing.
- Checks behavior shape: routing, mode, envelope fields, clarifying questions, assumptions, and block-vs-clarify separation.
- Does not change provider expert-pass behavior, clarify behavior, eval artifact preservation behavior, or UI behavior.

## Prompt set

| Case | Prompt shape | Example prompt to exercise | Expected judgment behavior | Evidence to check |
| --- | --- | --- | --- | --- |
| Trivial | Simple factual or definition request | `Define alpha in one sentence.` | Direct/simple behavior; avoid unnecessary expert complexity. Expected mode is `direct` or equivalent existing simple behavior. | `mode`, `meta.complexity`, and `meta.call_count`; current fake-provider route tests enforce one call. |
| Complex planning | Multi-part planning, review, or decision request | `Review this security migration plan, compare risks, identify assumptions, and decide whether the team should proceed this quarter.` | Expert path fires. The response envelope includes `answer`, `final_answer`, `considerations`, `assumptions`, `confidence`, `mode`, and `meta`. | Envelope fields are present; complex route uses the expert path with the existing fake provider. |
| Messy or vague | Noisy request with mixed goals and unclear priorities | `We need to fix onboarding, maybe compliance too, and leadership wants a plan soon; what should we do?` | System should not overstate certainty. It should either clarify or answer with explicit assumptions, depending on confidence. | `mode`, `confidence`, `clarifying_questions` when clarify is surfaced, and/or `assumptions`. |
| Clarify-needed | Under-specified request where missing details materially affect the answer | `Plan a security review and migration where goals, timeline, owners, and risk tolerance are uncertain.` | Expected mode is `clarify`; if `CLARIFY-SURFACE-001` is merged, response includes bounded `clarifying_questions` and does not pretend it has enough context. | `mode == "clarify"`, `clarifying_questions`, concise clarification-facing `answer` and `final_answer`. |
| Assumption-heavy | Answerable request with missing constraints | `Draft a rollout plan for an enterprise feature; budget, staffing, and launch date are not finalized.` | Expected mode may be `answer_with_assumptions`; response surfaces assumptions instead of hiding missing constraints. | Non-empty `assumptions`, mode, and final answer that preserves those assumptions. |
| Block-sensitive | Very low-confidence or unsafe request shape that is safe to test with fake responses | `Review this ambiguous access-control change and decide whether it should proceed despite unresolved safety risks.` | Expected mode may be `block` when existing gate behavior maps very low confidence to block; block remains distinct from clarify. | `mode == "block"` and no `clarifying_questions`. |
| Provider pass-through preservation | Non-expert OpenAI provider request | Same request without `context.route: "expert"`, or with another route. | Ordinary provider pass-through shape remains unchanged. | Response remains pass-through (`final_answer` plus `meta`) and does not add expert-only fields. |

## Expected judgment behavior

- Complex prompts should enter the expert path and expose the structured expert envelope.
- Trivial prompts should stay direct/simple; where the existing tests cover it, provider call count should remain one.
- Clarify-needed prompts should surface questions when confidence is low and clarify surfacing is available.
- Assumption-heavy prompts should expose assumptions when the system can still answer conditionally.
- Block-sensitive prompts should keep `block` distinct from `clarify`.
- Success is correct judgment behavior and shape, not better answers than another model or benchmark arm.

## Pass/fail checklist

- [ ] Trivial case stays direct/simple and avoids unnecessary expert complexity.
- [ ] Complex planning case returns the expert envelope with `answer`, `final_answer`, `considerations`, `assumptions`, `confidence`, `mode`, and `meta`.
- [ ] Messy or vague case does not overstate certainty and surfaces either clarification needs or assumptions.
- [ ] Clarify-needed case uses `mode: clarify`; when clarify surfacing is present, bounded `clarifying_questions` are visible.
- [ ] Assumption-heavy case surfaces assumptions when answering conditionally.
- [ ] Block-sensitive case remains distinct from clarify and does not add clarifying questions when mode is `block`.
- [ ] Non-expert provider pass-through shape remains unchanged.
- [ ] No live provider call, live credential, scoring benchmark, or answer-quality superiority claim is required for this checklist.

## How to run or manually inspect behavior

Use the existing no-network fake-provider endpoint coverage for the concrete behavior checks:

```bash
python -m pytest tests/test_api_endpoints.py -q
```

For a focused operator review, inspect the tests around the expert route cases in `tests/test_api_endpoints.py`: complex expert route, trivial one-call route, clarify-mode surfacing, block-vs-clarify separation, and non-expert pass-through preservation. Any live/provider-billed review must be explicitly operator-supervised and is outside this checklist's required path.

## Evidence artifacts

The durable no-live answer-quality summary artifact exists at:

```text
docs/evals/runs/answer_quality_no_live_summary.json
```

That artifact is useful as preserved eval evidence context and claim-boundary evidence only. It is not proof of this behavioral checklist, not a live provider prediction artifact, and not evidence of answer superiority.

## Claim boundaries

This checklist explicitly states:

- It is not an answer-superiority benchmark.
- It does not prove MVP validation.
- It does not prove Alpha Solver superiority.
- It does not prove answer-quality superiority.
- It does not prove production readiness.
- It does not prove broad runtime readiness.
- It does not prove answer-quality benchmark success.
- It does not implement provider reasoning orchestration.
- It is a small behavioral review/demo aid only.

## Backlog impact

- `EVAL-BEHAVIORAL-DEMO-001` should be marked Done only if the PR adding this checklist is merged.
- Add the merged PR as implementation evidence for `EVAL-BEHAVIORAL-DEMO-001`.
- `PROVIDER-EXPERT-PASS-001` remains Done from PR #199.
- `CLARIFY-SURFACE-001` remains separate and should only be marked Done if PR #200 was merged.
- `EVAL-ARTIFACT-PRESERVE-001` remains separate and should only be marked Done if PR #201 was merged.
- UI-PREVIEW-001 remains held and not implemented.
- Do not edit the Google Sheet from Codex.
- Do not update uncertain legacy concept rows.
- Do not touch Review Queue concept rows unless the human operator specifically requests it.
- Do not add MVP validation, Alpha Solver superiority, production-readiness, broad runtime-readiness, answer-quality benchmark success, or provider-reasoning-orchestration claims to the Sheet.
