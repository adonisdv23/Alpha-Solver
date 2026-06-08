from __future__ import annotations

from alpha.self_operator.command_classification import classify_command


def assert_blocked(command, reason_code: str) -> None:
    result = classify_command(command)
    assert result.allowed is False
    assert result.reason_code == reason_code
    assert result.findings


def test_allows_safe_local_check_and_read_commands() -> None:
    assert classify_command("git status --short").allowed is True
    assert classify_command(["python", "-m", "pytest", "-q", "tests/test_self_operator_preflight.py"]).allowed is True
    assert classify_command("rg -n local-only docs tests").reason_code == "allowed_local_read_check"


def test_blocks_provider_and_network_commands() -> None:
    assert_blocked("openai responses create --model hosted", "provider_call")
    assert_blocked("curl https://example.invalid", "network_external_api")


def test_blocks_browser_automation_commands() -> None:
    assert_blocked("python -m playwright install chromium", "browser_automation")


def test_blocks_deployment_commands() -> None:
    assert_blocked("kubectl apply -f deployment.yaml", "deployment")


def test_blocks_billing_commands() -> None:
    assert_blocked("stripe invoices list", "billing")


def test_blocks_credential_secret_commands() -> None:
    assert_blocked("cat .env", "credential_secret_access")
    assert_blocked("printenv API_KEY", "credential_secret_access")


def test_blocks_google_sheets_commands() -> None:
    assert_blocked("python scripts/update_google_sheets.py", "google_sheets")


def test_blocks_source_artifact_mutation_commands() -> None:
    assert_blocked("rm docs/evals/runs/source-artifact.json", "source_artifact_mutation")
    assert_blocked("sed -i s/a/b/ docs/file.md", "source_artifact_mutation")


def test_blocks_evidence_promotion_commands() -> None:
    assert_blocked("python scripts/promote_evidence.py --acceptance-passed", "evidence_promotion")


def test_marks_unclear_commands_for_operator_review() -> None:
    result = classify_command("python scripts/custom_unknown.py")
    assert result.allowed is False
    assert result.reason_code == "unclear_requires_operator_review"
    assert result.findings[0].id == "SELF_OPERATOR_COMMAND_REQUIRES_OPERATOR_REVIEW"
