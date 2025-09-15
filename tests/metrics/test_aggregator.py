import re
import time
import yaml
from pathlib import Path
import pytest
from pytest import MonkeyPatch

from alpha.metrics.aggregator import MetricsAggregator
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


def test_aggregator_prometheus_series_and_performance():
    agg = MetricsAggregator()
    client = agg.test_client()

    t0 = time.perf_counter()
    for _ in range(20):
        agg.record_gate("low_confidence")
        agg.record_replay("ok")
        agg.record_budget("under")
        agg.record_adapter("redis", latency_ms=3)
    text = client.get("/metrics").text
    elapsed_ms = (time.perf_counter() - t0) * 1000

    assert elapsed_ms < 100

    names = _metric_names(text)
    assert "alpha_solver_gate_total" in names
    assert "alpha_solver_replay_total" in names
    assert "alpha_solver_budget_total" in names
    assert "alpha_solver_adapter_calls_total" in names
    assert "alpha_solver_adapter_latency_ms" in names

