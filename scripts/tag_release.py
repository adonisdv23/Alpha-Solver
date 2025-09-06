import argparse
import re
import subprocess
from pathlib import Path


INIT_FILE = Path("alpha/__init__.py")


def _update_version(version: str) -> None:
    text = INIT_FILE.read_text()
    new_text = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{version}"', text)
    INIT_FILE.write_text(new_text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    version = args.version

    _update_version(version)
    subprocess.run(["git", "commit", "-am", f"Release {version}"], check=True)
    subprocess.run(["git", "tag", version], check=True)
    print(f"Created tag {version}. To push: git push origin HEAD && git push origin {version}")


if __name__ == "__main__":
    main()
