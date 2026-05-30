from __future__ import annotations

import json
from pathlib import Path

import pytest

from alpha.providers.base import ProviderCost, ProviderResult, ProviderUsage
from scripts import run_answer_quality_eval as aq


class RecordingClient:
    def __init__(self, texts):
        self.texts = list(texts)
        self.requests = []

    def execute(self, request):
        self.requests.append(request)
        text = self.texts.pop(0)
        return ProviderResult(
            provider="openai",
            model=request.model,
            text=text,
            finish_reason="stop",
            usage=ProviderUsage(input_tokens=10, output_tokens=3, total_tokens=13),
            cost=ProviderCost(estimated_usd=0.0001, source="price_hint"),
            latency_ms=7,
            request_id=request.request_id,
            raw_metadata={"raw": "must-not-be-written"},
        )


def _config(tmp_path: Path, *, live: bool = False, limit: int | None = None, ceiling: float = 5.0):
    return aq.EvalConfig(
        dataset=aq.DATASET_DEFAULT,
        quality_gate=aq.QUALITY_GATE_DEFAULT,
        artifact_root=tmp_path,
        live=live,
        limit=limit,
        cost_ceiling_usd=ceiling,
    )


def test_dataset_schema_is_gold_anchored_and_category_limited():
    cases = aq.load_cases(aq.DATASET_DEFAULT)

    assert len(cases) == 16
    assert {case.category for case in cases} == {
        "runtime_overclaim_detection",
        "source_hierarchy_conflict_detection",
        "lane_selection",
        "backlog_impact_classification",
    }
    assert all(case.gold_label in case.choices for case in cases)
    assert all(case.dataset_version == aq.DATASET_VERSION for case in cases)


def test_quality_gate_config_is_referenced():
    gate = aq.load_quality_gate(aq.QUALITY_GATE_DEFAULT)

    assert gate["primary_metric"] == "em"
    assert gate["max_cost_per_call"] == 0.01
    assert gate["answer_quality_eval"]["minimum_margin"] == 0.05
    assert aq.answer_quality_success_criteria(gate)["minimum_margin"] == 0.05


def test_default_dry_run_needs_no_key_and_makes_no_provider_calls(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ALPHA_LIVE_ANSWER_QUALITY", raising=False)
    client = RecordingClient(["OVERCLAIM"])

    report = aq.run_eval(_config(tmp_path, limit=1), client=client)

    assert report["live_predictions_generated"] is False
    assert report["case_count"] == 1
    assert client.requests == []
    artifact_dir = Path(report["artifact_dir"])
    assert (artifact_dir / "summary.json").exists()
    assert (artifact_dir / "predictions.jsonl").read_text(encoding="utf-8") == ""


def test_live_requires_explicit_env_gate_even_with_client_and_key(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-secret-value")
    monkeypatch.delenv("ALPHA_LIVE_ANSWER_QUALITY", raising=False)

    with pytest.raises(RuntimeError, match="ALPHA_LIVE_ANSWER_QUALITY=1"):
        aq.run_eval(_config(tmp_path, live=True, limit=1), client=RecordingClient(["OVERCLAIM"]))


def test_live_cost_ceiling_refuses_before_provider_call(monkeypatch, tmp_path):
    monkeypatch.setenv("ALPHA_LIVE_ANSWER_QUALITY", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-secret-value")
    client = RecordingClient(["OVERCLAIM"])

    with pytest.raises(RuntimeError, match="estimated cost"):
        aq.run_eval(_config(tmp_path, live=True, limit=1, ceiling=0.000001), client=client)

    assert client.requests == []


def test_live_producer_calls_baseline_and_treatment_with_controlled_settings(monkeypatch, tmp_path):
    monkeypatch.setenv("ALPHA_LIVE_ANSWER_QUALITY", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-secret-value")
    client = RecordingClient(["OVERCLAIM\nReason", "OVERCLAIM\nReason"])

    report = aq.run_eval(_config(tmp_path, live=True, limit=1), client=client)

    assert len(client.requests) == 2
    baseline, treatment = client.requests
    assert baseline.model == treatment.model == aq.DEFAULT_MODEL
    assert baseline.temperature == treatment.temperature == aq.DEFAULT_TEMPERATURE
    assert baseline.max_tokens == treatment.max_tokens == aq.DEFAULT_MAX_TOKENS
    assert baseline.seed == treatment.seed == aq.DEFAULT_SEED
    assert baseline.prompt == treatment.prompt
    assert baseline.system != treatment.system
    assert aq.shared_project_context() in baseline.system
    assert aq.shared_project_context() in treatment.system
    assert "Alpha Solver operator discipline checklist" not in baseline.system
    assert "Alpha Solver operator discipline checklist" in treatment.system
    for shared_rule in (
        "Source hierarchy",
        "not wired live Tree-of-Thought",
        "no-key/no-network defaults",
        "evidence, not proof",
        "provider.fallback.local are not implemented",
        "do not edit backlog workbooks",
    ):
        assert shared_rule in baseline.system
        assert shared_rule in treatment.system
    assert baseline.metadata["eval_arm"] == "baseline"
    assert treatment.metadata["eval_arm"] == "treatment"
    assert report["arms"]["baseline"]["accuracy"] == 1.0
    assert report["arms"]["treatment"]["accuracy"] == 1.0


def test_label_parser_requires_unambiguous_first_line_label():
    choices = ["OVERCLAIM", "SUPPORTED"]

    assert aq.extract_label("OVERCLAIM\nReason", choices) == "OVERCLAIM"
    assert aq.extract_label("Label: SUPPORTED\nReason", choices) == "SUPPORTED"
    assert aq.extract_label("Not OVERCLAIM; the claim is SUPPORTED.", choices) is None
    assert aq.extract_label("SUPPORTED or OVERCLAIM depending on interpretation", choices) is None
    assert aq.extract_label("Reason: this is OVERCLAIM", choices) is None


def test_negated_or_ambiguous_label_text_is_not_scored_correct():
    case = aq.EvalCase(
        id="parse-case",
        category="runtime_overclaim_detection",
        input="x",
        choices=["OVERCLAIM", "SUPPORTED"],
        gold_label="OVERCLAIM",
        rubric="x",
        dataset_version=aq.DATASET_VERSION,
    )

    assert aq.score_prediction("Not OVERCLAIM; probably SUPPORTED", case) == {
        "label": None,
        "correct": False,
    }


def test_artifact_redaction_excludes_secrets_and_raw_metadata(monkeypatch, tmp_path):
    monkeypatch.setenv("ALPHA_LIVE_ANSWER_QUALITY", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-secret-value")
    client = RecordingClient(
        [
            "OVERCLAIM\nBearer abcdefghijklmnop and sk-test-secret-value",
            "OVERCLAIM\nOPENAI_API_KEY=sk-test-secret-value",
        ]
    )

    report = aq.run_eval(_config(tmp_path, live=True, limit=1), client=client)
    artifact_dir = Path(report["artifact_dir"])
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            artifact_dir / "summary.json",
            artifact_dir / "predictions.jsonl",
            artifact_dir / "README.txt",
        )
    )

    assert "sk-test-secret-value" not in combined
    assert "Bearer abcdefghijklmnop" not in combined
    assert "raw_metadata" not in combined
    assert "must-not-be-written" not in combined
    assert "Evidence, not proof" in combined


def test_disputed_cases_are_rejected(tmp_path):
    dataset = tmp_path / "cases.jsonl"
    dataset.write_text(
        json.dumps(
            {
                "id": "disputed",
                "category": "lane_selection",
                "input": "x",
                "choices": ["A", "B"],
                "gold_label": "A",
                "rubric": "x",
                "dataset_version": aq.DATASET_VERSION,
                "disputed": True,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="marked disputed"):
        aq.load_cases(dataset)
