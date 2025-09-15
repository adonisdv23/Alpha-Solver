import json, sys, pathlib

THRESHOLDS = {
    "retry_p95_max": 2,
    "breaker_open_p95_ms_max": 100,
}

def p95(values):
    if not values:
        return 0
    values = sorted(values)
    idx = int(round(0.95 * (len(values) - 1)))
    return values[idx]

def extract_metrics(report):
    """
    pytest-json-report:
      report["tests"] -> list of test dicts; each may have test["metadata"] with:
        - "retries" (int)
        - "breaker_open_ms" (float/int)
    Missing fields are ignored.
    """
    tests = report.get("tests", [])
    retries, opens_ms = [], []
    for t in tests:
        meta = t.get("metadata", {}) or {}
        r = meta.get("retries")
        o = meta.get("breaker_open_ms")
        if isinstance(r, (int, float)):
            retries.append(int(r))
        if isinstance(o, (int, float)):
            opens_ms.append(float(o))
    return retries, opens_ms

def main(path="artifacts/reliability.json"):
    p = pathlib.Path(path)
    if not p.exists():
        print(f"[SLO] report not found: {path}", file=sys.stderr)
        return 2
    try:
        data = json.loads(p.read_text())
    except Exception as e:
        print(f"[SLO] failed to parse report {path}: {e}", file=sys.stderr)
        return 2

    retries, opens_ms = extract_metrics(data)
    retry_p95 = p95(retries)
    open_p95  = p95(opens_ms)

    ok_retry = retry_p95 < THRESHOLDS["retry_p95_max"]
    ok_open  = open_p95  < THRESHOLDS["breaker_open_p95_ms_max"]

    print(
        f"[SLO] retry_p95={retry_p95} (max<{THRESHOLDS['retry_p95_max']}), "
        f"breaker_open_p95_ms={open_p95:.0f} (max<{THRESHOLDS['breaker_open_p95_ms_max']})"
    )
    return 0 if (ok_retry and ok_open) else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "artifacts/reliability.json"))
