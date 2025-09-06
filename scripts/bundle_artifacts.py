from __future__ import annotations

import os
import zipfile
import hashlib
from datetime import datetime, timezone
from pathlib import Path


def bundle_artifacts(root: Path) -> tuple[Path, Path]:
    bundles = root / "bundles"
    bundles.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bundle_path = bundles / f"bundle_{ts}.zip"
    with zipfile.ZipFile(bundle_path, "w") as zf:
        lb = root / "leaderboard.md"
        if lb.exists():
            zf.write(lb, arcname="leaderboard.md")
        for folder in ["shortlists", "run", "env"]:
            sub = root / folder
            if sub.exists():
                for p in sub.rglob("*.json"):
                    zf.write(p, arcname=str(p.relative_to(root)))
        schemas_dir = Path("schemas")
        if schemas_dir.exists():
            for p in schemas_dir.rglob("*"):
                if p.is_file():
                    zf.write(p, arcname=str(p))
    sha_path = bundles / f"bundle_{ts}.sha256"
    h = hashlib.sha256()
    h.update(bundle_path.read_bytes())
    sha_path.write_text(h.hexdigest(), encoding="utf-8")
    return bundle_path, sha_path


def main() -> None:
    root = Path(os.environ.get("ALPHA_ARTIFACTS_DIR", "artifacts"))
    bundle, sha = bundle_artifacts(root)
    print(bundle)
    print(sha)


if __name__ == "__main__":
    main()
