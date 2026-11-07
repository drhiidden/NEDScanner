from __future__ import annotations

import pytest

from app.core import config
from app.core.scan_policy import (
    ScanPolicyError,
    require_scan_authorization,
    validate_interface,
    validate_inventory_ip,
    validate_ipv4_address,
    validate_ipv4_cidr,
    validate_nmap_targets,
)
from app.core.user_prefs import set_allow_public_scan, set_scan_authorized


def test_cidr_valid_private(authorized_env, prefs_tmp):
    set_scan_authorized(True)
    assert validate_ipv4_cidr("192.168.10.0/24") == "192.168.10.0/24"


def test_cidr_rejects_injection(authorized_env, prefs_tmp):
    set_scan_authorized(True)
    with pytest.raises(ScanPolicyError):
        validate_ipv4_cidr("192.168.1.0/24;rm -rf /")


def test_cidr_rejects_too_broad(authorized_env, prefs_tmp):
    set_scan_authorized(True)
    with pytest.raises(ScanPolicyError):
        validate_ipv4_cidr("10.0.0.0/8")


def test_cidr_rejects_public_without_flag(authorized_env, prefs_tmp):
    set_scan_authorized(True)
    set_allow_public_scan(False)
    with pytest.raises(ScanPolicyError):
        validate_ipv4_cidr("8.8.8.8/24")


def test_cidr_allows_public_with_pref(authorized_env, prefs_tmp):
    set_scan_authorized(True)
    set_allow_public_scan(True)
    assert validate_ipv4_cidr("8.8.8.0/24") == "8.8.8.0/24"


def test_require_auth_blocks_without_ack(prefs_tmp, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("NEDSCANNER_I_ACK_AUTHORIZED", raising=False)
    monkeypatch.delenv("NEDSCANNER_DEMO", raising=False)
    config.is_demo_mode.cache_clear()
    set_scan_authorized(False)
    with pytest.raises(PermissionError):
        require_scan_authorization()


def test_require_auth_allows_with_pref(authorized_env, prefs_tmp):
    set_scan_authorized(True)
    require_scan_authorization()


def test_demo_skips_require_auth(demo_env, prefs_tmp):
    set_scan_authorized(False)
    require_scan_authorization()


def test_nmap_rejects_shell_chars(demo_env):
    with pytest.raises(ScanPolicyError):
        validate_nmap_targets("192.168.1.1|id")


def test_nmap_accepts_private_ips_demo(demo_env):
    assert validate_nmap_targets("192.168.99.10") == "192.168.99.10"


def test_nmap_hostname_only_in_demo(demo_env):
    assert validate_nmap_targets("host.local") == "host.local"


def test_nmap_hostname_blocked_real_scan(authorized_env, prefs_tmp):
    set_scan_authorized(True)
    with pytest.raises(ScanPolicyError):
        validate_nmap_targets("router.local")


def test_interface_valid():
    assert validate_interface("wlan0") == "wlan0"
    assert validate_interface(None) is None


def test_interface_invalid():
    with pytest.raises(ScanPolicyError):
        validate_interface("wlan0; evil")


def test_inventory_ip():
    assert validate_inventory_ip("192.168.0.1") == "192.168.0.1"


def test_demo_cidr_skips_public_check(demo_env):
    assert validate_ipv4_cidr("192.168.99.0/24") == "192.168.99.0/24"
    config.is_demo_mode.cache_clear()
