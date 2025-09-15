from pathlib import Path
import subprocess, sys

def test_speckit_emit_creates_file(tmp_path):
    out = tmp_path / "test.md"
    cmd = ["python", "tools/speckit", "emit",
           "--id","X-TEST-001",
           "--track","TOOL",
           "--title","CLI Self Test",
           "--accept","ok",
           "--targets","a/b.py;c/d.py",
           "--out", str(out)]
    subprocess.check_call(cmd)
    s = out.read_text()
    assert "generated_at:" in s and "id: X-TEST-001" in s
