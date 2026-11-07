"""Rutas de datos locales del usuario."""
from __future__ import annotations

import os
from pathlib import Path


def nedscaner_home() -> Path:
    return Path(os.path.expanduser("~/.nedscaner"))


def known_devices_path() -> Path:
    return nedscaner_home() / "known-devices.json"
