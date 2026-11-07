from __future__ import annotations

import pytest

from app.adapters.discovery_adapter import DiscoveryAdapter
from app.adapters.nmap_adapter import NmapScanAdapter
from app.adapters.nmcli_adapter import WifiScanAdapter
from app.core.demo_data import DEMO_CIDR, DEMO_HOSTS, DEMO_NMAP, DEMO_WIFI
from app.core.scan_policy import ScanPolicyError


@pytest.mark.asyncio
async def test_discovery_demo_returns_hosts(demo_env):
    adapter = DiscoveryAdapter()
    try:
        hosts = await adapter.discover(DEMO_CIDR, use_arp=True, use_icmp=False)
        assert len(hosts) == len(DEMO_HOSTS)
        assert all(h.demo for h in hosts)
        assert {h.ip for h in hosts} == {h.ip for h in DEMO_HOSTS}
    finally:
        adapter.shutdown()


@pytest.mark.asyncio
async def test_wifi_demo_returns_networks(demo_env):
    nets = await WifiScanAdapter().list_networks()
    assert len(nets) >= 1
    assert nets[0].ssid in {w.ssid for w in DEMO_WIFI}


@pytest.mark.asyncio
async def test_nmap_demo_filters_target(demo_env):
    adapter = NmapScanAdapter()
    try:
        hosts = await adapter.scan("192.168.99.10", profile_index=1)
        assert hosts
        assert hosts[0].ip in {"192.168.99.10", "192.168.99.1"}
        all_hosts = await adapter.scan(",".join(h.ip for h in DEMO_NMAP[:2]), profile_index=1)
        assert len(all_hosts) >= 1
    finally:
        adapter.shutdown()


@pytest.mark.asyncio
async def test_discovery_rejects_bad_cidr_when_not_demo(authorized_env, prefs_tmp):
    from app.core.user_prefs import set_scan_authorized

    set_scan_authorized(True)
    adapter = DiscoveryAdapter()
    try:
        with pytest.raises((ScanPolicyError, ValueError)):
            await adapter.discover("not-a-network", use_arp=True)
    finally:
        adapter.shutdown()
