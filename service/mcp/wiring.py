from __future__ import annotations

"""MCP wiring helpers."""

from dataclasses import dataclass
import time
from typing import Any, Dict, Union

from registries.mcp.loader import load_registry


@dataclass
class MCPContext:
    """Runtime context for loaded MCP registry."""

    registry: Dict[str, Any]
    version: str
    loaded_at: float


def init_mcp(path_or_obj: Union[str, Dict[str, Any]]) -> MCPContext:
    """Load the registry and return an :class:`MCPContext` instance."""
    registry = load_registry(path_or_obj)
    version = str(registry.get("version", "unknown"))
    return MCPContext(registry=registry, version=version, loaded_at=time.time())


def tool_summary(ctx: MCPContext) -> Dict[str, Any]:
    """Return counts of tools by type and enabled/disabled."""
    summary_by_type = {"http": 0, "script": 0, "remote": 0}
    enabled = disabled = 0
    for tool in ctx.registry.get("tool", []):
        t_type = tool["type"]
        summary_by_type[t_type] = summary_by_type.get(t_type, 0) + 1
        if tool.get("enabled", True):
            enabled += 1
        else:
            disabled += 1
    return {"by_type": summary_by_type, "enabled": enabled, "disabled": disabled}


def to_route_explain(ctx: MCPContext) -> Dict[str, Any]:
    """Return a minimal dict for routing/explanation purposes."""
    return {"registry_version": ctx.version, "tools": tool_summary(ctx)}
