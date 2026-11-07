from __future__ import annotations

from app.core.user_prefs import (
    get_nmap_scan_timeout_s,
    is_allow_public_scan,
    is_scan_authorized,
    load_preferences,
    set_allow_public_scan,
    set_nmap_scan_timeout_s,
    set_scan_authorized,
)


def test_prefs_roundtrip(prefs_tmp):
    set_scan_authorized(True)
    set_allow_public_scan(True)
    data = load_preferences()
    assert data["scan_authorized"] is True
    assert data["allow_public_scan"] is True
    assert is_scan_authorized()
    assert is_allow_public_scan()


def test_nmap_timeout_roundtrip(prefs_tmp):
    set_nmap_scan_timeout_s(90)
    assert load_preferences()["nmap_scan_timeout_s"] == 90
    assert get_nmap_scan_timeout_s() == 90


def test_nmap_timeout_env_override(prefs_tmp, monkeypatch):
    set_nmap_scan_timeout_s(300)
    monkeypatch.setenv("NEDSCANNER_NMAP_TIMEOUT_S", "45")
    assert get_nmap_scan_timeout_s() == 45


def test_nmap_timeout_env_clamps_to_minimum(prefs_tmp, monkeypatch):
    monkeypatch.setenv("NEDSCANNER_NMAP_TIMEOUT_S", "1")
    assert get_nmap_scan_timeout_s() == 30
