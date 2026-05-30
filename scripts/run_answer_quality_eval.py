"""Gated MVP answer-quality eval prediction producer.

This script compares two live OpenAI arms only when explicitly gated:

* baseline: a direct/raw OpenAI prompt using provider primitives
* treatment: the same OpenAI model/settings with Alpha Solver operator-discipline
  prompt treatment

Default execution is a no-live dry run that validates the dataset, estimates cost,
and writes no provider predictions. Results are smoke evidence, not proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any, Iterable, Protocol

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alpha.providers.base import ProviderRequest, ProviderResult  # noqa: E402
from alpha.providers.openai import OpenAIProviderClient  # noqa: E402

DATASET_DEFAULT = ROOT / "datasets" / "answer_quality_operator_cases.jsonl"
QUALITY_GATE_DEFAULT = ROOT / "config" / "quality_gate.yaml"
ARTIFACT_ROOT_DEFAULT = ROOT / "artifacts" / "eval" / "answer_quality"
LIVE_GATE_ENV = "ALPHA_LIVE_ANSWER_QUALITY"
OPENAI_KEY_ENV = "OPENAI_API_KEY"
DATASET_VERSION = "answer_quality_operator_cases_v0.1"
TREATMENT_VERSION = "alpha_solver_operator_discipline_v0.1"
EVIDENCE_DISCLAIMER = "Evidence, not proof: this gated MVP eval is a small smoke signal only."
DEFAULT_MODEL = "gpt-5.4-mini"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 220
DEFAULT_TIMEOUT_MS = 45_000
DEFAULT_SEED = 123
DEFAULT_COST_CEILING_USD = 5.00
DEFAULT_PRICE_HINT = {"input_per_1k": 0.0015, "output_per_1k": 0.004}
DEFAULT_MIN_TREATMENT_MARGIN = 0.05
REQUIRED_FIELDS = {"id", "category", "input", "choices", "gold_label", "rubric"}
ALLOWED_CATEGORIES = {
    "runtime_overclaim_detection",
    "source_hierarchy_conflict_detection",
    "lane_selection",
    "backlog_impact_classification",
}
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_\-]{8,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]+", re.IGNORECASE),
    re.compile(r"(?i)(OPENAI_API_KEY\s*[=:]\s*)\S+"),
    re.compile(r"(?i)(Authorization\s*[:=]\s*)\S+"),
)


class ProviderClient(Protocol):
    def execute(self, request: ProviderRequest) -> ProviderResult:
        """Execute a provider request."""


@dataclass(frozen=True)
class EvalCase:
    id: str
    category: str
    input: str
    choices: list[str]
    gold_label: str
    rubric: str
    dataset_version: str


@dataclass(frozen=True)
class EvalConfig:
    dataset: Path = DATASET_DEFAULT
    quality_gate: Path = QUALITY_GATE_DEFAULT
    artifact_root: Path = ARTIFACT_ROOT_DEFAULT
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    max_tokens: int = DEFAULT_MAX_TOKENS
    timeout_ms: int = DEFAULT_TIMEOUT_MS
    seed: int | None = DEFAULT_SEED
    live: bool = False
    cost_ceiling_usd: float = DEFAULT_COST_CEILING_USD
    input_per_1k_usd: float = DEFAULT_PRICE_HINT["input_per_1k"]
    output_per_1k_usd: float = DEFAULT_PRICE_HINT["output_per_1k"]
    limit: int | None = None


def redact_text(value: str) -> str:
    """Return text with common API-key and authorization forms redacted."""
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(
            lambda match: match.group(1) + "[REDACTED]" if match.lastindex else "[REDACTED]",
            redacted,
        )
    return redacted


def redact_for_artifact(value: Any) -> Any:
    """Recursively redact strings before writing artifacts."""
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact_for_artifact(item) for item in value]
    if isinstance(value, dict):
        return {str(key): redact_for_artifact(item) for key, item in value.items()}
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_no}: invalid JSONL: {exc.msg}") from exc
    return rows


def load_cases(path: Path, *, limit: int | None = None) -> list[EvalCase]:
    rows = read_jsonl(path)
    cases: list[EvalCase] = []
    seen_ids: set[str] = set()
    for idx, row in enumerate(rows, start=1):
        missing = REQUIRED_FIELDS.difference(row)
        if missing:
            raise ValueError(f"case {idx} missing required fields: {sorted(missing)}")
        if row.get("disputed") is True:
            raise ValueError(
                f"case {row['id']} is marked disputed and must be resolved before scoring"
            )
        choices = row["choices"]
        if (
            not isinstance(choices, list)
            or len(choices) < 2
            or not all(isinstance(c, str) and c for c in choices)
        ):
            raise ValueError(f"case {row['id']} must define at least two string choices")
        case = EvalCase(
            id=str(row["id"]),
            category=str(row["category"]),
            input=str(row["input"]),
            choices=list(choices),
            gold_label=str(row["gold_label"]),
            rubric=str(row["rubric"]),
            dataset_version=str(row.get("dataset_version") or DATASET_VERSION),
        )
        if case.id in seen_ids:
            raise ValueError(f"duplicate case id: {case.id}")
        if case.category not in ALLOWED_CATEGORIES:
            raise ValueError(f"case {case.id} has unsupported category: {case.category}")
        if case.gold_label not in case.choices:
            raise ValueError(f"case {case.id} gold_label must be one of choices")
        if case.dataset_version != DATASET_VERSION:
            raise ValueError(f"case {case.id} dataset_version must be {DATASET_VERSION}")
        seen_ids.add(case.id)
        cases.append(case)
    if limit is not None:
        cases = cases[: int(limit)]
    return cases


def dataset_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_quality_gate(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("quality gate config must be a mapping")
    return data


def shared_project_context() -> str:
    return (
        "Shared Alpha Solver project context for both eval arms:\n"
        "- Source hierarchy: direct user instructions and checked-in repo/spec docs outrank "
        "external backlog ledgers, planning spreadsheets, marketing drafts, and convenience notes.\n"
        "- Current /v1/solve OpenAI behavior: the live OpenAI path is a single provider "
        "execute call, not wired live Tree-of-Thought or reasoning orchestration.\n"
        "- Default behavior: local/offline and no-key/no-network defaults must be preserved; "
        "live provider calls require explicit gates.\n"
        "- Evidence framing: smoke tests and small evals are evidence, not proof of production "
        "readiness or categorical model superiority.\n"
        "- Current constraints: budget enforcement, budget persistence, billing integration, "
        "local fallback after provider failure, and provider.fallback.local are not implemented.\n"
        "- Workflow constraints: do not edit backlog workbooks unless explicitly requested; "
        "do not expose secrets; do not treat simulated baseline token or latency behavior as "
        "live answer-quality evidence."
    )


def answer_quality_success_criteria(quality_gate: dict[str, Any]) -> dict[str, Any]:
    configured = quality_gate.get("answer_quality_eval")
    minimum_margin = DEFAULT_MIN_TREATMENT_MARGIN
    if isinstance(configured, dict) and "minimum_margin" in configured:
        minimum_margin = float(configured["minimum_margin"])
    return {
        "metric": "treatment_accuracy_minus_baseline_accuracy",
        "minimum_margin": minimum_margin,
        "quality_gate_reference": str(QUALITY_GATE_DEFAULT.relative_to(ROOT)),
    }


def case_prompt(case: EvalCase) -> str:
    choices = ", ".join(case.choices)
    return (
        "Alpha Solver-native answer-quality classification task.\n"
        f"Case ID: {case.id}\n"
        f"Category: {case.category}\n"
        f"Prompt: {case.input}\n"
        f"Allowed labels: {choices}\n"
        f"Rubric: {case.rubric}\n"
        "Return exactly one allowed label on the first line, followed by one concise reason."
    )


def baseline_system_prompt() -> str:
    return (
        "You are a careful assistant. Use the shared project context below when it is relevant.\n\n"
        f"{shared_project_context()}\n\n"
        "Task instruction: return exactly one allowed label on the first line, then one concise reason."
    )


def treatment_system_prompt() -> str:
    return (
        "You are applying the Alpha Solver operator-discipline treatment. Use the same shared project "
        "context as the baseline, then apply the structured discipline checklist below.\n\n"
        f"{shared_project_context()}\n\n"
        "Alpha Solver operator discipline checklist:\n"
        "1. Identify the controlling source in the prompt and reject lower-priority conflicts.\n"
        "2. Check whether a claim overstates current implementation, evidence, readiness, or scope.\n"
        "3. Preserve no-live, no-secret, no-workbook-edit, and no-simulated-evidence constraints.\n"
        "4. Choose only from the allowed labels; if evidence is insufficient, prefer the label that "
        "avoids unsupported claims.\n\n"
        "Task instruction: return exactly one allowed label on the first line, then one concise reason."
    )


def estimate_tokens(text: str) -> int:
    # Small conservative heuristic for pre-flight cost checks without importing a tokenizer.
    return max(1, (len(text) + 3) // 4)


def estimate_expected_cost(cases: Iterable[EvalCase], config: EvalConfig) -> float:
    if config.input_per_1k_usd < 0 or config.output_per_1k_usd < 0:
        raise ValueError("price hints must be non-negative")
    total = 0.0
    for case in cases:
        prompt = case_prompt(case)
        for system in (baseline_system_prompt(), treatment_system_prompt()):
            input_tokens = estimate_tokens(system + "\n" + prompt)
            total += (input_tokens / 1000.0 * config.input_per_1k_usd) + (
                config.max_tokens / 1000.0 * config.output_per_1k_usd
            )
    return total


def ensure_live_allowed(config: EvalConfig, cases: list[EvalCase], expected_cost: float) -> None:
    if not config.live:
        return
    if os.getenv(LIVE_GATE_ENV) != "1":
        raise RuntimeError(f"live eval requires {LIVE_GATE_ENV}=1")
    if not os.getenv(OPENAI_KEY_ENV, "").strip():
        raise RuntimeError(f"live eval requires non-empty {OPENAI_KEY_ENV}")
    if config.cost_ceiling_usd <= 0:
        raise RuntimeError("live eval cost ceiling must be greater than zero")
    if expected_cost > config.cost_ceiling_usd:
        raise RuntimeError(
            "refusing live eval because estimated cost "
            f"${expected_cost:.4f} exceeds ceiling ${config.cost_ceiling_usd:.2f}"
        )
    if not cases:
        raise RuntimeError("live eval requires at least one case")


def build_request(case: EvalCase, *, arm: str, config: EvalConfig) -> ProviderRequest:
    system = baseline_system_prompt() if arm == "baseline" else treatment_system_prompt()
    return ProviderRequest(
        prompt=case_prompt(case),
        system=system,
        model=config.model,
        max_tokens=config.max_tokens,
        timeout_ms=config.timeout_ms,
        temperature=config.temperature,
        seed=config.seed,
        metadata={
            "request_id": f"answer-quality-{case.id}-{arm}",
            "route": "answer_quality_eval",
            "model_set": "direct_provider_primitives",
            "eval_case_id": case.id,
            "eval_arm": arm,
            "treatment_version": (
                TREATMENT_VERSION if arm == "treatment" else "raw_openai_baseline_v0.1"
            ),
        },
    )


def extract_label(text: str, choices: list[str]) -> str | None:
    first_line = text.strip().splitlines()[0].strip() if text.strip() else ""
    if not first_line:
        return None
    candidates = [first_line]
    label_match = re.fullmatch(r"(?i)label\s*[:=]\s*(.+)", first_line)
    if label_match:
        candidates.append(label_match.group(1).strip())

    for candidate in candidates:
        normalized = re.sub(r"[^A-Za-z0-9_\-]", "", candidate).upper()
        matches = [choice for choice in choices if normalized == choice.upper()]
        if len(matches) == 1:
            return matches[0]
    return None


def score_prediction(text: str, case: EvalCase) -> dict[str, Any]:
    label = extract_label(text, case.choices)
    return {"label": label, "correct": label == case.gold_label}


def execute_arm(
    case: EvalCase, *, arm: str, config: EvalConfig, client: ProviderClient
) -> dict[str, Any]:
    started = perf_counter()
    result = client.execute(build_request(case, arm=arm, config=config))
    elapsed_ms = int((perf_counter() - started) * 1000)
    score = score_prediction(result.text, case)
    return {
        "arm": arm,
        "case_id": case.id,
        "category": case.category,
        "gold_label": case.gold_label,
        "predicted_label": score["label"],
        "correct": score["correct"],
        "text": result.text,
        "model": result.model,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "seed": config.seed,
        "seed_support": "carried_in_provider_request_not_sent_by_current_openai_client",
        "treatment_version": (
            TREATMENT_VERSION if arm == "treatment" else "raw_openai_baseline_v0.1"
        ),
        "usage": {
            "input_tokens": result.usage.input_tokens,
            "output_tokens": result.usage.output_tokens,
            "total_tokens": result.usage.total_tokens,
        },
        "latency_ms": result.latency_ms or elapsed_ms,
        "cost_estimate_usd": result.cost.estimated_usd,
        "cost_source": result.cost.source,
        "finish_reason": result.finish_reason,
        "request_id": result.request_id,
    }


def summarize_predictions(
    predictions: list[dict[str, Any]],
    cases: list[EvalCase],
    success_criteria: dict[str, Any],
) -> dict[str, Any]:
    by_arm: dict[str, list[dict[str, Any]]] = {"baseline": [], "treatment": []}
    for prediction in predictions:
        by_arm.setdefault(str(prediction["arm"]), []).append(prediction)

    arm_summary: dict[str, Any] = {}
    for arm, rows in by_arm.items():
        count = len(rows)
        correct = sum(1 for row in rows if row.get("correct") is True)
        arm_summary[arm] = {
            "count": count,
            "correct": correct,
            "accuracy": correct / count if count else 0.0,
            "token_usage": {
                "input_tokens": sum(row.get("usage", {}).get("input_tokens") or 0 for row in rows),
                "output_tokens": sum(
                    row.get("usage", {}).get("output_tokens") or 0 for row in rows
                ),
                "total_tokens": sum(row.get("usage", {}).get("total_tokens") or 0 for row in rows),
            },
            "known_cost_estimate_usd": sum(row.get("cost_estimate_usd") or 0.0 for row in rows),
        }

    baseline_acc = arm_summary["baseline"]["accuracy"]
    treatment_acc = arm_summary["treatment"]["accuracy"]
    observed_margin = treatment_acc - baseline_acc
    return {
        "disclaimer": EVIDENCE_DISCLAIMER,
        "dataset_version": DATASET_VERSION,
        "treatment_version": TREATMENT_VERSION,
        "case_count": len(cases),
        "categories": sorted({case.category for case in cases}),
        "arms": arm_summary,
        "pre_registered_success_criteria": success_criteria,
        "observed_margin": observed_margin,
        "success_criteria_met": observed_margin >= success_criteria["minimum_margin"],
    }


def write_artifacts(
    *,
    config: EvalConfig,
    dataset_path: Path,
    cases: list[EvalCase],
    summary: dict[str, Any],
    predictions: list[dict[str, Any]],
    dry_run: bool,
    expected_cost: float,
) -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out_dir = config.artifact_root / stamp
    out_dir.mkdir(parents=True, exist_ok=False)
    safe_summary = redact_for_artifact(
        {
            **summary,
            "dry_run": dry_run,
            "dataset_path": str(
                dataset_path.relative_to(ROOT)
                if dataset_path.is_relative_to(ROOT)
                else dataset_path
            ),
            "dataset_sha256": dataset_sha(dataset_path),
            "model": config.model,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "seed": config.seed,
            "seed_support": "carried_in_provider_request_not_sent_by_current_openai_client",
            "estimated_preflight_cost_usd": expected_cost,
            "cost_ceiling_usd": config.cost_ceiling_usd,
        }
    )
    (out_dir / "summary.json").write_text(
        json.dumps(safe_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (out_dir / "predictions.jsonl").open("w", encoding="utf-8") as fh:
        for row in predictions:
            fh.write(json.dumps(redact_for_artifact(row), sort_keys=True) + "\n")
    if dry_run:
        manifest_predictions = "not_generated_in_no_live_dry_run"
    else:
        manifest_predictions = "redacted_provider_text_only_no_raw_payloads"
    (out_dir / "README.txt").write_text(
        "\n".join(
            [
                EVIDENCE_DISCLAIMER,
                f"cases={len(cases)}",
                f"live={not dry_run}",
                f"predictions={manifest_predictions}",
                "Artifacts contain only redacted provider text, scoring metadata, and run summaries.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return out_dir


def run_eval(config: EvalConfig, *, client: ProviderClient | None = None) -> dict[str, Any]:
    cases = load_cases(config.dataset, limit=config.limit)
    quality_gate = load_quality_gate(config.quality_gate)
    expected_cost = estimate_expected_cost(cases, config)
    success_criteria = answer_quality_success_criteria(quality_gate)
    ensure_live_allowed(config, cases, expected_cost)

    if not config.live:
        summary = {
            "disclaimer": EVIDENCE_DISCLAIMER,
            "dataset_version": DATASET_VERSION,
            "treatment_version": TREATMENT_VERSION,
            "case_count": len(cases),
            "categories": sorted({case.category for case in cases}),
            "quality_gate_reference": str(config.quality_gate.relative_to(ROOT)),
            "quality_gate_primary_metric": quality_gate.get("primary_metric"),
            "pre_registered_success_criteria": {
                **success_criteria,
                "quality_gate_reference": str(config.quality_gate.relative_to(ROOT)),
            },
            "live_predictions_generated": False,
            "reason": f"Set {LIVE_GATE_ENV}=1 and pass --live to call OpenAI.",
        }
        out_dir = write_artifacts(
            config=config,
            dataset_path=config.dataset,
            cases=cases,
            summary=summary,
            predictions=[],
            dry_run=True,
            expected_cost=expected_cost,
        )
        return {
            **summary,
            "artifact_dir": str(out_dir),
            "estimated_preflight_cost_usd": expected_cost,
        }

    provider = client or OpenAIProviderClient(
        max_retries=0,
        price_hint={
            "input_per_1k": config.input_per_1k_usd,
            "output_per_1k": config.output_per_1k_usd,
        },
    )
    predictions: list[dict[str, Any]] = []
    spent = 0.0
    for case in cases:
        for arm in ("baseline", "treatment"):
            prediction = execute_arm(case, arm=arm, config=config, client=provider)
            spent += prediction.get("cost_estimate_usd") or 0.0
            if spent > config.cost_ceiling_usd:
                raise RuntimeError(
                    "aborting live eval because observed known cost estimate "
                    f"${spent:.4f} exceeds ceiling ${config.cost_ceiling_usd:.2f}"
                )
            predictions.append(prediction)

    summary = summarize_predictions(predictions, cases, success_criteria)
    out_dir = write_artifacts(
        config=config,
        dataset_path=config.dataset,
        cases=cases,
        summary=summary,
        predictions=predictions,
        dry_run=False,
        expected_cost=expected_cost,
    )
    return {**summary, "artifact_dir": str(out_dir), "estimated_preflight_cost_usd": expected_cost}


def config_from_args(args: argparse.Namespace) -> EvalConfig:
    return EvalConfig(
        dataset=Path(args.dataset),
        quality_gate=Path(args.quality_gate),
        artifact_root=Path(args.artifact_root),
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        timeout_ms=args.timeout_ms,
        seed=args.seed,
        live=args.live,
        cost_ceiling_usd=args.cost_ceiling_usd,
        input_per_1k_usd=args.input_per_1k_usd,
        output_per_1k_usd=args.output_per_1k_usd,
        limit=args.limit,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=str(DATASET_DEFAULT))
    parser.add_argument("--quality-gate", default=str(QUALITY_GATE_DEFAULT))
    parser.add_argument("--artifact-root", default=str(ARTIFACT_ROOT_DEFAULT))
    parser.add_argument("--model", default=os.getenv("ALPHA_AQ_MODEL", DEFAULT_MODEL))
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--timeout-ms", type=int, default=DEFAULT_TIMEOUT_MS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--cost-ceiling-usd",
        type=float,
        default=float(os.getenv("ALPHA_AQ_COST_CEILING_USD", DEFAULT_COST_CEILING_USD)),
    )
    parser.add_argument(
        "--input-per-1k-usd",
        type=float,
        default=float(os.getenv("ALPHA_AQ_INPUT_PER_1K_USD", DEFAULT_PRICE_HINT["input_per_1k"])),
    )
    parser.add_argument(
        "--output-per-1k-usd",
        type=float,
        default=float(os.getenv("ALPHA_AQ_OUTPUT_PER_1K_USD", DEFAULT_PRICE_HINT["output_per_1k"])),
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help=f"Call OpenAI only when {LIVE_GATE_ENV}=1 and {OPENAI_KEY_ENV} is set.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = run_eval(config_from_args(args))
    except Exception as exc:  # noqa: BLE001 - CLI must emit safe concise failures.
        print(f"answer_quality_eval: {redact_text(str(exc))}", file=sys.stderr)
        return 2
    print(json.dumps(redact_for_artifact(report), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
