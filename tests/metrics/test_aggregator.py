import re
import time
import yaml
from pathlib import Path
import pytest
from pytest import MonkeyPatch

from alpha.metrics.aggregator import (
    adapter_latency_ms,
    budget_spend_cents,
    gate_decisions_total,
    get_metrics_text,
    replay_pass_total,
)
from service.auth.jwt_utils import AuthKeyStore


@pytest.fixture(scope="session", autouse=True)
def _hires_auth_reload():
    mp = MonkeyPatch()
    orig = AuthKeyStore.reload

    def reload(self, force: bool = False) -> None:  # type: ignore[override]
        try:
            with self.path.open() as f:
                data = yaml.safe_load(f) or {}
        except FileNotFoundError:
            self._keys = {}
            return
        keys = {}
        for kid, value in data.items():
            if isinstance(value, dict):
                pem = value.get("public_key") or value.get("key") or ""
            else:
                pem = value or ""
            keys[kid] = pem
        self._keys = keys

    mp.setattr(AuthKeyStore, "reload", reload)
    yield
    mp.setattr(AuthKeyStore, "reload", orig)


def _metric_names(text: str) -> set[str]:
    names = set()
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        assert re.match(r"^[a-zA-Z_:][a-zA-Z0-9_:]*({.*})?\s+[-+]?[0-9.eE+-]+$", line)
        name = line.split("{" ,1)[0].split()[0]
        names.add(name)
    return names


def test_exporter_prometheus_series_and_performance():
    # Touch the counters so they appear in output.
    gate_decisions_total.inc()
    replay_pass_total.inc()
    budget_spend_cents.inc()
    adapter_latency_ms.observe(3)

    get_metrics_text()  # warm path
    t0 = time.perf_counter()
    text = get_metrics_text()
    elapsed_ms = (time.perf_counter() - t0) * 1000

    assert elapsed_ms < 100

    names = _metric_names(text)
    assert "gate_decisions_total" in names
    assert "replay_pass_total" in names
    assert "budget_spend_cents" in names
    assert "adapter_latency_ms" in names

