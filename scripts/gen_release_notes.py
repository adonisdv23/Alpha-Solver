import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


def _read_version() -> str:
    init = Path(__file__).resolve().parent.parent / "alpha" / "__init__.py"
    m = re.search(r'__version__ = "(.*)"', init.read_text())
    if not m:
        raise RuntimeError("could not find version string")
    return m.group(1)


def _extract_body(changelog: Path) -> str:
    lines = changelog.read_text().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## [Unreleased]":
            start = i + 1
            break
    if start is None:
        raise RuntimeError("Unreleased section not found")
    body_lines = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body_lines.append(line)
    return "\n".join(body_lines).strip()


def _write_notes(version: str, body: str) -> None:
    out_dir = Path("artifacts/release_notes")
    out_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    content = f"# Release Notes\n\nVersion: {version}\nDate: {now}\n\n{body}\n"
    (out_dir / "release_notes.md").write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--version")
    args = parser.parse_args()

    body = _extract_body(Path("CHANGELOG.md"))
    version = args.version or _read_version()
    if args.check:
        return
    _write_notes(version, body)


if __name__ == "__main__":
    main()
