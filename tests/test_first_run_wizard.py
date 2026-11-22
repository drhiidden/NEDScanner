from __future__ import annotations

from app.ui.first_run_wizard import should_offer_onboarding
from app.core.user_prefs import set_onboarding_complete


def test_should_offer_onboarding_when_incomplete(prefs_tmp):
    assert should_offer_onboarding() is True


def test_should_not_offer_when_complete(prefs_tmp):
    set_onboarding_complete(True)
    assert should_offer_onboarding() is False