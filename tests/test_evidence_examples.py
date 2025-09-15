import subprocess
import sys
from pathlib import Path
import re
import io
from contextlib import redirect_stdout


EXAMPLES_PATH = Path("docs/EVIDENCE_PACK.md")


def _run_snippet(code: str) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(compile(code, "<snippet>", "exec"), {})
    return buf.getvalue().strip()


def test_evidence_examples():
    content = EXAMPLES_PATH.read_text()
    blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)
    assert blocks, "no examples found"
    for block in blocks:
        lines = block.strip().splitlines()
        assert lines[-1].startswith("# EXPECT:"), "missing EXPECT marker"
        expected = lines[-1].split(":", 1)[1].strip()
        code = "\n".join(lines[:-1])
        output = _run_snippet(code)
        assert output == expected


def test_doc_build_clean(tmp_path):
    try:
        out = subprocess.run(["pdoc", "service", "--html", "--output-dir", str(tmp_path)], capture_output=True, text=True)
    except FileNotFoundError:
        out = subprocess.run([sys.executable, "-m", "pydoc", "service"], capture_output=True, text=True)
    combined = out.stdout + out.stderr
    assert out.returncode == 0
    assert "WARNING" not in combined


def test_docstring_checker_pass():
    out = subprocess.run([sys.executable, "scripts/check_docstrings.py", "--fail-under", "90"], capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr


def test_docstring_checker_fail_threshold():
    out = subprocess.run([sys.executable, "scripts/check_docstrings.py", "--fail-under", "101"], capture_output=True, text=True)
    assert out.returncode != 0


def test_docstring_checker_style(tmp_path):
    module = tmp_path / "mod.py"
    module.write_text("def foo(x):\n    \"\"\"TODO\"\"\"\n    return x\n")
    out = subprocess.run([sys.executable, "scripts/check_docstrings.py", str(module)], capture_output=True, text=True)
    assert out.returncode != 0
