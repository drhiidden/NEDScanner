from __future__ import annotations

import os

from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class GeneralSettingsPane(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        ui_group = QGroupBox("Interfaz de Usuario")
        ui_layout = QFormLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Claro", "Oscuro", "Sistema"])
        ui_layout.addRow("Tema:", self.theme_combo)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Español", "English", "Français", "Deutsch"])
        ui_layout.addRow("Idioma:", self.lang_combo)
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 16)
        self.font_size_spin.setValue(10)
        ui_layout.addRow("Tamaño de fuente:", self.font_size_spin)
        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)

        behavior_group = QGroupBox("Comportamiento")
        behavior_layout = QFormLayout()
        self.auto_save_check = QCheckBox("Guardar resultados automáticamente")
        self.auto_save_check.setChecked(True)
        behavior_layout.addRow(self.auto_save_check)
        self.confirm_actions_check = QCheckBox("Confirmar acciones peligrosas")
        self.confirm_actions_check.setChecked(True)
        behavior_layout.addRow(self.confirm_actions_check)
        self.auto_update_check = QCheckBox("Buscar actualizaciones al iniciar")
        self.auto_update_check.setChecked(True)
        behavior_layout.addRow(self.auto_update_check)
        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)

        dirs_group = QGroupBox("Directorios")
        dirs_layout = QFormLayout()
        self.data_dir_input = QLineEdit()
        self.data_dir_input.setReadOnly(True)
        self.data_dir_input.setText(os.path.expanduser("~/.nedscaner/data"))
        data_row = QHBoxLayout()
        data_btn = QPushButton("Cambiar...")
        data_btn.clicked.connect(self.select_data_dir)
        data_row.addWidget(self.data_dir_input)
        data_row.addWidget(data_btn)
        dirs_layout.addRow("Directorio de datos:", data_row)
        self.export_dir_input = QLineEdit()
        self.export_dir_input.setReadOnly(True)
        self.export_dir_input.setText(os.path.expanduser("~/Documentos/NEDScaner"))
        export_row = QHBoxLayout()
        export_btn = QPushButton("Cambiar...")
        export_btn.clicked.connect(self.select_export_dir)
        export_row.addWidget(self.export_dir_input)
        export_row.addWidget(export_btn)
        dirs_layout.addRow("Directorio de exportación:", export_row)
        dirs_group.setLayout(dirs_layout)
        layout.addWidget(dirs_group)
        layout.addStretch()

    def select_data_dir(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self, "Seleccionar Directorio de Datos", self.data_dir_input.text()
        )
        if directory:
            self.data_dir_input.setText(directory)

    def select_export_dir(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self, "Seleccionar Directorio de Exportación", self.export_dir_input.text()
        )
        if directory:
            self.export_dir_input.setText(directory)

    def reset_defaults(self) -> None:
        self.theme_combo.setCurrentIndex(0)
        self.lang_combo.setCurrentIndex(0)
        self.font_size_spin.setValue(10)
        self.auto_save_check.setChecked(True)
        self.confirm_actions_check.setChecked(True)
        self.auto_update_check.setChecked(True)
        self.data_dir_input.setText(os.path.expanduser("~/.nedscaner/data"))
        self.export_dir_input.setText(os.path.expanduser("~/Documentos/NEDScaner"))
