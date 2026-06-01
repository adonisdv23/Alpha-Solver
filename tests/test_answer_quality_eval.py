from __future__ import annotations

import json
from collections import Counter
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

    assert len(cases) == 48
    assert {case.category for case in cases} == {
        "runtime_overclaim_detection",
        "source_hierarchy_conflict_detection",
        "lane_selection",
        "backlog_impact_classification",
    }
    assert Counter(case.category for case in cases) == {
        "runtime_overclaim_detection": 12,
        "source_hierarchy_conflict_detection": 12,
        "lane_selection": 12,
        "backlog_impact_classification": 12,
    }
    assert all(case.gold_label in case.choices for case in cases)
    assert all(case.dataset_version == aq.DATASET_VERSION for case in cases)


def test_dataset_has_unique_ids_and_harder_multichoice_cases():
    cases = aq.load_cases(aq.DATASET_DEFAULT)
    ids = [case.id for case in cases]

    assert len(ids) == len(set(ids)) == 48
    assert sum(len(case.choices) >= 3 for case in cases) >= 12


def test_original_cases_are_preserved_and_tracked_anchor_is_unchanged():
    rows = [
        json.loads(line)
        for line in aq.DATASET_DEFAULT.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by_id = {row["id"]: row for row in rows}

    assert {f"aq-overclaim-{idx:03d}" for idx in range(1, 5)} <= set(by_id)
    assert {f"aq-source-{idx:03d}" for idx in range(1, 5)} <= set(by_id)
    assert {f"aq-lane-{idx:03d}" for idx in range(1, 5)} <= set(by_id)
    assert {f"aq-backlog-{idx:03d}" for idx in range(1, 5)} <= set(by_id)
    assert by_id["aq-lane-003"] == {
        "id": "aq-lane-003",
        "category": "lane_selection",
        "input": "Task: compare raw OpenAI against operator prompt treatment. Existing alpha/eval harness has simulated compare_baseline token savings. Which evidence lane is valid?",
        "choices": ["LIVE_GATED_PROVIDER_PREDICTIONS", "SIMULATED_COMPARE_BASELINE"],
        "gold_label": "LIVE_GATED_PROVIDER_PREDICTIONS",
        "rubric": "Simulated compare_baseline token/latency behavior must not be used as real answer-quality evidence.",
        "dataset_version": aq.DATASET_VERSION,
    }


def test_simulated_vs_live_sibling_cases_are_present():
    cases = aq.load_cases(aq.DATASET_DEFAULT)
    by_id = {case.id: case for case in cases}

    expected_siblings = {
        "aq-lane-003",
        "aq-lane-005",
        "aq-lane-006",
        "aq-lane-007",
        "aq-lane-008",
        "aq-lane-009",
        "aq-lane-010",
    }
    assert expected_siblings <= set(by_id)
    joined = "\n".join(
        f"{by_id[case_id].input} {by_id[case_id].rubric}"
        for case_id in expected_siblings
    )
    for phrase in (
        "simulated",
        "dry-run",
        "mocked",
        "heuristic",
        "environment validation",
        "artifact presence",
        "live",
    ):
        assert phrase in joined.lower()


def test_quality_gate_config_is_referenced():
    gate = aq.load_quality_gate(aq.QUALITY_GATE_DEFAULT)

    assert gate["primary_metric"] == "em"
    assert gate["max_cost_per_call"] == 0.01
    assert gate["answer_quality_eval"]["minimum_margin"] == 0.0625
    assert aq.answer_quality_success_criteria(gate)["minimum_margin"] == 0.0625


def test_default_model_uses_known_working_live_mini_model(monkeypatch):
    monkeypatch.delenv("ALPHA_AQ_MODEL", raising=False)

    args = aq.parse_args([])

    assert aq.DEFAULT_MODEL == "gpt-5.4-mini"
    assert args.model == "gpt-5.4-mini"
    assert args.live is False


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


def test_no_live_save_summary_writes_safe_docs_artifact(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ALPHA_LIVE_ANSWER_QUALITY", raising=False)
    summary_path = tmp_path / "docs" / "evals" / "runs" / "answer_quality_no_live_summary.json"
    client = RecordingClient(["OVERCLAIM"])
    config = aq.EvalConfig(
        dataset=aq.DATASET_DEFAULT,
        quality_gate=aq.QUALITY_GATE_DEFAULT,
        artifact_root=tmp_path / "ephemeral",
        limit=1,
        save_summary=True,
        summary_output=summary_path,
    )

    report = aq.run_eval(config, client=client)

    assert client.requests == []
    assert report["live_predictions_generated"] is False
    assert report["summary_artifact_path"] == str(summary_path)
    assert summary_path.exists()
    artifact = json.loads(summary_path.read_text(encoding="utf-8"))
    assert artifact["artifact_schema_version"] == aq.SUMMARY_ARTIFACT_SCHEMA_VERSION
    assert artifact["artifact_kind"] == "answer_quality_no_live_summary"
    assert artifact["mode"] == "no_live"
    assert artifact["live_predictions_generated"] is False
    assert artifact["case_count"] == 1
    assert artifact["dataset_path"] == "datasets/answer_quality_operator_cases.jsonl"
    assert artifact["skipped_status"] == "no_live_dry_run_no_provider_predictions"

    combined = json.dumps(artifact, sort_keys=True).lower()
    for forbidden in (
        "api key",
        "authorization",
        "bearer",
        "raw request",
        "raw response",
        "raw provider payload",
        "environment dump",
        "sk-test-secret",
    ):
        assert forbidden not in combined
    assert "provider_payloads" in combined
    assert "process_environment" in combined


def test_default_no_live_does_not_write_summary_artifact(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ALPHA_LIVE_ANSWER_QUALITY", raising=False)
    summary_path = tmp_path / "docs" / "evals" / "runs" / "answer_quality_no_live_summary.json"
    config = aq.EvalConfig(
        dataset=aq.DATASET_DEFAULT,
        quality_gate=aq.QUALITY_GATE_DEFAULT,
        artifact_root=tmp_path / "ephemeral",
        limit=1,
        summary_output=summary_path,
    )

    report = aq.run_eval(config, client=RecordingClient(["OVERCLAIM"]))

    assert "summary_artifact_path" not in report
    assert not summary_path.exists()


def test_save_summary_cli_no_live_alias_and_output_path(tmp_path):
    summary_path = tmp_path / "summary.json"

    args = aq.parse_args(["--no-live", "--save-summary", "--summary-output", str(summary_path)])
    config = aq.config_from_args(args)

    assert args.live is False
    assert config.live is False
    assert config.save_summary is True
    assert config.summary_output == summary_path


def test_answer_quality_docs_describe_summary_artifact_path_and_safety_exclusions():
    text = Path("docs/evals/ANSWER_QUALITY_EVAL.md").read_text(encoding="utf-8")

    assert "docs/evals/runs/answer_quality_no_live_summary.json" in text
    assert "--save-summary" in text
    for phrase in (
        "API keys",
        "auth headers",
        "raw provider payloads",
        "raw request/response bodies",
        "environment dumps",
        "MVP validation",
        "Alpha Solver superiority",
        "production readiness",
        "broad runtime readiness",
        "answer-quality benchmark success",
        "provider reasoning orchestration",
    ):
        assert phrase in text


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
    readme = (artifact_dir / "README.txt").read_text(encoding="utf-8")
    assert "raw provider request" not in readme
    assert "raw provider response" not in readme
    assert "environment dump" not in readme
    assert "OPENAI_API_KEY" not in readme


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


def test_no_live_repeatability_writes_aggregate_without_provider_calls(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ALPHA_LIVE_ANSWER_QUALITY", raising=False)
    client = RecordingClient(["OVERCLAIM"])

    report = aq.run_repeatability(_config(tmp_path, limit=2), repeat_runs=3, client=client)

    assert report["mode"] == "answer_quality_repeatability"
    assert report["requested_runs"] == 3
    assert report["completed_runs"] == 3
    assert report["live"] is False
    assert report["mean_margin"] is None
    assert report["margin_stddev"] is None
    assert report["apparent_treatment_advantage_stability"] == "inconclusive"
    assert "evidence" in report["conclusion"].lower()
    assert "proof" in report["disclaimer"].lower()
    assert client.requests == []

    artifact_dir = Path(report["artifact_dir"])
    assert (artifact_dir / "repeatability_summary.json").exists()
    assert (artifact_dir / "README.txt").exists()
    assert len(list(artifact_dir.glob("run_*/**/summary.json"))) == 3
    assert report["tracked_case"]["case_id"] == "aq-lane-003"
    assert report["tracked_case"]["by_arm"]["baseline"]["hit_rate"] is None


def test_live_repeatability_aggregates_per_run_case_hits_and_tracked_case(monkeypatch, tmp_path):
    monkeypatch.setenv("ALPHA_LIVE_ANSWER_QUALITY", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-secret-value")
    dataset = tmp_path / "tracked_cases.jsonl"
    dataset.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "id": "aq-runtime-001",
                        "category": "runtime_overclaim_detection",
                        "input": "x",
                        "choices": ["OVERCLAIM", "SUPPORTED"],
                        "gold_label": "OVERCLAIM",
                        "rubric": "x",
                        "dataset_version": aq.DATASET_VERSION,
                    }
                ),
                json.dumps(
                    {
                        "id": "aq-lane-003",
                        "category": "lane_selection",
                        "input": "x",
                        "choices": [
                            "LIVE_GATED_PROVIDER_PREDICTIONS",
                            "SIMULATED_COMPARE_BASELINE",
                        ],
                        "gold_label": "LIVE_GATED_PROVIDER_PREDICTIONS",
                        "rubric": "x",
                        "dataset_version": aq.DATASET_VERSION,
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    config = aq.EvalConfig(
        dataset=dataset,
        quality_gate=aq.QUALITY_GATE_DEFAULT,
        artifact_root=tmp_path / "artifacts",
        live=True,
    )
    client = RecordingClient(
        [
            "OVERCLAIM\nReason",
            "OVERCLAIM\nReason",
            "LIVE_GATED_PROVIDER_PREDICTIONS\nReason",
            "LIVE_GATED_PROVIDER_PREDICTIONS\nReason",
            "OVERCLAIM\nReason",
            "OVERCLAIM\nReason",
            "LIVE_GATED_PROVIDER_PREDICTIONS\nReason",
            "SIMULATED_COMPARE_BASELINE\nReason",
        ]
    )

    report = aq.run_repeatability(config, repeat_runs=2, client=client)

    assert report["requested_runs"] == 2
    assert report["completed_runs"] == 2
    assert len(client.requests) == 8
    assert [row["baseline_accuracy"] for row in report["per_run"]] == [1.0, 1.0]
    assert [row["treatment_accuracy"] for row in report["per_run"]] == [1.0, 0.5]
    assert [row["observed_margin"] for row in report["per_run"]] == [0.0, -0.5]
    assert report["mean_margin"] == -0.25
    assert report["margin_min"] == -0.5
    assert report["margin_max"] == 0.0
    assert report["margin_stddev"] is not None
    assert report["success_count_by_run"] == 0
    first_case = report["per_case_hit_rates_by_arm"]["aq-runtime-001"]
    assert first_case["baseline"]["hit_rate"] == 1.0
    assert first_case["treatment"]["hit_rate"] == 1.0
    tracked = report["tracked_case"]["by_arm"]
    assert tracked["baseline"]["hit_rate"] == 1.0
    assert tracked["treatment"]["hit_rate"] == 0.5
    assert report["apparent_treatment_advantage_stability"] == "inconclusive"


def test_live_repeatability_total_cost_ceiling_refuses_before_provider_call(monkeypatch, tmp_path):
    monkeypatch.setenv("ALPHA_LIVE_ANSWER_QUALITY", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-secret-value")
    client = RecordingClient(["OVERCLAIM"])

    report = aq.run_repeatability(
        _config(tmp_path, live=True, limit=1, ceiling=0.000001), repeat_runs=3, client=client
    )

    assert report["requested_runs"] == 3
    assert report["completed_runs"] == 0
    assert "estimated cost" in report["stopped_reason"]
    assert client.requests == []
    assert (Path(report["artifact_dir"]) / "repeatability_summary.json").exists()
