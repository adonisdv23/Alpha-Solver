import pytest
from service.metrics.testing import reset_registry

@pytest.fixture(autouse=True)
def _reset_metrics():
    reset_registry()
    yield
