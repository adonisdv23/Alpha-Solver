# Alternatives not selected

## 1. Implementation bug

Not selected.

The current code explicitly blocks the bounded startup-plan answer-with-assumptions route when `_assumption_gate_failed_reason_codes` returns any reason. The same code emits `missing_information_too_broad` when there are more than two missing-information entries. The retry 007 gate trace matches that behavior, so the evidence does not show a narrow mismatch between intended deterministic behavior and observed behavior.

## 2. Deterministic scanner false positive

Not selected.

The failure was not caused by acceptable final answer text being rejected by a scanner/parser. Pass 2 was not called, no final answer was rejected, and the preserved reason code was an assumption-gate breadth decision rather than a scanner false positive.

## 3. Pass 2 model output limitation

Not selected.

The Prompt 3 gate trace records `pass_two_called=false`. Because Pass 2 did not run, the observed failure cannot be attributed to Pass 2 model output.

## 4. `qwen2.5:3b` local-model behavior limitation

Not selected as the primary classification.

The source artifact was produced with `qwen2.5:3b`, and the model's Pass 1 output was part of the observed path. However, the decisive failure reason is the deterministic gate's current handling of the parsed missing-information breadth. The classification question is whether the smoke should still expect `answer_with_assumptions` when that guard fires, not whether the local model is broadly capable.

## 5. Prompt expectation mismatch requiring spec review

Selected.

This is best supported because the implementation appears to have behaved according to the current guard and spec safety preference, while the smoke expectation still required a different mode for Prompt 3.

## 6. Artifact blocked/incomplete

Not selected.

The import packet confirmed the artifact is parseable and complete enough for interpretation. It preserved five results, provenance, command status, loopback/local metadata, no-provider-key and no-hosted-fallback boundaries, and safe gate traces.
