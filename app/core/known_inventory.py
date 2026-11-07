"""Inventario de dispositivos/redes conocidos (~/.nedscaner/known-devices.json)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from app.core.paths import known_devices_path

_SCHEMA_VERSION = 1


def _normalize_mac(mac: str | None) -> str:
    if not mac or mac == "—":
        return ""
    cleaned = re.sub(r"[^0-9a-fA-F]", "", mac)
    if len(cleaned) != 12:
        return mac.lower().strip()
    return ":".join(cleaned[i : i + 2] for i in range(0, 12, 2)).lower()


def _empty_doc() -> dict[str, Any]:
    return {"version": _SCHEMA_VERSION, "devices": [], "networks": []}


def load_inventory(path: Path | None = None) -> dict[str, Any]:
    p = path or known_devices_path()
    if not p.is_file():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(_empty_doc(), indent=2), encoding="utf-8")
        return _empty_doc()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = _empty_doc()
    if "devices" not in data:
        data["devices"] = []
    if "networks" not in data:
        data["networks"] = []
    return data


def save_inventory(data: dict[str, Any], path: Path | None = None) -> None:
    p = path or known_devices_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    data["version"] = _SCHEMA_VERSION
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")


def is_host_known(
    ip: str | None,
    mac: str | None = None,
    hostname: str | None = None,
    *,
    path: Path | None = None,
) -> bool:
    data = load_inventory(path)
    nip = (ip or "").strip()
    nmac = _normalize_mac(mac)
    host = (hostname or "").strip().lower()
    for dev in data["devices"]:
        if nmac and _normalize_mac(dev.get("mac")) == nmac:
            return True
        if nip and dev.get("ip") == nip:
            return True
        if host and (dev.get("hostname") or "").lower() == host:
            return True
    return False


def is_wifi_known(ssid: str | None, bssid: str | None = None, *, path: Path | None = None) -> bool:
    data = load_inventory(path)
    ss = (ssid or "").strip()
    b = _normalize_mac(bssid)
    for net in data["networks"]:
        if ss and net.get("ssid") == ss:
            return True
        if b and _normalize_mac(net.get("bssid")) == b:
            return True
    return False


def host_trust_label(
    ip: str | None,
    mac: str | None = None,
    hostname: str | None = None,
    *,
    path: Path | None = None,
) -> str:
    return "Conocido" if is_host_known(ip, mac, hostname, path=path) else "Desconocido"


def wifi_trust_label(ssid: str, bssid: str | None = None) -> str:
    return "Conocida" if is_wifi_known(ssid, bssid) else "Desconocida"


def add_known_host(
    ip: str,
    mac: str | None = None,
    hostname: str | None = None,
    label: str | None = None,
    *,
    path: Path | None = None,
) -> None:
    data = load_inventory(path)
    entry = {
        "ip": ip.strip(),
        "mac": _normalize_mac(mac) or (mac or "").strip(),
        "hostname": (hostname or "").strip(),
        "label": (label or "").strip(),
    }
    if is_host_known(entry["ip"], entry["mac"] or None, entry["hostname"] or None, path=path):
        return
    data["devices"].append(entry)
    save_inventory(data, path)


def add_known_network(
    ssid: str,
    bssid: str | None = None,
    label: str | None = None,
    *,
    path: Path | None = None,
) -> None:
    data = load_inventory(path)
    if is_wifi_known(ssid, bssid, path=path):
        return
    data["networks"].append(
        {
            "ssid": ssid.strip(),
            "bssid": _normalize_mac(bssid) or (bssid or "").strip(),
            "label": (label or "").strip(),
        }
    )
    save_inventory(data, path)


def remove_device_at(index: int) -> None:
    data = load_inventory()
    if 0 <= index < len(data["devices"]):
        data["devices"].pop(index)
        save_inventory(data)


def remove_network_at(index: int) -> None:
    data = load_inventory()
    if 0 <= index < len(data["networks"]):
        data["networks"].pop(index)
        save_inventory(data)


def list_devices() -> list[dict[str, Any]]:
    return list(load_inventory()["devices"])


def list_networks() -> list[dict[str, Any]]:
    return list(load_inventory()["networks"])


def unknown_hosts_from_payload(payload: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in payload:
        ip = row.get("ip", "")
        mac = row.get("mac")
        hostname = row.get("hostname")
        if not is_host_known(ip, mac, hostname):
            out.append(row)
    return out
