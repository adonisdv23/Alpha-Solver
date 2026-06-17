# Routing preview behavior

The console uses the existing backend metadata-only routing modules:

- `alpha/model_router.py`
- `alpha/tool_router.py`
- existing model and tool catalog files loaded by those routers

The console adapter builds a read-only preview response from those modules. It sets hosted provider execution to not allowed for preview and exposes `provider_or_local_execution_authorized=false` and `tool_execution_authorized=false`.

No provider client, local model runtime, tool executor, browser, runtime GitHub call, external network call, file mutation, telemetry, or persistence path is part of preview behavior.
