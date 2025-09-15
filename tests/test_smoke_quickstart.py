from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from alpha.executors.math_exec import evaluate
from cli.alpha_solver_cli import ObsResult, solve
from service.app import app

SMOKE_DECK_PATH = Path("data/scenarios/decks/smoke.jsonl")
SMOKE_RECORDS = [
    {
        "id": "smoke-001",
        "intent": "plan",
        "prompt": "List three quick wins for improving focus during remote work.",
        "route_expected": "llm_only",
        "notes": "focus",
    },
    {
        "id": "smoke-002",
        "intent": "plan",
        "prompt": "Outline steps to prepare a simple weeknight pasta dinner.",
        "route_expected": "llm_only",
        "notes": "cooking",
    },
    {
        "id": "smoke-003",
        "intent": "plan",
        "prompt": "Give tips for organising a shared study session with friends.",
        "route_expected": "llm_only",
        "notes": "study",
    },
    {
        "id": "smoke-004",
        "intent": "plan",
        "prompt": "Describe how to set up a weekend hiking day pack checklist.",
        "route_expected": "llm_only",
        "notes": "outdoors",
    },
    {
        "id": "smoke-005",
        "intent": "plan",
        "prompt": "List daily habits that help maintain healthy sleep routines.",
        "route_expected": "llm_only",
        "notes": "sleep",
    },
    {
        "id": "smoke-006",
        "intent": "plan",
        "prompt": "Summarise how to welcome a new teammate on their first day.",
        "route_expected": "llm_only",
        "notes": "onboarding",
    },
]

TOKEN_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"),
]
DOCS_TO_SCAN = [
    Path("docs/README.md"),
    Path("docs/PILOT_CHECKLIST.md"),
    Path("docs/RELEASE_NOTES_v0.1.md"),
]


def ensure_smoke_deck(path: Path = SMOKE_DECK_PATH) -> list[dict[str, str]]:
    path.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, str]] = []
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    data = json.loads(line)
                    records.append(data)
        except json.JSONDecodeError:
            records = []
    if not (5 <= len(records) <= 10):
        records = SMOKE_RECORDS
        with path.open("w", encoding="utf-8") as handle:
            for item in records:
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    return records


def _evaluate_record(record: dict[str, str]) -> tuple[ObsResult, bool]:
    result = solve(record["prompt"], max_tokens=120, min_budget_tokens=60)
    success = result.budget_verdict == "within"
    return result, success


def run_smoke_suite(echo: bool = True) -> dict[str, object]:
    records = ensure_smoke_deck()
    evaluations = [_evaluate_record(record) for record in records]
    successes = sum(1 for _, ok in evaluations if ok)
    pass_rate = successes / len(evaluations) if evaluations else 0.0
    if echo:
        print(f"Smoke deck size: {len(evaluations)}")
        print(f"Pass rate: {pass_rate:.0%}")
        if evaluations:
            print("Obs Card sample:", evaluations[0][0].to_card())
    if pass_rate < 0.95:
        raise RuntimeError(f"Smoke deck pass rate below threshold: {pass_rate:.2%}")
    sample_card = evaluations[0][0].to_card() if evaluations else ""
    return {
        "pass_rate": pass_rate,
        "record_count": len(evaluations),
        "sample_card": sample_card,
    }


def test_quickstart_endpoints_and_evidence():
    with TestClient(app) as client:
        resp = client.get("/healthz")
        assert resp.status_code == 200
        metrics = client.get("/metrics")
        assert metrics.status_code == 200
        assert "alpha_requests_total" in metrics.text

    result = evaluate("2+2")
    assert result["result"] == 4.0


def test_smoke_deck_pass_rate_and_obs_card():
    records = ensure_smoke_deck()
    assert 5 <= len(records) <= 10
    info = run_smoke_suite(echo=False)
    assert info["pass_rate"] >= 0.95
    assert "plan=" in info["sample_card"]


def test_release_script(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "ci@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "CI"], cwd=repo, check=True)

    docs_dir = repo / "docs"
    scripts_dir = repo / "scripts"
    docs_dir.mkdir()
    scripts_dir.mkdir()

    release_src = Path(__file__).resolve().parents[1] / "scripts" / "release.py"
    shutil.copy2(release_src, scripts_dir / "release.py")

    (repo / "README.md").write_text("initial\n", encoding="utf-8")
    (docs_dir / "RELEASE_NOTES_v0.1.md").write_text("placeholder\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md", "docs/RELEASE_NOTES_v0.1.md", "scripts/release.py"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "chore: initial"], cwd=repo, check=True)
    subprocess.run(["git", "tag", "-a", "v0.0.1", "-m", "prev"], cwd=repo, check=True)

    (docs_dir / "update.md").write_text("change\n", encoding="utf-8")
    subprocess.run(["git", "add", "docs/update.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "feat: add change"], cwd=repo, check=True)

    cmd = [sys.executable, "scripts/release.py", "--version", "0.1.0"]
    subprocess.run(cmd, cwd=repo, check=True)

    version_text = (repo / "VERSION").read_text(encoding="utf-8").strip()
    assert version_text == "0.1.0"

    notes = (docs_dir / "RELEASE_NOTES_v0.1.md").read_text(encoding="utf-8")
    assert "feat: add change" in notes
    assert "Release script tags v0.1.0" in notes

    tag_info = subprocess.run(
        ["git", "for-each-ref", "refs/tags/v0.1.0", "--format=%(objecttype) %(taggername)"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    assert tag_info.startswith("tag ")

    before = notes
    subprocess.run(cmd, cwd=repo, check=True)
    after = (docs_dir / "RELEASE_NOTES_v0.1.md").read_text(encoding="utf-8")
    assert before == after
    assert (repo / "VERSION").read_text(encoding="utf-8").strip() == "0.1.0"


def test_docs_have_no_token_like_strings():
    for doc_path in DOCS_TO_SCAN:
        text = doc_path.read_text(encoding="utf-8")
        for pattern in TOKEN_PATTERNS:
            assert not pattern.search(text), f"token-like string found in {doc_path}"


if __name__ == "__main__":
    run_smoke_suite()
