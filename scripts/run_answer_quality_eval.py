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
import statistics
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
REPEATABILITY_TRACKED_CASE_ID = "aq-lane-003"
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


def relative_path_for_artifact(path: Path) -> str:
    """Return a repository-relative path when possible for safe artifacts."""
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


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


def ensure_live_allowed(
    config: EvalConfig,
    cases: list[EvalCase],
    expected_cost: float,
    *,
    context: str = "eval",
) -> None:
    if not config.live:
        return
    if os.getenv(LIVE_GATE_ENV) != "1":
        raise RuntimeError(f"live {context} requires {LIVE_GATE_ENV}=1")
    if not os.getenv(OPENAI_KEY_ENV, "").strip():
        raise RuntimeError(f"live {context} requires non-empty {OPENAI_KEY_ENV}")
    if config.cost_ceiling_usd <= 0:
        raise RuntimeError(f"live {context} cost ceiling must be greater than zero")
    if expected_cost > config.cost_ceiling_usd:
        raise RuntimeError(
            f"refusing live {context} because estimated cost "
            f"${expected_cost:.4f} exceeds ceiling ${config.cost_ceiling_usd:.2f}"
        )
    if not cases:
        raise RuntimeError(f"live {context} requires at least one case")


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
            "dataset_path": relative_path_for_artifact(dataset_path),
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



def _empty_hit_rate(case_id: str, case: EvalCase | None) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "category": case.category if case else None,
        "gold_label": case.gold_label if case else None,
        "runs_with_prediction": 0,
        "correct": 0,
        "hit_rate": None,
    }


def build_repeatability_summary(
    *,
    config: EvalConfig,
    cases: list[EvalCase],
    requested_runs: int,
    completed_reports: list[dict[str, Any]],
    completed_predictions: list[list[dict[str, Any]]],
    expected_cost_per_run: float,
    aggregate_artifact_dir: Path,
    stopped_reason: str | None = None,
) -> dict[str, Any]:
    """Build an evidence-not-proof aggregate over completed answer-quality eval runs."""
    per_run: list[dict[str, Any]] = []
    margins: list[float] = []
    success_count = 0
    for idx, report in enumerate(completed_reports, start=1):
        baseline = report.get("arms", {}).get("baseline", {})
        treatment = report.get("arms", {}).get("treatment", {})
        margin = report.get("observed_margin")
        if isinstance(margin, (int, float)):
            margins.append(float(margin))
        success_met = report.get("success_criteria_met")
        if success_met is True:
            success_count += 1
        per_run.append(
            {
                "run_index": idx,
                "artifact_dir": report.get("artifact_dir"),
                "baseline_accuracy": baseline.get("accuracy"),
                "treatment_accuracy": treatment.get("accuracy"),
                "observed_margin": margin,
                "success_criteria_met": success_met,
                "live_predictions_generated": report.get("live_predictions_generated", True),
            }
        )

    predictions_flat = [row for run_rows in completed_predictions for row in run_rows]
    cases_by_id = {case.id: case for case in cases}
    per_case_hit_rates: dict[str, dict[str, dict[str, Any]]] = {}
    for case in cases:
        per_case_hit_rates[case.id] = {
            "baseline": _empty_hit_rate(case.id, case),
            "treatment": _empty_hit_rate(case.id, case),
        }
    for row in predictions_flat:
        case_id = str(row.get("case_id"))
        arm = str(row.get("arm"))
        if arm not in {"baseline", "treatment"}:
            continue
        case = cases_by_id.get(case_id)
        per_case_hit_rates.setdefault(
            case_id,
            {
                "baseline": _empty_hit_rate(case_id, case),
                "treatment": _empty_hit_rate(case_id, case),
            },
        )
        arm_row = per_case_hit_rates[case_id][arm]
        arm_row["runs_with_prediction"] += 1
        if row.get("correct") is True:
            arm_row["correct"] += 1
    for arms in per_case_hit_rates.values():
        for arm_row in arms.values():
            count = arm_row["runs_with_prediction"]
            arm_row["hit_rate"] = arm_row["correct"] / count if count else None

    min_margin = min(margins) if margins else None
    max_margin = max(margins) if margins else None
    mean_margin = statistics.fmean(margins) if margins else None
    margin_stddev = statistics.stdev(margins) if len(margins) > 1 else None
    minimum_margin = answer_quality_success_criteria(load_quality_gate(config.quality_gate))[
        "minimum_margin"
    ]
    completed_runs = len(completed_reports)
    if completed_runs == 0:
        stability = "inconclusive"
        conclusion = "No completed runs are available; repeatability evidence is inconclusive."
    elif completed_runs == 1:
        stability = "inconclusive"
        conclusion = (
            "One completed run is not enough to assess run-to-run stability; treat the result as "
            "evidence, not proof."
        )
    elif margins and all(margin >= minimum_margin for margin in margins):
        stability = "stable"
        conclusion = (
            "The apparent treatment advantage met the pre-registered margin in every completed "
            "repeatability run, but this remains evidence, not proof."
        )
    elif margins and any(margin >= minimum_margin for margin in margins):
        stability = "unstable"
        conclusion = (
            "The apparent treatment advantage did not meet the pre-registered margin consistently "
            "across completed runs; treat the evidence as unstable."
        )
    else:
        stability = "inconclusive"
        conclusion = (
            "Completed runs did not show a repeatable treatment-margin pass; the evidence is "
            "inconclusive and does not prove superiority."
        )

    return redact_for_artifact(
        {
            "disclaimer": EVIDENCE_DISCLAIMER,
            "mode": "answer_quality_repeatability",
            "requested_runs": requested_runs,
            "completed_runs": completed_runs,
            "stopped_reason": stopped_reason,
            "live": config.live,
            "dataset_version": DATASET_VERSION,
            "dataset_path": relative_path_for_artifact(config.dataset),
            "dataset_sha256": dataset_sha(config.dataset),
            "case_count": len(cases),
            "model": config.model,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "seed": config.seed,
            "seed_support": "carried_in_provider_request_not_sent_by_current_openai_client",
            "pre_registered_success_criteria": answer_quality_success_criteria(
                load_quality_gate(config.quality_gate)
            ),
            "estimated_preflight_cost_per_run_usd": expected_cost_per_run,
            "estimated_preflight_cost_total_usd": expected_cost_per_run * requested_runs,
            "cost_ceiling_usd": config.cost_ceiling_usd,
            "per_run": per_run,
            "mean_margin": mean_margin,
            "margin_stddev": margin_stddev,
            "margin_min": min_margin,
            "margin_max": max_margin,
            "success_count_by_run": success_count,
            "per_case_hit_rates_by_arm": per_case_hit_rates,
            "tracked_case": {
                "case_id": REPEATABILITY_TRACKED_CASE_ID,
                "by_arm": per_case_hit_rates.get(
                    REPEATABILITY_TRACKED_CASE_ID,
                    {
                        "baseline": _empty_hit_rate(
                            REPEATABILITY_TRACKED_CASE_ID,
                            cases_by_id.get(REPEATABILITY_TRACKED_CASE_ID),
                        ),
                        "treatment": _empty_hit_rate(
                            REPEATABILITY_TRACKED_CASE_ID,
                            cases_by_id.get(REPEATABILITY_TRACKED_CASE_ID),
                        ),
                    },
                ),
            },
            "apparent_treatment_advantage_stability": stability,
            "conclusion": conclusion,
            "artifact_dir": str(aggregate_artifact_dir),
        }
    )


def _read_predictions_jsonl(artifact_dir: Path) -> list[dict[str, Any]]:
    path = artifact_dir / "predictions.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_repeatability_artifacts(summary: dict[str, Any], aggregate_dir: Path) -> None:
    aggregate_dir.mkdir(parents=True, exist_ok=True)
    (aggregate_dir / "repeatability_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (aggregate_dir / "README.txt").write_text(
        "\n".join(
            [
                EVIDENCE_DISCLAIMER,
                "Repeatability measures run-to-run variability; it does not prove superiority, MVP validation, or production readiness.",
                f"requested_runs={summary['requested_runs']}",
                f"completed_runs={summary['completed_runs']}",
                f"stability={summary['apparent_treatment_advantage_stability']}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def run_repeatability(
    config: EvalConfig,
    *,
    repeat_runs: int,
    client: ProviderClient | None = None,
) -> dict[str, Any]:
    """Run the existing answer-quality eval repeatedly and aggregate completed runs."""
    if repeat_runs < 1:
        raise ValueError("repeat_runs must be at least 1")
    if repeat_runs == 1:
        return run_eval(config, client=client)

    cases = load_cases(config.dataset, limit=config.limit)
    expected_cost_per_run = estimate_expected_cost(cases, config)
    expected_total_cost = expected_cost_per_run * repeat_runs
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    aggregate_dir = config.artifact_root / f"{stamp}_repeatability"
    aggregate_dir.mkdir(parents=True, exist_ok=False)

    stopped_reason: str | None = None
    if config.live:
        try:
            ensure_live_allowed(
                config,
                cases,
                expected_total_cost,
                context=f"repeatability ({repeat_runs} runs)",
            )
        except Exception as exc:  # noqa: BLE001 - preserve aggregate for operator diagnosis.
            stopped_reason = redact_text(str(exc))
            summary = build_repeatability_summary(
                config=config,
                cases=cases,
                requested_runs=repeat_runs,
                completed_reports=[],
                completed_predictions=[],
                expected_cost_per_run=expected_cost_per_run,
                aggregate_artifact_dir=aggregate_dir,
                stopped_reason=stopped_reason,
            )
            write_repeatability_artifacts(summary, aggregate_dir)
            return summary

    completed_reports: list[dict[str, Any]] = []
    completed_predictions: list[list[dict[str, Any]]] = []
    cumulative_known_cost = 0.0
    for run_index in range(1, repeat_runs + 1):
        run_cost_ceiling = config.cost_ceiling_usd
        if config.live:
            remaining_ceiling = config.cost_ceiling_usd - cumulative_known_cost
            if remaining_ceiling <= 0:
                stopped_reason = (
                    "repeatability stopped before run "
                    f"{run_index}: observed known cost estimate reached ceiling "
                    f"${config.cost_ceiling_usd:.2f}"
                )
                break
            run_cost_ceiling = remaining_ceiling
        run_config = EvalConfig(
            dataset=config.dataset,
            quality_gate=config.quality_gate,
            artifact_root=aggregate_dir / f"run_{run_index:03d}",
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout_ms=config.timeout_ms,
            seed=config.seed,
            live=config.live,
            cost_ceiling_usd=run_cost_ceiling,
            input_per_1k_usd=config.input_per_1k_usd,
            output_per_1k_usd=config.output_per_1k_usd,
            limit=config.limit,
        )
        try:
            report = run_eval(run_config, client=client)
        except Exception as exc:  # noqa: BLE001 - write aggregate for interrupted/aborted live runs.
            stopped_reason = f"run {run_index} stopped: {redact_text(str(exc))}"
            break
        completed_reports.append(report)
        completed_predictions.append(_read_predictions_jsonl(Path(str(report["artifact_dir"]))))
        if config.live:
            for arm in ("baseline", "treatment"):
                cumulative_known_cost += (
                    report.get("arms", {}).get(arm, {}).get("known_cost_estimate_usd") or 0.0
                )
            if cumulative_known_cost > config.cost_ceiling_usd:
                stopped_reason = (
                    "repeatability stopped after run "
                    f"{run_index}: observed known cost estimate ${cumulative_known_cost:.4f} "
                    f"exceeds ceiling ${config.cost_ceiling_usd:.2f}"
                )
                break

    summary = build_repeatability_summary(
        config=config,
        cases=cases,
        requested_runs=repeat_runs,
        completed_reports=completed_reports,
        completed_predictions=completed_predictions,
        expected_cost_per_run=expected_cost_per_run,
        aggregate_artifact_dir=aggregate_dir,
        stopped_reason=stopped_reason,
    )
    write_repeatability_artifacts(summary, aggregate_dir)
    return summary


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
    parser.add_argument(
        "--repeat-runs",
        type=int,
        default=1,
        help=(
            "Opt-in repeatability mode. Values greater than 1 run the existing eval N times, "
            "preserve each run under its own artifact subdirectory, and write an aggregate summary."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = run_repeatability(config_from_args(args), repeat_runs=args.repeat_runs)
    except Exception as exc:  # noqa: BLE001 - CLI must emit safe concise failures.
        print(f"answer_quality_eval: {redact_text(str(exc))}", file=sys.stderr)
        return 2
    print(json.dumps(redact_for_artifact(report), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
