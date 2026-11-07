from __future__ import annotations

from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core.known_inventory import (
    add_known_host,
    add_known_network,
    list_devices,
    list_networks,
    load_inventory,
    remove_device_at,
    remove_network_at,
)
from app.core.paths import known_devices_path


class InventorySettingsPane(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel(f"Archivo: {known_devices_path()}"))

        self.devices_list = QListWidget()
        dev_group = QGroupBox("Dispositivos LAN conocidos")
        dev_l = QVBoxLayout()
        dev_l.addWidget(self.devices_list)
        dev_row = QHBoxLayout()
        self.dev_ip = QLineEdit()
        self.dev_ip.setPlaceholderText("IP")
        self.dev_mac = QLineEdit()
        self.dev_mac.setPlaceholderText("MAC (opcional)")
        self.dev_name = QLineEdit()
        self.dev_name.setPlaceholderText("Hostname o etiqueta")
        dev_row.addWidget(self.dev_ip)
        dev_row.addWidget(self.dev_mac)
        dev_row.addWidget(self.dev_name)
        add_dev = QPushButton("Añadir")
        add_dev.clicked.connect(self._add_device)
        rm_dev = QPushButton("Quitar selección")
        rm_dev.clicked.connect(self._remove_device)
        dev_row.addWidget(add_dev)
        dev_row.addWidget(rm_dev)
        dev_l.addLayout(dev_row)
        dev_group.setLayout(dev_l)
        layout.addWidget(dev_group)

        self.networks_list = QListWidget()
        net_group = QGroupBox("Redes Wi‑Fi conocidas")
        net_l = QVBoxLayout()
        net_l.addWidget(self.networks_list)
        net_row = QHBoxLayout()
        self.net_ssid = QLineEdit()
        self.net_ssid.setPlaceholderText("SSID")
        self.net_bssid = QLineEdit()
        self.net_bssid.setPlaceholderText("BSSID (opcional)")
        net_row.addWidget(self.net_ssid)
        net_row.addWidget(self.net_bssid)
        add_net = QPushButton("Añadir")
        add_net.clicked.connect(self._add_network)
        rm_net = QPushButton("Quitar selección")
        rm_net.clicked.connect(self._remove_network)
        net_row.addWidget(add_net)
        net_row.addWidget(rm_net)
        net_l.addLayout(net_row)
        net_group.setLayout(net_l)
        layout.addWidget(net_group)

        reload_btn = QPushButton("Recargar inventario")
        reload_btn.clicked.connect(self.refresh_lists)
        layout.addWidget(reload_btn)

        load_inventory()
        self.refresh_lists()

    def refresh_lists(self) -> None:
        self.devices_list.clear()
        for d in list_devices():
            self.devices_list.addItem(
                f"{d.get('ip', '?')}  {d.get('mac', '')}  "
                f"{d.get('hostname') or d.get('label', '')}"
            )
        self.networks_list.clear()
        for n in list_networks():
            self.networks_list.addItem(f"{n.get('ssid', '?')}  {n.get('bssid', '')}")

    def _add_device(self) -> None:
        ip = self.dev_ip.text().strip()
        if not ip:
            return
        try:
            add_known_host(
                ip, self.dev_mac.text() or None, self.dev_name.text() or None
            )
        except ValueError as exc:
            return
        self.dev_ip.clear()
        self.dev_mac.clear()
        self.dev_name.clear()
        self.refresh_lists()

    def _add_network(self) -> None:
        ssid = self.net_ssid.text().strip()
        if not ssid:
            return
        try:
            add_known_network(ssid, self.net_bssid.text() or None)
        except ValueError:
            return
        self.net_ssid.clear()
        self.net_bssid.clear()
        self.refresh_lists()

    def _remove_device(self) -> None:
        row = self.devices_list.currentRow()
        if row >= 0:
            remove_device_at(row)
            self.refresh_lists()

    def _remove_network(self) -> None:
        row = self.networks_list.currentRow()
        if row >= 0:
            remove_network_at(row)
            self.refresh_lists()
