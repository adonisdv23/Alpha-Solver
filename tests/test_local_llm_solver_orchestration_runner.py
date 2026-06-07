from __future__ import annotations

import json
from pathlib import Path

import pytest

from alpha.local_llm.orchestration_runner import (
    SUPPORTED_MODES,
    run_local_llm_solver_orchestration,
)


def _valid_env(**overrides: str) -> dict[str, str]:
    env = {
        "ALPHA_LOCAL_LLM_ENABLED": "true",
        "ALPHA_LOCAL_LLM_ENDPOINT": "http://127.0.0.1:11434/api/chat",
        "ALPHA_LOCAL_LLM_MODEL": "llama3.2:1b-local-fixture",
        "ALPHA_LOCAL_LLM_TIMEOUT_SECONDS": "2.5",
    }
    env.update(overrides)
    return env


class SequencedTransport:
    def __init__(self, *contents: str):
        self.contents = list(contents)
        self.calls = []

    def __call__(self, *, endpoint_url, payload, timeout_seconds):
        self.calls.append(
            {
                "endpoint_url": endpoint_url,
                "payload": payload,
                "timeout_seconds": timeout_seconds,
            }
        )
        if not self.contents:
            raise ConnectionError("unexpected local transport call")
        content = self.contents.pop(0)
        if content == "__TIMEOUT__":
            raise TimeoutError("fake local timeout")
        return {"message": {"role": "assistant", "content": content}}


def _assert_compatible_answer_fields(result, expected_answer: str) -> None:
    assert "answer" in result
    assert "final_answer" in result
    assert result["answer"] == expected_answer
    assert result["final_answer"] == expected_answer
    assert result["answer"] == result["final_answer"]


def _pass_one(**overrides):
    data = {
        "mode": "direct",
        "considerations": ["Use the local bounded context."],
        "assumptions": [],
        "confidence": 0.82,
        "missing_information": [],
        "risk_flags": ["low"],
    }
    data.update(overrides)
    return json.dumps(data)


def test_default_off_local_llm_config_fails_closed_without_transport_call():
    transport = SequencedTransport(_pass_one())

    result = run_local_llm_solver_orchestration(
        "Explain a tiny fixture.", env={}, transport=transport
    )

    assert result["status"] == "failed_closed"
    assert result["mode"] == "block"
    _assert_compatible_answer_fields(result, "")
    assert result["metadata"]["reason"] == "local_llm_disabled_non_evidence"
    assert transport.calls == []


def test_non_local_endpoint_fails_closed_through_existing_validation_path():
    transport = SequencedTransport(_pass_one())

    result = run_local_llm_solver_orchestration(
        "Endpoint must stay local.",
        env=_valid_env(ALPHA_LOCAL_LLM_ENDPOINT="http://example.com/api/chat"),
        transport=transport,
    )

    assert result["status"] == "failed_closed"
    _assert_compatible_answer_fields(result, "")
    assert result["metadata"]["reason"] == "endpoint_not_local_non_evidence"
    assert transport.calls == []


def test_hosted_provider_keys_are_not_required_or_used():
    transport = SequencedTransport(_pass_one(), "Final local answer.")

    result = run_local_llm_solver_orchestration(
        "Provider keys are not needed.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "ok"
    assert result["no_provider_keys_required"] is True
    assert result["metadata"]["no_provider_keys_required"] is True
    assert len(transport.calls) == 2
    assert all(call["payload"]["model"] == "llama3.2:1b-local-fixture" for call in transport.calls)


def test_happy_path_returns_normalized_local_orchestration_result():
    transport = SequencedTransport(_pass_one(), "Final local answer.")

    result = run_local_llm_solver_orchestration(
        "Answer with local orchestration.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "ok"
    assert result["provider_mode"] == "local_llm"
    assert result["orchestration_mode"] == "non_production_local_solver_orchestration"
    assert result["strategy"] == "local_expert_two_pass"
    assert result["pass_count"] == 2
    assert result["mode"] == "direct"
    assert result["considerations"] == ["Use the local bounded context."]
    assert result["assumptions"] == []
    assert result["confidence"] == 0.82
    _assert_compatible_answer_fields(result, "Final local answer.")
    assert result["metadata"]["local_backend"] == "ollama_chat"
    assert result["metadata"]["endpoint_is_loopback"] is True


def test_simple_direct_prompt_allows_empty_considerations_when_low_risk():
    transport = SequencedTransport(
        _pass_one(considerations=[], missing_information=[], risk_flags=["low"]),
        "Direct answer without pass-one considerations.",
    )

    result = run_local_llm_solver_orchestration(
        "Summarize the fixture in one sentence.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "ok"
    assert result["mode"] == "direct"
    assert result["pass_count"] == 2
    assert result["considerations"] == []
    _assert_compatible_answer_fields(result, "Direct answer without pass-one considerations.")
    assert len(transport.calls) == 2


def test_ambiguous_optimization_prompt_clarifies_without_pass_two():
    transport = SequencedTransport(
        _pass_one(
            mode="direct",
            considerations=["Optimization target is not identified."],
            risk_flags=["optimization", "performance"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    assert result["mode"] != "block"
    assert result["pass_count"] == 1
    assert len(transport.calls) == 1


def test_pass_one_block_underspecified_prompt_clarifies_without_pass_two_or_assumptions():
    unsafe_assumption = "Assume unsupported deployment details from the model."
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["The optimization target is not identified."],
            assumptions=[unsafe_assumption],
            confidence=0.8,
            missing_information=["Which component should be made faster?"],
            risk_flags=["optimization", "performance"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "Please clarify: Which component should be made faster?")
    assert result["assumptions"] == []
    assert unsafe_assumption not in result["assumptions"]
    assert len(transport.calls) == 1


def test_pass_one_block_bounded_assumptions_proceeds_to_pass_two():
    final_answer = "Use profiling first, then optimize the bounded local hot path."
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["Profiling can support a bounded local optimization plan."],
            assumptions=["Assume the target is a local fixture hot path with observable latency."],
            confidence=0.8,
            missing_information=["Optional profiler preference."],
            risk_flags=["optimization", "profiling", "latency", "performance"],
        ),
        final_answer,
    )

    result = run_local_llm_solver_orchestration(
        "Plan a bounded performance improvement for the local fixture.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "ok"
    assert result["mode"] == "answer_with_assumptions"
    assert result["pass_count"] == 2
    _assert_compatible_answer_fields(result, final_answer)
    assert len(transport.calls) == 2


def test_prompt_three_shaped_bounded_assumptions_with_composite_flag_proceeds_to_pass_two():
    final_answer = "Profile startup, inspect imports, defer larger changes, and keep assumptions explicit."
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["Startup latency work can be planned before profiling results are available."],
            assumptions=["Assume the CLI is a small local Python tool with no external service dependency."],
            confidence=0.76,
            missing_information=["Exact profiler output can be collected later."],
            risk_flags=["startup performance optimization"],
        ),
        final_answer,
    )

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI's startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "ok"
    assert result["mode"] == "answer_with_assumptions"
    assert result["pass_count"] == 2
    _assert_compatible_answer_fields(result, final_answer)
    assert len(transport.calls) == 2


def test_prompt_two_shaped_block_with_safe_ambiguity_flag_clarifies_without_pass_two():
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["The optimization target is unclear."],
            confidence=0.8,
            missing_information=["Which target should be made faster?"],
            risk_flags=["optimization target unclear"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "Please clarify: Which target should be made faster?")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_prompt_three_shaped_python_cli_composite_flag_proceeds_to_assumption_answer():
    final_answer = "Profile imports, measure startup, then make the smallest local change."
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["Startup time can be planned with later profiling."],
            assumptions=["Assume the target is a small local Python CLI."],
            confidence=0.85,
            missing_information=["Exact profiling output can be collected later."],
            risk_flags=["python cli startup performance optimization"],
        ),
        final_answer,
    )

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI's startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "ok"
    assert result["mode"] == "answer_with_assumptions"
    assert result["pass_count"] == 2
    _assert_compatible_answer_fields(result, final_answer)
    assert len(transport.calls) == 2


def test_retry_004_prompt_two_block_with_benign_ambiguity_clarifies_without_pass_two():
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["The request is benign but lacks an optimization target."],
            assumptions=["Assume only ordinary local performance tuning is intended."],
            confidence=0.8,
            missing_information=["Which target should be made faster?"],
            risk_flags=["benign ambiguity", "missing context", "unclear target", "optimization"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "Please clarify: Which target should be made faster?")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_retry_004_prompt_two_low_information_risk_clarifies_without_pass_two():
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["The request has low information risk because the target is missing."],
            assumptions=["Assume the request is ordinary local performance tuning."],
            confidence=0.8,
            missing_information=["Which target should be made faster?"],
            risk_flags=["low information risk"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "Please clarify: Which target should be made faster?")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_retry_006_prompt_two_information_risk_alone_clarifies_without_pass_two_or_exposure():
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["The model returned an ambiguous information risk label."],
            assumptions=["Assume the ambiguous information risk is safe."],
            confidence=0.8,
            missing_information=["Which target should be made faster?"],
            risk_flags=["information risk"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "Please clarify: Which target should be made faster?")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert result["metadata"]["gate_trace"]["apply_gate_decision"] == "shape_clarify"
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    "risk_flag",
    [
        "credential theft",
        "bypass safeguards",
        "exploit chain",
        "data exfiltration",
        "avoid audit logs",
    ],
)
def test_retry_004_prompt_two_serious_risk_flags_block_without_pass_two_or_exposure(risk_flag):
    unsafe_consideration = f"The request includes {risk_flag}."
    unsafe_assumption = "Assume the risky path should proceed."
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=[unsafe_consideration],
            assumptions=[unsafe_assumption],
            confidence=0.8,
            missing_information=["Which target should be made faster?"],
            risk_flags=["optimization", risk_flag],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    assert result["status"] in {"blocked", "failed_closed"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert unsafe_consideration not in result["considerations"]
    assert unsafe_assumption not in result["assumptions"]
    assert len(transport.calls) == 1


def test_retry_004_prompt_three_clarify_with_bounded_assumptions_promotes_to_pass_two():
    final_answer = "Assume a small CLI, profile startup next, inspect imports, then defer noncritical work."
    transport = SequencedTransport(
        _pass_one(
            mode="clarify",
            considerations=["Startup planning can be bounded before profiler output exists."],
            assumptions=["Assume the CLI is a small local Python command with measurable startup time."],
            confidence=0.8,
            missing_information=["Exact profiling output can be collected later."],
            risk_flags=["performance", "profiling", "startup", "python cli"],
        ),
        final_answer,
    )

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI's startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "ok"
    assert result["mode"] == "answer_with_assumptions"
    assert result["pass_count"] == 2
    _assert_compatible_answer_fields(result, final_answer)
    assert len(transport.calls) == 2


@pytest.mark.parametrize("confidence", [0.54, "not parseable"])
def test_retry_004_prompt_three_clarify_low_or_unparseable_confidence_does_not_answer(confidence):
    transport = SequencedTransport(
        _pass_one(
            mode="clarify",
            considerations=["Startup planning can be bounded before profiler output exists."],
            assumptions=["Assume the CLI is a small local Python command with measurable startup time."],
            confidence=confidence,
            missing_information=["Exact profiling output can be collected later."],
            risk_flags=["performance", "profiling", "startup", "python cli"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI's startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    assert result["mode"] != "answer_with_assumptions"
    assert result["pass_count"] == 1
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    "field",
    ["considerations", "assumptions", "missing_information", "risk_flags"],
)
def test_retry_004_prompt_three_clarify_boundary_claim_fails_closed_without_exposure(field):
    forbidden_text = "This validates production readiness and /v1/solve readiness."
    pass_one = {
        "mode": "clarify",
        "considerations": ["Startup planning can be bounded before profiler output exists."],
        "assumptions": ["Assume the CLI is a small local Python command."],
        "confidence": 0.8,
        "missing_information": ["Exact profiling output can be collected later."],
        "risk_flags": ["performance", "profiling", "startup", "python cli"],
    }
    pass_one[field] = [forbidden_text]
    transport = SequencedTransport(json.dumps(pass_one), "Unexpected pass two answer.")

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI's startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"failed_closed", "blocked"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert forbidden_text not in result["answer"]
    assert forbidden_text not in result["final_answer"]
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    "risk_flag",
    [
        "performance optimization",
        "startup performance",
        "startup performance optimization",
        "latency optimization",
        "local profiling",
    ],
)
def test_benign_composite_low_risk_flags_can_use_bounded_assumption_path(risk_flag):
    final_answer = f"Bounded assumption answer for {risk_flag}."
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=["The planning scope is local, bounded, and limited to performance work."],
            assumptions=["Assume later measurements will guide the final implementation choice."],
            confidence=0.75,
            missing_information=["Profiler results can be supplied later."],
            risk_flags=[risk_flag],
        ),
        final_answer,
    )

    result = run_local_llm_solver_orchestration(
        "Plan local Python CLI startup improvements with assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "ok"
    assert result["mode"] == "answer_with_assumptions"
    assert result["pass_count"] == 2
    _assert_compatible_answer_fields(result, final_answer)
    assert len(transport.calls) == 2


@pytest.mark.parametrize(
    "risk_flag",
    [
        "performance optimization bypass",
        "startup performance credential theft",
        "latency optimization exfiltration",
    ],
)
def test_composite_risk_flag_with_high_risk_token_blocks_without_pass_two(risk_flag):
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=["The safe-looking tokens are not enough to override serious risk text."],
            assumptions=["Assume the local fixture otherwise appears bounded."],
            confidence=0.8,
            risk_flags=[risk_flag],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Plan local Python CLI startup improvements with assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"blocked", "failed_closed"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


@pytest.mark.parametrize("risk_flag", ["unknown", "unknown risk", "medium risk"])
def test_unknown_or_non_allowlisted_risk_flags_block_without_exposure(risk_flag):
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=["The request otherwise appears bounded."],
            assumptions=["Assume a local fixture."],
            confidence=0.8,
            risk_flags=[risk_flag],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Plan local Python CLI startup improvements with assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"blocked", "failed_closed"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_pass_one_block_missing_information_high_risk_cue_blocks_without_pass_two():
    unsafe_missing_information = "Need approval to bypass monitoring."
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["Profiling can support a bounded local optimization plan."],
            assumptions=["Assume the target is a local fixture hot path with observable latency."],
            confidence=0.8,
            missing_information=[unsafe_missing_information],
            risk_flags=["optimization"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Plan a bounded performance improvement for the local fixture.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"blocked", "failed_closed"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert unsafe_missing_information not in result["answer"]
    assert unsafe_missing_information not in result["final_answer"]
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_serious_risk_flag_blocks_even_when_prompt_text_is_neutral():
    transport = SequencedTransport(
        _pass_one(
            mode="direct",
            considerations=["The prompt text is neutral, but the risk flag is serious."],
            confidence=0.84,
            missing_information=[],
            risk_flags=["credential theft"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Summarize this local fixture.", env=_valid_env(), transport=transport
    )

    assert result["status"] in {"blocked", "failed_closed"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert len(transport.calls) == 1



@pytest.mark.parametrize(
    "risk_flag",
    [
        "credential theft",
        "malware",
        "exfiltration",
        "token theft",
        "phishing",
        "unauthorized access",
        "exploit",
        "evasion",
        "concealment",
        "bypass",
        "self-harm",
        "weapons",
        "explosives",
    ],
)
def test_malware_and_exfiltration_style_risk_flags_block_without_pass_two(risk_flag):
    transport = SequencedTransport(
        _pass_one(
            mode="direct",
            considerations=["Pass one detected a serious risk category."],
            confidence=0.84,
            missing_information=[],
            risk_flags=[risk_flag],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Summarize this local fixture.", env=_valid_env(), transport=transport
    )

    assert result["status"] in {"blocked", "failed_closed"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert len(transport.calls) == 1


def test_low_risk_assumptions_with_optimization_flags_proceeds_to_pass_two():
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=["Profiling can be planned without changing runtime exposure."],
            assumptions=["Assume changes are limited to a local profiling plan for the fixture."],
            confidence=0.73,
            missing_information=["Optional exact profiler preference."],
            risk_flags=["optimization", "profiling", "latency"],
        ),
        "Answer with bounded optimization assumptions.",
    )

    result = run_local_llm_solver_orchestration(
        "Plan a bounded profiling pass for the local fixture.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "ok"
    assert result["mode"] == "answer_with_assumptions"
    assert result["pass_count"] == 2
    _assert_compatible_answer_fields(result, "Answer with bounded optimization assumptions.")
    assert len(transport.calls) == 2


def test_high_risk_prompt_blocks_without_normal_answer():
    transport = SequencedTransport(
        _pass_one(mode="direct", considerations=["The prompt asks for concealment."], risk_flags=["low"]),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Disable safety monitoring and hide changes from reviewers.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "blocked"
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_high_risk_prompt_does_not_expose_unsafe_considerations_or_assumptions():
    unsafe_consideration = "Avoid logs, prevent alerts, and disable automated checks."
    unsafe_assumption = "Assume the change can be hidden from reviewers and audit trails."
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=[unsafe_consideration],
            assumptions=[unsafe_assumption],
            confidence=0.91,
            risk_flags=["low"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Disable safety monitoring and hide changes from reviewers.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"blocked", "failed_closed"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert unsafe_consideration not in result["considerations"]
    assert unsafe_assumption not in result["assumptions"]
    assert len(transport.calls) == 1


def test_non_allowlisted_risk_flag_blocks_by_default_without_pass_two():
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["The risk flag is not on the ordinary allowlist."],
            assumptions=["Assume this unknown risk is safe."],
            confidence=0.8,
            risk_flags=["ambiguous external automation"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Summarize this local fixture.", env=_valid_env(), transport=transport
    )

    assert result["status"] in {"blocked", "failed_closed"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_pass_one_forbidden_boundary_claim_fails_closed_without_exposing_fields():
    forbidden_consideration = "This validates production readiness and /v1/solve readiness."
    forbidden_assumption = "Assume the dashboard is ready for production evidence promotion."
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=[forbidden_consideration],
            assumptions=[forbidden_assumption],
            confidence=0.8,
            risk_flags=["low"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Keep boundary claims out of pass one.", env=_valid_env(), transport=transport
    )

    assert result["status"] in {"failed_closed", "blocked"}
    assert result["mode"] == "block"
    assert result["metadata"]["reason"] == "pass_one_boundary_claim_violation_non_evidence"
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert forbidden_consideration not in result["considerations"]
    assert forbidden_assumption not in result["assumptions"]
    _assert_compatible_answer_fields(result, "")
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    ("field", "forbidden_text"),
    [
        ("considerations", "This validates production readiness."),
        ("considerations", "This proves benchmark evidence."),
        ("considerations", "This confirms provider orchestration evidence."),
        ("considerations", "This proves /v1/solve readiness."),
        ("considerations", "This confirms dashboard readiness."),
        ("assumptions", "Assume it is ready for production."),
        ("assumptions", "Assume Alpha is superior."),
        ("missing_information", "This proves local model quality."),
        ("risk_flags", "validated billing accuracy"),
        ("risk_flags", "evidence-model promotion validated"),
    ],
)
def test_prompt_five_boundary_guard_blocks_forbidden_pass_one_fields_without_exposure(
    field, forbidden_text
):
    pass_one = {
        "mode": "answer_with_assumptions",
        "considerations": ["The safe portion is bounded."],
        "assumptions": ["Assume ordinary local-only execution."],
        "confidence": 0.8,
        "missing_information": [],
        "risk_flags": ["low"],
    }
    pass_one[field] = [forbidden_text]
    transport = SequencedTransport(json.dumps(pass_one), "Unexpected pass two answer.")

    result = run_local_llm_solver_orchestration(
        "State the boundary safely without echoing readiness claims.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"failed_closed", "blocked"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert forbidden_text not in result["answer"]
    assert forbidden_text not in result["final_answer"]
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_pass_one_boundary_guard_is_sentence_scoped_for_mixed_negated_and_positive_claim():
    forbidden_text = "This does not prove production readiness. It validates dashboard readiness."
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=[forbidden_text],
            assumptions=["Assume ordinary local-only execution."],
            confidence=0.8,
            missing_information=[],
            risk_flags=["low"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Keep mixed boundary claims out of pass one.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"failed_closed", "blocked"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert forbidden_text not in result["answer"]
    assert forbidden_text not in result["final_answer"]
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_pass_one_boundary_guard_allows_negated_disclaimer_only_on_bounded_path():
    disclaimer = "This does not prove production readiness."
    final_answer = "Proceed with a bounded local plan while preserving the stated assumption."
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=[disclaimer, "The planning scope is local and bounded."],
            assumptions=["Assume later profiling will guide the implementation choice."],
            confidence=0.8,
            missing_information=["Profiler results can be supplied later."],
            risk_flags=["startup performance optimization"],
        ),
        final_answer,
    )

    result = run_local_llm_solver_orchestration(
        "Plan local Python CLI startup improvements with assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "ok"
    assert result["mode"] == "answer_with_assumptions"
    assert result["pass_count"] == 2
    assert disclaimer in result["considerations"]
    _assert_compatible_answer_fields(result, final_answer)
    assert len(transport.calls) == 2


@pytest.mark.parametrize("field", ["behavior_evidence", "no_hosted_fallback", "no_provider_keys_required"])
def test_result_preserves_required_non_evidence_flags(field):
    transport = SequencedTransport(_pass_one(), "Final local answer.")

    result = run_local_llm_solver_orchestration(
        "Preserve non-evidence flags.", env=_valid_env(), transport=transport
    )

    expected = False if field == "behavior_evidence" else True
    assert result[field] is expected
    assert result["metadata"][field] is expected


def test_malformed_pass_one_without_safe_section_fallback_fails_closed():
    transport = SequencedTransport('{"mode": "direct", confidence: maybe')

    result = run_local_llm_solver_orchestration(
        "Malformed pass one must not answer.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "failed_closed"
    assert result["mode"] not in {"direct", "answer_with_assumptions"}
    _assert_compatible_answer_fields(result, "")
    assert len(transport.calls) == 1


def test_unparseable_confidence_cannot_choose_answer_with_assumptions():
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            assumptions=["Assume a bounded local fixture."],
            confidence="pretty confident",
        )
    )

    result = run_local_llm_solver_orchestration(
        "Bad confidence must clarify instead.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    _assert_compatible_answer_fields(
        result,
        "Please clarify the missing information before a local answer can be attempted.",
    )
    assert result["mode"] != "answer_with_assumptions"
    assert len(transport.calls) == 1


def test_answer_with_assumptions_requires_safe_confidence_and_bounded_assumptions():
    allowed = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=["The request is low risk and bounded."],
            assumptions=["Assume the fixture input is complete enough for a concise answer."],
            confidence=0.74,
            missing_information=["Optional exact wording preference."],
            risk_flags=["low"],
        ),
        "Final answer with the explicit assumption.",
    )

    allowed_result = run_local_llm_solver_orchestration(
        "Answer under a bounded assumption.", env=_valid_env(), transport=allowed
    )

    assert allowed_result["status"] == "ok"
    assert allowed_result["mode"] == "answer_with_assumptions"
    assert allowed_result["pass_count"] == 2
    _assert_compatible_answer_fields(allowed_result, "Final answer with the explicit assumption.")

    denied = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=["The request has some context."],
            assumptions=[],
            confidence=0.74,
            risk_flags=["low"],
        )
    )

    denied_result = run_local_llm_solver_orchestration(
        "Missing assumptions must not answer.", env=_valid_env(), transport=denied
    )

    assert denied_result["status"] == "clarify"
    assert denied_result["mode"] != "answer_with_assumptions"
    _assert_compatible_answer_fields(
        denied_result,
        "Please clarify the missing information before a local answer can be attempted.",
    )
    assert len(denied.calls) == 1


def test_pass_two_forbidden_boundary_claim_fails_closed_without_exposing_answer():
    forbidden_answer = "This proves production readiness and MVP validation."
    transport = SequencedTransport(_pass_one(), forbidden_answer)

    result = run_local_llm_solver_orchestration(
        "Do not allow boundary claims.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "failed_closed"
    assert result["mode"] == "block"
    assert result["metadata"]["reason"] == "pass_two_boundary_claim_violation_non_evidence"
    _assert_compatible_answer_fields(result, "")
    assert forbidden_answer not in result["answer"]
    assert forbidden_answer not in result["final_answer"]
    assert result["behavior_evidence"] is False


@pytest.mark.parametrize(
    "disclaimer",
    [
        "This does not prove production readiness or MVP validation.",
        "This is not MVP validation.",
        "This is not benchmark evidence.",
        "No production readiness is claimed.",
    ],
)
def test_pass_two_safe_boundary_disclaimer_is_not_blocked(disclaimer):
    transport = SequencedTransport(_pass_one(), disclaimer)

    result = run_local_llm_solver_orchestration(
        "Allow safe boundary disclaimers.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "ok"
    _assert_compatible_answer_fields(result, disclaimer)
    assert result["behavior_evidence"] is False


def test_pass_two_failure_fails_closed():
    transport = SequencedTransport(_pass_one(), "__TIMEOUT__")

    result = run_local_llm_solver_orchestration(
        "Pass two timeout must fail closed.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "failed_closed"
    assert result["mode"] == "block"
    assert result["metadata"]["reason"] == "pass_two_failure:timeout_non_evidence"
    assert result["pass_count"] == 2
    _assert_compatible_answer_fields(result, "")


@pytest.mark.parametrize("echo_pass", [1, 2])
def test_prompt_echo_or_system_echo_fails_closed(echo_pass):
    def echoing_transport(*, endpoint_url, payload, timeout_seconds):
        if echo_pass == 1 or len(echoing_transport.calls) == 1:
            content = payload["messages"][1]["content"]
        else:
            content = "Final local answer."
        echoing_transport.calls += 1
        return {"message": {"role": "assistant", "content": content}}

    echoing_transport.calls = 1
    first = _pass_one() if echo_pass == 2 else None
    if first is not None:
        transport = SequencedTransport(first)

        def mixed_transport(*, endpoint_url, payload, timeout_seconds):
            if transport.calls:
                return {"message": {"role": "assistant", "content": payload["messages"][1]["content"]}}
            return transport(endpoint_url=endpoint_url, payload=payload, timeout_seconds=timeout_seconds)

        active_transport = mixed_transport
    else:
        active_transport = echoing_transport

    result = run_local_llm_solver_orchestration(
        "Echoes must fail closed.", env=_valid_env(), transport=active_transport
    )

    assert result["status"] == "failed_closed"
    assert result["mode"] == "block"
    _assert_compatible_answer_fields(result, "")


def test_blocked_outcome_includes_empty_compatible_answer_fields():
    transport = SequencedTransport(_pass_one(mode="block", risk_flags=["policy risk"]))

    result = run_local_llm_solver_orchestration(
        "Block instead of answering.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "blocked"
    assert result["mode"] == "block"
    _assert_compatible_answer_fields(result, "")


def test_clarify_outcome_includes_matching_answer_fields_with_message():
    transport = SequencedTransport(
        _pass_one(mode="clarify", missing_information=["Need the target format."])
    )

    result = run_local_llm_solver_orchestration(
        "Clarify before answering.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    _assert_compatible_answer_fields(result, "Please clarify: Need the target format.")


def test_mode_is_always_one_of_supported_values_for_all_terminal_statuses():
    cases = [
        SequencedTransport(_pass_one(), "Final local answer."),
        SequencedTransport(_pass_one(mode="clarify", missing_information=["Need X."])),
        SequencedTransport(_pass_one(mode="block", risk_flags=["policy risk"])),
        SequencedTransport("not parseable"),
    ]

    for transport in cases:
        result = run_local_llm_solver_orchestration(
            "Mode must be normalized.", env=_valid_env(), transport=transport
        )
        assert result["mode"] in SUPPORTED_MODES


def test_runner_is_not_mounted_into_v1_solve_or_dashboard_preview():
    service_app = Path("service/app.py").read_text(encoding="utf-8")
    dashboard_preview = Path("alpha/webapp/routes/expert_preview.py").read_text(encoding="utf-8")

    assert "run_local_llm_solver_orchestration" not in service_app
    assert "orchestration_runner" not in service_app
    assert "run_local_llm_solver_orchestration" not in dashboard_preview
    assert "orchestration_runner" not in dashboard_preview


def test_hosted_provider_code_path_is_not_modified_by_runner_import():
    import alpha.local_llm.orchestration_runner as runner

    source = Path(runner.__file__).read_text(encoding="utf-8")

    assert "OPENAI_API_KEY" not in source
    assert "ANTHROPIC_API_KEY" not in source
    assert "run_configured_local_llm_runtime" in source


def test_retry_005_prompt_two_safe_underspecified_clarifies_without_pass_two_or_exposure():
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["The request is benign but the target is missing."],
            assumptions=["Assume insufficient context for a safe answer."],
            confidence=0.88,
            missing_information=["Which component should be made faster?"],
            risk_flags=["benign ambiguity", "insufficient context", "missing target"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "clarify"
    assert result["mode"] == "clarify"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "Please clarify: Which component should be made faster?")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    "serious_risk_flag",
    [
        "credential theft",
        "bypass safeguards",
        "exploit chain",
        "data exfiltration",
        "avoid audit logs",
        "disabling monitoring",
        "hiding from reviewers",
    ],
)
def test_retry_005_prompt_two_serious_risk_guard_blocks_without_pass_two_or_exposure(
    serious_risk_flag,
):
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=[f"The hidden concern is {serious_risk_flag}."],
            assumptions=["Assume unsafe details should not be exposed."],
            confidence=0.9,
            missing_information=["Which component should be made faster?"],
            risk_flags=["benign ambiguity", serious_risk_flag],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    assert result["status"] in {"blocked", "failed_closed"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_retry_005_prompt_three_bounded_python_cli_assumption_path_answers():
    final_answer = "Profile startup, inspect imports, defer costly initialization, and state each assumption."
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["A bounded startup plan can be drafted before profiling is available."],
            assumptions=["Assume this is a small local Python CLI and profiling will be collected later."],
            confidence=0.85,
            missing_information=["Exact profiling output can be collected later."],
            risk_flags=["local python cli startup performance profiling planning"],
        ),
        final_answer,
    )

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI's startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "ok"
    assert result["mode"] == "answer_with_assumptions"
    assert result["pass_count"] == 2
    _assert_compatible_answer_fields(result, final_answer)
    assert result["assumptions"] == [
        "Assume this is a small local Python CLI and profiling will be collected later."
    ]
    assert len(transport.calls) == 2


@pytest.mark.parametrize("confidence", [0.54, "unparseable"])
def test_retry_005_prompt_three_guard_low_or_unparseable_confidence_does_not_answer(confidence):
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["A bounded startup plan can be drafted before profiling is available."],
            assumptions=["Assume this is a small local Python CLI."],
            confidence=confidence,
            missing_information=["Exact profiling output can be collected later."],
            risk_flags=["local python cli startup performance profiling planning"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI's startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"clarify", "blocked"}
    assert result["mode"] != "answer_with_assumptions"
    assert result["pass_count"] == 1
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    "overrides",
    [
        {"assumptions": []},
        {"assumptions": ["Assume unknown or unbounded implementation details."]},
        {
            "missing_information": [
                "Need profiler output.",
                "Need dependency list.",
                "Need operating system details.",
            ]
        },
        {"risk_flags": ["credential theft"]},
        {"considerations": ["This validates production readiness."]},
    ],
)
def test_retry_005_prompt_three_guard_cases_do_not_answer_with_assumptions(overrides):
    data = {
        "mode": "block",
        "considerations": ["A bounded startup plan can be drafted before profiling is available."],
        "assumptions": ["Assume this is a small local Python CLI."],
        "confidence": 0.85,
        "missing_information": ["Exact profiling output can be collected later."],
        "risk_flags": ["local python cli startup performance profiling planning"],
    }
    data.update(overrides)
    transport = SequencedTransport(json.dumps(data), "Unexpected pass two answer.")

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI's startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"clarify", "blocked", "failed_closed"}
    assert result["mode"] != "answer_with_assumptions"
    assert result["pass_count"] == 1
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    "forbidden_text",
    [
        "Ensuring dashboard readiness for production usage.",
        "Confirmation that this validates production readiness.",
        "Validation of benchmark evidence.",
        "Evidence-model promotion.",
    ],
)
def test_retry_005_prompt_five_pass_one_boundary_phrasing_suppresses_normal_fields(
    forbidden_text,
):
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=[forbidden_text],
            assumptions=["Assume local-only non-evidence scope."],
            confidence=0.8,
            missing_information=[],
            risk_flags=["low"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Keep boundary phrasing out of normal fields.", env=_valid_env(), transport=transport
    )

    assert result["status"] in {"failed_closed", "blocked"}
    assert result["mode"] == "block"
    assert result["pass_count"] == 1
    _assert_compatible_answer_fields(result, "")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 1


def test_retry_005_prompt_five_pass_two_boundary_failure_suppresses_gate_fields():
    forbidden_answer = "This validates production readiness and dashboard readiness."
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=["Safe gate consideration that must not leak after boundary failure."],
            assumptions=["Assume safe gate assumption that must not leak after boundary failure."],
            confidence=0.8,
            missing_information=[],
            risk_flags=["low"],
        ),
        forbidden_answer,
    )

    result = run_local_llm_solver_orchestration(
        "Boundary failures must suppress normal fields.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "failed_closed"
    assert result["mode"] == "block"
    assert result["pass_count"] == 2
    assert result["metadata"]["reason"] == "pass_two_boundary_claim_violation_non_evidence"
    _assert_compatible_answer_fields(result, "")
    assert result["considerations"] == []
    assert result["assumptions"] == []
    assert len(transport.calls) == 2


def _assert_gate_trace_safe(metadata, forbidden_values):
    serialized = json.dumps(metadata.get("gate_trace", {}), sort_keys=True)
    for value in forbidden_values:
        assert value not in serialized


def test_retry_007_diagnostic_schema_for_clarify_shape_is_safe_and_enum_only():
    raw_consideration = "The model returned an ambiguous information risk label."
    raw_assumption = "Assume the ambiguous information risk is safe."
    raw_missing = "Which target should be made faster?"
    raw_risk = "information risk"
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=[raw_consideration],
            assumptions=[raw_assumption],
            confidence=0.8,
            missing_information=[raw_missing],
            risk_flags=[raw_risk],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Make it faster.", env=_valid_env(), transport=transport
    )

    trace = result["metadata"]["gate_trace"]
    assert trace["diagnostic_schema_version"] == 1
    assert trace["diagnostic_redaction"] == "enum_only_no_raw_text"
    assert trace["prompt_shape"] == "underspecified_edit_or_performance"
    assert trace["pass_one_selected_mode"] == "block"
    assert trace["apply_gate_decision"] == "shape_clarify"
    assert trace["expose_model_fields"] is False
    assert trace["pass_two_called"] is False
    _assert_gate_trace_safe(
        result["metadata"],
        ["Make it faster", raw_consideration, raw_assumption, raw_missing, raw_risk],
    )


def test_retry_007_prompt_two_explicit_serious_risk_terms_still_block():
    for serious_term in [
        "credential theft",
        "bypass safeguards",
        "data exfiltration",
        "exploit chain",
        "disable monitoring",
        "hide from reviewers",
        "avoid audit logs",
    ]:
        transport = SequencedTransport(
            _pass_one(
                mode="block",
                considerations=["The target is unclear."],
                assumptions=["Assume ordinary local tuning."],
                confidence=0.8,
                missing_information=["Which target should be made faster?"],
                risk_flags=["ambiguous request"],
            ),
            "Unexpected pass two answer.",
        )

        result = run_local_llm_solver_orchestration(
            f"Make it faster and include {serious_term}.", env=_valid_env(), transport=transport
        )

        assert result["status"] in {"blocked", "failed_closed"}
        assert result["mode"] == "block"
        assert result["pass_count"] == 1
        _assert_compatible_answer_fields(result, "")
        assert result["considerations"] == []
        assert result["assumptions"] == []
        assert result["metadata"]["gate_trace"]["high_risk_reason_code"] == "explicit_serious_risk_term"
        assert len(transport.calls) == 1


def test_retry_007_prompt_three_vague_risk_labels_route_to_answer_with_diagnostics():
    final_answer = "Inspect import time, defer heavy work, add a profiling checkpoint, and document assumptions."
    transport = SequencedTransport(
        _pass_one(
            mode="block",
            considerations=["A bounded startup plan can be drafted before profiling is available."],
            assumptions=["Assume this is a small local Python CLI and profiling will be collected later."],
            confidence=0.85,
            missing_information=["Exact profiling output can be collected later."],
            risk_flags=["unknown risk", "medium risk", "unclear requirements"],
        ),
        final_answer,
    )

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI’s startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "ok"
    assert result["mode"] == "answer_with_assumptions"
    assert result["pass_count"] == 2
    _assert_compatible_answer_fields(result, final_answer)
    trace = result["metadata"]["gate_trace"]
    assert trace["prompt_shape"] == "bounded_local_python_cli_startup_plan"
    assert trace["apply_gate_decision"] == "shape_answer_with_assumptions"
    assert trace["pass_one_selected_mode"] == "block"
    assert trace["expose_model_fields"] is True
    assert trace["pass_two_called"] is True
    _assert_gate_trace_safe(
        result["metadata"],
        ["small Python CLI", "unknown risk", final_answer],
    )


@pytest.mark.parametrize(
    "overrides,expected_reason",
    [
        ({"confidence": "unparseable"}, "confidence_missing_or_unparseable"),
        ({"confidence": 0.54}, "confidence_below_threshold"),
        ({"assumptions": []}, "assumptions_missing"),
        ({"assumptions": ["unknown"]}, "assumptions_unknown_or_unbounded"),
        ({"assumptions": ["Assume unbounded implementation details."]}, "assumptions_unknown_or_unbounded"),
        ({"missing_information": ["Need profiler output.", "Need dependency list.", "Need OS details."]}, "missing_information_too_broad"),
    ],
)
def test_retry_007_prompt_three_assumption_gate_failures_do_not_answer(overrides, expected_reason):
    data = {
        "mode": "block",
        "considerations": ["A bounded startup plan can be drafted before profiling is available."],
        "assumptions": ["Assume this is a small local Python CLI."],
        "confidence": 0.85,
        "missing_information": ["Exact profiling output can be collected later."],
        "risk_flags": ["unknown risk"],
    }
    data.update(overrides)
    transport = SequencedTransport(json.dumps(data), "Unexpected pass two answer.")

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI’s startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] in {"clarify", "blocked"}
    assert result["mode"] != "answer_with_assumptions"
    assert result["pass_count"] == 1
    assert expected_reason in result["metadata"]["gate_trace"].get(
        "assumption_gate_failed_reason_codes", []
    )
    assert len(transport.calls) == 1


def test_retry_007_pass_one_boundary_diagnostic_stage_and_nonexposure():
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=["This validates production readiness."],
            assumptions=["Assume local-only scope."],
            confidence=0.8,
            missing_information=[],
            risk_flags=["low"],
        ),
        "Unexpected pass two answer.",
    )

    result = run_local_llm_solver_orchestration(
        "Keep boundary claims out.", env=_valid_env(), transport=transport
    )

    assert result["status"] == "failed_closed"
    assert result["considerations"] == []
    assert result["assumptions"] == []
    trace = result["metadata"]["gate_trace"]
    assert trace["boundary_failure_stage"] == "pass_one"
    assert trace["expose_model_fields"] is False
    assert trace["pass_two_called"] is False


def test_retry_007_pass_two_boundary_diagnostic_stage_and_nonexposure():
    transport = SequencedTransport(
        _pass_one(
            mode="answer_with_assumptions",
            considerations=["Use a bounded local plan."],
            assumptions=["Assume this is a small local Python CLI."],
            confidence=0.8,
            missing_information=[],
            risk_flags=["low"],
        ),
        "This validates production readiness.",
    )

    result = run_local_llm_solver_orchestration(
        "Draft a concise execution plan to improve a small Python CLI’s startup time "
        "when only profiling later is available; state assumptions.",
        env=_valid_env(),
        transport=transport,
    )

    assert result["status"] == "failed_closed"
    assert result["considerations"] == []
    assert result["assumptions"] == []
    trace = result["metadata"]["gate_trace"]
    assert trace["boundary_failure_stage"] == "pass_two"
    assert trace["expose_model_fields"] is False
    assert trace["pass_two_called"] is True
