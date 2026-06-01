# CLARIFY-SURFACE-001 · Expert Route Clarify Surface

## Purpose

Surface bounded clarification questions when the opt-in OpenAI expert route returns `mode == "clarify"`. This is a narrow follow-up to `PROVIDER-EXPERT-PASS-001` and keeps default local/offline behavior and ordinary OpenAI pass-through behavior unchanged.

## Scope

- Applies only to `/v1/solve` requests with `MODEL_PROVIDER=openai` and `context.route == "expert"`.
- Applies only when the existing expert confidence/gate mapping produces `mode == "clarify"`.
- Adds stable `clarifying_questions` to the expert envelope in clarify mode.
- Sets `answer` and `final_answer` to a concise clarification-facing message in clarify mode.
- Preserves `considerations`, `assumptions`, `confidence`, and `meta` from the expert envelope.
- Does not add a provider call for clarification question generation.

## Existing clarify/template machinery inspection result

The repository has clarify modules under `service/clarify/` and the `NEW-009` spec entry, but that machinery is not reused for this lane because it is broader than the provider expert-route path and currently renders one template-oriented question from router-style payload flags. The expert-route surface needs 2 to 4 deterministic questions derived from the expert preview request context without rewiring unrelated routing, UI, eval, or provider behavior.

This lane therefore uses a small local fallback in `service/app.py`, scoped to expert-route clarify mode only.

## Response shape

Clarify-mode expert responses include the existing expert envelope fields plus `clarifying_questions`:

```json
{
  "final_answer": "I need a few details before I can answer this well.",
  "answer": "I need a few details before I can answer this well.",
  "clarifying_questions": [
    "What is the main outcome you want from this request?",
    "What constraints or context should I preserve?",
    "What tradeoffs or priorities matter most?"
  ],
  "considerations": [],
  "assumptions": [],
  "confidence": 0.35,
  "mode": "clarify",
  "meta": {
    "route": "expert",
    "complexity": "complex",
    "provider": "openai",
    "model": "...",
    "call_count": 2
  }
}
```

The exact question wording may vary, but it must remain deterministic, bounded, and no-network.

## Validation expectations

No-network tests with fake provider clients should prove:

- complex expert-route clarify mode includes `clarifying_questions`;
- `answer` and `final_answer` are clarification-facing and not final-answer text;
- complex clarify mode remains exactly two provider calls;
- trivial expert mode remains one provider call and does not add `clarifying_questions`;
- non-expert OpenAI pass-through response shape remains unchanged;
- local/offline behavior remains unchanged;
- block mode remains distinct from clarify mode;
- responses do not leak secrets, raw provider request bodies, raw provider response bodies, raw prompts, credentials, authorization headers, or raw provider metadata.

## Non-goals and claim boundaries

- No MVP validation claim.
- No Alpha Solver superiority claim.
- No answer-superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No provider reasoning orchestration claim.
- No UI preview.
- No behavioral demo checklist.
- No eval artifact preservation.
- No eval benchmark work.
- No live provider tests.
- No provider reasoning planning, verify-revise loop, fan-out, re-synthesis, or broad provider architecture change.
