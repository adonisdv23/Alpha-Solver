"""Session-wide test configuration.

The bundled API app (``service.app:app``) only mounts the dashboard UI when a
non-default ``ALPHA_DASHBOARD_PASSWORD`` is configured (fail-closed). That
decision is made at import time, so the password must already be present before
any test module imports ``service.app``. pytest imports this rootdir conftest
before collecting test modules, so setting the values here keeps the real-app
dashboard tests exercising a configured deployment. Individual tests still
override these via ``monkeypatch`` as needed.
"""

import os

os.environ.setdefault("ALPHA_DASHBOARD_PASSWORD", "ci-dashboard-secret")
os.environ.setdefault("ALPHA_DASHBOARD_SECRET_KEY", "ci-dashboard-signing-key")
