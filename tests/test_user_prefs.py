from __future__ import annotations

from app.core.user_prefs import (
    is_allow_public_scan,
    is_scan_authorized,
    load_preferences,
    set_allow_public_scan,
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
