"""Red ficticia para UI sin privileges (no sockets raw). Distinta de referencias GPL."""
from app.models.host import HostRecord
from app.models.nmap_host import NmapHost, NmapPort
from app.models.wifi_network import WifiNetwork

DEMO_CIDR = "192.168.99.0/24"

DEMO_HOSTS: list[HostRecord] = [
    HostRecord("192.168.99.1", "aa:bb:cc:00:00:01", "gateway.home", ["demo"], vendor="Demo", demo=True),
    HostRecord("192.168.99.10", "aa:bb:cc:00:00:0a", "workstation.home", ["demo", "ARP"], vendor="Demo", demo=True),
    HostRecord("192.168.99.20", "aa:bb:cc:00:00:14", "printer.home", ["demo", "mDNS"], vendor="Demo", demo=True),
    HostRecord("192.168.99.50", "aa:bb:cc:00:00:32", "iot-camera.home", ["demo", "ICMP"], vendor="Demo", demo=True),
]

DEMO_WIFI: list[WifiNetwork] = [
    WifiNetwork("NED-Demo", "aa:bb:cc:dd:ee:01", 1, -45, "WPA2", demo=True),
    WifiNetwork("NED-Lab-5G", "11:22:33:44:55:66", 36, -58, "WPA2-Enterprise", demo=True),
    WifiNetwork("NED-Guest", "aa:bb:cc:00:11:22", 11, -70, "Abierta", demo=True),
]

DEMO_NMAP: list[NmapHost] = [
    NmapHost(
        "192.168.99.1",
        hostname="gateway.home",
        status="up",
        mac="aa:bb:cc:00:00:01",
        vendor="Demo",
        os_match="Linux",
        ports=[
            NmapPort(22, "tcp", "open", "ssh"),
            NmapPort(443, "tcp", "open", "https"),
        ],
        demo=True,
    ),
    NmapHost(
        "192.168.99.10",
        hostname="workstation.home",
        status="up",
        mac="aa:bb:cc:00:00:0a",
        vendor="Demo",
        os_match="Linux",
        ports=[NmapPort(22, "tcp", "open", "ssh")],
        demo=True,
    ),
]
