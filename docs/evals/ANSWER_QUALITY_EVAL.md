# EVAL-ANSWER-QUALITY-001: Gated MVP Answer Quality Eval

Status: initial gated MVP implementation. This eval is a prompt-level treatment comparison unless a future change actually wires live reasoning orchestration onto `/v1/solve`.

This eval produces smoke evidence, not proof. A passing run must not be described as production readiness, budget enforcement, fallback support, or proof that Alpha Solver is categorically better than a frontier model.

## Source plan

This implementation follows the Stage 0 plan in `docs/evals/ANSWER_QUALITY_EVAL_PLAN.md`:

- FastAPI `/v1/solve` OpenAI mode is currently provider pass-through, not Alpha Solver reasoning orchestration.
- Local/default `/v1/solve` remains local/offline reasoning and does not call a live LLM by default.
- The MVP hypothesis tested here is whether Alpha Solver-style operator discipline improves outputs when applied as a prompt treatment around the same OpenAI model.

## Case set

Dataset: `datasets/answer_quality_operator_cases.jsonl`

Version: `answer_quality_operator_cases_v0.1`

The initial case set contains 16 Alpha Solver-native, gold-anchored cases across four categories:

1. Runtime overclaim detection.
2. Source hierarchy conflict detection.
3. Lane selection.
4. Backlog impact classification.

Each row has an unambiguous `gold_label`, a closed `choices` list, and a short rubric. Generic trivia is intentionally excluded.

### Disputed gold-label rule

If a gold label is disputed, mark the row with `"disputed": true` or remove the row from the scored dataset until the repo source-of-truth conflict is resolved. The runner refuses to score rows marked as disputed.

## Arms compared

The runner uses the same provider primitive for both arms: `OpenAIProviderClient.execute(ProviderRequest(...))`.

| Arm | Definition |
| --- | --- |
| Baseline | Raw/direct OpenAI with a minimal careful-assistant system prompt. |
| Treatment | The same OpenAI model/settings plus the Alpha Solver operator-discipline system prompt: source hierarchy, SAFE-OUT framing, no unsupported claims, workflow constraints, no simulated evidence, no secret exposure, and no backlog workbook edits unless explicitly requested. |

Controlled settings include model, temperature, max tokens, seed value carried in `ProviderRequest`, input case order, redaction policy, and artifact schema. The current OpenAI client keeps seed in the provider request but does not send seed to the Responses API until endpoint support is validated.

## Live gating and default behavior

No live calls happen by default.

Default dry run:

```bash
python scripts/run_answer_quality_eval.py
```

The dry run validates the dataset, reads `config/quality_gate.yaml`, estimates pre-flight cost, and writes a no-live artifact with no provider predictions. It does not require `OPENAI_API_KEY` and does not call the network.

Live run requires both an explicit CLI flag and an explicit environment gate:

```bash
ALPHA_LIVE_ANSWER_QUALITY=1 OPENAI_API_KEY=... python scripts/run_answer_quality_eval.py --live
```

This is intentionally separate from CI and from the skipped-by-default live OpenAI smoke test. Do not enable it in default test jobs.

## Cost ceiling

The default live cost ceiling is `$5.00` estimated total provider cost. Override it only deliberately:

```bash
ALPHA_LIVE_ANSWER_QUALITY=1 OPENAI_API_KEY=... python scripts/run_answer_quality_eval.py --live --cost-ceiling-usd 2.50
```

Before a live run, the runner estimates the full two-arm dataset cost from prompt size, max tokens, and price hints. It refuses the live run if the expected cost exceeds the ceiling. During a live run, it also aborts if known returned cost estimates exceed the ceiling.

Price hints default to the repo's `cost_saver` model-set values and can be overridden with:

- `ALPHA_AQ_INPUT_PER_1K_USD`
- `ALPHA_AQ_OUTPUT_PER_1K_USD`

These are pre-flight controls, not billing integration or budget enforcement.

## Pre-registered success criteria

Primary smoke metric: treatment accuracy minus baseline accuracy.

Pre-registered margin: treatment must beat baseline by at least `0.05` absolute accuracy on this dataset to count as a positive smoke signal.

The runner references `config/quality_gate.yaml` for existing quality-gate context but does not repurpose simulated `compare_baseline` token or latency behavior as answer-quality evidence.

## Artifacts and safety

Artifacts are written under `artifacts/eval/answer_quality/<timestamp>/` unless overridden.

Files:

- `summary.json`: human- and machine-readable summary with model, temperature, max tokens, seed support, dataset version, treatment version, token usage, latency, known cost estimates, pre-flight estimate, cost ceiling, and the evidence-not-proof disclaimer.
- `predictions.jsonl`: redacted provider text and scoring metadata only. Dry runs leave this empty.
- `README.txt`: artifact safety manifest and disclaimer.

Safety controls:

- No raw provider request dumps.
- No raw provider response dumps.
- No environment dumps.
- No API keys.
- Common `sk-...`, `Bearer ...`, `OPENAI_API_KEY=...`, and `Authorization: ...` forms are redacted before artifact writes and CLI errors.

## Non-goals

This implementation does not add production hosting, Google Cloud deployment, runtime budget enforcement, billing integration, local fallback, `provider.fallback.local`, CLI remote provider execution, portable solver remote provider execution, replay/determinism provider integration, production dashboards, tracing/SLO enforcement, or broad eval-platform functionality.
