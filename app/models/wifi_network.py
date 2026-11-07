from dataclasses import dataclass


@dataclass
class WifiNetwork:
    ssid: str
    bssid: str
    channel: int
    signal_dbm: int
    security: str
    demo: bool = False
