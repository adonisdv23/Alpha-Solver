from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path


def _find_repo_root(start: Path) -> str | None:
    p = start
    while True:
        if (p / ".git").exists():
            return str(p)
        if p.parent == p:
            return None
        p = p.parent


def collect_snapshot() -> dict:
    data: dict = {
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "paths": {
            "sys_executable": sys.executable,
            "cwd": str(Path.cwd()),
            "repo_root": _find_repo_root(Path.cwd()),
        },
        "env": {k: v for k, v in os.environ.items() if k.startswith("ALPHA_")},
        "runtime_modules": {},
        "file_hashes": {},
    }
    modules = ["json", "subprocess", "asyncio", "importlib", "argparse"]
    for m in modules:
        try:
            data["runtime_modules"][m] = metadata.version(m)
        except Exception:
            data["runtime_modules"][m] = None
    files = [
        "alpha/core/registry_provider.py",
        "alpha/core/runner.py",
        "scripts/telemetry_leaderboard.py",
    ]
    for rel in files:
        p = Path(rel)
        if p.exists():
            h = hashlib.sha256()
            h.update(p.read_bytes())
            data["file_hashes"][rel] = h.hexdigest()
    return data


def main() -> Path:
    base = Path(os.environ.get("ALPHA_ARTIFACTS_DIR", "artifacts"))
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = base / "env" / f"env_snapshot_{ts}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = collect_snapshot()
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=True)
    print(path)
    return path


if __name__ == "__main__":
    main()
