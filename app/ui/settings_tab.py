from __future__ import annotations

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.settings.advanced_pane import AdvancedSettingsPane
from app.ui.settings.general_pane import GeneralSettingsPane
from app.ui.settings.inventory_pane import InventorySettingsPane
from app.ui.settings.security_pane import SecuritySettingsPane
from app.ui.settings.tools_pane import ToolsSettingsPane


class SettingsTab(QWidget):
    """Orquestador de preferencias: pestañas en `app/ui/settings/`."""

    def __init__(self) -> None:
        super().__init__()
        self.general = GeneralSettingsPane()
        self.tools = ToolsSettingsPane()
        self.security = SecuritySettingsPane()
        self.advanced = AdvancedSettingsPane()
        self.inventory = InventorySettingsPane()
        self._build_ui()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        tabs = QTabWidget()
        tabs.addTab(self.general, "General")
        tabs.addTab(self.tools, "Herramientas")
        tabs.addTab(self.security, "Seguridad")
        tabs.addTab(self.advanced, "Avanzado")
        tabs.addTab(self.inventory, "Inventario")
        main_layout.addWidget(tabs)

        row = QHBoxLayout()
        reset_btn = QPushButton("Restaurar Valores Predeterminados")
        reset_btn.clicked.connect(self.reset_settings)
        apply_btn = QPushButton("Aplicar")
        apply_btn.setDefault(True)
        apply_btn.clicked.connect(self.apply_settings)
        row.addWidget(reset_btn)
        row.addStretch()
        row.addWidget(apply_btn)
        main_layout.addLayout(row)

    def reset_settings(self) -> None:
        if (
            QMessageBox.question(
                self,
                "Restaurar Valores Predeterminados",
                "¿Restaurar todos los ajustes?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            != QMessageBox.StandardButton.Yes
        ):
            return
        self.general.reset_defaults()
        self.tools.reset_defaults()
        self.security.reset_defaults()
        self.advanced.reset_defaults()
        QMessageBox.information(self, "Restaurar", "Valores predeterminados restaurados.")

    def apply_settings(self) -> None:
        self.security.apply_preferences()
        self.tools.apply_preferences()
        window = self.window()
        if hasattr(window, "refresh_security_status"):
            window.refresh_security_status()  # type: ignore[attr-defined]
        QMessageBox.information(self, "Aplicar Configuración", "Configuración aplicada.")
