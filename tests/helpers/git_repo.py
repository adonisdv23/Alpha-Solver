"""Helpers for tests that create throwaway Git repositories."""

from __future__ import annotations

import subprocess
from pathlib import Path


def init_unsigned_git_repo(repo: Path, *, user_email: str, user_name: str) -> None:
    """Initialize a temporary Git repo that is isolated from signing config.

    Some developer and CI environments enforce commit or tag signing globally.
    Tests that create disposable repositories only need commits as fixtures, so
    disable signing in the local repository config after ``git init`` instead of
    relying on or mutating global Git configuration.
    """

    subprocess.run(["git", "init"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", user_email], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", user_name], cwd=repo, check=True)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=repo, check=True)
    subprocess.run(["git", "config", "tag.gpgsign", "false"], cwd=repo, check=True)
