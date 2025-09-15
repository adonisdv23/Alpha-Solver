from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from alpha.api.health import get_health


def test_health_smoke():
    data = get_health()
    assert data["app"] == "ok"
