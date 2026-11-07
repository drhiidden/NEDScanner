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

echo "== known inventory =="
"$PY" - <<'PY'
import tempfile
from pathlib import Path
from app.core import known_inventory as ki

with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "known-devices.json"
    assert not ki.is_host_known("10.0.0.5", path=p)
    ki.add_known_host("10.0.0.1", "aa:bb:cc:dd:ee:01", label="gw", path=p)
    assert ki.is_host_known("10.0.0.1", path=p)
    assert ki.host_trust_label("10.0.0.9", path=p) == "Desconocido"
    ki.add_known_network("Home", "11:22:33:44:55:66", path=p)
    assert ki.is_wifi_known("Home", path=p)
print("inventory-ok")
PY

echo "verify-local: OK"
