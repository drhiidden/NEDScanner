from __future__ import annotations

from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.user_prefs import (
    is_allow_public_scan,
    is_scan_authorized,
    set_allow_public_scan,
    set_scan_authorized,
)


class SecuritySettingsPane(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        perms_group = QGroupBox("Permisos y Privilegios")
        perms_layout = QVBoxLayout()
        self.perms_text = QTextEdit()
        self.perms_text.setReadOnly(True)
        self.perms_text.setText(
            """Permisos actuales:

1. Nmap: No configurado para ejecutarse sin sudo
2. Scapy: No configurado para ejecutarse sin sudo
3. NetworkManager: Acceso vía D-Bus o nmcli

sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/nmap
sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/python3
"""
        )
        perms_layout.addWidget(self.perms_text)
        check_btn = QPushButton("Verificar Permisos")
        check_btn.clicked.connect(self._check_permissions)
        perms_layout.addWidget(check_btn)
        perms_group.setLayout(perms_layout)
        layout.addWidget(perms_group)

        auth_group = QGroupBox("Autorización de escaneo en red real")
        auth_layout = QVBoxLayout()
        self.scan_authorized_check = QCheckBox(
            "Declaro permiso para escanear solo redes autorizadas"
        )
        self.scan_authorized_check.setChecked(is_scan_authorized())
        self.allow_public_check = QCheckBox(
            "Permitir objetivos fuera de LAN privada (permiso legal explícito)"
        )
        self.allow_public_check.setChecked(is_allow_public_scan())
        auth_layout.addWidget(self.scan_authorized_check)
        auth_layout.addWidget(self.allow_public_check)
        hint = QLabel("Se guarda en ~/.nedscaner/preferences.json. En modo demo no aplica.")
        hint.setWordWrap(True)
        auth_layout.addWidget(hint)
        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)

        creds_group = QGroupBox("Almacenamiento de Credenciales")
        creds_layout = QVBoxLayout()
        self.use_keyring_check = QCheckBox("Usar keyring del sistema")
        self.use_keyring_check.setChecked(True)
        creds_layout.addWidget(self.use_keyring_check)
        clear_btn = QPushButton("Limpiar Credenciales Guardadas")
        clear_btn.clicked.connect(self._clear_credentials)
        creds_layout.addWidget(clear_btn)
        creds_group.setLayout(creds_layout)
        layout.addWidget(creds_group)
        layout.addStretch()

    def apply_preferences(self) -> None:
        set_scan_authorized(self.scan_authorized_check.isChecked())
        set_allow_public_scan(self.allow_public_check.isChecked())

    def reset_defaults(self) -> None:
        self.use_keyring_check.setChecked(True)
        self.scan_authorized_check.setChecked(False)
        self.allow_public_check.setChecked(False)

    def _check_permissions(self) -> None:
        QMessageBox.information(
            self, "Verificación de Permisos", "Verificación completada (stub)."
        )

    def _clear_credentials(self) -> None:
        if (
            QMessageBox.question(
                self,
                "Limpiar Credenciales",
                "¿Eliminar credenciales guardadas?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            == QMessageBox.StandardButton.Yes
        ):
            QMessageBox.information(self, "Limpiar Credenciales", "Credenciales eliminadas (stub).")
