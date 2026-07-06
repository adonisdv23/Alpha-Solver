# ALPHA-SOLVER-TOT-ECHO-HONESTY-HOTFIX-001 · Local ToT Echo/Template Honesty Hotfix

Status: Implemented

Answer-integrity lane: make local deterministic output honest, not smarter.

## Goal

Prevent the local deterministic Alpha Solver paths from returning
non-substantive artifacts — exact/normalized prompt echo, ToT
template-prefixed strings (`Rephrase:`, `Decompose:`, `Edge cases:`,
`Counterpoints:`, `Summarize:`), and CoT fallback wrappers around the prompt —
as if they were real answers. When the local path cannot synthesize, it must
return a bounded SAFE-OUT-style response with diagnostics explaining why.

## Motivation (repo evidence)

- `alpha/reasoning/tot.py` `TEMPLATE_FUNCS` builds branch contents by
  prefixing the prompt; the best node's content is returned as `answer`.
- The previous guard in `alpha/solver/observability.py` caught only exact
  normalized prompt echo. Live leak paths on current main:
  - SAFE-OUT CoT fallback shipped `To proceed, consider: <query>`
    (`alpha/reasoning/cot.py`) as `final_answer` whenever ToT confidence fell
    below the threshold, while `solution` carried the raw prompt echo.
  - ToT cache hits returned arbitrary stored `answer` text with no honesty
    check, so stale/poisoned caches could surface `Rephrase: <query>`.
  - No code anywhere checked the five template prefixes in a final answer.

## Scope

- `alpha/solver/observability.py`: broaden the exact-echo guard into
  `_enforce_local_output_honesty` with an explicit artifact classifier
  (`_classify_local_artifact`: `prompt_echo` / `template_branch` /
  `cot_template`; no fuzzy heuristics). Supported fixture derivations are
  preserved; unsupported artifacts become bounded SAFE-OUT text. Diagnostics
  record `echo_detected`, `template_branch_detected`, `answer_kind`,
  `synthesis_available`, `raw_echo_answer` / `raw_template_answer`, and
  stable `reason` / evidence labels.
- `alpha/reasoning/tot.py`: mark deterministic search output as
  non-synthesized at the source (`answer_kind` = `prompt_echo` /
  `template_branch` / `cached_search_artifact`; `synthesis_available: False`).
  Additive metadata only; search behavior unchanged.
- `alpha_solver_portable.py`: light standalone mirror
  (`portable_local_output_honesty`, `PORTABLE_LOCAL_ARTIFACT_PREFIXES`,
  `PORTABLE_LOCAL_UNSUPPORTED_SAFEOUT`) applied to the portable local
  deterministic path only. No repo imports; the PR #646 Substantive Lift
  Contract text and `check_substantive_lift` semantics are untouched.

## Non-goals

- Does not make local ToT smarter; local deterministic synthesis remains
  unavailable without a model, and that boundary is now stated in output.
- No provider, hosted-model, or local-model calls; no network calls.
- No route/persona activation, no scoring, ranking, blinding, or unblinding.
- No new canned answers: the four existing supported fixture derivations are
  preserved exactly and none are added.
- No `/v1/solve`, dashboard, or API exposure changes.
- No benchmark, readiness, production, provider-validation,
  local-model-validation, or Alpha-superiority claims.

## Code Targets

- `alpha/solver/observability.py`
- `alpha/reasoning/tot.py`
- `alpha_solver_portable.py`
- `tests/test_alpha_local_runtime_honesty.py`

## Test Plan

`tests/test_alpha_local_runtime_honesty.py` (failing before the patch,
passing after): unsupported high-headroom prompts never echo and never start
with blocked prefixes across default, CoT-fallback, and multi-branch configs;
bounded SAFE-OUT text and diagnostics on replacement; the live CoT-fallback
leak is bounded; poisoned-cache template answers are bounded; the four
supported fixture prompts keep prior behavior; the guard injects no lift-block
labels (low-headroom precedence intact); classifier unit coverage for single,
chained, echo, and legitimate inputs; portable path artifact-free across
seeds; portable helper standalone behavior.

## Acceptance Criteria

Covered 1:1 by the test plan above plus existing suites:
`tests/test_alpha_no_echo_wiring.py`, `tests/test_alpha_substantive_lift_contract.py`,
`tests/test_alpha_minimal_behavior_contract.py`, `tests/reasoning`,
`tests/policy`, `tests/observability`, `tests/test_tot_determinism.py` all
pass unchanged.

## Definition of Done

Guard, metadata, portable mirror, tests, and this spec merged; focused and
full validation pass; all boundaries above hold. A passing run means only
that the configured honesty rules held; it is not a quality judgment.
