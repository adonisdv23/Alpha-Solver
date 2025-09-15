from __future__ import annotations

"""Per-request model-set resolver.

Selects a model set based on explicit request parameters, tenant defaults, or
configured global default. The resolution is deterministic and records an
explanation for observability.
"""

from typing import Dict, Mapping, Optional, Tuple

from .modelset_registry import ModelSet, ModelSetRegistry, ModelSetError

__all__ = ["ModelSetResolver"]


class ModelSetResolver:
    def __init__(self, registry: ModelSetRegistry, global_default: str = "default"):
        self.registry = registry
        self.global_default = (
            global_default if global_default in registry.names() else registry.names()[0]
        )

    # --------------------------------------------------------------
    def resolve(
        self,
        *,
        requested: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
        tenant_default: Optional[str] = None,
        route_explain: Optional[Dict[str, str]] = None,
    ) -> Tuple[ModelSet, str]:
        """Resolve the model set.

        Args:
            requested: explicit request flag.
            headers: request headers (case-insensitive lookup for ``X-Model-Set``).
            tenant_default: tenant configured default model set name.
            route_explain: optional dict populated with ``model_set`` and
                ``model_set_reason``.

        Returns:
            (ModelSet, reason) tuple where reason explains the selection.
        """

        reason = ""

        header_choice = None
        if headers:
            for k, v in headers.items():
                if k.lower() == "x-model-set":
                    header_choice = v
                    break

        candidate = requested or header_choice
        if candidate:
            if candidate in self.registry.names():
                selected_name = candidate
                reason = "requested"
            else:
                selected_name = self.global_default
                reason = f"unknown-requested:{candidate}"
        elif tenant_default and tenant_default in self.registry.names():
            selected_name = tenant_default
            reason = "tenant-default"
        else:
            selected_name = self.global_default
            if tenant_default and tenant_default not in self.registry.names():
                reason = f"unknown-tenant-default:{tenant_default}"
            else:
                reason = "global-default"

        if route_explain is not None:
            route_explain["model_set"] = selected_name
            route_explain["model_set_reason"] = reason

        return self.registry.get(selected_name), reason

