"""Sandboxed subprocess execution with resource limits."""
from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from typing import List

try:  # resource only on Unix
    import resource  # type: ignore
except Exception:  # pragma: no cover
    resource = None  # type: ignore


@dataclass
class RunResult:
    rc: int
    stdout: str
    stderr: str
    duration: float
    timed_out: bool
    mem_kb: int


def run_subprocess(cmd: List[str], timeout_s: float, max_rss_kb: int | None = None) -> RunResult:
    """Run ``cmd`` with optional timeout and memory limit."""
    preexec = None
    if resource is not None and max_rss_kb is not None:
        def _limits() -> None:
            limit = max(0, int(max_rss_kb)) * 1024
            resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
        preexec = _limits
    start = time.time()
    timed_out = False
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        preexec_fn=preexec,
    )
    try:
        out, err = proc.communicate(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        timed_out = True
    duration = time.time() - start
    rc = proc.returncode if proc.returncode is not None else -1
    mem_kb = 0
    if resource is not None:
        try:
            mem_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        except Exception:
            mem_kb = 0
    return RunResult(rc=rc, stdout=out, stderr=err, duration=duration, timed_out=timed_out, mem_kb=int(mem_kb))
