"""Red ficticia para UI sin privileges (no sockets raw). Distinta de referencias GPL."""
from app.models.host import HostRecord

DEMO_CIDR = "192.168.99.0/24"

DEMO_HOSTS: list[HostRecord] = [
    HostRecord("192.168.99.1", "aa:bb:cc:00:00:01", "gateway.home", ["demo"], vendor="Demo", demo=True),
    HostRecord("192.168.99.10", "aa:bb:cc:00:00:0a", "workstation.home", ["demo", "ARP"], vendor="Demo", demo=True),
    HostRecord("192.168.99.20", "aa:bb:cc:00:00:14", "printer.home", ["demo", "mDNS"], vendor="Demo", demo=True),
    HostRecord("192.168.99.50", "aa:bb:cc:00:00:32", "iot-camera.home", ["demo", "ICMP"], vendor="Demo", demo=True),
]
