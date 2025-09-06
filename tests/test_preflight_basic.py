from scripts.preflight import _basic_registry_checks
import pytest

def test_duplicate_detection():
    tools = [
        {"tool_id":"x","name":"A","description":"d"},
        {"tool_id":"x","name":"B","description":"d"},
    ]
    with pytest.raises(SystemExit):
        _basic_registry_checks(tools)

def test_required_fields():
    tools = [{"tool_id":"x","name":"A","description":"d"}]
    # Should pass without raising
    _basic_registry_checks(tools)
