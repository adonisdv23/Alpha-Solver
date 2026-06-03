# OUTPUT-DIFF-A3-LIVE-CAPTURE-MODELSET-001 · A3 Live Capture Model Set

## Purpose

Provide an explicit live-capture model set for the A3 output-differentiation
capture lane so operator-supervised A3 runs do not rely on the existing
`cost_saver` 1024-token output budget.

## Background

During diagnostic-only investigation of the blocked A3-1 capture, the HHE-009
plain `/v1/solve` surface under `MODEL_SET=cost_saver` reached the OpenAI
Responses API output cap before a complete answer was available:

- model: `gpt-5-mini-2025-08-07`
- response status: `incomplete`
- incomplete reason: `max_output_tokens`
- configured `max_output_tokens`: `1024`
- output tokens: `1024`
- reasoning tokens: `768`
- `_text_from_payload` extracted text when text existed

The prior clean A3-1 attempt stopped on HHE-009 plain with HTTP 502 SAFE-OUT:
`Provider returned an empty answer.` This indicates a live-capture output-budget
configuration blocker, not the PR #237 sanitizer false positive and not a text
extraction bug when provider text exists.

## Scope

Add a dedicated model set named `a3_live_capture` in
`service/config/model_sets.yaml`.

The model set must:

- use `provider: openai`;
- use the same model family as `cost_saver` unless a later operator-approved spec
  changes it;
- set `max_tokens` to at least `4096`;
- set `timeout_ms` to at least `60000`;
- use price hints consistent with the selected model family.

## Non-goals

- Do not modify `default`.
- Do not modify `cost_saver`.
- Do not change production defaults.
- Do not change OpenAI provider request/response behavior.
- Do not change prompt text or HHE prompt selection.
- Do not run or implement A3-1 capture.
- Do not populate eval artifacts, score, unblind, update Google Sheets, or start
  Batch B.

## Acceptance Criteria

1. `ModelSetRegistry` loads `a3_live_capture` successfully.
2. `MODEL_SET=a3_live_capture` resolves to the configured provider, model,
   `max_tokens`, and `timeout_ms`.
3. `/v1/solve` can select `a3_live_capture` through the existing model-set
   selection path.
4. `ProviderRequest.max_tokens` maps to the `a3_live_capture` configured
   `max_tokens`.
5. Existing `default` and `cost_saver` model-set behavior remains unchanged.
6. Existing environment validation remains valid for supported provider settings.
7. Existing PR #237 sanitizer behavior remains covered by tests.
8. Existing PR #238 and PR #239 empty-answer guard behavior remains covered by
   tests.

## Operator Notes

A later fresh A3-1 capture may use this model set only after this config PR lands
and any applicable operator bookkeeping is completed. Previous failed-capture
partial outputs remain invalid and must not be reused.
