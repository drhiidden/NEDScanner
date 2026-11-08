"""Puertos hexagonales (typing.Protocol) — contratos de adaptadores."""
from __future__ import annotations

from typing import Optional, Protocol

from app.models.host import HostRecord
from app.models.nmap_host import NmapHost
from app.models.wifi_network import WifiNetwork


class SupportsShutdown(Protocol):
    def shutdown(self) -> None: ...


class DiscoveryPort(Protocol):
    async def discover(
        self,
        target: str,
        *,
        use_arp: bool = True,
        use_icmp: bool = True,
    ) -> list[HostRecord]: ...

    def shutdown(self) -> None: ...


class NmapScanPort(Protocol):
    async def scan(
        self,
        target: str,
        profile_index: int = 1,
        service_version: bool = False,
        os_detection: bool = False,
    ) -> list[NmapHost]: ...

    def shutdown(self) -> None: ...


class WifiScanPort(Protocol):
    async def rescan(self) -> None: ...

    async def list_networks(self, interface: Optional[str] = None) -> list[WifiNetwork]: ...
