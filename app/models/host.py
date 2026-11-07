from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HostRecord:
    ip: str
    mac: str = ""
    hostname: str = ""
    methods: list[str] = field(default_factory=list)
    vendor: str = ""
    demo: bool = False

    def method_label(self) -> str:
        return ", ".join(self.methods) if self.methods else "—"
