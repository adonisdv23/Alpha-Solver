import os
import sys
import pytest

from alpha.executors.sandbox import run_subprocess


def test_run_subprocess_success():
    result = run_subprocess([sys.executable, "-c", "print('ok')"], timeout_s=1)
    assert result.rc == 0
    assert result.stdout.strip() == "ok"
    assert not result.timed_out


def test_run_subprocess_timeout():
    result = run_subprocess([sys.executable, "-c", "import time; time.sleep(2)"], timeout_s=0.5)
    assert result.timed_out
    assert result.rc != 0


@pytest.mark.skipif(os.name != "posix", reason="requires Unix resource limits")
def test_run_subprocess_memory_cap():
    result = run_subprocess(
        [sys.executable, "-c", "a='x'*1024*1024*2"],
        timeout_s=1,
        max_rss_kb=1024,
    )
    assert result.rc != 0
