# MVP-CLOSEOUT-001 · MVP Tester Handoff and Readiness Packet

## 1. Purpose

This packet is a tester/operator handoff for the current Alpha Solver MVP lanes. It collects what landed, how to run no-network checks, how to inspect the supervised expert preview, where evidence artifacts live, and which claims are explicitly outside this closeout lane.

This document is intentionally narrow. It does not add runtime behavior, provider behavior, clarify behavior, eval behavior, preview UI behavior, live-provider tests, or product features.

## 2. MVP contents

The current MVP handoff covers these completed implementation lanes:

- `PROVIDER-EXPERT-PASS-001`: opt-in expert provider pass for complex OpenAI requests on `/v1/solve` when the request context selects `route: "expert"`.
- `CLARIFY-SURFACE-001`: clarify questions surfaced when the expert route produces clarify mode.
- `EVAL-ARTIFACT-PRESERVE-001`: no-live eval summary artifacts preserved under `docs/evals/runs/`.
- `EVAL-BEHAVIORAL-DEMO-001`: expert-pass behavioral demo checklist for operator review.
- `UI-PREVIEW-001`: authenticated plain-vs-expert preview UI for supervised operator comparison.

## 3. How to run local tests

Use the offline/local test path first. These commands should not require live provider credentials:

```bash
git diff --check
python -m pytest -q
```

Focused checks for this handoff and its underlying MVP lanes:

```bash
python -m pytest tests/test_api_endpoints.py -q
python -m pytest tests/test_answer_quality_eval.py -q
python -m pytest tests/ui/test_expert_preview.py -q
```

## 4. How to test the provider expert route

The provider expert route is exercised through `/v1/solve` with OpenAI provider mode explicitly enabled and request context containing `route: "expert"`. No live OpenAI call is required for the committed route tests; they use the repository fake provider client.

Expected route behavior to verify with the focused API tests:

- complex prompts use the expert route and return an expert envelope with `answer`, `final_answer`, `considerations`, `assumptions`, `confidence`, `mode`, and `meta`;
- trivial prompts remain direct/simple and avoid unnecessary expert complexity;
- non-expert provider requests preserve the ordinary provider pass-through shape;
- raw provider metadata, request IDs, authorization headers, bearer tokens, request bodies, response bodies, and secrets are not exposed in responses.

Run:

```bash
python -m pytest tests/test_api_endpoints.py -q
```

## 5. How to test clarify behavior

Clarify behavior is bounded to the expert-route response shape. When the expert route determines that the request is under-specified, it should return `mode == "clarify"`, a concise clarification-facing `answer`/`final_answer`, and a bounded `clarifying_questions` list.

Expected clarify behavior:

- clarify questions are surfaced only when clarify mode is produced;
- direct/trivial expert responses do not add clarify questions;
- block mode remains distinct from clarify mode and does not add clarify questions;
- clarify output does not expose raw provider metadata or secrets.

Run:

```bash
python -m pytest tests/test_api_endpoints.py -q
```

## 6. How to access and use the authenticated expert preview UI

The supervised preview route is:

```text
/dashboard/expert-preview
```

Usage expectations:

- Authentication is required before loading `/dashboard/expert-preview`.
- Logged-out users should be blocked and redirected to login by the dashboard auth flow.
- The plain pane means same-provider non-expert output.
- The expert pane means same-provider output with `context.route == "expert"`.
- The visible supervised-preview disclaimer must remain visible.
- Raw metadata, raw request bodies, raw response bodies, authorization headers, API keys, bearer tokens, and other secrets must not be exposed.
- The preview is for supervised comparison and explanation, not an automated quality judgment.

Run:

```bash
python -m pytest tests/ui/test_expert_preview.py -q
```

See also `docs/DASHBOARD_AUTH.md` for dashboard authentication setup and expectations.

## 7. How to use the behavioral demo checklist

Use `docs/evals/EXPERT_PASS_BEHAVIORAL_DEMO.md` as the compact behavioral demo checklist for operator review. It describes representative prompt shapes for trivial, complex planning, messy/vague, clarify-needed, assumption-heavy, block-sensitive, and provider pass-through cases.

The checklist is a review aid. It should be used to observe routing and envelope behavior, clarify behavior, assumptions, and block-vs-clarify separation. It is not a substitute for live evaluation or real user testing.

## 8. Where eval summary artifacts live

The durable no-live answer-quality summary artifact lives at:

```text
docs/evals/runs/answer_quality_no_live_summary.json
```

Use `docs/evals/ANSWER_QUALITY_EVAL.md` for the broader answer-quality eval procedure, including the distinction between no-live artifacts and gated live evaluation. The committed no-live artifact is preserved as evidence that the no-live eval summary path works; it is not proof of answer-quality performance.

## 9. What evidence exists

Current evidence for this MVP handoff includes:

- route-level `/v1/solve` tests for provider pass-through, expert route behavior, clarify mode, block-vs-clarify separation, and response secret redaction;
- authenticated preview UI tests for login gating, disclaimer visibility, plain-vs-expert rendering, same-provider routing, public metadata rendering, and secret redaction;
- answer-quality eval tests for dataset shape, dry-run/no-live behavior, durable summary artifact preservation, repeatability reporting, and claim-boundary language;
- `docs/evals/EXPERT_PASS_BEHAVIORAL_DEMO.md` as the operator-facing behavioral demo checklist;
- `docs/evals/runs/answer_quality_no_live_summary.json` as the durable no-live eval summary artifact.

## 10. What is not claimed

This handoff states the following claim boundaries explicitly:

- This is a tester/operator handoff.
- It does not prove MVP validation.
- It does not prove Alpha Solver superiority.
- It does not prove answer-quality superiority.
- It does not prove production readiness.
- It does not prove broad runtime readiness.
- It does not prove answer-quality benchmark success.
- It does not implement or claim provider reasoning orchestration.
- It does not replace live evaluation or real user testing.

## 11. Known limitations

- Expert preview is supervised/operator-facing.
- Confidence is a preview/self-rating or mode signal, not calibrated truth.
- No answer-quality superiority benchmark has been passed.
- Live provider use remains gated and should be operator-supervised.
- MVP behavior is bounded to the implemented lanes listed in this packet.
- Further hardening may be needed before production deployment.

## 12. Out-of-scope items

This closeout lane does not include:

- runtime behavior changes;
- provider expert-pass behavior changes;
- clarify behavior changes;
- eval artifact behavior changes;
- behavioral demo behavior changes;
- preview UI behavior changes;
- live provider tests;
- broad provider orchestration, provider loops, fan-out, verify-revise behavior, or re-synthesis;
- a broad eval platform;
- backlog workbook edits;
- edits to uncertain legacy concept rows or Review Queue concept rows.

## 13. Backlog impact

- `MVP-CLOSEOUT-001` should be marked Done only if the PR that adds this packet is merged.
- Add the PR as implementation evidence for final MVP handoff/readiness documentation.
- Existing lane rows should remain tied to their own implementation PRs:
  - `PROVIDER-EXPERT-PASS-001`: PR #199
  - `CLARIFY-SURFACE-001`: PR #200
  - `EVAL-ARTIFACT-PRESERVE-001`: PR #201
  - `EVAL-BEHAVIORAL-DEMO-001`: PR #202
  - `UI-PREVIEW-001`: PR #203
- Do not mutate uncertain legacy concept rows.
- Do not touch Review Queue concept rows unless the human operator specifically requests it.
- Do not claim MVP validation, Alpha Solver superiority, production readiness, broad runtime readiness, answer-quality benchmark success, or provider reasoning orchestration.
