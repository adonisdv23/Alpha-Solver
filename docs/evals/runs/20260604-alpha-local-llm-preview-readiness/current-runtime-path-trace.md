# Current Runtime Path Trace

Lane ID: `ALPHA-LOCAL-LLM-PREVIEW-READINESS-001`

Status: trace only; no runtime execution performed.

## `/dashboard/expert-preview` request path

1. `service/app.py` conditionally mounts dashboard routes when dashboard auth configuration is enabled.
2. `alpha/webapp/routes/expert_preview.py` renders the authenticated expert-preview page.
3. On submit, the preview route calls `_solve_preview(request, prompt, expert=False)` for the plain pane and `_solve_preview(request, prompt, expert=True)` for the expert pane.
4. `_solve_preview()` lazily imports `SolveRequest` and `solve` from `service.app` and then calls `await solve(SolveRequest(query=prompt, context=context), request)`.
5. Provider accounting is captured only through the safe accounting sink, and public metrics are merged into the preview payload if records exist.

## Plain vs expert pane path

- **Plain pane:** `_solve_preview(..., expert=False)` uses an empty context dict. It calls the shared `solve()` function with only the sanitized prompt and no expert route marker.
- **Expert pane:** `_solve_preview(..., expert=True)` sets `context["route"] = "expert"` before calling the same shared `solve()` function.
- In OpenAI provider mode, `service.app.solve()` detects `context.route == "expert"` and uses the expert-preview flow, which may perform a Step 1 considerations/assumptions/confidence request and a Step 2 answer request for non-trivial prompts.
- In local mode, `service.app.solve()` strips `context.route` through `_local_solver_params()` before calling the deterministic local solver. Therefore the expert pane does not become a portable-contract LLM execution merely because `context["route"] = "expert"` was set.

## Where `context["route"] = "expert"` is set

`context["route"] = "expert"` is set inside `alpha/webapp/routes/expert_preview.py` in `_solve_preview()` when the route is called with `expert=True`.

## `/v1/solve` path

1. `service.app.solve()` receives `SolveRequest` at `POST /v1/solve`.
2. The query is sanitized.
3. `params = req.context or {}` and `strategy = req.strategy or params.get("strategy")` are computed.
4. If `MODEL_PROVIDER=openai`, provider execution is enabled and the code builds a `ProviderRequest` from query, system prompt if supplied, model set, route metadata, and request metadata.
5. If `context.route == "expert"` in OpenAI mode, the provider-backed expert flow is used.
6. If `MODEL_PROVIDER` is anything other than `openai`, the code uses local/offline execution: `strategy == "react"` calls `run_react_lite`; otherwise `_tree_of_thought(query, **_local_solver_params(params))` is called.
7. The local/offline result is returned directly as JSON.

## Current local provider path

With `MODEL_PROVIDER=local` or an unset `MODEL_PROVIDER`:

1. `service.app._is_openai_provider_enabled()` returns false.
2. The code does not instantiate `OpenAIProviderClient` and does not use the provider path.
3. For most requests, the code calls `_tree_of_thought()` imported from `alpha_solver_entry.py`.
4. `alpha_solver_entry.py` lazily loads `alpha-solver-v91-python.py` from disk and re-exports `_tree_of_thought`, `AlphaSolver`, and `get_solver`.
5. `alpha-solver-v91-python.py` executes deterministic Tree-of-Thought behavior through the modular solver classes.
6. `alpha_solver_portable.py` does not appear in this call chain.

## Where entrypoint files appear

| File | Current role in traced path | Appears in `/dashboard/expert-preview` local mode? | Appears in `/v1/solve` local mode? | Consumes portable contract? |
| --- | --- | --- | --- | --- |
| `alpha_solver_entry.py` | Lazy bridge that loads v91 file and exposes `_tree_of_thought`. | Yes, through `service.app` import. | Yes, through `service.app` import. | No. |
| `alpha-solver-v91-python.py` | Deterministic Tree-of-Thought implementation loaded by `alpha_solver_entry.py`. | Yes, through `_tree_of_thought`. | Yes, through `_tree_of_thought`. | No. |
| `alpha_solver_portable.py` | Portable prompt/spec monolith intended for manual portable-surface use. | No proven role in current local preview path. | No proven role in current `/v1/solve` path. | Not by current runtime path. |

## Likely source of prompt-echo behavior

The local preview prompt-echo observation should be treated as a blocked/invalid surface symptom. Based on the current wiring, it likely came from the smoke-oriented local/offline path or deterministic placeholder-like behavior rather than from a local LLM consuming the portable Alpha contract. This readiness spike did not reproduce the behavior and does not import screenshots or outputs as evidence.
