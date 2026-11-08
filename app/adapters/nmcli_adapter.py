import asyncio
import logging
import shutil
from typing import Optional

from app.core.config import is_demo_mode
from app.core.log_redact import redact_subprocess_stderr
from app.core.scan_policy import validate_interface
from app.core.demo_data import DEMO_WIFI
from app.models.wifi_network import WifiNetwork

logger = logging.getLogger("NEDScanner.nmcli")


class WifiScanAdapter:
    async def rescan(self) -> None:
        if is_demo_mode() or not shutil.which("nmcli"):
            return
        proc = await asyncio.create_subprocess_exec(
            "nmcli", "device", "wifi", "rescan",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()

    async def list_networks(self, interface: Optional[str] = None) -> list[WifiNetwork]:
        if is_demo_mode():
            await asyncio.sleep(0.6)
            return list(DEMO_WIFI)

        if not shutil.which("nmcli"):
            logger.warning("nmcli no encontrado; usa NEDSCANNER_DEMO=1 en entornos sin NetworkManager")
            return list(DEMO_WIFI)

        await self.rescan()
        await asyncio.sleep(1.0)

        iface = validate_interface(interface)
        cmd = ["nmcli", "-t", "-f", "SSID,BSSID,CHAN,SIGNAL,SECURITY", "device", "wifi", "list"]
        if iface:
            cmd.extend(["ifname", iface])

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate()
        if proc.returncode != 0:
            logger.error(
                "nmcli falló (rc=%s): %s",
                proc.returncode,
                redact_subprocess_stderr(err),
            )
            return []

        networks: list[WifiNetwork] = []
        for line in out.decode(errors="replace").splitlines():
            if not line.strip():
                continue
            parts = line.split(":")
            if len(parts) < 5:
                continue
            ssid, bssid, chan, signal, security = parts[0], parts[1], parts[2], parts[3], parts[4]
            if not ssid.strip():
                continue
            try:
                channel = int(chan) if chan else 0
                signal_dbm = int(signal) if signal else 0
            except ValueError:
                channel, signal_dbm = 0, 0
            networks.append(
                WifiNetwork(
                    ssid=ssid.replace("\\:", ":"),
                    bssid=bssid,
                    channel=channel,
                    signal_dbm=signal_dbm,
                    security=security or "—",
                )
            )
        return networks
