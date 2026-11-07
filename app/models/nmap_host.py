from dataclasses import dataclass, field


@dataclass
class NmapPort:
    port: int
    protocol: str
    state: str
    service: str


@dataclass
class NmapHost:
    ip: str
    hostname: str = ""
    status: str = "unknown"
    mac: str = ""
    vendor: str = ""
    os_match: str = ""
    ports: list[NmapPort] = field(default_factory=list)
    demo: bool = False
