# Recommended Integration Order

## Required order

1. `local expert two-pass`
2. `local orchestration envelope`
3. `local confidence/clarify/block gates`
4. `local ToT-lite`
5. `/v1/solve exposure later`
6. `dashboard exposure later`

## Rationale

### 1. Local expert two-pass

Start with the highest-value response-shaping surface because the existing expert route already separates analysis-style metadata from final answer construction. A local version can directly improve answer structure by first extracting considerations, assumptions, and confidence, then asking the local model to answer with those constraints.

### 2. Local orchestration envelope

After local two-pass exists, wrap the result in a local orchestration envelope so downstream evidence stays structured. This should happen before API/UI exposure so provenance, status, confidence, mode, assumptions, and boundaries are stable.

### 3. Local confidence/clarify/block gates

Next integrate deterministic mode selection so low-confidence, missing-confidence, or unsafe output is not presented as a normal answer. This should be local-only and fail closed without provider fallback.

### 4. Local ToT-lite

Then add bounded local ToT-lite only after the two-pass and gate envelope can contain extra candidates, timeouts, and failure modes. This avoids multiplying local calls before the core local answer contract is stable.

### 5. `/v1/solve` exposure later

Production `/v1/solve` exposure must remain blocked until local orchestration implementation and a focused local orchestration smoke pass prove the local path can produce the new local envelope without provider fallback or boundary drift. The current spec explicitly blocks `/v1/solve` for local LLM mode until a later lane authorizes it.

### 6. Dashboard exposure later

Dashboard exposure must remain blocked until local orchestration implementation and smoke pass because the UI is a review surface that can be mistaken for readiness or quality validation. It should consume a stable local orchestration result only after the local API contract is settled in a separate lane.

## Provider fallback boundary

Provider fallback must remain blocked unless a separate explicit hybrid lane authorizes it. The local LLM spec prohibits silent hosted-provider fallback and requires any later fallback lane to define operator opt-in, trigger conditions, hosted-provider credentials, provenance labels, and tests.
