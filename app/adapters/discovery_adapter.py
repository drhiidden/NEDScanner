import asyncio
import logging
import socket
from concurrent.futures import ThreadPoolExecutor
from ipaddress import ip_network
from typing import Callable, Optional

from app.core.config import is_demo_mode
from app.core.scan_policy import validate_ipv4_cidr
from app.core.demo_data import DEMO_CIDR, DEMO_HOSTS
from app.models.host import HostRecord

logger = logging.getLogger("NEDScanner.discovery")

class DiscoveryAdapter:
    """Descubrimiento pasivo/activo ligero. Sin MITM ni credenciales (alcance NEDScanner MIT)."""

    def __init__(self, max_workers: int = 8) -> None:
        self._pool = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="ned-disc")

    def shutdown(self) -> None:
        self._pool.shutdown(wait=False, cancel_futures=True)

    async def discover(
        self,
        target: str,
        *,
        use_arp: bool = True,
        use_icmp: bool = True,
        use_mdns: bool = False,
        use_llmnr: bool = False,
        timeout_s: float = 5.0,
        progress: Optional[Callable[[str], None]] = None,
    ) -> list[HostRecord]:
        if is_demo_mode():
            if progress:
                progress("Modo demo: red ficticia")
            await asyncio.sleep(0.8)
            return list(DEMO_HOSTS)

        normalized = validate_ipv4_cidr(target.strip() or DEMO_CIDR)

        if progress:
            progress(f"Descubriendo {normalized}…")

        loop = asyncio.get_running_loop()
        hosts: dict[str, HostRecord] = {}

        if use_arp:
            arp_hosts = await loop.run_in_executor(
                self._pool,
                lambda: self._arp_scan(normalized, timeout_s),
            )
            for h in arp_hosts:
                hosts[h.ip] = h

        if use_icmp:
            icmp_hosts = await loop.run_in_executor(
                self._pool,
                lambda: self._icmp_scan(normalized, timeout_s),
            )
            for h in icmp_hosts:
                if h.ip in hosts:
                    hosts[h.ip].methods = sorted(set(hosts[h.ip].methods + ["ICMP"]))
                else:
                    hosts[h.ip] = h

        if use_mdns or use_llmnr:
            if progress:
                progress("mDNS/LLMNR: próximamente (v1.1)")

        return sorted(hosts.values(), key=lambda x: socket.inet_aton(x.ip))

    def _arp_scan(self, cidr: str, timeout_s: float) -> list[HostRecord]:
        try:
            from scapy.all import ARP, Ether, srp  # type: ignore
        except ImportError as exc:
            logger.warning("Scapy no disponible: %s", exc)
            return []

        try:
            pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=cidr)
            answered, _ = srp(pkt, timeout=timeout_s, verbose=0)
        except PermissionError:
            logger.error("ARP requiere cap_net_raw (setcap o sudo)")
            raise
        except OSError as exc:
            logger.error("ARP falló: %s", exc)
            raise

        out: list[HostRecord] = []
        for _, received in answered:
            ip = received.psrc
            mac = received.hwsrc
            out.append(HostRecord(ip=ip, mac=mac, methods=["ARP"]))
        return out

    def _icmp_scan(self, cidr: str, timeout_s: float) -> list[HostRecord]:
        net = ip_network(cidr, strict=False)
        hosts = list(net.hosts())[:254]
        found: list[HostRecord] = []

        def ping(ip: str) -> Optional[HostRecord]:
            try:
                from scapy.all import ICMP, IP, sr1  # type: ignore
            except ImportError:
                return None
            try:
                resp = sr1(IP(dst=ip) / ICMP(), timeout=timeout_s, verbose=0)
                if resp is not None:
                    return HostRecord(ip=ip, methods=["ICMP"])
            except PermissionError:
                raise
            except Exception:
                return None
            return None

        # Limit ping fan-out for /24
        for addr in hosts[:64]:
            rec = ping(str(addr))
            if rec:
                found.append(rec)
        return found
