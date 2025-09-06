import argparse
import re
from pathlib import Path


VERSION_FILE = Path(__file__).resolve().parent.parent / "alpha" / "__init__.py"
PATTERN = re.compile(r'__version__ = "(.*)"')


def bump(version: str, part: str) -> str:
    m = re.match(r"(\d+)\.(\d+)\.(\d+)(?:([a-z])(\d+))?", version)
    if not m:
        raise ValueError(f"unrecognized version: {version}")
    major, minor, patch = map(int, m.group(1, 2, 3))
    pre = m.group(4)
    pre_num = int(m.group(5)) if m.group(5) else None

    if part == "major":
        major += 1
        minor = 0
        patch = 0
        pre = None
        pre_num = None
    elif part == "minor":
        minor += 1
        patch = 0
        pre = None
        pre_num = None
    elif part == "patch":
        patch += 1
        pre = None
        pre_num = None
    elif part == "prerelease":
        if pre and pre_num is not None:
            pre_num += 1
        else:
            pre = "b"
            pre_num = 1

    new = f"{major}.{minor}.{patch}"
    if pre and pre_num is not None:
        new += f"{pre}{pre_num}"
    return new


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", choices=["major", "minor", "patch", "prerelease"], required=True)
    args = ap.parse_args()

    text = VERSION_FILE.read_text()
    current = PATTERN.search(text).group(1)  # type: ignore[union-attr]
    new_version = bump(current, args.part)
    VERSION_FILE.write_text(PATTERN.sub(f'__version__ = "{new_version}"', text))
    print(new_version)


if __name__ == "__main__":  # pragma: no cover
    main()

