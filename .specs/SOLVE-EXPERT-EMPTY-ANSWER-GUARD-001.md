# SOLVE-EXPERT-EMPTY-ANSWER-GUARD-001 - Expert Route Empty Primary Answer Guard

## Goal

Prevent the expert-route `/v1/solve` response assembly path from returning HTTP 200 with empty `final_answer` / `answer` when the Step 2 provider call succeeds but its extracted answer text is empty or whitespace.

## Root cause

The complex expert route performs a Step 1 preview call, selects a mode, then performs a Step 2 answer call. `_primary_expert_answer` strips the Step 2 text and returns approved deterministic fallbacks only for narrow `answer_with_assumptions` cases. If Step 2 text is empty or unextractable and no approved deterministic fallback applies, the empty provider text can continue into `_expert_response`, which serializes the empty string into both `final_answer` and `answer` under HTTP 200.

## Scope

- Add a minimal runtime guard in the complex expert-route `/v1/solve` response assembly path.
- When the assembled primary expert answer is empty after existing clarify, block, and approved fallback handling, return a typed provider SAFE-OUT-style response instead of a successful empty expert envelope.
- Preserve existing expert clarify behavior.
- Preserve existing expert block behavior.
- Preserve existing trivial expert-route behavior.
- Preserve non-empty direct expert-route pass-through behavior.
- Preserve plain `/v1/solve` behavior outside the focused empty-output guard.
- Add focused fake-provider tests for the empty Step 2 path, no-secret/no-raw-payload response safety, and non-empty expert pass-through preservation.

## Non-goals

- No A3-1 capture execution.
- No reuse of partial failed-capture outputs.
- No scoring or unblinding.
- No eval artifact population.
- No Google Sheets updates.
- No Batch B work.
- No provider prompt refactor.
- No broad routing, SAFE-OUT, budget, telemetry, replay, or SolverEnvelope refactor.
- No claims of MVP validation, Alpha Solver superiority, answer-quality superiority, production readiness, broad runtime readiness, benchmark success, exact billing accuracy, or provider reasoning orchestration.

## Safety requirements

The empty-answer guard response must not leak API keys, authorization headers, bearer tokens, raw provider payloads, raw provider metadata, raw prompts, raw system prompts, raw user query dumps, exception strings, tracebacks, environment dumps, config dumps, or unsafe internal metadata.

## Acceptance criteria

- A complex expert-route request whose Step 1 preview yields high-confidence direct mode and whose Step 2 answer text is empty or whitespace does not return HTTP 200 with empty `final_answer` / `answer`.
- The empty Step 2 case returns a safe non-empty SAFE-OUT-style response or typed safe failure response.
- The empty Step 2 response is allowlist-shaped and redacted.
- Non-empty complex expert-route direct answers still pass through.
- Existing clarify, block, trivial expert-route, and sanitizer false-positive behavior remains covered by tests.
