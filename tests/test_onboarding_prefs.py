from __future__ import annotations

from app.core.user_prefs import (
    is_onboarding_complete,
    set_onboarding_complete,
    load_preferences,
)


def test_onboarding_defaults_false(prefs_tmp):
    assert load_preferences()["onboarding_complete"] is False
    assert is_onboarding_complete() is False


def test_onboarding_roundtrip(prefs_tmp):
    set_onboarding_complete(True)
    assert load_preferences()["onboarding_complete"] is True
    assert is_onboarding_complete() is True


def test_onboarding_skip_env(prefs_tmp, monkeypatch):
    set_onboarding_complete(False)
    monkeypatch.setenv("NEDSCANNER_SKIP_ONBOARDING", "1")
    assert is_onboarding_complete() is True