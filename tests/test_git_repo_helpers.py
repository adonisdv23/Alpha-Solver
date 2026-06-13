from __future__ import annotations

import subprocess

from tests.helpers.git_repo import init_unsigned_git_repo


def test_init_unsigned_git_repo_overrides_global_signing(tmp_path, monkeypatch):
    global_config = tmp_path / "global-gitconfig"
    global_config.write_text(
        "[commit]\n"
        "\tgpgsign = true\n"
        "[tag]\n"
        "\tgpgsign = true\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))

    repo = tmp_path / "repo"
    repo.mkdir()
    init_unsigned_git_repo(repo, user_email="ci@example.com", user_name="CI")

    assert _git_config(repo, "--get", "commit.gpgsign") == "false"
    assert _git_config(repo, "--get", "tag.gpgsign") == "false"

    (repo / "README.md").write_text("fixture\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "fixture"], cwd=repo, check=True)
    subprocess.run(["git", "tag", "-a", "v0.0.1", "-m", "fixture"], cwd=repo, check=True)


def _git_config(repo, *args: str) -> str:
    return subprocess.run(
        ["git", "config", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
