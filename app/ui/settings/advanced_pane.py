from __future__ import annotations

import os

from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class AdvancedSettingsPane(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        logging_group = QGroupBox("Logging")
        logging_layout = QFormLayout()
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["ERROR", "WARNING", "INFO", "DEBUG"])
        self.log_level_combo.setCurrentIndex(2)
        logging_layout.addRow("Nivel de log:", self.log_level_combo)
        self.log_file_input = QLineEdit(os.path.expanduser("~/.nedscaner/nedscaner.log"))
        log_row = QHBoxLayout()
        log_btn = QPushButton("Cambiar...")
        log_btn.clicked.connect(self._select_log_file)
        log_row.addWidget(self.log_file_input)
        log_row.addWidget(log_btn)
        logging_layout.addRow("Archivo de log:", log_row)
        view_btn = QPushButton("Ver Log")
        view_btn.clicked.connect(self._view_log)
        logging_layout.addRow(view_btn)
        logging_group.setLayout(logging_layout)
        layout.addWidget(logging_group)

        perf_group = QGroupBox("Rendimiento")
        perf_layout = QFormLayout()
        self.parallel_scans_spin = QSpinBox()
        self.parallel_scans_spin.setRange(1, 10)
        self.parallel_scans_spin.setValue(2)
        perf_layout.addRow("Escaneos paralelos máximos:", self.parallel_scans_spin)
        self.cache_size_spin = QSpinBox()
        self.cache_size_spin.setRange(10, 1000)
        self.cache_size_spin.setValue(100)
        self.cache_size_spin.setSuffix(" MB")
        perf_layout.addRow("Tamaño máximo de caché:", self.cache_size_spin)
        clear_cache = QPushButton("Limpiar Caché")
        clear_cache.clicked.connect(self._clear_cache)
        perf_layout.addRow(clear_cache)
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)

        db_group = QGroupBox("Base de Datos")
        db_layout = QVBoxLayout()
        db_layout.addWidget(QLabel("Base de datos SQLite: ~/.nedscaner/database.db"))
        db_buttons = QHBoxLayout()
        backup_btn = QPushButton("Respaldar BD")
        backup_btn.clicked.connect(self._backup_database)
        restore_btn = QPushButton("Restaurar BD")
        restore_btn.clicked.connect(self._restore_database)
        reset_btn = QPushButton("Reiniciar BD")
        reset_btn.clicked.connect(self._reset_database)
        db_buttons.addWidget(backup_btn)
        db_buttons.addWidget(restore_btn)
        db_buttons.addWidget(reset_btn)
        db_layout.addLayout(db_buttons)
        db_group.setLayout(db_layout)
        layout.addWidget(db_group)
        layout.addStretch()

    def reset_defaults(self) -> None:
        self.log_level_combo.setCurrentIndex(2)
        self.log_file_input.setText(os.path.expanduser("~/.nedscaner/nedscaner.log"))
        self.parallel_scans_spin.setValue(2)
        self.cache_size_spin.setValue(100)

    def _select_log_file(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Seleccionar Archivo de Log", self.log_file_input.text()
        )
        if path:
            self.log_file_input.setText(path)

    def _view_log(self) -> None:
        QMessageBox.information(self, "Ver Log", f"Log: {self.log_file_input.text()}")

    def _clear_cache(self) -> None:
        QMessageBox.information(self, "Limpiar Caché", "Caché limpiada (stub).")

    def _backup_database(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Respaldo",
            os.path.expanduser("~/nedscaner_backup.db"),
            "Archivos SQLite (*.db)",
        )
        if path:
            QMessageBox.information(self, "Respaldo", f"Respaldo en: {path} (stub).")

    def _restore_database(self) -> None:
        QMessageBox.information(self, "Restaurar", "Restauración (stub).")

    def _reset_database(self) -> None:
        QMessageBox.warning(self, "Reiniciar BD", "Reinicio (stub).")
