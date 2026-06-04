# Post-Improvement Run Plan

Status: planning only

No capture, provider calls, scoring, or rescoring is performed here. This packet plans a valid future measurement path for PR #263 without changing runtime behavior, provider behavior, model configuration, routing, `/v1/solve`, scoring rubrics, Sheets, or Batch C.

## Purpose

Measure whether PR #263's portable minimal behavior contract improves answer shape, claim boundaries, and artifact stop-condition behavior without destroying substantive lift.

## Evidence basis

- PR #251: Batch B pilot scored artifacts were populated under `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/`.
- PR #252: Batch B interpretation review documented that the limited 12-comparison pilot favored Alpha while preserving conservative claim boundaries.
- PR #253: Post-interpretation decision artifacts chose further planning rather than validation or production-readiness claims.
- PR #254: Alpha brevity-control planning spec identified brevity/control risks, including Batch B brevity weakness.
- PR #255: Batch B lift-vs-polish diagnostic plan separated substantive lift from polish and brevity concerns.
- PR #256: Alpha selective expert engagement planning memo scoped expert engagement without implementing provider orchestration.
- PR #257: Alpha claim-boundary calibration planning packet constrained unsupported claims.
- PR #258: Alpha answer-structure V2 planning spec prepared answer-shape improvements without changing runtime.
- PR #259: Complexity-gradient holdout planning packet defined future holdout slots without final prompt text in this packet.
- PR #260: Alpha implementation surface map identified the portable contract as a candidate implementation surface.
- PR #261: Implementation-readiness review and decision matrix supported a minimal portable behavior-contract path.
- PR #262: Offline contract tests and fixtures were added for minimal Alpha behavior-contract cases.
- PR #263: `alpha_solver_portable.py` implemented the minimal Alpha behavior contract and `minimal_behavior_contract_summary()` without changing provider/model/routing behavior, `/v1/solve`, scoring rubrics, scored artifacts, capture scripts, Sheets, or Batch C.

## Measurement design options

### Option A: Portable surface diagnostic

- Load `alpha_solver_portable.py` as the Alpha system/behavior contract.
- Compare against plain provider output under a controlled prompt packet.
- Use the existing response-quality rubric and blind scoring procedure.
- Requires a future frozen packet and approved capture.
- Validity: valid for measuring PR #263 if the Alpha condition explicitly loads the portable contract and the scorer packet remains blinded.

### Option B: Runtime `/v1/solve` diagnostic

- Only valid if `/v1/solve` consumes the changed portable contract.
- The inspected endpoint currently uses provider mode or the modular/reference local solver path through `alpha_solver_entry.py`; it does not show a call into `alpha_solver_portable.py`.
- Therefore, this option is invalid for measuring PR #263 unless a future approved change wires the endpoint to the portable contract or proves an existing binding.
- Do not run this option in this PR.

### Option C: Offline contract compliance expansion

- Expand offline tests without live provider calls.
- Valid for contract compliance, artifact stop-condition behavior, and summary-helper checks.
- Not valid as output-quality measurement, runtime API measurement, provider behavior evidence, or benchmark evidence.
- This can be a safe future lane if the operator wants more offline assurance before live capture planning.

### Option D: Complexity-gradient holdout

- Use the PR #259 slot plan to create a future frozen prompt packet.
- Do not include final prompts here.
- Best for future robust measurement after operator approval because it can reduce overfitting to A3-1 and Batch B prompts while preserving the same evaluation discipline.

## Recommended measurement path

Recommended next lane: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`.

The next lane should create a frozen prompt packet and capture packet for a portable-surface diagnostic. It should explicitly instruct the Alpha condition to load `alpha_solver_portable.py` as the behavior contract, preserve blinding, avoid final scoring until after capture, and avoid any runtime/provider/model/routing changes.

## Prompt reuse policy

- Existing A3-1 and Batch B prompts may be design references.
- Existing A3-1 and Batch B prompts should not be the only post-improvement proof because planning and implementation used them heavily.
- Complexity-gradient slots should guide fresh frozen prompts.
- Final prompt text should be created in a separate PR to reduce contamination and to keep this packet planning-only.

## Scoring and blinding plan

- Use the same 14 response-quality rubric dimensions unless a separate approved PR changes the rubric.
- Keep the scorer-facing packet blinded.
- Keep the operator-only unblinding map separate until scoring is complete.
- Preserve score tables, defect notes, source packets, capture notes, and artifact checks.
- Compute lift, polish, and brevity clusters after scoring and approved unblinding.
- Include token/length fields if feasible without exact-billing claims.
- Do not unblind before scoring.

## Success criteria, planning only

Tentative success criteria for a future approved measurement:

- Improved or non-worse brevity on concise prompts.
- Preserved claim-boundary and evidence-uncertainty dimensions.
- Fewer invented scaffolding defects.
- Correct artifact stop-condition behavior.
- No broad validation or superiority claims.
- No regression in substantive lift dimensions.

## Not authorized

- No capture.
- No provider calls.
- No final prompts.
- No scoring.
- No rescoring.
- No runtime changes.
- No provider/model/routing changes.
- No Sheet update.
- No Batch C.

## Non-claims

This packet does not claim:

- MVP validation.
- Alpha Solver superiority generally.
- Broad plain-provider inferiority.
- Answer-quality superiority generally.
- Production readiness.
- Broad runtime readiness.
- Benchmark success.
- Exact billing accuracy.
- Provider reasoning orchestration.
