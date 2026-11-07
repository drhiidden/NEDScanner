#!/usr/bin/env sh
# Verificación local pre-push (sin CI remoto). Ejecutar desde raíz del repo.
set -e
cd "$(dirname "$0")/.."
PY="${PY:-./venv/bin/python}"
if [ ! -x "$PY" ]; then PY=python3; fi

export NEDSCANNER_DEMO=1

echo "== OPSEC quick scan =="
if command -v rg >/dev/null 2>&1; then
  if rg -n '\.procontext|/home/[a-z]+/projects/HALETHEIA|MINIPROMPT' app docs README.md AGENTS.md main.py 2>/dev/null; then
    echo "OPSEC violation" >&2
    exit 1
  fi
fi

echo "== smoke adapters =="
"$PY" - <<'PY'
import asyncio
from app.adapters.discovery_adapter import DiscoveryAdapter
from app.adapters.nmcli_adapter import WifiScanAdapter
from app.adapters.nmap_adapter import NmapScanAdapter

async def main():
    d = await DiscoveryAdapter().discover("10.0.0.0/24")
    assert len(d) == 4
    w = await WifiScanAdapter().list_networks()
    assert len(w) >= 1
    n = await NmapScanAdapter().scan("192.168.99.10")
    assert n
    print("smoke-ok")

asyncio.run(main())
PY

echo "verify-local: OK"
