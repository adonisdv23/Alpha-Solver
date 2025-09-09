#!/usr/bin/env bash
# Reliable, idempotent setup for pre-commit via an isolated venv
set -u  # don't use -e so Codespaces won't fall into recovery on transient errors

VENV="$HOME/.venvs/precommit"
STAMP=".devcontainer/last_setup.txt"

# Ensure PATH includes our venv and user bin directories now and later
export PATH="$VENV/bin:$HOME/.local/bin:$PATH"
grep -qxF "export PATH=\"$VENV/bin:$HOME/.local/bin:\$PATH\"" ~/.bashrc  || echo "export PATH=\"$VENV/bin:$HOME/.local/bin:\$PATH\"" >> ~/.bashrc
grep -qxF "export PATH=\"$VENV/bin:$HOME/.local/bin:\$PATH\"" ~/.profile || echo "export PATH=\"$VENV/bin:$HOME/.local/bin:\$PATH\"" >> ~/.profile

# Avoid pip env quirks that break console_scripts
unset PIP_TARGET PIP_PREFIX PYTHONUSERBASE || true

# Proxy-aware pip config
if [ -n "${HTTPS_PROXY:-${HTTP_PROXY:-}}" ]; then
  mkdir -p "$HOME/.pip"
  {
    echo "[global]"
    echo "proxy = ${HTTPS_PROXY:-${HTTP_PROXY}}"
  } > "$HOME/.pip/pip.conf"
fi

# Install pre-commit if needed with wheel fallbacks
if ! "$VENV/bin/pre-commit" --version 2>/dev/null | grep -q '^pre-commit 4.3.0'; then
  python -m venv "$VENV" >/dev/null 2>&1 || true
  "$VENV/bin/python" -m pip install --upgrade pip wheel >/dev/null 2>&1 || true
  if ! "$VENV/bin/python" -m pip install pre-commit==4.3.0 >/dev/null 2>&1; then
    if ! "$VENV/bin/python" -m pip install ".devcontainer/assets/pre_commit-4.3.0-py3-none-any.whl" >/dev/null 2>&1; then
      "$VENV/bin/python" -m pip install "https://github.com/pre-commit/pre-commit/releases/download/v4.3.0/pre_commit-4.3.0-py3-none-any.whl" >/dev/null 2>&1 || true
    fi
  fi
fi

# Shim (idempotent)
mkdir -p "$HOME/.local/bin"
ln -sf "$VENV/bin/pre-commit" "$HOME/.local/bin/pre-commit"

# Final checks and hook setup (safe on reruns)
python -m pre_commit --version || true
"$VENV/bin/pre-commit" --version || true
pre-commit install && pre-commit run --files README.md || true

# Breadcrumb
{
  "$VENV/bin/pre-commit" --version 2>/dev/null || echo "pre-commit missing"
  echo "setup-complete"
} > "$STAMP"

exit 0
