import io
import re
import subprocess
import sys
from pathlib import Path

try:  # Python 3.11+
    import tomllib
except Exception:  # pragma: no cover
    import tomli as tomllib  # type: ignore

EXAMPLE_RE = re.compile(
    r"```(python|bash)\n(.*?)```\n```text\n(.*?)```",
    re.DOTALL,
)

def iter_examples():
    text = Path('docs/EVIDENCE_PACK.md').read_text()
    for match in EXAMPLE_RE.finditer(text):
        lang, code, expected = match.groups()
        yield lang, code.strip(), expected.strip()

def test_examples_run():
    for lang, code, expected in iter_examples():
        if lang == 'python':
            proc = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True)
            output = proc.stdout.strip()
            assert proc.returncode == 0
        else:
            proc = subprocess.run(code, shell=True, capture_output=True, text=True)
            output = proc.stdout.strip()
            assert proc.returncode == 0
        assert expected in output

def test_docs_build_clean():
    cfg = tomllib.loads(Path('pyproject.toml').read_text())
    modules = cfg.get('tool', {}).get('docs', {}).get('modules', [])
    for mod in modules:
        proc = subprocess.run([sys.executable, '-m', 'pydoc', mod], capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        assert 'WARNING' not in output
