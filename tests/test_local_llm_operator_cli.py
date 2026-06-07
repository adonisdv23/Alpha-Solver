from __future__ import annotations

import ast
import io
import json
from pathlib import Path

import pytest

from alpha.local_llm import operator_cli


_BASE_ARGS = [
    "--enable-local-llm",
    "--endpoint-url",
    "http://127.0.0.1:11434/api/chat",
    "--model",
    "llama3.2:1b-local-fixture",
    "--timeout-seconds",
    "2.5",
]


def _ok_result() -> dict[str, object]:
    return {
        "status": "ok",
        "answer": "local answer fixture",
        "final_answer": "local answer fixture",
        "behavior_evidence": False,
        "no_hosted_fallback": True,
        "no_provider_keys_required": True,
        "metadata": {
            "behavior_evidence": False,
            "no_hosted_fallback": True,
            "no_provider_keys_required": True,
        },
    }


class ReadForbiddenStdin(io.StringIO):
    def read(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("stdin must not be read without --prompt-stdin")


def test_help_text_includes_local_default_off_non_production_and_non_evidence_language(capsys):
    with pytest.raises(SystemExit) as exc:
        operator_cli.main(["--help"])

    assert exc.value.code == 0
    help_text = capsys.readouterr().out
    assert "local-only" in help_text
    assert "default-off" in help_text
    assert "non-production" in help_text
    assert "operator-only" in help_text
    assert "not smoke evidence" in help_text
    assert "not model-quality evidence" in help_text
    assert "not benchmark evidence" in help_text
    assert "not readiness evidence" in help_text
    assert "not evidence-model promotion" in help_text


def test_missing_explicit_opt_in_fails_before_runner_use(monkeypatch):
    called = {"runner": False}

    def forbidden_runner(prompt, *, env):  # type: ignore[no-untyped-def]
        called["runner"] = True
        return _ok_result()

    monkeypatch.setattr(operator_cli, "run_local_llm_solver_orchestration", forbidden_runner)

    with pytest.raises(SystemExit) as exc:
        operator_cli.main(
            [
                "--prompt",
                "hello",
                "--endpoint-url",
                "http://127.0.0.1:11434/api/chat",
                "--model",
                "llama3.2:1b-local-fixture",
                "--timeout-seconds",
                "2.5",
            ]
        )

    assert exc.value.code == 2
    assert called["runner"] is False


@pytest.mark.parametrize(
    "args",
    [
        _BASE_ARGS,
        [*_BASE_ARGS, "--prompt", "one", "--prompt-file", "prompt.txt"],
        [*_BASE_ARGS, "--prompt", "one", "--prompt-stdin"],
    ],
)
def test_missing_or_ambiguous_prompt_source_fails(args, monkeypatch):
    called = {"runner": False}

    def forbidden_runner(prompt, *, env):  # type: ignore[no-untyped-def]
        called["runner"] = True
        return _ok_result()

    monkeypatch.setattr(operator_cli, "run_local_llm_solver_orchestration", forbidden_runner)

    with pytest.raises(SystemExit) as exc:
        operator_cli.main(args)

    assert exc.value.code == 2
    assert called["runner"] is False


def test_empty_prompt_fails_without_runner_use(monkeypatch):
    called = {"runner": False}

    def forbidden_runner(prompt, *, env):  # type: ignore[no-untyped-def]
        called["runner"] = True
        return _ok_result()

    monkeypatch.setattr(operator_cli, "run_local_llm_solver_orchestration", forbidden_runner)

    stdout = io.StringIO()
    stderr = io.StringIO()
    rc = operator_cli.main([*_BASE_ARGS, "--prompt", "   "], stdout=stdout, stderr=stderr)

    assert rc == 2
    assert stdout.getvalue() == ""
    assert "prompt is required" in stderr.getvalue()
    assert called["runner"] is False


def test_valid_prompt_calls_runner_and_prints_stable_json(monkeypatch):
    observed: dict[str, object] = {}

    def fake_runner(prompt, *, env):  # type: ignore[no-untyped-def]
        observed["prompt"] = prompt
        observed["env"] = env
        return _ok_result()

    monkeypatch.setattr(operator_cli, "run_local_llm_solver_orchestration", fake_runner)
    stdout = io.StringIO()

    rc = operator_cli.main([*_BASE_ARGS, "--prompt", "operator prompt"], stdout=stdout)

    assert rc == 0
    assert observed["prompt"] == "operator prompt"
    env = observed["env"]
    assert isinstance(env, dict)
    assert env["ALPHA_LOCAL_LLM_ENABLED"] == "true"
    assert env["ALPHA_LOCAL_LLM_ENDPOINT"] == "http://127.0.0.1:11434/api/chat"
    assert env["ALPHA_LOCAL_LLM_MODEL"] == "llama3.2:1b-local-fixture"
    assert env["ALPHA_LOCAL_LLM_TIMEOUT_SECONDS"] == "2.5"
    parsed = json.loads(stdout.getvalue())
    assert parsed["status"] == "ok"
    assert parsed["answer"] == "local answer fixture"
    assert parsed["final_answer"] == "local answer fixture"
    assert parsed["behavior_evidence"] is False
    assert parsed["no_hosted_fallback"] is True
    assert parsed["no_provider_keys_required"] is True
    assert stdout.getvalue().startswith('{\n  "answer"')


def test_prompt_file_reads_prompt_text(monkeypatch, tmp_path):
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("file prompt\n", encoding="utf-8")
    observed: dict[str, str] = {}

    def fake_runner(prompt, *, env):  # type: ignore[no-untyped-def]
        observed["prompt"] = prompt
        return {**_ok_result(), "status": "clarify"}

    monkeypatch.setattr(operator_cli, "run_local_llm_solver_orchestration", fake_runner)
    stdout = io.StringIO()

    rc = operator_cli.main([*_BASE_ARGS, "--prompt-file", str(prompt_file)], stdout=stdout)

    assert rc == 0
    assert observed["prompt"] == "file prompt\n"
    assert json.loads(stdout.getvalue())["status"] == "clarify"


def test_prompt_stdin_reads_only_when_explicitly_requested(monkeypatch):
    prompts: list[str] = []

    def fake_runner(prompt, *, env):  # type: ignore[no-untyped-def]
        prompts.append(prompt)
        return {**_ok_result(), "status": "blocked"}

    monkeypatch.setattr(operator_cli, "run_local_llm_solver_orchestration", fake_runner)

    stdout = io.StringIO()
    rc = operator_cli.main(
        [*_BASE_ARGS, "--prompt", "direct prompt"],
        stdin=ReadForbiddenStdin("stdin prompt"),
        stdout=stdout,
    )
    assert rc == 0
    assert prompts == ["direct prompt"]

    stdout = io.StringIO()
    rc = operator_cli.main(
        [*_BASE_ARGS, "--prompt-stdin"],
        stdin=io.StringIO("stdin prompt"),
        stdout=stdout,
    )
    assert rc == 0
    assert prompts == ["direct prompt", "stdin prompt"]


def test_non_loopback_endpoint_fails_closed_through_existing_validation_path():
    stdout = io.StringIO()

    rc = operator_cli.main(
        [
            "--enable-local-llm",
            "--prompt",
            "No transport should be used for invalid endpoint.",
            "--endpoint-url",
            "http://example.com/api/chat",
            "--model",
            "llama3.2:1b-local-fixture",
            "--timeout-seconds",
            "2.5",
        ],
        stdout=stdout,
        environ={},
    )

    parsed = json.loads(stdout.getvalue())
    assert rc == 1
    assert parsed["status"] == "failed_closed"
    assert parsed["metadata"]["reason"] == "endpoint_not_local_non_evidence"
    assert parsed["behavior_evidence"] is False
    assert parsed["no_hosted_fallback"] is True


@pytest.mark.parametrize("timeout", ["0", "-1", "nan", "inf", "not-a-number"])
def test_invalid_timeout_fails_nonzero_without_transport(timeout):
    stdout = io.StringIO()

    rc = operator_cli.main(
        [
            "--enable-local-llm",
            "--prompt",
            "No transport should be used for invalid timeout.",
            "--endpoint-url",
            "http://127.0.0.1:11434/api/chat",
            "--model",
            "llama3.2:1b-local-fixture",
            "--timeout-seconds",
            timeout,
        ],
        stdout=stdout,
        environ={},
    )

    parsed = json.loads(stdout.getvalue())
    assert rc == 1
    assert parsed["status"] == "failed_closed"
    assert parsed["metadata"]["reason"] == "invalid_timeout_non_evidence"


def test_hosted_provider_key_env_preserves_fail_closed_rejection_without_leak():
    secret = "sk-test-secret-must-not-leak"
    stdout = io.StringIO()
    stderr = io.StringIO()

    rc = operator_cli.main(
        [*_BASE_ARGS, "--prompt", "Provider key env must fail closed."],
        stdout=stdout,
        stderr=stderr,
        environ={"OPENAI_API_KEY": secret},
    )

    stdout_text = stdout.getvalue()
    stderr_text = stderr.getvalue()
    parsed = json.loads(stdout_text)
    assert rc == 1
    assert parsed["status"] == "failed_closed"
    assert parsed["metadata"]["reason"] == "provider_keys_forbidden_non_evidence"
    assert secret not in stdout_text
    assert secret not in stderr_text


def test_no_hosted_provider_key_cli_flag_exists(capsys):
    with pytest.raises(SystemExit) as exc:
        operator_cli.main(["--help"])

    assert exc.value.code == 0
    help_text = capsys.readouterr().out
    assert "--hosted-provider-key" not in help_text
    assert "--api-key" not in help_text
    assert "--openai-api-key" not in help_text
    assert "--anthropic-api-key" not in help_text
    assert "--google-api-key" not in help_text


def test_wrapper_does_not_import_or_call_forbidden_surfaces():
    source = Path("alpha/local_llm/operator_cli.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules: list[str] = []
    called_names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                called_names.append(func.id)
            elif isinstance(func, ast.Attribute):
                called_names.append(func.attr)

    forbidden_import_fragments = ("webapp", "dashboard", "routes", "fallback")
    assert not any(
        fragment in module for module in imported_modules for fragment in forbidden_import_fragments
    )
    assert "run_local_llm_solver_orchestration" in called_names
    assert "solve" not in called_names
    assert "dashboard" not in called_names
    assert "fallback" not in called_names


def test_failed_closed_result_exits_nonzero_with_parseable_sorted_json(monkeypatch):
    def fake_runner(prompt, *, env):  # type: ignore[no-untyped-def]
        return {
            "status": "failed_closed",
            "answer": "",
            "final_answer": "",
            "behavior_evidence": False,
            "no_hosted_fallback": True,
            "no_provider_keys_required": True,
            "metadata": {"reason": "fixture_failure"},
        }

    monkeypatch.setattr(operator_cli, "run_local_llm_solver_orchestration", fake_runner)
    stdout = io.StringIO()

    rc = operator_cli.main([*_BASE_ARGS, "--prompt", "prompt"], stdout=stdout)

    assert rc == 1
    parsed = json.loads(stdout.getvalue())
    assert parsed["status"] == "failed_closed"
    assert stdout.getvalue().startswith('{\n  "answer"')
