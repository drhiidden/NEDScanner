import json
from pathlib import Path

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTextEdit, QTableWidget, QTableWidgetItem, QLabel,
                             QProgressBar, QGroupBox, QHeaderView, QComboBox,
                             QCheckBox, QSpinBox, QFormLayout, QLineEdit,
                             QRadioButton, QButtonGroup, QGridLayout, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import logging

from qasync import asyncSlot

from app.adapters.discovery_adapter import DiscoveryAdapter
from app.core.config import is_demo_mode
from app.core.known_inventory import add_known_host, host_trust_label
from app.core.scan_history import ScanRecord, append_record
from app.models.host import HostRecord

logger = logging.getLogger("NEDScanner.ui.discovery")


class DiscoveryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.scanning = False
        self._adapter = DiscoveryAdapter()
        self._last_hosts: list[HostRecord] = []
        
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Panel superior: configuración de descubrimiento
        config_group = QGroupBox("Configuración de Descubrimiento Rápido")
        config_layout = QVBoxLayout()
        config_group.setLayout(config_layout)
        
        # Objetivo del escaneo
        target_layout = QFormLayout()
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Ej: 192.168.1.0/24")
        target_layout.addRow("Objetivo:", self.target_input)
        config_layout.addLayout(target_layout)
        
        # Métodos de descubrimiento
        methods_group = QGroupBox("Métodos de Descubrimiento")
        methods_layout = QGridLayout()
        
        # Crear opciones de métodos
        self.arp_check = QCheckBox("ARP Ping (solo LAN)")
        self.arp_check.setChecked(True)
        self.icmp_check = QCheckBox("ICMP Echo (ping)")
        self.tcp_check = QCheckBox("TCP SYN (puerto 80)")
        self.udp_check = QCheckBox("UDP (puerto 53)")
        self.mdns_check = QCheckBox("mDNS Discovery")
        self.llmnr_check = QCheckBox("LLMNR Discovery")
        
        # Organizar en grid
        methods_layout.addWidget(self.arp_check, 0, 0)
        methods_layout.addWidget(self.icmp_check, 0, 1)
        methods_layout.addWidget(self.tcp_check, 1, 0)
        methods_layout.addWidget(self.udp_check, 1, 1)
        methods_layout.addWidget(self.mdns_check, 2, 0)
        methods_layout.addWidget(self.llmnr_check, 2, 1)
        
        methods_group.setLayout(methods_layout)
        config_layout.addWidget(methods_group)
        
        # Opciones avanzadas
        advanced_layout = QFormLayout()
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 30)
        self.timeout_spin.setValue(5)
        self.timeout_spin.setSuffix(" s")
        advanced_layout.addRow("Timeout:", self.timeout_spin)
        
        self.retries_spin = QSpinBox()
        self.retries_spin.setRange(0, 5)
        self.retries_spin.setValue(2)
        advanced_layout.addRow("Reintentos:", self.retries_spin)
        
        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 100)
        self.threads_spin.setValue(10)
        advanced_layout.addRow("Hilos:", self.threads_spin)
        
        config_layout.addLayout(advanced_layout)
        
        main_layout.addWidget(config_group)
        
        # Botón de escaneo
        scan_button_layout = QHBoxLayout()
        self.scan_button = QPushButton("Iniciar Descubrimiento")
        self.scan_button.clicked.connect(self.start_scan)
        self.scan_button.setMinimumHeight(40)
        scan_button_layout.addWidget(self.scan_button)
        main_layout.addLayout(scan_button_layout)
        
        # Tabla de resultados
        results_group = QGroupBox("Dispositivos Descubiertos")
        results_layout = QVBoxLayout()
        
        self.results_table = QTableWidget(0, 5)
        self.results_table.setHorizontalHeaderLabels(["IP", "MAC", "Hostname", "Método", "Estado"])
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        results_layout.addWidget(self.results_table)
        
        # Acciones para los resultados
        actions_layout = QHBoxLayout()
        
        self.export_button = QPushButton("Exportar Resultados")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_results)
        
        self.nmap_scan_button = QPushButton("Escanear con Nmap")
        self.nmap_scan_button.setEnabled(False)
        self.nmap_scan_button.clicked.connect(self.scan_with_nmap)

        self.trust_button = QPushButton("Marcar selección como conocida")
        self.trust_button.setEnabled(False)
        self.trust_button.clicked.connect(self.mark_selection_known)
        
        actions_layout.addWidget(self.export_button)
        actions_layout.addWidget(self.trust_button)
        actions_layout.addWidget(self.nmap_scan_button)
        
        results_layout.addLayout(actions_layout)
        results_group.setLayout(results_layout)
        
        main_layout.addWidget(results_group)
        
        # Barra de estado
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Listo")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(status_layout)
    
    @asyncSlot()
    async def start_scan(self):
        """Inicia el proceso de descubrimiento rápido"""
        if self.scanning:
            return

        target = self.target_input.text().strip()
        if not target:
            self.status_label.setText("Error: Especifique un objetivo para el descubrimiento")
            return

        if not any([
            self.arp_check.isChecked(),
            self.icmp_check.isChecked(),
            self.tcp_check.isChecked(),
            self.udp_check.isChecked(),
            self.mdns_check.isChecked(),
            self.llmnr_check.isChecked()
        ]):
            self.status_label.setText("Error: Seleccione al menos un método de descubrimiento")
            return

        self.scanning = True
        self.scan_button.setEnabled(False)
        self.status_label.setText(f"Descubriendo dispositivos en {target}...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        self.results_table.setRowCount(0)
        self.export_button.setEnabled(False)
        self.nmap_scan_button.setEnabled(False)

        await self._run_discovery(target)

    async def _run_discovery(self, target: str) -> None:
        def on_progress(msg: str) -> None:
            self.status_label.setText(msg)

        try:
            hosts: list[HostRecord] = await self._adapter.discover(
                target,
                use_arp=self.arp_check.isChecked(),
                use_icmp=self.icmp_check.isChecked(),
                use_mdns=self.mdns_check.isChecked(),
                use_llmnr=self.llmnr_check.isChecked(),
                timeout_s=float(self.timeout_spin.value()),
                progress=on_progress,
            )
            self._last_hosts = hosts
            self.populate_hosts(hosts)
            append_record(
                ScanRecord(
                    kind="discovery",
                    target=target,
                    summary=f"{len(hosts)} hosts",
                    payload=[
                        {
                            "ip": h.ip,
                            "mac": h.mac,
                            "hostname": h.hostname,
                            "methods": h.methods,
                            "demo": h.demo,
                        }
                        for h in hosts
                    ],
                )
            )
            window = self.window()
            if hasattr(window, "notify_scan_recorded"):
                window.notify_scan_recorded()  # type: ignore[attr-defined]
            suffix = " (demo)" if is_demo_mode() else ""
            self.status_label.setText(f"Descubrimiento completado — {len(hosts)} host(s){suffix}")
        except ValueError as exc:
            self.status_label.setText(f"Error: {exc}")
        except PermissionError:
            self.status_label.setText(
                "Error: sin permisos raw — setcap python3 o export NEDSCANNER_DEMO=1"
            )
        except Exception as exc:
            logger.exception("discovery failed")
            self.status_label.setText(f"Error: {exc}")
        finally:
            self.scanning = False
            self.scan_button.setEnabled(True)
            self.progress_bar.setVisible(False)
            if self.results_table.rowCount() > 0:
                self.export_button.setEnabled(True)
                self.nmap_scan_button.setEnabled(True)

    def populate_hosts(self, hosts: list[HostRecord]) -> None:
        self.results_table.setRowCount(0)
        unknown_count = 0
        for host in hosts:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            trust = host_trust_label(host.ip, host.mac, host.hostname)
            if trust == "Desconocido":
                unknown_count += 1
            self.results_table.setItem(row, 0, QTableWidgetItem(host.ip))
            self.results_table.setItem(row, 1, QTableWidgetItem(host.mac or "—"))
            self.results_table.setItem(row, 2, QTableWidgetItem(host.hostname or "—"))
            self.results_table.setItem(row, 3, QTableWidgetItem(host.method_label()))
            state_item = QTableWidgetItem(trust)
            if trust == "Desconocido":
                orange = QColor(255, 140, 60)
                for col in range(5):
                    item = self.results_table.item(row, col)
                    if item:
                        item.setBackground(orange)
            self.results_table.setItem(row, 4, state_item)
        self.trust_button.setEnabled(len(hosts) > 0)
        if unknown_count:
            self.status_label.setText(
                f"{len(hosts)} host(s) — {unknown_count} desconocido(s) (revisa columna Estado)"
            )

    def mark_selection_known(self) -> None:
        selected = self.results_table.selectedItems()
        if not selected:
            for host in self._last_hosts:
                add_known_host(host.ip, host.mac, host.hostname)
            self.populate_hosts(self._last_hosts)
            self.status_label.setText("Todo el último escaneo añadido al inventario")
            return
        rows = sorted({self.results_table.row(i) for i in selected})
        for row in rows:
            ip = self.results_table.item(row, 0).text()
            mac = self.results_table.item(row, 1).text()
            hostname = self.results_table.item(row, 2).text()
            add_known_host(ip, None if mac == "—" else mac, None if hostname == "—" else hostname)
        self.populate_hosts(self._last_hosts)
        self.status_label.setText(f"{len(rows)} dispositivo(s) guardados en ~/.nedscaner/known-devices.json")
    
    def export_results(self) -> None:
        if not self._last_hosts:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar descubrimiento",
            str(Path.home() / "nedscanner-discovery.json"),
            "JSON (*.json)",
        )
        if not path:
            return
        payload = {
            "demo": is_demo_mode(),
            "hosts": [
                {
                    "ip": h.ip,
                    "mac": h.mac,
                    "hostname": h.hostname,
                    "methods": h.methods,
                }
                for h in self._last_hosts
            ],
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.status_label.setText(f"Exportado: {path}")

    def scan_with_nmap(self):
        selected_items = self.results_table.selectedItems()
        if selected_items:
            rows = {self.results_table.row(i) for i in selected_items}
            ips = [self.results_table.item(r, 0).text() for r in rows]
        else:
            ips = [h.ip for h in self._last_hosts]

        if not ips:
            self.status_label.setText("Sin hosts para Nmap")
            return

        window = self.window()
        if hasattr(window, "handoff_to_nmap"):
            window.handoff_to_nmap(ips)  # type: ignore[attr-defined]
        else:
            self.status_label.setText(f"IPs: {', '.join(ips)}")
