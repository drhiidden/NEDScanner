"""Preferencias locales del usuario (sin dependencia de Qt)."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.core.paths import nedscaner_home
from app.core.safe_io import atomic_write_json

_PREFS_FILE = "preferences.json"
_DEFAULTS: dict[str, Any] = {
    "scan_authorized": False,
    "allow_public_scan": False,
}


def preferences_path() -> Path:
    return nedscaner_home() / _PREFS_FILE


def load_preferences() -> dict[str, Any]:
    path = preferences_path()
    if not path.is_file():
        return dict(_DEFAULTS)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULTS)
    merged = dict(_DEFAULTS)
    merged.update({k: data[k] for k in _DEFAULTS if k in data})
    return merged


def save_preferences(data: dict[str, Any]) -> None:
    payload = dict(_DEFAULTS)
    payload.update({k: data.get(k, _DEFAULTS[k]) for k in _DEFAULTS})
    atomic_write_json(preferences_path(), payload)


def is_scan_authorized() -> bool:
    if os.environ.get("NEDSCANNER_I_ACK_AUTHORIZED", "").strip() == "1":
        return True
    return bool(load_preferences().get("scan_authorized"))


def set_scan_authorized(authorized: bool) -> None:
    data = load_preferences()
    data["scan_authorized"] = authorized
    save_preferences(data)


def is_allow_public_scan() -> bool:
    if os.environ.get("NEDSCANNER_ALLOW_PUBLIC", "").strip() == "1":
        return True
    return bool(load_preferences().get("allow_public_scan"))


def set_allow_public_scan(allowed: bool) -> None:
    data = load_preferences()
    data["allow_public_scan"] = allowed
    save_preferences(data)
