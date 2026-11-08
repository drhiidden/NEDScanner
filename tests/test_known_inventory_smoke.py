from __future__ import annotations

import tempfile
from pathlib import Path

from app.core import known_inventory as ki


def test_inventory_roundtrip_temp_path():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "known-devices.json"
        assert not ki.is_host_known("10.0.0.5", path=p)
        ki.add_known_host("10.0.0.1", "aa:bb:cc:dd:ee:01", label="gw", path=p)
        assert ki.is_host_known("10.0.0.1", path=p)
        assert ki.host_trust_label("10.0.0.9", path=p) == "Desconocido"
        ki.add_known_network("Home", "11:22:33:44:55:66", path=p)
        assert ki.is_wifi_known("Home", path=p)
