import asyncio
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor

from app.core.config import is_demo_mode
from app.core.demo_data import DEMO_NMAP
from app.models.nmap_host import NmapHost, NmapPort

logger = logging.getLogger("NEDScanner.nmap")

_PROFILES = {
    0: "-sn",
    1: "-F",
    2: "-p1-1000",
    3: "-p-",
}


class NmapScanAdapter:
    def __init__(self) -> None:
        self._pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix="ned-nmap")

    def shutdown(self) -> None:
        self._pool.shutdown(wait=False, cancel_futures=True)

    async def scan(
        self,
        target: str,
        profile_index: int = 1,
        service_version: bool = False,
        os_detection: bool = False,
    ) -> list[NmapHost]:
        if is_demo_mode():
            await asyncio.sleep(0.8)
            if target.strip():
                return [h for h in DEMO_NMAP if h.ip in target or target in h.ip]
            return list(DEMO_NMAP)

        if not shutil.which("nmap"):
            raise RuntimeError("nmap no instalado (sudo apt install nmap)")

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self._pool,
            lambda: self._scan_sync(target, profile_index, service_version, os_detection),
        )

    def _scan_sync(
        self,
        target: str,
        profile_index: int,
        service_version: bool,
        os_detection: bool,
    ) -> list[NmapHost]:
        import nmap  # lazy

        arguments = _PROFILES.get(profile_index, "-F")
        if service_version:
            arguments += " -sV"
        if os_detection:
            arguments += " -O"

        scanner = nmap.PortScanner()
        scanner.scan(hosts=target, arguments=arguments)

        hosts: list[NmapHost] = []
        for host in scanner.all_hosts():
            info = scanner[host]
            status = info.state()
            hostname = info.hostname() or ""
            mac = ""
            vendor = ""
            if "addresses" in info and "mac" in info["addresses"]:
                mac = info["addresses"]["mac"]
            if "vendor" in info and mac in info["vendor"]:
                vendor = info["vendor"][mac]

            os_match = ""
            if "osmatch" in info and info["osmatch"]:
                os_match = info["osmatch"][0].get("name", "")

            ports: list[NmapPort] = []
            for proto in info.all_protocols():
                for port in sorted(info[proto].keys()):
                    pdata = info[proto][port]
                    ports.append(
                        NmapPort(
                            int(port),
                            proto,
                            pdata.get("state", ""),
                            pdata.get("name", ""),
                        )
                    )

            hosts.append(
                NmapHost(
                    ip=host,
                    hostname=hostname,
                    status=status,
                    mac=mac,
                    vendor=vendor,
                    os_match=os_match,
                    ports=ports,
                )
            )
        return hosts
