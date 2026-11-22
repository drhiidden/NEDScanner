#!/usr/bin/env sh
# Verificación local pre-push (Tier D adoptante). Lógica en tests/ (incl. OPSEC).
set -e
cd "$(dirname "$0")/.."
PY="${PY:-./venv/bin/python}"
if [ ! -x "$PY" ]; then PY=python3; fi

if ! "$PY" -c "import pytest" 2>/dev/null; then
  echo "pytest no instalado — pip install -r requirements-dev.txt" >&2
  exit 1
fi

echo "== pytest =="
env -u NEDSCANNER_DEMO "$PY" -m pytest -q tests/

echo "== commit messages (ahead of origin) =="
if [ -x scripts/check-unpushed-commit-messages.sh ]; then
  sh scripts/check-unpushed-commit-messages.sh
fi

echo "verify-local: OK"
