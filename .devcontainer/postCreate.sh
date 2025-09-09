#!/usr/bin/env bash
# Safe, idempotent setup for pre-commit via an isolated venv
set -u  # don't use -e so Codespaces won't fall into recovery on transient errors

# Ensure PATH includes our shims/venv now and later
export PATH="$HOME/.local/bin:$HOME/.venvs/precommit/bin:$PATH"
grep -qxF 'export PATH="$HOME/.local/bin:$HOME/.venvs/precommit/bin:$PATH"' ~/.bashrc  || echo 'export PATH="$HOME/.local/bin:$HOME/.venvs/precommit/bin:$PATH"' >> ~/.bashrc
grep -qxF 'export PATH="$HOME/.local/bin:$HOME/.venvs/precommit/bin:$PATH"' ~/.profile || echo 'export PATH="$HOME/.local/bin:$HOME/.venvs/precommit/bin:$PATH"' >> ~/.profile

# Avoid pip env quirks that break console_scripts
unset PIP_TARGET PIP_PREFIX PYTHONUSERBASE || true

# Create the venv if missing and install/upgrade pre-commit
if [ ! -x "$HOME/.venvs/precommit/bin/python" ]; then
  python -m venv "$HOME/.venvs/precommit" || true
fi
"$HOME/.venvs/precommit/bin/python" -m pip install --upgrade pip wheel pre-commit >/dev/null 2>&1 || true

# Shim (idempotent)
mkdir -p "$HOME/.local/bin"
ln -sf "$HOME/.venvs/precommit/bin/pre-commit" "$HOME/.local/bin/pre-commit"

# Register hooks; don't fail the container on lint issues
"$HOME/.venvs/precommit/bin/pre-commit" install >/dev/null 2>&1 || true
"$HOME/.venvs/precommit/bin/pre-commit" run --files README.md >/dev/null 2>&1 || true

# Breadcrumb
"$HOME/.venvs/precommit/bin/pre-commit" --version > .devcontainer/last_setup.txt 2>/dev/null || echo "pre-commit not installed" > .devcontainer/last_setup.txt
echo "setup-complete" >> .devcontainer/last_setup.txt

exit 0
