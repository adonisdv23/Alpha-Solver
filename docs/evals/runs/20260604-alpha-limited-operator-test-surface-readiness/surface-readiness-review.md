# Surface Readiness Review

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SURFACE-READINESS-001`

Status: docs-only review; no operator-test execution.

## Review boundary

This review determines surface readiness and evidence labels only. It does not run the limited operator test, import screenshot observations as results, call providers, measure `/v1/solve`, change runtime behavior, score outputs, rescore outputs, unblind artifacts, inspect operator-only maps, update Google Sheets, start Batch C, or make broad validation/readiness claims.

This review preserves two separate tracks:

1. Portable-contract manual simulation track: the already-approved operator-test packet remains a manual portable Alpha behavior-contract test. Its evidence can be valid for that manual simulation purpose when correctly labeled, but it is not product/runtime, `/v1/solve`, provider, benchmark-validation, MVP-validation, or production-readiness evidence.
2. Product/runtime execution-surface track: a separate future track needed only if the project wants product/runtime operator evidence. That track requires a future surface-fix/readiness lane and must not be inferred from the current manual packet.

## Findings

### 1. What `/dashboard/expert-preview` tests in `MODEL_PROVIDER=local`

In local mode, `/dashboard/expert-preview` tests the authenticated preview UI path, prompt extraction, two-pane rendering, and the ability to submit one plain request and one expert-route request through the shared `service.app.solve` function without enabling OpenAI.

The preview route sends:

- a plain request with an empty context; and
- an Alpha preview request with `context["route"] = "expert"`.

When `MODEL_PROVIDER=local`, `service.app.solve` does not enter the OpenAI provider branch. It strips local solver control keys such as `route`, then calls the deterministic local `_tree_of_thought` path imported from `alpha_solver_entry`.

Therefore local preview tests UI/local smoke continuity. It does not test provider-backed answer behavior and does not prove that the expert pane is executing the portable Alpha behavior contract. This local-preview blocker does not invalidate the separate manual portable-contract simulation track; it only blocks using the local preview as answer-behavior evidence.

### 2. Whether local mode is expected to echo or produce deterministic placeholder output

Local mode is expected to use deterministic local/offline solver execution rather than live provider calls. The local-smoke spec requires that the route render both panes for a simple prompt and preserve the prompt after submit; it explicitly avoids OpenAI enablement, live provider smoke, answer-quality claims, and superiority claims.

If the local deterministic solver produces output that looks like an echo or placeholder, that can still satisfy a UI smoke objective, but it is insufficient for behavior testing. Echo-like output should be treated as a blocked/invalid behavior-test surface rather than as an Alpha pass/fail result.

### 3. Whether `/dashboard/expert-preview` currently consumes `alpha_solver_portable.py`

No. The reviewed route lazily imports `SolveRequest` and `solve` from `service.app`, then calls `solve` for the plain and expert panes. `service.app` imports `_tree_of_thought` from `alpha_solver_entry`, and `alpha_solver_entry` loads `alpha-solver-v91-python.py`.

No reviewed preview path imports or calls `alpha_solver_portable.py`. The preview may display an “Alpha Solver expert preview” pane, but the current local path does not prove consumption of the portable behavior contract.

### 4. Whether `/v1/solve` currently consumes `alpha_solver_portable.py`

No. The reviewed `/v1/solve` endpoint is implemented in `service.app.solve`. In OpenAI mode, it builds provider requests and may execute the expert-route preview logic. In local mode, it calls `_tree_of_thought` from `alpha_solver_entry` after stripping `context.route`.

`alpha_solver_entry` loads `alpha-solver-v91-python.py`, not `alpha_solver_portable.py`. This review therefore does not treat `/v1/solve` as evidence for the portable Alpha behavior contract.

### 5. Whether the limited operator test can validly run on the current local preview

No. The current local preview can be used as a smoke path, but it is blocked for limited-operator behavior testing if it only echoes prompts or produces placeholder-like local output. Running the current packet on that local preview surface would risk importing UI-smoke behavior as answer-behavior evidence.

This does not mean the already-approved operator packet requires a product/runtime surface. The PR #273 packet defined a portable-contract manual test, and that scope should be preserved through a correctly labeled manual simulation lane.

The attempted local preview screenshots should remain non-results. They should not be classified as Alpha pass/fail results, scored, imported, or used to claim product/runtime readiness.

### 6. Whether a ChatGPT-project-thread test is product/runtime evidence

No. A ChatGPT project-thread test can be classified only as portable-contract prompt/manual simulation evidence. It may help inspect the portable prompt contract manually and is aligned with the current operator-test packet if correctly labeled. It does not test the repository's web UI, `/v1/solve`, provider adapters, routing, runtime configuration, capture path, accounting path, or product execution behavior.

### 7. What surface is required only if the lane changes to product/runtime operator testing

The current operator packet does not require a product/runtime surface because it is a portable-contract manual packet. If the project later wants product/runtime operator evidence, that separate future track requires an approved product execution surface that is proven, from repository wiring and/or an explicitly authorized implementation lane, to consume the intended Alpha behavior contract and produce substantive answers under controlled conditions.

Minimum required properties for that future product/runtime track:

- The surface must be an actual product/runtime surface, not only a ChatGPT prompt simulation.
- The surface must be proven to consume the intended Alpha contract for the test lane.
- It must produce substantive answer behavior, not prompt echoes or placeholder-only output.
- Any provider-backed execution must be separately authorized before enabling live provider access.
- Any `/v1/solve` use must be preceded by proof that `/v1/solve` consumes the intended Alpha contract for this test.
- The lane must preserve claim boundaries and avoid MVP validation, broad Alpha superiority, production-readiness, runtime-readiness, benchmark-success, exact-billing, provider-orchestration, self-healing, adaptive-learning, self-optimization, or autonomous-optimization claims.

## Surface-by-surface review

### Local supervised preview: `/dashboard/expert-preview` with `MODEL_PROVIDER=local`

#### What it tests

- Authenticated dashboard preview route availability when dashboard configuration allows mounting.
- Prompt extraction and preservation.
- Plain and Alpha-pane rendering.
- Shared `service.app.solve` invocation from the UI route.
- Local/offline deterministic execution without enabling OpenAI.
- That `context.route = "expert"` no longer crashes local mode because `route` is treated as a service/provider routing seam and stripped before local solver invocation.

#### What it does not test

- Portable Alpha behavior-contract execution via `alpha_solver_portable.py`.
- Live provider behavior.
- Provider orchestration.
- Runtime readiness for the limited operator test.
- Answer-quality benchmark success.
- Alpha-vs-plain superiority.
- Valid operator-test behavior if outputs are prompt echoes or placeholders.

#### Readiness conclusion

Valid only for smoke. Blocked for limited-operator behavior testing if it echoes prompts or emits placeholder/offline output rather than substantive answers.

### ChatGPT/manual prompt-contract surface

#### What it tests

- Manual simulation of the portable Alpha prompt/behavior contract.
- Operator-facing usefulness of the contract wording.
- Whether the contract appears answer-first, concise where appropriate, evidence-bounded, and claim-bounded in a manual thread.

#### What it does not test

- Product runtime behavior.
- Repository UI behavior.
- `/v1/solve` behavior.
- Provider adapter behavior.
- Routing behavior.
- Billing, accounting, capture, scoring, or production behavior.

#### Readiness conclusion

Valid as portable-contract/manual simulation evidence and aligned with the current operator-test packet if correctly labeled. It is not product/runtime evidence.

### Runtime `/v1/solve`

#### What it tests

- The service endpoint's configured runtime path.
- In local mode, deterministic local `_tree_of_thought` execution through `alpha_solver_entry`.
- In OpenAI mode, provider-backed execution with the service's provider request and expert-route logic, subject to authorization and configuration.

#### What it does not test in this lane

- The portable Alpha behavior contract unless a future repo change or proof shows `/v1/solve` consumes `alpha_solver_portable.py` or the intended contract for this operator test.
- The current limited operator test surface, because this lane did not measure `/v1/solve` and did not authorize runtime or provider execution.

#### Readiness conclusion

Not evidence for the current manual portable-contract packet. It should not be used as product/runtime operator-test evidence until a separate readiness/fix lane proves the endpoint consumes the intended Alpha contract under controlled conditions.

### Potential live provider preview

#### What it tests

- Provider-backed preview behavior through the product UI and shared service solve path.
- Same-provider plain output versus expert-route preview behavior under explicit OpenAI configuration.
- Request metrics display when provider accounting records are available.

#### What it does not test without further proof

- The portable Alpha behavior contract if the provider-backed prompt path is not shown to consume the intended contract.
- Production readiness, broad runtime readiness, broad answer-quality benchmark success, or Alpha superiority.

#### Readiness conclusion

Requires separate explicit authorization. Live provider preview must remain disabled unless a separate approved lane authorizes provider access, caps, configuration, and evidence handling.
