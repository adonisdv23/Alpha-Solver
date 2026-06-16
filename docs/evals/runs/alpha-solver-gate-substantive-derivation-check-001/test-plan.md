# Test Plan

## Test mode

This lane is docs-only. Tests can be static only for this PR. Future execution may add deterministic fixture tests if a separate lane authorizes fixtures or checker code.

No provider, local model, runtime endpoint, external service, dashboard, public API, `/v1/solve`, Google Sheets, scoring, unblinding, source-map, dependency installation, or release implementation test is authorized by this lane.

## Existing safe tests

The repository already contains a deterministic no-echo substantive gate with synthetic fixtures. Those tests are safe to run because they do not call providers, local models, runtime endpoints, or external services.

## Pass criteria for this gate spec

This docs gate passes if:

- required packet files exist;
- criteria define exact echo, near echo, paraphrase-only response, substantive derivation, acceptable source text use, unsupported copying, and examples;
- fixture plan includes positive and negative fixture categories, frozen text rules, and expected labels;
- heuristic spec includes overlap ratio, copied-span ratio, added-reasoning markers, source-preserving transformed markers, non-answer safe-out markers, and the proof boundary;
- stop conditions and non-actions preserve the hard boundaries;
- source-of-truth docs agree on `OPERATOR_REVIEW_REQUIRED_AFTER_SUBSTANTIVE_DERIVATION_CHECK_001`;
- changed Markdown passes narrative claim-safety lint;
- `git diff --check` passes.

## Fail criteria

The gate fails if any packet file is missing, if source-of-truth docs disagree on selected-next state, if raw Alpha or baseline outputs are inspected, if scores are changed, if providers or local models are run, if runtime or public API behavior is changed, if dependencies are added, or if the packet makes broad value, readiness, benchmark, provider, local-model, security/privacy, production, public, partnership, Pi.dev integration, or Alpha-superiority claims.

## Tests added

No new tests are added in this PR. The lane is review-only and the existing deterministic no-echo tests already cover the safe local checker history. Future fixture or checker changes should add focused tests in the existing safe no-echo test area if authorized.
