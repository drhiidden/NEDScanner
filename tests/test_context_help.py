from __future__ import annotations

from app.ui.context_help import HELP_BY_TAB, tab_key_from_index


def test_tab_key_from_index_matches_tabs():
    assert tab_key_from_index(0) == "wifi"
    assert tab_key_from_index(4) == "learning"
    assert tab_key_from_index(5) == "settings"
    assert tab_key_from_index(99) is None


def test_help_covers_all_tab_keys():
    for key in ("wifi", "nmap", "discovery", "results", "learning", "settings"):
        assert key in HELP_BY_TAB
        title, body = HELP_BY_TAB[key]
        assert title
        assert body