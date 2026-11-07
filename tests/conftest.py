"""Fixtures aisladas para tests (sin tocar red real)."""
from __future__ import annotations

import pytest

from app.core import config


@pytest.fixture(autouse=True)
def _reset_demo_cache():
    config.is_demo_mode.cache_clear()
    yield
    config.is_demo_mode.cache_clear()


@pytest.fixture
def demo_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NEDSCANNER_DEMO", "1")
    config.is_demo_mode.cache_clear()
    yield
    monkeypatch.delenv("NEDSCANNER_DEMO", raising=False)
    config.is_demo_mode.cache_clear()


@pytest.fixture
def authorized_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("NEDSCANNER_DEMO", raising=False)
    monkeypatch.setenv("NEDSCANNER_I_ACK_AUTHORIZED", "1")
    config.is_demo_mode.cache_clear()
    yield


@pytest.fixture
def prefs_tmp(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Inventario y preferencias en directorio temporal."""
    prefs_file = tmp_path / "preferences.json"
    known_file = tmp_path / "known-devices.json"

    def _prefs_path():
        return prefs_file

    def _known_path():
        return known_file

    import app.core.user_prefs as user_prefs
    import app.core.known_inventory as known_inventory

    monkeypatch.setattr(user_prefs, "preferences_path", _prefs_path)
    monkeypatch.setattr(known_inventory, "known_devices_path", _known_path)
    yield tmp_path
