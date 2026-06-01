# PROVIDER-EXPERT-PASS-001 · Opt-in Expert Provider Pass

## Purpose

Add an explicitly opt-in expert pass for complex OpenAI provider requests. The pass is a supervised preview surface for callers that ask for the `expert` route and does not change local/offline defaults or ordinary OpenAI provider pass-through.

## Non-goals

- No production readiness claim.
- No MVP validation claim.
- No answer-superiority claim.
- No provider multi-step planning system beyond the fixed pass described here.
- No verify-revise loop.
- No fan-out.
- No re-synthesis.
- No UI work.
- No eval benchmark work.
- No clarify-template rendering or full clarify surface behavior.
- No portable provider, CLI, hosting, billing, budget persistence, fallback, or observability expansion.

## Boundary

- Complex expert requests make exactly two fixed model calls.
- Trivial expert requests make exactly one provider call.
- There are no loops.
- There is no per-sub-question fan-out.
- There is no re-synthesis.
- The complexity decision is deterministic and uses local heuristics only.
- Default `MODEL_PROVIDER=local` behavior remains local/offline.
- OpenAI provider pass-through remains unchanged unless the caller explicitly requests the expert route.

## Opt-in behavior

The initial seam is `context.route == "expert"` on `/v1/solve` while `MODEL_PROVIDER=openai` is explicitly enabled. This seam is already accepted by the request context and maps onto existing provider request metadata, so it avoids adding `expert` to the `strategy` enum and preserves the existing OpenAPI strategy contract.

No environment flag is added in this lane. The context route is explicit, request-scoped, and testable with fake provider clients.

## Complexity gate

The gate is cheap, deterministic, and no-network. It may consider:

- prompt length;
- multi-part markers;
- decision, review, and planning markers;
- domain or expert markers;
- ambiguity and uncertainty markers.

Gate outcomes:

- `trivial`: one direct provider call;
- `complex`: one preview call followed by one answer call conditioned on the preview.

## Complex expert path

Step 1 requests compact JSON containing:

- considerations;
- assumptions;
- self-rated confidence from `0` to `1`.

Step 2 answers the user request using the normalized Step 1 considerations and assumptions.

The pass reuses the configured provider client, `ProviderRequest`, `ProviderResult`, provider telemetry, provider accounting, and provider SAFE-OUT handling used by the existing OpenAI provider path.

## Self-rating caveat

The confidence value is a model self-rating for supervised preview. It is not calibrated. Gate behavior and assumption surfacing are the hedges for this MVP lane. Calibration is out of scope.

## Confidence-to-mode mapping

The expert envelope exposes one of:

- `direct`;
- `answer_with_assumptions`;
- `clarify`;
- `block`.

The service adapts the existing gate helper where practical. Very low self-ratings may map to `block`; low or mid-band self-ratings may map to `clarify`; higher ratings with assumptions may map to `answer_with_assumptions`; otherwise the mode is `direct`.

If mode is `clarify`, this lane only returns the mode in the envelope. It does not render clarify templates or implement the full clarify surface.

## Response envelope

Expert-route responses return a structured envelope and retain `final_answer` as a compatibility alias:

```json
{
  "final_answer": "...",
  "answer": "...",
  "considerations": [],
  "assumptions": [],
  "confidence": 0.0,
  "mode": "direct",
  "meta": {
    "route": "expert",
    "complexity": "trivial",
    "provider": "openai",
    "model": "...",
    "call_count": 1
  }
}
```

The envelope must not include secrets, raw provider request bodies, raw provider response bodies, raw prompts, credentials, authorization headers, exception dumps, or provider raw metadata.

## Forbidden wording

The response envelope, code comments, tests, and this spec must not emit the prohibited multi-step-provider label named in the lane request. This spec avoids spelling that label out so repository search can detect accidental drift.

## Validation expectations

Tests must use fake provider clients and must not require OpenAI credentials or network calls. Coverage should prove:

- complex expert route call count is exactly two;
- trivial expert route call count is exactly one;
- complex expert envelopes include non-empty answer, considerations, confidence, and mode;
- assumption-bearing modes include assumptions;
- OpenAI opt-out pass-through shape remains unchanged;
- local/offline behavior remains unchanged;
- expert envelopes do not leak secrets or raw provider metadata;
- expert responses do not emit the prohibited label.
