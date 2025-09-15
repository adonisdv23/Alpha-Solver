import os
from typing import Dict


def compute_snapshot() -> Dict[str, str]:
    """Compute a minimal snapshot of environment state."""
    return {
        "model_set": os.getenv("MODEL_SET", "default"),
        "rules_sha": os.getenv("RULES_SHA", "rules"),
        "gates_sha": os.getenv("GATES_SHA", "gates"),
        "tool_registry_sha": os.getenv("TOOL_REGISTRY_SHA", "tools"),
    }
