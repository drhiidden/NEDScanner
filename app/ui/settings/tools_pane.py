from __future__ import annotations

from PyQt6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.core.user_prefs import get_nmap_scan_timeout_s, set_nmap_scan_timeout_s


class ToolsSettingsPane(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        nmap_group = QGroupBox("Nmap")
        nmap_layout = QFormLayout()
        self.nmap_path_input = QLineEdit("/usr/bin/nmap")
        nmap_path_row = QHBoxLayout()
        nmap_btn = QPushButton("Buscar...")
        nmap_btn.clicked.connect(lambda: self._pick_executable(self.nmap_path_input, "Nmap"))
        nmap_path_row.addWidget(self.nmap_path_input)
        nmap_path_row.addWidget(nmap_btn)
        nmap_layout.addRow("Ruta de Nmap:", nmap_path_row)
        self.nmap_sudo_check = QCheckBox("Usar sudo para Nmap")
        nmap_layout.addRow(self.nmap_sudo_check)
        self.nmap_args_input = QLineEdit()
        self.nmap_args_input.setPlaceholderText("Argumentos por defecto para Nmap")
        nmap_layout.addRow("Argumentos por defecto:", self.nmap_args_input)
        self.nmap_timeout_spin = QSpinBox()
        self.nmap_timeout_spin.setRange(30, 3600)
        self.nmap_timeout_spin.setValue(get_nmap_scan_timeout_s())
        self.nmap_timeout_spin.setSuffix(" s")
        nmap_layout.addRow("Timeout global de escaneo:", self.nmap_timeout_spin)
        nmap_group.setLayout(nmap_layout)
        layout.addWidget(nmap_group)

        nm_group = QGroupBox("NetworkManager")
        nm_layout = QFormLayout()
        self.nmcli_path_input = QLineEdit("/usr/bin/nmcli")
        nm_row = QHBoxLayout()
        nm_btn = QPushButton("Buscar...")
        nm_btn.clicked.connect(lambda: self._pick_executable(self.nmcli_path_input, "nmcli"))
        nm_row.addWidget(self.nmcli_path_input)
        nm_row.addWidget(nm_btn)
        nm_layout.addRow("Ruta de nmcli:", nm_row)
        self.nm_dbus_radio = QRadioButton("Usar D-Bus (recomendado)")
        self.nm_dbus_radio.setChecked(True)
        self.nm_cli_radio = QRadioButton("Usar CLI (nmcli)")
        nm_method_group = QButtonGroup(self)
        nm_method_group.addButton(self.nm_dbus_radio)
        nm_method_group.addButton(self.nm_cli_radio)
        nm_method = QHBoxLayout()
        nm_method.addWidget(self.nm_dbus_radio)
        nm_method.addWidget(self.nm_cli_radio)
        nm_layout.addRow("Método de acceso:", nm_method)
        nm_group.setLayout(nm_layout)
        layout.addWidget(nm_group)

        scapy_group = QGroupBox("Scapy")
        scapy_layout = QFormLayout()
        self.scapy_timeout_spin = QSpinBox()
        self.scapy_timeout_spin.setRange(1, 30)
        self.scapy_timeout_spin.setValue(5)
        self.scapy_timeout_spin.setSuffix(" s")
        scapy_layout.addRow("Timeout por defecto:", self.scapy_timeout_spin)
        self.scapy_retries_spin = QSpinBox()
        self.scapy_retries_spin.setRange(0, 5)
        self.scapy_retries_spin.setValue(2)
        scapy_layout.addRow("Reintentos por defecto:", self.scapy_retries_spin)
        self.scapy_threads_spin = QSpinBox()
        self.scapy_threads_spin.setRange(1, 100)
        self.scapy_threads_spin.setValue(10)
        scapy_layout.addRow("Hilos por defecto:", self.scapy_threads_spin)
        scapy_group.setLayout(scapy_layout)
        layout.addWidget(scapy_group)
        layout.addStretch()

    def _pick_executable(self, field: QLineEdit, title: str) -> None:
        path, _ = QFileDialog.getOpenFileName(self, f"Seleccionar {title}", field.text())
        if path:
            field.setText(path)

    def apply_preferences(self) -> None:
        set_nmap_scan_timeout_s(self.nmap_timeout_spin.value())

    def reset_defaults(self) -> None:
        self.nmap_path_input.setText("/usr/bin/nmap")
        self.nmap_sudo_check.setChecked(False)
        self.nmap_args_input.clear()
        self.nmap_timeout_spin.setValue(300)
        self.nmcli_path_input.setText("/usr/bin/nmcli")
        self.nm_dbus_radio.setChecked(True)
        self.scapy_timeout_spin.setValue(5)
        self.scapy_retries_spin.setValue(2)
        self.scapy_threads_spin.setValue(10)
