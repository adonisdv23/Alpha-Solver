from __future__ import annotations

import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def bundle_artifacts(root: Path) -> Path:
    bundles = root / "bundles"
    bundles.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bundle_path = bundles / f"bundle_{ts}.zip"
    with zipfile.ZipFile(bundle_path, "w") as zf:
        lb = root / "leaderboard.md"
        if lb.exists():
            zf.write(lb, arcname="leaderboard.md")
        shortlists = root / "shortlists"
        if shortlists.exists():
            for p in shortlists.rglob("*.json"):
                zf.write(p, arcname=str(p.relative_to(root)))
    return bundle_path


def main() -> None:
    root = Path(os.environ.get("ALPHA_ARTIFACTS_DIR", "artifacts"))
    bundle = bundle_artifacts(root)
    print(bundle)


if __name__ == "__main__":
    main()
