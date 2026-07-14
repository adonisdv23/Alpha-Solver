from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
PR_WORKFLOWS = ("ci.yml", "tests.yml", "gates.yml", "reliability-slo.yml")
PR_ACTIVITY_TYPES = {
    "opened",
    "synchronize",
    "reopened",
    "ready_for_review",
    "converted_to_draft",
}


def _workflow(name: str) -> dict:
    # BaseLoader keeps YAML 1.1 words such as `on` as strings, matching the
    # keys GitHub Actions consumes rather than coercing `on` to True.
    return yaml.load((WORKFLOWS / name).read_text(), Loader=yaml.BaseLoader)


def _run_commands(workflow: dict) -> str:
    commands = []
    for job in workflow["jobs"].values():
        for step in job.get("steps", []):
            if "run" in step:
                commands.append(step["run"])
    return "\n".join(commands)


def test_full_suite_runs_once_per_pull_request_revision() -> None:
    ci_commands = _run_commands(_workflow("ci.yml"))
    test_commands = _run_commands(_workflow("tests.yml"))

    assert "make check-local-llm-orchestration-guardrails" in ci_commands
    assert "pytest -q" not in ci_commands
    assert "python -m pytest -q" in test_commands


def test_reliability_and_metrics_gates_have_distinct_ownership() -> None:
    gates_commands = _run_commands(_workflow("gates.yml"))
    reliability_commands = _run_commands(_workflow("reliability-slo.yml"))

    assert "tests/metrics/test_aggregator.py" in gates_commands
    assert "tests/reliability" not in gates_commands
    assert "alpha.reliability.slo" not in gates_commands
    assert "tests/reliability" in reliability_commands
    assert "python -m alpha.reliability.slo" in reliability_commands
    assert "docker run" in reliability_commands


def test_docker_build_is_tag_only() -> None:
    push = _workflow("docker-publish.yml")["on"]["push"]

    assert push["tags"] == ["v*"]
    assert "branches" not in push


def test_pr_workflows_skip_drafts_and_run_when_ready() -> None:
    for name in PR_WORKFLOWS:
        workflow = _workflow(name)
        pull_request = workflow["on"]["pull_request"]
        assert PR_ACTIVITY_TYPES.issubset(set(pull_request["types"]))

        concurrency = workflow["concurrency"]
        assert "github.event.pull_request.number" in concurrency["group"]
        assert "github.run_id" in concurrency["group"]
        assert concurrency["cancel-in-progress"] in {
            "true",
            "${{ github.event_name == 'pull_request' }}",
        }

        for job in workflow["jobs"].values():
            assert "github.event.pull_request.draft == false" in job["if"]
